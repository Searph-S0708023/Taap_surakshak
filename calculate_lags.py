import sqlite3

conn = sqlite3.connect("mumbai_heat_health.db")

conn.execute("""
UPDATE fact_climate_daily

SET temp_lag_1d = (
    SELECT temp_mean_c
    FROM fact_climate_daily AS previous
    WHERE previous.ward_id = fact_climate_daily.ward_id
    AND previous.date =
        date(fact_climate_daily.date, '-1 day')
)
""")

conn.execute("""
UPDATE fact_climate_daily

SET temp_lag_3d = (
    SELECT temp_mean_c
    FROM fact_climate_daily AS previous
    WHERE previous.ward_id = fact_climate_daily.ward_id
    AND previous.date =
        date(fact_climate_daily.date, '-3 day')
)
""")

conn.execute("""
UPDATE fact_climate_daily

SET temp_lag_7d = (
    SELECT temp_mean_c
    FROM fact_climate_daily AS previous
    WHERE previous.ward_id = fact_climate_daily.ward_id
    AND previous.date =
        date(fact_climate_daily.date, '-7 day')
)
""")

conn.execute("""
UPDATE fact_climate_daily

SET humidity_lag_1d = (
    SELECT humidity_pct
    FROM fact_climate_daily AS previous
    WHERE previous.ward_id = fact_climate_daily.ward_id
    AND previous.date =
        date(fact_climate_daily.date, '-1 day')
)
""")

conn.execute("""
UPDATE fact_climate_daily

SET humidity_lag_3d = (
    SELECT humidity_pct
    FROM fact_climate_daily AS previous
    WHERE previous.ward_id = fact_climate_daily.ward_id
    AND previous.date =
        date(fact_climate_daily.date, '-3 day')
)
""")

conn.execute("""
UPDATE fact_climate_daily

SET humidity_lag_7d = (
    SELECT humidity_pct
    FROM fact_climate_daily AS previous
    WHERE previous.ward_id = fact_climate_daily.ward_id
    AND previous.date =
        date(fact_climate_daily.date, '-7 day')
)
""")

conn.commit()
conn.close()

print("Lagged weather calculated.")