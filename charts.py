from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT=Path("static/charts")
OUT.mkdir(parents=True,exist_ok=True)

def create_charts(df):
    names=[]
    if df.empty: return names
    charts=[
      ("month","Accidents by month","monthly.png"),
      ("severity","Recorded severity distribution","severity.png"),
      ("region","Recorded accidents by region","locations.png"),
      ("vehicle_type","Accidents by vehicle type","vehicles.png")
    ]
    for col,title,filename in charts:
        counts=df.groupby(col).size().sort_values(ascending=False)
        fig,ax=plt.subplots(figsize=(8,4))
        counts.plot(kind="bar",ax=ax)
        ax.set_title(title); ax.set_ylabel("Recorded accident count")
        ax.set_xlabel(col.replace("_"," ").title())
        fig.tight_layout(); fig.savefig(OUT/filename,dpi=130); plt.close(fig)
        names.append("charts/"+filename)
    return names
