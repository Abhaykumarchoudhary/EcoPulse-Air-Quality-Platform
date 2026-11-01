"""
Forecasting and Time Series Data for Delhi-NCR and individual monitoring stations.
Includes historical 7-day observed series, 3-day forecast with confidence interval bands,
and multi-week observed vs predicted series with anomaly flags.
"""
from typing import Dict, List, Any

# 7-day past observed + 3-day forecast data for All Delhi-NCR (Mean)
# Reference Date: 12 Jan 2025 (Today)
FORECAST_DATA_NCR = {
    "historical": [
        {"day_label": "06 Jan", "date": "2025-01-06", "observed": 188, "type": "observed"},
        {"day_label": "07 Jan", "date": "2025-01-07", "observed": 142, "type": "observed"},
        {"day_label": "08 Jan", "date": "2025-01-08", "observed": 125, "type": "observed"},
        {"day_label": "09 Jan", "date": "2025-01-09", "observed": 118, "type": "observed"},
        {"day_label": "10 Jan", "date": "2025-01-10", "observed": 134, "type": "observed"},
        {"day_label": "11 Jan", "date": "2025-01-11", "observed": 156, "type": "observed"},
        {"day_label": "12 Jan (Today)", "date": "2025-01-12", "observed": 112, "type": "observed"},
    ],
    "forecast": [
        {"day_label": "13 Jan (+1d)", "date": "2025-01-13", "predicted": 128, "lower": 114, "upper": 142, "type": "forecast"},
        {"day_label": "14 Jan (+2d)", "date": "2025-01-14", "predicted": 145, "lower": 128, "upper": 162, "type": "forecast"},
        {"day_label": "15 Jan (+3d)", "date": "2025-01-15", "predicted": 119, "lower": 101, "upper": 137, "type": "forecast"},
    ]
}

# Per-station forecast adjustments
STATION_FORECASTS = {
    "anand_vihar": {
        "historical": [
            {"day_label": "06 Jan", "observed": 235},
            {"day_label": "07 Jan", "observed": 195},
            {"day_label": "08 Jan", "observed": 182},
            {"day_label": "09 Jan", "observed": 178},
            {"day_label": "10 Jan", "observed": 192},
            {"day_label": "11 Jan", "observed": 210},
            {"day_label": "12 Jan (Today)", "observed": 186},
        ],
        "forecast": [
            {"day_label": "13 Jan (+1d)", "predicted": 198, "lower": 180, "upper": 216},
            {"day_label": "14 Jan (+2d)", "predicted": 212, "lower": 190, "upper": 234},
            {"day_label": "15 Jan (+3d)", "predicted": 184, "lower": 160, "upper": 208},
        ]
    },
    "jahangirpuri": {
        "historical": [
            {"day_label": "06 Jan", "observed": 215},
            {"day_label": "07 Jan", "observed": 180},
            {"day_label": "08 Jan", "observed": 165},
            {"day_label": "09 Jan", "observed": 158},
            {"day_label": "10 Jan", "observed": 176},
            {"day_label": "11 Jan", "observed": 192},
            {"day_label": "12 Jan (Today)", "observed": 174},
        ],
        "forecast": [
            {"day_label": "13 Jan (+1d)", "predicted": 182, "lower": 166, "upper": 198},
            {"day_label": "14 Jan (+2d)", "predicted": 195, "lower": 175, "upper": 215},
            {"day_label": "15 Jan (+3d)", "predicted": 168, "lower": 146, "upper": 190},
        ]
    }
}

# Long-term Observed vs Predicted Time Series (Dec 1, 2024 to Jan 12, 2025)
# Used for the lower time series chart with anomaly red dots in Wireframe 2b
LONG_TERM_SERIES = [
    {"date": "2024-12-01", "observed": 138, "predicted": 134, "anomaly": False, "sigma": 0.4},
    {"date": "2024-12-02", "observed": 171, "predicted": 133, "anomaly": True, "sigma": 2.1},
    {"date": "2024-12-03", "observed": 140, "predicted": 136, "anomaly": False, "sigma": 0.5},
    {"date": "2024-12-04", "observed": 145, "predicted": 142, "anomaly": False, "sigma": 0.3},
    {"date": "2024-12-05", "observed": 150, "predicted": 148, "anomaly": False, "sigma": 0.2},
    {"date": "2024-12-06", "observed": 160, "predicted": 152, "anomaly": False, "sigma": 0.9},
    {"date": "2024-12-07", "observed": 155, "predicted": 149, "anomaly": False, "sigma": 0.7},
    {"date": "2024-12-08", "observed": 162, "predicted": 154, "anomaly": False, "sigma": 0.8},
    {"date": "2024-12-09", "observed": 230, "predicted": 159, "anomaly": True, "sigma": 3.5},
    {"date": "2024-12-10", "observed": 175, "predicted": 165, "anomaly": False, "sigma": 1.1},
    {"date": "2024-12-11", "observed": 168, "predicted": 162, "anomaly": False, "sigma": 0.6},
    {"date": "2024-12-12", "observed": 142, "predicted": 138, "anomaly": False, "sigma": 0.4},
    {"date": "2024-12-13", "observed": 130, "predicted": 126, "anomaly": False, "sigma": 0.4},
    {"date": "2024-12-14", "observed": 135, "predicted": 129, "anomaly": False, "sigma": 0.6},
    {"date": "2024-12-15", "observed": 162, "predicted": 121, "anomaly": True, "sigma": 2.2},
    {"date": "2024-12-16", "observed": 145, "predicted": 140, "anomaly": False, "sigma": 0.5},
    {"date": "2024-12-17", "observed": 152, "predicted": 146, "anomaly": False, "sigma": 0.6},
    {"date": "2024-12-18", "observed": 160, "predicted": 155, "anomaly": False, "sigma": 0.5},
    {"date": "2024-12-19", "observed": 158, "predicted": 150, "anomaly": False, "sigma": 0.8},
    {"date": "2024-12-20", "observed": 165, "predicted": 156, "anomaly": False, "sigma": 0.9},
    {"date": "2024-12-21", "observed": 199, "predicted": 151, "anomaly": True, "sigma": 2.4},
    {"date": "2024-12-22", "observed": 170, "predicted": 162, "anomaly": False, "sigma": 0.8},
    {"date": "2024-12-23", "observed": 160, "predicted": 158, "anomaly": False, "sigma": 0.2},
    {"date": "2024-12-24", "observed": 155, "predicted": 152, "anomaly": False, "sigma": 0.3},
    {"date": "2024-12-25", "observed": 172, "predicted": 166, "anomaly": False, "sigma": 0.6},
    {"date": "2024-12-26", "observed": 180, "predicted": 172, "anomaly": False, "sigma": 0.8},
    {"date": "2024-12-27", "observed": 185, "predicted": 176, "anomaly": False, "sigma": 0.9},
    {"date": "2024-12-28", "observed": 241, "predicted": 168, "anomaly": True, "sigma": 3.6},
    {"date": "2024-12-29", "observed": 195, "predicted": 182, "anomaly": False, "sigma": 1.3},
    {"date": "2024-12-30", "observed": 178, "predicted": 170, "anomaly": False, "sigma": 0.8},
    {"date": "2024-12-31", "observed": 182, "predicted": 175, "anomaly": False, "sigma": 0.7},
    {"date": "2025-01-01", "observed": 190, "predicted": 180, "anomaly": False, "sigma": 1.0},
    {"date": "2025-01-02", "observed": 176, "predicted": 130, "anomaly": True, "sigma": 2.6},
    {"date": "2025-01-03", "observed": 150, "predicted": 144, "anomaly": False, "sigma": 0.6},
    {"date": "2025-01-04", "observed": 142, "predicted": 139, "anomaly": False, "sigma": 0.3},
    {"date": "2025-01-05", "observed": 148, "predicted": 141, "anomaly": False, "sigma": 0.7},
    {"date": "2025-01-06", "observed": 188, "predicted": 128, "anomaly": True, "sigma": 3.1},
    {"date": "2025-01-07", "observed": 142, "predicted": 136, "anomaly": False, "sigma": 0.6},
    {"date": "2025-01-08", "observed": 125, "predicted": 122, "anomaly": False, "sigma": 0.3},
    {"date": "2025-01-09", "observed": 118, "predicted": 115, "anomaly": False, "sigma": 0.3},
    {"date": "2025-01-10", "observed": 134, "predicted": 130, "anomaly": False, "sigma": 0.4},
    {"date": "2025-01-11", "observed": 204, "predicted": 132, "anomaly": True, "sigma": 3.4},
    {"date": "2025-01-12", "observed": 112, "predicted": 110, "anomaly": False, "sigma": 0.2},
]
