DROP VIEW IF EXISTS v_ml_features_daily;

CREATE VIEW v_ml_features_daily AS
SELECT
    c.date,
    c.ward_id,
    w.ward_name,

    c.temp_mean_c,
    c.temp_max_c,
    c.temp_min_c,

    c.humidity_pct,
    c.wind_speed_ms,
    c.solar_radiation_kwh_m2,

    c.heat_index_c,
    c.wbgt_c,
    c.utci_c,

    c.lst_day_c,
    c.lst_night_c,

    c.temperature_anomaly_c,

    c.is_heatwave_day,
    c.heatwave_duration_days,

    c.temp_lag_1d,
    c.temp_lag_3d,
    c.temp_lag_7d,

    c.humidity_lag_1d,
    c.humidity_lag_3d,
    c.humidity_lag_7d,

    v.population,
    v.population_density_km2,
    v.elderly_percent,
    v.outdoor_worker_percent,
    v.built_up_density_percent,
    v.healthcare_facilities,
    v.healthcare_access_score

FROM fact_climate_daily c

JOIN dim_ward w
    ON c.ward_id = w.ward_id

LEFT JOIN fact_ward_vulnerability_yearly v
    ON c.ward_id = v.ward_id
    AND CAST(strftime('%Y', c.date) AS INTEGER) = v.year;