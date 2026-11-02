import pandas as pd
import numpy as np
from database import fetch_all

def load_data():
    rows = fetch_all("""SELECT a.accident_id,a.accident_datetime,l.region,l.road_name,
        a.vehicle_type,a.severity,a.weather,a.source
        FROM accidents a JOIN locations l ON a.location_id=l.location_id
        ORDER BY a.accident_datetime DESC""")
    df = pd.DataFrame(rows)
    if not df.empty:
        df["accident_datetime"] = pd.to_datetime(df["accident_datetime"])
        df["date"] = df["accident_datetime"].dt.date
        df["month"] = df["accident_datetime"].dt.to_period("M").astype(str)
        df["hour"] = df["accident_datetime"].dt.hour
    return df

def summary(df):
    if df.empty:
        return dict(total=0, locations=0, serious=0, fatal=0, avg_daily=0, missing_weather=0)
    return dict(total=len(df), locations=df.region.nunique(),
        serious=int((df.severity=="Serious").sum()), fatal=int((df.severity=="Fatal").sum()),
        avg_daily=round(float(np.mean(df.groupby("date").size())),2),
        missing_weather=int(df.weather.isna().sum()))
