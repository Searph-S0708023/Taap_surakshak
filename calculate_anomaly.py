import sqlite3

conn = sqlite3.connect("mumbai_heat_health.db")

# Calculate monthly historical baseline
conn.execute("""
DROP TABLE IF EXISTS monthly_baseline
""")

conn.execute("""
CREATE TEMP TABLE monthly_baseline AS

SELECT
    CAST(strftime('%m', date) AS INTEGER) AS month,
    AVG(temp_mean_c) AS baseline_temp

FROM fact_climate_daily

WHERE date < '2024-01-01'

GROUP BY month
""")

conn.execute("""
UPDATE fact_climate_daily

SET temperature_anomaly_c =
(
    temp_mean_c -

    (
        SELECT baseline_temp
        FROM monthly_baseline
        WHERE monthly_baseline.month =
              CAST(strftime('%m', fact_climate_daily.date) AS INTEGER)
    )
)
""")

conn.commit()
conn.close()

print("Temperature anomalies calculated.")