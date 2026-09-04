import sqlite3
import math

def heat_index_celsius(temp_c, rh):

    if temp_c is None or rh is None:
        return None

    temp_f = temp_c * 9 / 5 + 32

    # Simple Celsius approximation for lower temperatures
    if temp_f < 80:
        return temp_c

    hi = (
        -42.379
        + 2.04901523 * temp_f
        + 10.14333127 * rh
        - 0.22475541 * temp_f * rh
        - 0.00683783 * temp_f**2
        - 0.05481717 * rh**2
        + 0.00122874 * temp_f**2 * rh
        + 0.00085282 * temp_f * rh**2
        - 0.00000199 * temp_f**2 * rh**2
    )

    return (hi - 32) * 5 / 9


conn = sqlite3.connect("mumbai_heat_health.db")

rows = conn.execute(
    """
    SELECT id, temp_mean_c, humidity_pct
    FROM fact_climate_daily
    """
).fetchall()

for row_id, temp, rh in rows:

    hi = heat_index_celsius(temp, rh)

    conn.execute(
        """
        UPDATE fact_climate_daily
        SET heat_index_c = ?
        WHERE id = ?
        """,
        (hi, row_id)
    )

conn.commit()
conn.close()

print("Heat Index calculated.")