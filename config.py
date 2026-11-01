"""
Configuration, constants, and color definitions for EcoPulse.
Aligned with Delhi-NCR geospatial coordinates and CPCB standards.
"""

# Geospatial Center & Bounding Box for Delhi-NCR
DELHI_CENTER = [28.6139, 77.2090]
DELHI_ZOOM = 10

# Bounding coordinates for 1 km grid generation (Delhi-NCR core domain)
# Lat: approx 28.40 to 28.85, Lon: approx 76.95 to 77.40
NCR_BOUNDS = {
    "lat_min": 28.42,
    "lat_max": 28.84,
    "lon_min": 76.95,
    "lon_max": 77.38,
}

# CPCB PM2.5 standard categories and color hex codes
# Matches standard air quality bands
AQI_CATEGORIES = [
    {"name": "Good", "min": 0, "max": 30, "color": "#22c55e", "bg": "#dcfce7", "text": "#15803d"},
    {"name": "Satisfactory", "min": 31, "max": 60, "color": "#84cc16", "bg": "#ecfccb", "text": "#3f6212"},
    {"name": "Moderate", "min": 61, "max": 90, "color": "#eab308", "bg": "#fef9c3", "text": "#854d0e"},
    {"name": "Poor", "min": 91, "max": 120, "color": "#f97316", "bg": "#ffedd5", "text": "#9a3412"},
    {"name": "Very Poor", "min": 121, "max": 250, "color": "#ef4444", "bg": "#fee2e2", "text": "#991b1b"},
    {"name": "Severe", "min": 251, "max": 9999, "color": "#7f1d1d", "bg": "#fef2f2", "text": "#450a0a"},
]

def get_pm25_category(val: float):
    for cat in AQI_CATEGORIES:
        if cat["min"] <= val <= cat["max"]:
            return cat
    return AQI_CATEGORIES[-1]

# App Theme Colors matching Wireframe Design
COLORS = {
    "sidebar_bg": "#0f172a",          # Deep navy
    "sidebar_hover": "#1e293b",
    "teal_primary": "#0f766e",        # Wireframe active teal
    "teal_light": "#ccfbf1",
    "teal_hover": "#115e59",
    "accent_orange": "#f97316",
    "accent_red": "#ef4444",
    "accent_amber": "#f59e0b",
    "card_bg": "#ffffff",
    "card_border": "#e2e8f0",
    "text_dark": "#0f172a",
    "text_muted": "#64748b",
    "bg_main": "#f8fafc",
    "alert_bg": "#fffbeb",
    "alert_border": "#f59e0b",
    "alert_text": "#92400e",
}

# Key dates
DEFAULT_DATE = "12 Jan 2025"
AVAILABLE_DATES = [
    "01 Jan 2025", "02 Jan 2025", "03 Jan 2025", "04 Jan 2025",
    "05 Jan 2025", "06 Jan 2025", "07 Jan 2025", "08 Jan 2025",
    "09 Jan 2025", "10 Jan 2025", "11 Jan 2025", "12 Jan 2025"
]
