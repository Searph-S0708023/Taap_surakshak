import sqlite3
import pandas as pd
import numpy as np

# --- 1. COMPUTATIONAL HELPERS FOR CLIMATE INDICES ---

def calculate_wbgt(temp_c, rh, wind_ms, solar_kwh):
    """Approximates Wet Bulb Globe Temperature (WBGT) outdoors in direct sun."""
    if pd.isna(temp_c) or pd.isna(rh):
        return np.nan
    
    # Estimate Natural Wet Bulb Temp (Stull Formula)
    tw = (temp_c * np.arctan(0.151977 * (rh + 8.313659)**0.5) 
          + np.arctan(temp_c + rh) - np.arctan(rh - 1.676331) 
          + 0.00391838 * (rh)**1.5 * np.arctan(0.023101 * rh) - 4.686035)
    
    # Estimate Globe Temperature using solar radiation & wind speed
    wind_ms = max(wind_ms, 0.1) if pd.notna(wind_ms) else 1.0
    solar_w = (solar_kwh * 1000 / 24) if pd.notna(solar_kwh) else 200
    tg = temp_c + (solar_w / (1 + 0.3 * wind_ms)) * 0.01
    
    # Outdoor WBGT Formula: 0.7*Tw + 0.2*Tg + 0.1*Tdb
    return 0.7 * tw + 0.2 * tg + 0.1 * temp_c


def calculate_utci(temp_c, rh, wind_ms):
    """Approximates Universal Thermal Climate Index (UTCI)."""
    if pd.isna(temp_c) or pd.isna(rh):
        return np.nan
    
    wind_ms = wind_ms if pd.notna(wind_ms) else 1.0
    
    # Polynomial approximation for UTCI heat load
    utci = (temp_c 
            + (0.607 * (temp_c - 20) * (rh / 100)) 
            - (0.25 * wind_ms) 
            + (0.002 * (rh**1.2)))
    return utci


# --- 2. LOAD DATA FROM DATABASE ---

conn = sqlite3.connect("mumbai_heat_health.db")

df = pd.read_sql(
    """
    SELECT * 
    FROM v_ml_features_daily 
    ORDER BY date, ward_id
    """, 
    conn
)

# --- 3. FILL FILLABLE COLUMNS VIA CALCULATION & INTERPOLATION ---

print("Calculating missing climate indices (WBGT, UTCI)...")
df['wbgt_c'] = df.apply(
    lambda r: calculate_wbgt(r['temp_mean_c'], r['humidity_pct'], r['wind_speed_ms'], r['solar_radiation_kwh_m2']), 
    axis=1
)

df['utci_c'] = df.apply(
    lambda r: calculate_utci(r['temp_mean_c'], r['humidity_pct'], r['wind_speed_ms']), 
    axis=1
)

# Impute missing temporal weather values and lags via time-series interpolation
weather_cols = [
    'temp_mean_c', 'temp_max_c', 'temp_min_c', 'humidity_pct', 
    'wind_speed_ms', 'solar_radiation_kwh_m2', 'heat_index_c',
    'temperature_anomaly_c', 'temp_lag_1d', 'temp_lag_3d', 'temp_lag_7d',
    'humidity_lag_1d', 'humidity_lag_3d', 'humidity_lag_7d'
]

df[weather_cols] = df.groupby('ward_id')[weather_cols].transform(
    lambda group: group.ffill().bfill().interpolate(method='linear')
)

# --- 4. EXPORT FILE 1: FILLED DATASET ---

df.to_csv("mumbai_ml_filled.csv", index=False)
print("Saved: 'mumbai_ml_filled.csv' (populated using calculations and interpolation).")


# --- 5. EXPORT FILE 2: STRICT CLEAN DATASET (NO UNFILLED COLUMNS) ---

# Drop remaining columns that contain ALL or ANY unfillable NaN values 
# (e.g., LST satellite readings and ward vulnerability metrics lacking external sources)
df_no_unfilled = df.dropna(how='all', axis=1).copy()
df_no_unfilled = df_no_unfilled.dropna(axis=1)

df_no_unfilled.to_csv("mumbai_ml_cleaned_no_empty_cols.csv", index=False)
print(f"Saved: 'mumbai_ml_cleaned_no_empty_cols.csv' ({len(df_no_unfilled.columns)} columns remain).")

conn.close()