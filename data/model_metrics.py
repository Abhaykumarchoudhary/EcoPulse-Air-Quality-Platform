"""
Model performance metrics, cross-validation LOSO results, and SHAP explainability.
Directly matches Wireframe 2c.
"""
from typing import List, Dict, Any
import numpy as np

# Model Comparison Table
MODEL_COMPARISON: List[Dict[str, Any]] = [
    {
        "name": "Weather-only",
        "r2": 0.52,
        "rmse": 48.1,
        "mae": 35.6,
        "is_best": False
    },
    {
        "name": "AOD-only linear",
        "r2": 0.61,
        "rmse": 42.7,
        "mae": 31.2,
        "is_best": False
    },
    {
        "name": "RF/XGBoost fusion",
        "r2": 0.78,
        "rmse": 29.4,
        "mae": 21.8,
        "is_best": True
    }
]

# Per-station leave-one-station-out (LOSO) cross-validation error
# Worst station in amber (Anand Vihar), others in teal
STATION_LOSO_ERRORS: List[Dict[str, Any]] = [
    {"station": "Anand Vihar", "mae": 32.4, "is_worst": True, "color": "#f59e0b"},
    {"station": "Jahangirpuri", "mae": 26.8, "is_worst": False, "color": "#0f766e"},
    {"station": "Wazirpur", "mae": 24.1, "is_worst": False, "color": "#0f766e"},
    {"station": "Rohini", "mae": 22.5, "is_worst": False, "color": "#0f766e"},
    {"station": "Punjabi Bagh", "mae": 21.0, "is_worst": False, "color": "#0f766e"},
    {"station": "Dwarka Sec 8", "mae": 19.8, "is_worst": False, "color": "#0f766e"},
    {"station": "ITO", "mae": 18.2, "is_worst": False, "color": "#0f766e"},
]

# SHAP Feature Importance
# AOD in teal, others in slate grey
SHAP_IMPORTANCE: List[Dict[str, Any]] = [
    {"feature": "AOD", "importance": 0.46, "color": "#0f766e", "description": "Satellite Aerosol Optical Depth (1 km)"},
    {"feature": "BLH", "importance": 0.28, "color": "#64748b", "description": "Boundary-layer height (atmospheric mixing depth)"},
    {"feature": "Wind", "importance": 0.16, "color": "#64748b", "description": "Surface wind speed (dispersion velocity)"},
    {"feature": "RH", "importance": 0.10, "color": "#64748b", "description": "Relative humidity (secondary aerosol hygroscopic growth)"},
]

def generate_scatter_data(n_points: int = 120, seed: int = 42):
    """
    Generates realistic observed vs predicted scatter points for R^2 = 0.78.
    """
    np.random.seed(seed)
    observed = np.random.uniform(50, 240, n_points)
    # y = x + normal error proportional to residual variance (R2 ~ 0.78)
    error = np.random.normal(0, 18.5, n_points)
    predicted = 0.82 * observed + 22.0 + error
    predicted = np.clip(predicted, 40, 260)
    
    return [
        {"observed": round(float(o), 1), "predicted": round(float(p), 1)}
        for o, p in zip(observed, predicted)
    ]

SCATTER_POINTS = generate_scatter_data()
