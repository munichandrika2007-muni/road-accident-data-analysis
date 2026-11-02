import csv, io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from config import Config
from database import fetch_all, execute
from analysis import load_data, summary
from charts import create_charts

app=Flask(__name__)
app.config.from_object(Config)
VEHICLES=["Car","Motorcycle","Bus","Truck","Van","Bicycle","Pedestrian","Other"]
SEVERITIES=["Minor","Serious","Fatal","Unknown"]

def save_location(region,road):
    found=fetch_all("""SELECT location_id FROM locations WHERE region=%s
        AND (road_name=%s OR (road_name IS NULL AND %s='')) LIMIT 1""",
        (region,road or "",road or ""))
    if found: return found[0]["location_id"]
    return execute("INSERT INTO locations(region,road_name) VALUES(%s,%s)",(region,road or None))

def validate(row):
    errors=[]
    try: dt=datetime.fromisoformat((row.get("accident_datetime") or "").replace("T"," "))
    except ValueError:
        dt=None; errors.append("Invalid date/time. Use YYYY-MM-DD HH:MM.")
    region=(row.get("region") or "").strip()
    vehicle=(row.get("vehicle_type") or "").strip()
    severity=(row.get("severity") or "Unknown").strip().title()
    if not region: errors.append("Region is required.")
    if vehicle not in VEHICLES: errors.append("Unsupported vehicle type.")
    if severity not in SEVERITIES: errors.append("Severity must be Minor, Serious, Fatal or Unknown.")
    return dt,region,(row.get("road_name") or "").strip(),vehicle,severity,(row.get("weather") or "").strip(),errors

def insert_record(dt,region,road,vehicle,severity,weather,source):
    loc=save_location(region,road)
    execute("""INSERT INTO accidents(accident_datetime,location_id,vehicle_type,severity,weather,source)
        VALUES(%s,%s,%s,%s,%s,%s)""",(dt,loc,vehicle,severity,weather or None,source))

@app.route("/")
def home(): return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    df=load_data()
    charts=create_charts(df)
    top=df.groupby("region").size().sort_values(ascending=False).head(8).to_dict() if not df.empty else {}
    missing=[]
    if not df.empty:
        for c in ["accident_datetime","region","vehicle_type","severity","weather"]:
            missing.append({"field":c,"count":int(df[c].isna().sum())})
    return render_template("dashboard.html",stats=summary(df),charts=charts,top=top,missing=missing)

@app.route("/accidents")
def accidents():
    df=load_data()
    rows=df.head(500).to_dict("records") if not df.empty else []
    return render_template("accidents.html",rows=rows)

@app.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        dt,region,road,vehicle,severity,weather,errors=validate(request.form)
        if errors:
            for e in errors: flash(e,"danger")
        else:
            insert_record(dt,region,road,vehicle,severity,weather,"Manual entry")
            flash("Accident record saved.","success")
            return redirect(url_for("accidents"))
    return render_template("add.html",vehicles=VEHICLES,severities=SEVERITIES)

@app.route("/import",methods=["GET","POST"])
def import_csv():
    if request.method=="POST":
        f=request.files.get("file")
        if not f or not f.filename.lower().endswith(".csv"):
            flash("Choose a CSV file.","danger"); return redirect(url_for("import_csv"))
        reader=csv.DictReader(io.StringIO(f.stream.read().decode("utf-8-sig")))
        required={"accident_datetime","region","vehicle_type","severity"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            flash("Required CSV headers: accident_datetime, region, vehicle_type, severity.","danger")
            return redirect(url_for("import_csv"))
        good=bad=0
        for row in reader:
            dt,region,road,vehicle,severity,weather,errors=validate(row)
            if errors: bad+=1; continue
            try: insert_record(dt,region,road,vehicle,severity,weather,f.filename); good+=1
            except Exception: bad+=1
        flash(f"Import finished: {good} imported, {bad} rejected.","info")
        return redirect(url_for("dashboard"))
    return render_template("import.html")

@app.route("/reports")
def reports():
    df=load_data()
    def counts(col):
        return df.groupby(col).size().sort_values(ascending=False).to_dict() if not df.empty else {}
    missing=[{"field":c,"count":int(df[c].isna().sum())} for c in ["weather","road_name","source"]] if not df.empty else []
    return render_template("reports.html",severity=counts("severity"),vehicles=counts("vehicle_type"),
                           months=counts("month"),regions=counts("region"),missing=missing,total=len(df))

@app.route("/export")
def export():
    df=load_data()
    out=io.StringIO()
    if df.empty: out.write("No records\n")
    else: df.drop(columns=["date","month","hour"],errors="ignore").to_csv(out,index=False)
    return send_file(io.BytesIO(out.getvalue().encode("utf-8-sig")),mimetype="text/csv",
        as_attachment=True,download_name="road_accident_report.csv")

@app.errorhandler(404)
def not_found(_): return render_template("404.html"),404

if __name__=="__main__": app.run(debug=True)
