PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dim_date (
    date TEXT PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_of_year INTEGER,
    week INTEGER
);

CREATE TABLE IF NOT EXISTS dim_ward (
    ward_id INTEGER PRIMARY KEY,
    ward_name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_climate_daily (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    date TEXT NOT NULL,
    ward_id INTEGER NOT NULL,

    temp_mean_c REAL,
    temp_max_c REAL,
    temp_min_c REAL,

    humidity_pct REAL,
    wind_speed_ms REAL,
    solar_radiation_kwh_m2 REAL,

    heat_index_c REAL,
    wbgt_c REAL,
    utci_c REAL,

    lst_day_c REAL,
    lst_night_c REAL,

    temperature_anomaly_c REAL,

    is_heatwave_day INTEGER DEFAULT 0,
    heatwave_duration_days INTEGER,

    temp_lag_1d REAL,
    temp_lag_3d REAL,
    temp_lag_7d REAL,

    humidity_lag_1d REAL,
    humidity_lag_3d REAL,
    humidity_lag_7d REAL,

    FOREIGN KEY (date) REFERENCES dim_date(date),
    FOREIGN KEY (ward_id) REFERENCES dim_ward(ward_id),

    UNIQUE(date, ward_id)
);

CREATE TABLE IF NOT EXISTS fact_climate_monthly (
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    ward_id INTEGER NOT NULL,

    temp_mean_c REAL,
    temp_max_c REAL,
    temp_min_c REAL,

    humidity_mean_pct REAL,
    wind_speed_mean_ms REAL,
    solar_radiation_mean REAL,

    heat_index_mean_c REAL,
    wbgt_mean_c REAL,
    utci_mean_c REAL,

    lst_mean_c REAL,
    temperature_anomaly_c REAL,

    heatwave_days INTEGER,

    PRIMARY KEY(year, month, ward_id)
);

CREATE TABLE IF NOT EXISTS fact_climate_yearly (
    year INTEGER NOT NULL,
    ward_id INTEGER NOT NULL,

    temp_mean_c REAL,
    temp_max_c REAL,
    temp_min_c REAL,

    humidity_mean_pct REAL,
    wind_speed_mean_ms REAL,
    solar_radiation_mean REAL,

    heat_index_mean_c REAL,
    wbgt_mean_c REAL,
    utci_mean_c REAL,

    lst_mean_c REAL,
    temperature_anomaly_c REAL,

    heatwave_days INTEGER,

    PRIMARY KEY(year, ward_id)
);

CREATE TABLE IF NOT EXISTS fact_ward_vulnerability_yearly (
    year INTEGER NOT NULL,
    ward_id INTEGER NOT NULL,

    population INTEGER,
    population_density_km2 REAL,

    elderly_percent REAL,
    outdoor_worker_percent REAL,

    built_up_density_percent REAL,

    healthcare_facilities INTEGER,
    healthcare_access_score REAL,

    PRIMARY KEY(year, ward_id)
);

CREATE TABLE IF NOT EXISTS fact_heat_health_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,

    event_date TEXT,
    ward_id INTEGER,

    event_type TEXT,

    max_temperature_c REAL,

    deaths INTEGER,
    hospitalizations INTEGER,

    source TEXT,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_daily_date
ON fact_climate_daily(date);

CREATE INDEX IF NOT EXISTS idx_daily_ward
ON fact_climate_daily(ward_id);

CREATE INDEX IF NOT EXISTS idx_vulnerability_ward
ON fact_ward_vulnerability_yearly(ward_id);
CREATE TABLE IF NOT EXISTS fact_ward_vulnerability_yearly (
    year INTEGER NOT NULL,
    ward_id INTEGER NOT NULL,

    population INTEGER,
    population_density_km2 REAL,

    elderly_percent REAL,
    outdoor_worker_percent REAL,

    built_up_density_percent REAL,

    healthcare_facilities INTEGER,
    healthcare_access_score REAL,

    PRIMARY KEY (year, ward_id),

    FOREIGN KEY (ward_id)
        REFERENCES dim_ward(ward_id)
);