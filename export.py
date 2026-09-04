import sqlite3
import pandas as pd

conn = sqlite3.connect("mumbai_heat_health.db")

df = pd.read_sql(
    """
    SELECT *
    FROM v_ml_features_daily
    ORDER BY date, ward_id
    """,
    conn
)

df.to_csv(
    "mumbai_ml_ready.csv",
    index=False
)

conn.close()

print("Export complete.")
print("Rows:", len(df))
print("Columns:", len(df.columns))