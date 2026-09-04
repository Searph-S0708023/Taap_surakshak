import sqlite3
from datetime import date, timedelta

conn = sqlite3.connect("mumbai_heat_health.db")

start = date(2000, 1, 1)
end = date(2026, 9, 1)

current = start

while current <= end:

    conn.execute(
        """
        INSERT OR IGNORE INTO dim_date
        (date, year, month, day, day_of_year, week)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            current.isoformat(),
            current.year,
            current.month,
            current.day,
            current.timetuple().tm_yday,
            current.isocalendar().week
        )
    )

    current += timedelta(days=1)

conn.commit()
conn.close()

print("Date dimension populated.")