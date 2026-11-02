import random
from datetime import datetime,timedelta
from database import get_connection

def main():
    random.seed(13)
    regions=[("Hyderabad","NH 44"),("Hyderabad","Outer Ring Road"),("Warangal","NH 163"),
             ("Karimnagar","SH 1"),("Nizamabad","NH 63"),("Khammam","NH 365")]
    vehicles=["Car","Motorcycle","Bus","Truck","Van","Bicycle","Pedestrian"]
    severities=["Minor","Serious","Fatal","Unknown"]
    weather=["Clear","Rain","Fog","Cloudy",None]
    conn=get_connection(); cur=conn.cursor()
    ids=[]
    for region,road in regions:
        cur.execute("INSERT IGNORE INTO locations(region,road_name) VALUES(%s,%s)",(region,road))
        cur.execute("SELECT location_id FROM locations WHERE region=%s AND road_name=%s",(region,road))
        ids.append(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM accidents")
    if cur.fetchone()[0]==0:
        now=datetime.now().replace(minute=0,second=0,microsecond=0)
        for _ in range(300):
            dt=now-timedelta(days=random.randint(0,364),hours=random.randint(0,23))
            cur.execute("""INSERT INTO accidents(accident_datetime,location_id,vehicle_type,severity,weather,source)
                VALUES(%s,%s,%s,%s,%s,%s)""",(dt,random.choice(ids),random.choice(vehicles),
                random.choices(severities,[55,30,8,7])[0],random.choice(weather),"Synthetic demonstration data"))
    conn.commit(); cur.close(); conn.close()
    print("Synthetic seed data is ready.")
if __name__=="__main__": main()
