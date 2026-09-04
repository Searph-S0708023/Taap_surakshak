import sqlite3

DB = "mumbai_heat_health.db"

with open("schema.sql", "r", encoding="utf-8") as f:
    schema = f.read()

conn = sqlite3.connect(DB)
conn.executescript(schema)
conn.commit()
conn.close()

print("Database created successfully.")