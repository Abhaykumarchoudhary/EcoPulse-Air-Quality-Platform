"""
Combined Insights Data: Cross-correlation between PM2.5 and Sector Emissions.
Includes monthly dual-axis series with winter masks, Pearson correlation matrix,
seasonal 12-month profile, and emission hotspot facilities.
"""
from typing import List, Dict, Any

# Dual-axis monthly series (Jan 2023 - Dec 2024)
MONTHLY_DUAL_AXIS = [
    # 2023
    {"month": "Jan 2023", "pm25": 195, "emissions": 5.8, "is_winter": True},
    {"month": "Feb 2023", "pm25": 160, "emissions": 5.4, "is_winter": True},
    {"month": "Mar 2023", "pm25": 98,  "emissions": 5.1, "is_winter": False},
    {"month": "Apr 2023", "pm25": 82,  "emissions": 4.9, "is_winter": False},
    {"month": "May 2023", "pm25": 76,  "emissions": 5.3, "is_winter": False},
    {"month": "Jun 2023", "pm25": 65,  "emissions": 5.6, "is_winter": False},
    {"month": "Jul 2023", "pm25": 42,  "emissions": 4.8, "is_winter": False},
    {"month": "Aug 2023", "pm25": 38,  "emissions": 4.7, "is_winter": False},
    {"month": "Sep 2023", "pm25": 48,  "emissions": 4.9, "is_winter": False},
    {"month": "Oct 2023", "pm25": 125, "emissions": 5.5, "is_winter": False},
    {"month": "Nov 2023", "pm25": 235, "emissions": 6.2, "is_winter": True},
    {"month": "Dec 2023", "pm25": 210, "emissions": 6.4, "is_winter": True},
    # 2024
    {"month": "Jan 2024", "pm25": 204, "emissions": 6.0, "is_winter": True},
    {"month": "Feb 2024", "pm25": 155, "emissions": 5.5, "is_winter": True},
    {"month": "Mar 2024", "pm25": 92,  "emissions": 5.0, "is_winter": False},
    {"month": "Apr 2024", "pm25": 78,  "emissions": 4.8, "is_winter": False},
    {"month": "May 2024", "pm25": 72,  "emissions": 5.4, "is_winter": False},
    {"month": "Jun 2024", "pm25": 60,  "emissions": 5.7, "is_winter": False},
    {"month": "Jul 2024", "pm25": 39,  "emissions": 4.9, "is_winter": False},
    {"month": "Aug 2024", "pm25": 35,  "emissions": 4.6, "is_winter": False},
    {"month": "Sep 2024", "pm25": 45,  "emissions": 5.0, "is_winter": False},
    {"month": "Oct 2024", "pm25": 130, "emissions": 5.6, "is_winter": False},
    {"month": "Nov 2024", "pm25": 240, "emissions": 6.3, "is_winter": True},
    {"month": "Dec 2024", "pm25": 218, "emissions": 6.5, "is_winter": True},
]

# Pearson Correlation Heatmap Table (PM2.5 vs Sector Emissions)
CORRELATION_HEATMAP = [
    {
        "sector": "Power",
        "r": 0.68,
        "color": "#ef4444",      # Vibrant Red/Coral for strong positive
        "bg_color": "#fee2e2",
        "text_color": "#991b1b"
    },
    {
        "sector": "Transport",
        "r": 0.41,
        "color": "#f87171",      # Light pink/peach
        "bg_color": "#ffedd5",
        "text_color": "#9a3412"
    },
    {
        "sector": "Industry",
        "r": 0.37,
        "color": "#fca5a5",      # Soft pink
        "bg_color": "#fef2f2",
        "text_color": "#b91c1c"
    },
    {
        "sector": "Buildings",
        "r": -0.12,
        "color": "#93c5fd",      # Soft blue for negative/neutral
        "bg_color": "#eff6ff",
        "text_color": "#1e40af"
    }
]

# 12-Month Seasonal PM2.5 Pattern (Average monthly PM2.5 across Delhi-NCR)
# Dark navy for winter months, lighter slate grey for non-winter
SEASONAL_PATTERN = [
    {"month": "Jan", "pm25": 200, "is_winter": True,  "color": "#0f172a"},
    {"month": "Feb", "pm25": 158, "is_winter": True,  "color": "#0f172a"},
    {"month": "Mar", "pm25": 95,  "is_winter": False, "color": "#475569"},
    {"month": "Apr", "pm25": 80,  "is_winter": False, "color": "#64748b"},
    {"month": "May", "pm25": 74,  "is_winter": False, "color": "#64748b"},
    {"month": "Jun", "pm25": 62,  "is_winter": False, "color": "#94a3b8"},
    {"month": "Jul", "pm25": 40,  "is_winter": False, "color": "#94a3b8"},
    {"month": "Aug", "pm25": 36,  "is_winter": False, "color": "#94a3b8"},
    {"month": "Sep", "pm25": 46,  "is_winter": False, "color": "#94a3b8"},
    {"month": "Oct", "pm25": 128, "is_winter": False, "color": "#64748b"},
    {"month": "Nov", "pm25": 238, "is_winter": True,  "color": "#0f172a"},
    {"month": "Dec", "pm25": 214, "is_winter": True,  "color": "#0f172a"},
]

# Point emission source hotspots across Delhi-NCR
# Displayed as purple/violet diamonds/squares on the hotspot map
EMISSION_HOTSPOTS = [
    {
        "id": "power_badarpur",
        "name": "Badarpur Energy Hub",
        "sector": "Power",
        "lat": 28.5085,
        "lon": 77.3039,
        "emissions_kt": 4850,
        "marker_size": 26,
        "color": "#7c3aed"
    },
    {
        "id": "power_dadri",
        "name": "NTPC Dadri Complex",
        "sector": "Power",
        "lat": 28.5833,
        "lon": 77.5500,
        "emissions_kt": 6200,
        "marker_size": 32,
        "color": "#7c3aed"
    },
    {
        "id": "power_indraprastha",
        "name": "IP Thermal Hub (historical)",
        "sector": "Power",
        "lat": 28.6258,
        "lon": 77.2492,
        "emissions_kt": 1420,
        "marker_size": 18,
        "color": "#7c3aed"
    },
    {
        "id": "ind_bawana",
        "name": "Bawana Industrial Area",
        "sector": "Industry",
        "lat": 28.7900,
        "lon": 77.0400,
        "emissions_kt": 2850,
        "marker_size": 22,
        "color": "#8b5cf6"
    },
    {
        "id": "ind_mayapuri",
        "name": "Mayapuri Industrial Cluster",
        "sector": "Industry",
        "lat": 28.6350,
        "lon": 77.1250,
        "emissions_kt": 1950,
        "marker_size": 19,
        "color": "#8b5cf6"
    },
    {
        "id": "ind_ghaziabad",
        "name": "Sahibabad Industrial Area",
        "sector": "Industry",
        "lat": 28.6750,
        "lon": 77.3650,
        "emissions_kt": 3100,
        "marker_size": 24,
        "color": "#8b5cf6"
    },
    {
        "id": "trans_anandvihar",
        "name": "Anand Vihar ISBT & Terminal",
        "sector": "Transport",
        "lat": 28.6475,
        "lon": 77.3150,
        "emissions_kt": 2100,
        "marker_size": 20,
        "color": "#a855f7"
    },
    {
        "id": "trans_kashmeregate",
        "name": "Kashmere Gate Transit Node",
        "sector": "Transport",
        "lat": 28.6670,
        "lon": 77.2280,
        "emissions_kt": 1800,
        "marker_size": 18,
        "color": "#a855f7"
    },
    {
        "id": "trans_dhaula_kuan",
        "name": "Dhaula Kuan Highway Interchange",
        "sector": "Transport",
        "lat": 28.5925,
        "lon": 77.1610,
        "emissions_kt": 1650,
        "marker_size": 17,
        "color": "#a855f7"
    }
]
