import sqlite3

conn = sqlite3.connect("mumbai_heat_health.db")

conn.execute("""
DELETE FROM fact_climate_monthly
""")

conn.execute("""
INSERT INTO fact_climate_monthly

SELECT
    CAST(strftime('%Y', date) AS INTEGER),
    CAST(strftime('%m', date) AS INTEGER),
    ward_id,

    AVG(temp_mean_c),
    MAX(temp_max_c),
    MIN(temp_min_c),

    AVG(humidity_pct),
    AVG(wind_speed_ms),
    AVG(solar_radiation_kwh_m2),

    AVG(heat_index_c),
    AVG(wbgt_c),
    AVG(utci_c),

    AVG(lst_day_c),
    AVG(temperature_anomaly_c),

    SUM(is_heatwave_day)

FROM fact_climate_daily

GROUP BY
    strftime('%Y', date),
    strftime('%m', date),
    ward_id
""")

conn.execute("""
DELETE FROM fact_climate_yearly
""")

conn.execute("""
INSERT INTO fact_climate_yearly

SELECT
    CAST(strftime('%Y', date) AS INTEGER),
    ward_id,

    AVG(temp_mean_c),
    MAX(temp_max_c),
    MIN(temp_min_c),

    AVG(humidity_pct),
    AVG(wind_speed_ms),
    AVG(solar_radiation_kwh_m2),

    AVG(heat_index_c),
    AVG(wbgt_c),
    AVG(utci_c),

    AVG(lst_day_c),
    AVG(temperature_anomaly_c),

    SUM(is_heatwave_day)

FROM fact_climate_daily

GROUP BY
    strftime('%Y', date),
    ward_id
""")

conn.commit()
conn.close()

print("Monthly and yearly tables updated.")