import requests
import sqlite3
from datetime import datetime

LAT = 19.0760
LON = 72.8777

START = "20000101"
END = "20260901"

url = (
    "https://power.larc.nasa.gov/api/temporal/daily/point"
    "?parameters=T2M,T2M_MAX,T2M_MIN,RH2M,WS2M,ALLSKY_SFC_SW_DWN"
    "&community=RE"
    f"&longitude={LON}"
    f"&latitude={LAT}"
    f"&start={START}"
    f"&end={END}"
    "&format=JSON"
)

print("Downloading NASA POWER data...")

response = requests.get(url, timeout=180)
response.raise_for_status()

data = response.json()["properties"]["parameter"]

temperature = data["T2M"]
maximum = data["T2M_MAX"]
minimum = data["T2M_MIN"]
humidity = data["RH2M"]
wind = data["WS2M"]
solar = data["ALLSKY_SFC_SW_DWN"]

conn = sqlite3.connect("mumbai_heat_health.db")

count = 0

for d in temperature:

    sql_date = datetime.strptime(
        d, "%Y%m%d"
    ).strftime("%Y-%m-%d")

    conn.execute(
        """
        INSERT OR REPLACE INTO fact_climate_daily
        (
            date,
            ward_id,
            temp_mean_c,
            temp_max_c,
            temp_min_c,
            humidity_pct,
            wind_speed_ms,
            solar_radiation_kwh_m2
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sql_date,
            0,
            temperature[d],
            maximum[d],
            minimum[d],
            humidity[d],
            wind[d],
            solar[d]
        )
    )

    count += 1

conn.commit()
conn.close()

print(f"Inserted {count} daily observations.")