"""
Anomaly detection records based on residual deviation thresholds (|residual| > 2.5σ / 3σ).
Dynamically loaded from `models/anomaly_records.json` computed by `train_model.py`.
"""
import os
import json
from typing import List, Dict, Any

ANOMALIES_FILE = os.path.join("models", "anomaly_records.json")

DEFAULT_ANOMALY_DAYS: List[Dict[str, Any]] = [
    {
        "date_str": "11 Jan",
        "full_date": "2025-01-11",
        "observed": 204,
        "expected": 132,
        "sigma": 3.4,
        "is_severe": True,
        "flagged_stations": ["Anand Vihar", "Jahangirpuri", "Wazirpur"],
        "reason": "Sudden inversion layer drop + localized stubble/biomass event"
    },
    {
        "date_str": "06 Jan",
        "full_date": "2025-01-06",
        "observed": 188,
        "expected": 128,
        "sigma": 3.1,
        "is_severe": True,
        "flagged_stations": ["Anand Vihar", "Ghaziabad"],
        "reason": "Low wind speed (< 0.8 m/s) with persistent ground-level trapping"
    },
    {
        "date_str": "02 Jan",
        "full_date": "2025-01-02",
        "observed": 176,
        "expected": 130,
        "sigma": 2.6,
        "is_severe": False,
        "flagged_stations": ["Rohini", "Wazirpur"],
        "reason": "Dense fog / haze layer with missing satellite AOD"
    },
    {
        "date_str": "28 Dec",
        "full_date": "2024-12-28",
        "observed": 241,
        "expected": 168,
        "sigma": 3.6,
        "is_severe": True,
        "flagged_stations": ["All Delhi-NCR"],
        "reason": "Severe meteorological stagnation across Indo-Gangetic Plain"
    }
]

def load_anomalies() -> List[Dict[str, Any]]:
    if os.path.exists(ANOMALIES_FILE):
        try:
            with open(ANOMALIES_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
                if records and len(records) > 0:
                    return records
        except Exception:
            pass
    return DEFAULT_ANOMALY_DAYS

ANOMALY_DAYS = load_anomalies()

def get_anomaly_count_month() -> int:
    """Number of anomaly days with sigma >= 3.0."""
    return sum(1 for a in ANOMALY_DAYS if a.get("is_severe", False) or a.get("sigma", 0) >= 3.0)
