import sqlite3

conn = sqlite3.connect("mumbai_heat_health.db")

conn.execute(
    """
    INSERT OR REPLACE INTO dim_ward
    (ward_id, ward_name, latitude, longitude)
    VALUES (?, ?, ?, ?)
    """,
    (
        0,
        "Mumbai Citywide",
        19.0760,
        72.8777
    )
)

conn.commit()
conn.close()

print("Mumbai added.")