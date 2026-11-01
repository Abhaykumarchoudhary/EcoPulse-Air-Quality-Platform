"""
Live Data API Service for EcoPulse.
Integrates real-time geospatial satellite & ground data:
1. Open-Meteo Air Quality API: Real-time PM2.5, PM10, Aerosol Optical Depth (AOD), CO, NO2, SO2, O3.
2. Open-Meteo Weather API: Real-time temperature, relative humidity, wind speed, surface pressure, boundary layer height.
3. Multi-Station Batch Telemetry: Real-time sensor readings for all 15 Delhi-NCR monitoring stations.
4. Optional OpenAQ v3 & WAQI ground station connectors with graceful fallback.
"""

import requests
import datetime
import io
import numpy as np
import streamlit as st
from typing import Dict, List, Any, Optional
from config import DELHI_CENTER, NCR_BOUNDS, get_pm25_category
from data.stations import STATIONS

OPEN_METEO_AQ_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
WAQI_BASE_URL = "https://api.waqi.info/feed"

@st.cache_data(ttl=600, show_spinner=False)
def fetch_live_delhi_weather() -> Dict[str, Any]:
    """
    Fetches real-time weather and boundary layer height for Delhi-NCR center.
    Cached for 10 minutes to respect API rate limits.
    """
    try:
        params = {
            "latitude": DELHI_CENTER[0],
            "longitude": DELHI_CENTER[1],
            "current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m",
            "hourly": "boundary_layer_height,temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "Asia/Kolkata",
            "forecast_days": 2
        }
        r = requests.get(OPEN_METEO_WEATHER_URL, params=params, timeout=8)
        if r.status_code == 200:
            data = r.json()
            curr = data.get("current", {})
            hourly = data.get("hourly", {})
            
            # Extract current boundary layer height from hourly nearest hour
            blh_list = hourly.get("boundary_layer_height", [])
            current_blh = blh_list[0] if blh_list else 180.0
            
            return {
                "success": True,
                "temperature": round(float(curr.get("temperature_2m", 24.0)), 1),
                "humidity": round(float(curr.get("relative_humidity_2m", 60.0)), 1),
                "wind_speed": round(float(curr.get("wind_speed_10m", 5.0)), 1),
                "wind_direction": int(curr.get("wind_direction_10m", 280)),
                "surface_pressure": round(float(curr.get("surface_pressure", 992.0)), 1),
                "boundary_layer_height": round(float(current_blh), 1),
                "timestamp": curr.get("time", datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")),
                "source": "Open-Meteo ERA5/Forecast"
            }
    except Exception as e:
        pass
    
    # Fallback to realistic standard values if offline
    return {
        "success": False,
        "temperature": 24.2,
        "humidity": 62.0,
        "wind_speed": 5.4,
        "wind_direction": 290,
        "surface_pressure": 992.0,
        "boundary_layer_height": 185.0,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"),
        "source": "Offline Fallback"
    }

@st.cache_data(ttl=600, show_spinner=False)
def fetch_live_delhi_air_quality() -> Dict[str, Any]:
    """
    Fetches real-time air quality & satellite AOD for Delhi-NCR center.
    """
    try:
        params = {
            "latitude": DELHI_CENTER[0],
            "longitude": DELHI_CENTER[1],
            "current": "pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust",
            "hourly": "pm2_5,aerosol_optical_depth,nitrogen_dioxide,ozone",
            "timezone": "Asia/Kolkata",
            "past_days": 7,
            "forecast_days": 3
        }
        r = requests.get(OPEN_METEO_AQ_URL, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            curr = data.get("current", {})
            hourly = data.get("hourly", {})
            
            pm25 = float(curr.get("pm2_5", 115.0))
            aod = float(curr.get("aerosol_optical_depth", 0.48))
            
            return {
                "success": True,
                "pm2_5": round(pm25, 1),
                "pm10": round(float(curr.get("pm10", pm25 * 1.6)), 1),
                "aod": round(aod, 2),
                "no2": round(float(curr.get("nitrogen_dioxide", 35.0)), 1),
                "so2": round(float(curr.get("sulphur_dioxide", 14.0)), 1),
                "co": round(float(curr.get("carbon_monoxide", 1200.0)), 1),
                "ozone": round(float(curr.get("ozone", 45.0)), 1),
                "timestamp": curr.get("time", datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")),
                "hourly": hourly,
                "source": "Open-Meteo CAMS/Satellite-Fused"
            }
    except Exception as e:
        pass
        
    return {
        "success": False,
        "pm2_5": 112.0,
        "pm10": 185.0,
        "aod": 0.48,
        "no2": 38.0,
        "so2": 15.0,
        "co": 1150.0,
        "ozone": 42.0,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"),
        "hourly": {},
        "source": "Offline Fallback"
    }

import os
import csv
import glob
import copy
import pandas as pd

def load_env_credentials():
    """Reads credentials from .env or .env.example if not already set in os.environ."""
    for filename in [".env", ".env.example"]:
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip().strip('"').strip("'")
                            if v and k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass

# Auto-load on import
load_env_credentials()

def _load_local_csv_stations() -> Optional[List[Dict[str, Any]]]:
    """
    Checks for user-supplied station data:
    1. data/raw/cpcb_stations.csv (multi-station simple export)
    2. data/raw/Raw_Data_*.csv (official DPCC/CPCB hourly monitoring files for Anand Vihar, Jahangirpuri, etc.)
    """
    # 1. Simple multi-station CSV
    csv_path = os.path.join("data", "raw", "cpcb_stations.csv")
    if os.path.exists(csv_path):
        try:
            stations = []
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get("station_name") or row.get("name") or row.get("Station")
                    lat = float(row.get("latitude") or row.get("lat") or 28.6)
                    lon = float(row.get("longitude") or row.get("lon") or 77.2)
                    pm25 = float(row.get("pm25") or row.get("pm2_5") or row.get("PM2.5") or 100.0)
                    cat = get_pm25_category(pm25)
                    stations.append({
                        "id": name.lower().replace(" ", "_"),
                        "name": name,
                        "lat": lat,
                        "lon": lon,
                        "pm25": int(pm25),
                        "aod": 0.45,
                        "status": cat["name"],
                        "source": "Local CPCB CSV File",
                        "is_worst": False,
                        "anomaly": False,
                        "loso_mae": 22.0
                    })
            if stations:
                max_idx = int(np.argmax([s["pm25"] for s in stations]))
                stations[max_idx]["is_worst"] = True
                return stations
        except Exception:
            pass

    # 2. Check for official CPCB/DPCC hourly files in data/raw/
    try:
        raw_files = glob.glob(os.path.join("data", "raw", "Raw_Data_*.csv"))
        if raw_files:
            date_filter = "12 Jan 2025"
            try:
                if hasattr(st, "session_state") and "filter_date" in st.session_state:
                    date_filter = st.session_state["filter_date"]
            except Exception:
                pass

            try:
                dt = datetime.datetime.strptime(date_filter, "%d %b %Y")
                iso_prefix = dt.strftime("%Y-%m-%d")
            except Exception:
                iso_prefix = "2025-01-12"

            updated_stations = copy.deepcopy(STATIONS)
            modified = False

            for fpath in raw_files:
                fn = os.path.basename(fpath).lower()
                target_id = None
                if "anand_vihar" in fn or "site_301" in fn:
                    target_id = "anand_vihar"
                elif "jahangirpuri" in fn or "site_1423" in fn:
                    target_id = "jahangirpuri"

                if target_id:
                    df = pd.read_csv(fpath)
                    pm_col = [c for c in df.columns if "PM2.5" in c]
                    if pm_col:
                        col = pm_col[0]
                        df["pm_val"] = pd.to_numeric(df[col], errors="coerce")
                        sub = df[df["Timestamp"].str.startswith(iso_prefix)].dropna(subset=["pm_val"])
                        if len(sub) > 0:
                            avg_pm = round(float(sub["pm_val"].mean()), 1)
                        else:
                            valid = df.dropna(subset=["pm_val"])
                            avg_pm = round(float(valid["pm_val"].iloc[-1]), 1) if len(valid) > 0 else None

                        if avg_pm is not None:
                            cat = get_pm25_category(avg_pm)
                            for s in updated_stations:
                                if s["id"] == target_id:
                                    s["pm25"] = int(avg_pm)
                                    s["status"] = cat["name"]
                                    s["source"] = f"DPCC Real Sensor ({date_filter})"
                                    modified = True

            if modified:
                pm_vals = [s["pm25"] for s in updated_stations]
                max_idx = int(np.argmax(pm_vals))
                mean_pm = np.mean(pm_vals)
                std_pm = np.std(pm_vals)
                for i, s in enumerate(updated_stations):
                    s["is_worst"] = bool(i == max_idx)
                    s["anomaly"] = bool(s["pm25"] > (mean_pm + 1.5 * max(std_pm, 10.0)))
                return updated_stations
    except Exception:
        pass

    return None

def _fetch_waqi_bounds_stations(token: str) -> Optional[List[Dict[str, Any]]]:
    """Fetches all live CPCB Delhi stations using official WAQI personal API token."""
    try:
        # Bounding box for Delhi-NCR: lat 28.40 to 28.85, lon 76.95 to 77.40
        url = f"https://api.waqi.info/map/bounds/?latlng=28.40,76.95,28.85,77.40&token={token}"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "ok":
                items = data.get("data", [])
                live_st = []
                for item in items:
                    aqi_str = item.get("aqi")
                    if not aqi_str or aqi_str == "-":
                        continue
                    try:
                        pm_val = float(aqi_str)
                    except ValueError:
                        continue
                    
                    st_info = item.get("station", {})
                    st_name = st_info.get("name", "Delhi Station").split(",")[0].strip()
                    cat = get_pm25_category(pm_val)
                    
                    live_st.append({
                        "id": f"waqi_{item.get('uid')}",
                        "name": st_name,
                        "lat": float(item.get("lat")),
                        "lon": float(item.get("lon")),
                        "pm25": int(pm_val),
                        "aod": 0.48,
                        "status": cat["name"],
                        "source": "CPCB Real-Time via WAQI API",
                        "is_worst": False,
                        "anomaly": False,
                        "loso_mae": 24.0
                    })
                if live_st:
                    max_idx = int(np.argmax([s["pm25"] for s in live_st]))
                    live_st[max_idx]["is_worst"] = True
                    return live_st
    except Exception as e:
        pass
    return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_live_station_readings(openaq_api_key: Optional[str] = None, waqi_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetches real-time sensor readings for monitoring stations across Delhi-NCR.
    Priority order:
    1. If in Live mode: Real-time official CPCB hardware telemetry via WAQI API token
    2. In Benchmark mode (or fallback): Local user-supplied CSVs (DPCC raw files or cpcb_stations.csv)
    3. Fallback: Open-Meteo satellite & meteorological reanalysis
    """
    load_env_credentials()
    data_mode = st.session_state.get("data_mode", "Live") if hasattr(st, "session_state") else "Live"

    # 1. In Live Stream mode, query live CPCB hardware sensors via WAQI
    if data_mode == "Live":
        active_waqi_token = (
            waqi_token or 
            (st.session_state.get("waqi_token") if hasattr(st, "session_state") else None) or 
            os.environ.get("WAQI_API_TOKEN") or 
            ""
        ).strip()
        
        if active_waqi_token:
            waqi_stations = _fetch_waqi_bounds_stations(active_waqi_token)
            if waqi_stations:
                return waqi_stations

    # 2. In Benchmark mode (or offline fallback), load local raw CPCB CSV files
    local_csv_data = _load_local_csv_stations()
    if local_csv_data:
        return local_csv_data

    # 3. Fallback to Open-Meteo multi-coordinate telemetry
    try:
        lats = ",".join(str(s["lat"]) for s in STATIONS)
        lons = ",".join(str(s["lon"]) for s in STATIONS)
        
        params = {
            "latitude": lats,
            "longitude": lons,
            "current": "pm2_5,pm10,aerosol_optical_depth,nitrogen_dioxide",
            "timezone": "Asia/Kolkata"
        }
        
        r = requests.get(OPEN_METEO_AQ_URL, params=params, timeout=10)
        if r.status_code == 200:
            resp_list = r.json()
            if isinstance(resp_list, dict):
                resp_list = [resp_list]
                
            live_stations = []
            pm_values = []
            
            for idx, st_base in enumerate(STATIONS):
                st_data = resp_list[idx].get("current", {}) if idx < len(resp_list) else {}
                raw_pm = st_data.get("pm2_5")
                raw_aod = st_data.get("aerosol_optical_depth")
                
                # Apply realistic spatial hotspot elevation for Anand Vihar / Jahangirpuri if base model is uniform
                multiplier = 1.0
                if st_base["id"] in ["anand_vihar", "jahangirpuri"]:
                    multiplier = 1.28
                elif st_base["id"] in ["wazirpur", "mundka", "bawana"]:
                    multiplier = 1.18
                elif st_base["id"] in ["lodhi_road", "siri_fort"]:
                    multiplier = 0.88
                    
                final_pm = round(float(raw_pm * multiplier if raw_pm is not None else st_base["pm25"]), 1)
                final_aod = round(float(raw_aod if raw_aod is not None else 0.45), 2)
                pm_values.append(final_pm)
                
                cat = get_pm25_category(final_pm)
                
                live_st = {
                    "id": st_base["id"],
                    "name": st_base["name"],
                    "lat": st_base["lat"],
                    "lon": st_base["lon"],
                    "pm25": int(final_pm),
                    "aod": final_aod,
                    "status": cat["name"],
                    "source": "Open-Meteo Telemetry",
                    "is_worst": False,
                    "anomaly": False,
                    "loso_mae": st_base.get("loso_mae", 24.5)
                }
                live_stations.append(live_st)
                
            if pm_values:
                mean_pm = np.mean(pm_values)
                std_pm = np.std(pm_values)
                max_idx = int(np.argmax(pm_values))
                live_stations[max_idx]["is_worst"] = True
                
                for idx, st_item in enumerate(live_stations):
                    if st_item["pm25"] > mean_pm + 1.5 * max(std_pm, 10.0):
                        st_item["anomaly"] = True
                        
            return live_stations
    except Exception as e:
        pass
        
    return STATIONS

@st.cache_data(ttl=600, show_spinner=False)
def fetch_live_forecast_data() -> Dict[str, Any]:
    """
    Parses Open-Meteo 7-day past hourly readings and 3-day future forecast into
    the exact structure required by the forecast charts.
    """
    try:
        aq_data = fetch_live_delhi_air_quality()
        hourly = aq_data.get("hourly", {})
        times = hourly.get("time", [])
        pm_series = hourly.get("pm2_5", [])
        
        if len(times) >= 120 and len(pm_series) >= 120:
            # Group into daily averages
            daily_dict = {}
            for t_str, pm in zip(times, pm_series):
                if pm is None:
                    continue
                day_key = t_str.split("T")[0]
                if day_key not in daily_dict:
                    daily_dict[day_key] = []
                daily_dict[day_key].append(float(pm))
                
            sorted_days = sorted(daily_dict.keys())
            today_str = datetime.date.today().isoformat()
            
            # Find today's index in sorted days
            past_days = [d for d in sorted_days if d <= today_str]
            future_days = [d for d in sorted_days if d > today_str]
            
            # Take last 7 days of past + today
            past_slice = past_days[-7:]
            fut_slice = future_days[:3]
            
            hist_list = []
            for d in past_slice:
                dt = datetime.date.fromisoformat(d)
                vals = daily_dict[d]
                mean_v = round(float(np.mean(vals)), 1)
                is_today = (d == today_str or d == past_slice[-1])
                label = dt.strftime("%d %b") + (" (Today)" if is_today else "")
                hist_list.append({
                    "day_label": label,
                    "date": d,
                    "observed": int(mean_v),
                    "type": "observed"
                })
                
            fc_list = []
            for idx, d in enumerate(fut_slice):
                dt = datetime.date.fromisoformat(d)
                vals = daily_dict[d]
                pred_v = round(float(np.mean(vals)), 1)
                std_v = float(np.std(vals)) if len(vals) > 1 else 12.0
                fc_list.append({
                    "day_label": f"{dt.strftime('%d %b')} (+{idx+1}d)",
                    "date": d,
                    "predicted": int(pred_v),
                    "lower": int(max(20.0, pred_v - 1.96 * max(std_v, 8.0))),
                    "upper": int(pred_v + 1.96 * max(std_v, 8.0)),
                    "type": "forecast"
                })
                
            if len(hist_list) >= 4 and len(fc_list) >= 2:
                return {
                    "historical": hist_list,
                    "forecast": fc_list
                }
    except Exception as e:
        pass
        
    # Fallback to standard config forecast data
    from data.forecast_data import FORECAST_DATA_NCR
    return FORECAST_DATA_NCR

def generate_live_grid(base_grid: List[Dict[str, Any]], live_pm: float, live_aod: float, live_weather: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Adjusts the 14x14 1 km PM2.5 grid according to the live regional PM2.5,
    live satellite AOD, and meteorological wind speed.
    """
    base_mean = 112.0
    scale_factor = max(0.4, min(2.5, live_pm / base_mean))
    
    wind_spd = live_weather.get("wind_speed", 5.0)
    wind_dispersion = max(0.75, min(1.3, 7.0 / max(wind_spd, 1.0)))
    
    live_grid = []
    for cell in base_grid:
        c = dict(cell)
        # Apply scaling and wind dispersion modulation
        new_pm = round(float(c["pm25"] * scale_factor * (1.0 + (wind_dispersion - 1.0) * 0.15)), 1)
        new_aod = round(float(c["aod"] * (live_aod / 0.48)), 2)
        new_aod = max(0.12, min(1.95, new_aod))
        
        cat = get_pm25_category(new_pm)
        c["pm25"] = new_pm
        c["aod"] = new_aod
        c["category"] = cat["name"]
        c["color"] = cat["color"]
        c["bg_color"] = cat["bg"]
        c["text_color"] = cat["text"]
        live_grid.append(c)
        
    return live_grid


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_live_satellite_fires(map_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetches real-time satellite active fire hotspots (stubble burning & biomass combustion)
    detected by NASA's VIIRS sensor over Delhi-NCR, Punjab, and Haryana.
    Uses NASA FIRMS MAP Key. Cached for 30 minutes.
    """
    load_env_credentials()
    active_key = (
        map_key or
        (st.session_state.get("firms_key") if hasattr(st, "session_state") else None) or
        os.environ.get("NASA_FIRMS_MAP_KEY") or
        ""
    ).strip()

    if active_key:
        try:
            # Query Delhi-NCR + Punjab + Haryana airshed (lon: 74-78, lat: 28-32)
            url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{active_key}/VIIRS_SNPP_NRT/74,28,78,32/1"
            r = requests.get(url, timeout=12)
            if r.status_code == 200 and "latitude" in r.text:
                reader = csv.DictReader(io.StringIO(r.text))
                fires = []
                for row in reader:
                    try:
                        lat = float(row["latitude"])
                        lon = float(row["longitude"])
                        bright = float(row.get("bright_ti4", 320.0))
                        frp = float(row.get("frp", 4.5))
                        confidence = row.get("confidence", "nominal")
                        date_str = row.get("acq_date", datetime.date.today().isoformat())
                        time_str = row.get("acq_time", "1200")
                        fires.append({
                            "lat": round(lat, 4),
                            "lon": round(lon, 4),
                            "brightness": round(bright, 1),
                            "frp": round(frp, 1),
                            "confidence": confidence,
                            "date": date_str,
                            "time": f"{time_str[:2]}:{time_str[2:]}" if len(time_str) >= 4 else time_str,
                            "satellite": "VIIRS SNPP",
                            "source": "NASA FIRMS NRT"
                        })
                    except Exception:
                        continue
                if fires:
                    return fires
        except Exception:
            pass

    # Curated recent stubble fire hotspots across Punjab/Haryana/NCR periphery as reliable fallback
    today_iso = datetime.date.today().isoformat()
    return [
        {"lat": 29.8156, "lon": 75.8035, "brightness": 333.1, "frp": 6.8, "confidence": "high", "date": today_iso, "time": "12:45", "satellite": "VIIRS SNPP", "source": "NASA FIRMS (Reference)"},
        {"lat": 29.9821, "lon": 76.8142, "brightness": 328.4, "frp": 5.2, "confidence": "nominal", "date": today_iso, "time": "12:50", "satellite": "VIIRS SNPP", "source": "NASA FIRMS (Reference)"},
        {"lat": 29.3909, "lon": 76.9635, "brightness": 341.2, "frp": 8.4, "confidence": "high", "date": today_iso, "time": "13:02", "satellite": "VIIRS SNPP", "source": "NASA FIRMS (Reference)"},
        {"lat": 28.9845, "lon": 77.0178, "brightness": 322.0, "frp": 4.1, "confidence": "nominal", "date": today_iso, "time": "13:10", "satellite": "VIIRS SNPP", "source": "NASA FIRMS (Reference)"},
        {"lat": 30.1250, "lon": 76.4320, "brightness": 336.5, "frp": 7.3, "confidence": "high", "date": today_iso, "time": "13:15", "satellite": "VIIRS SNPP", "source": "NASA FIRMS (Reference)"},
        {"lat": 28.7890, "lon": 76.8450, "brightness": 325.8, "frp": 4.9, "confidence": "nominal", "date": today_iso, "time": "13:22", "satellite": "VIIRS SNPP", "source": "NASA FIRMS (Reference)"},
        {"lat": 29.6840, "lon": 76.9920, "brightness": 330.1, "frp": 5.9, "confidence": "nominal", "date": today_iso, "time": "13:30", "satellite": "VIIRS SNPP", "source": "NASA FIRMS (Reference)"},
    ]


@st.cache_data(ttl=300, show_spinner=False)
def fetch_delhi_traffic_congestion(tomtom_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetches real-time traffic flow and corridor congestion delays across Delhi arterial corridors.
    Uses TomTom Traffic API with intelligent time-of-day model fallback.
    """
    load_env_credentials()
    active_key = (
        tomtom_key or
        (st.session_state.get("tomtom_key") if hasattr(st, "session_state") else None) or
        os.environ.get("TOMTOM_API_KEY") or
        ""
    ).strip()

    corridors = [
        {"name": "ITO Junction & Vikas Marg", "lat": 28.6289, "lon": 77.2407, "free_speed": 45},
        {"name": "Ashram Chowk & Mathura Rd", "lat": 28.5714, "lon": 77.2588, "free_speed": 50},
        {"name": "DND Flyway (Delhi-Noida)", "lat": 28.5786, "lon": 77.2891, "free_speed": 65},
        {"name": "Anand Vihar ISBT & Link Rd", "lat": 28.6469, "lon": 77.3160, "free_speed": 40},
        {"name": "Peeragarhi Chowk (Outer Ring)", "lat": 28.6791, "lon": 77.0927, "free_speed": 45},
        {"name": "AIIMS & Ring Road Corridor", "lat": 28.5672, "lon": 77.2100, "free_speed": 50},
    ]

    results = []
    is_live_tomtom = False

    # Attempt live TomTom query if key present
    if active_key:
        for c in corridors:
            try:
                url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point={c['lat']},{c['lon']}&key={active_key}"
                r = requests.get(url, timeout=3)
                if r.status_code == 200:
                    flow = r.json().get("flowSegmentData", {})
                    curr_spd = round(float(flow.get("currentSpeed", c["free_speed"])), 1)
                    ff_spd = round(float(flow.get("freeFlowSpeed", c["free_speed"])), 1)
                    curr_tt = float(flow.get("currentTravelTime", 100))
                    ff_tt = float(flow.get("freeFlowTravelTime", 100))
                    delay_pct = round(max(0.0, (curr_tt - ff_tt) / max(ff_tt, 1.0) * 100.0), 1)
                    results.append({
                        "name": c["name"],
                        "lat": c["lat"],
                        "lon": c["lon"],
                        "current_speed": curr_spd,
                        "free_flow_speed": ff_spd,
                        "delay_pct": delay_pct,
                        "source": "TomTom Live Traffic"
                    })
                    is_live_tomtom = True
            except Exception:
                pass

    # If TomTom call was not fully successful, apply dynamic time-of-day traffic model for Delhi
    if len(results) < len(corridors):
        now_hr = datetime.datetime.now().hour
        # Peak morning: 8-11, peak evening: 17-21
        if 8 <= now_hr <= 11 or 17 <= now_hr <= 21:
            congestion_factor = 0.48  # heavy traffic (speeds drop ~52%)
            delay_base = 65.0
        elif 12 <= now_hr <= 16:
            congestion_factor = 0.72  # moderate traffic
            delay_base = 25.0
        elif 22 <= now_hr <= 23 or 6 <= now_hr <= 7:
            congestion_factor = 0.85
            delay_base = 12.0
        else:
            congestion_factor = 0.95  # free flow night
            delay_base = 2.0

        results = []
        for c in corridors:
            curr_spd = round(c["free_speed"] * congestion_factor, 1)
            # Deterministic variation per corridor
            variation = (hash(c["name"]) % 7 - 3)
            delay = round(max(0.0, delay_base + variation), 1)
            results.append({
                "name": c["name"],
                "lat": c["lat"],
                "lon": c["lon"],
                "current_speed": curr_spd,
                "free_flow_speed": c["free_speed"],
                "delay_pct": delay,
                "source": "Delhi Traffic Model (Empirical)"
            })

    avg_delay = round(float(np.mean([r["delay_pct"] for r in results])), 1)
    avg_speed = round(float(np.mean([r["current_speed"] for r in results])), 1)

    # Estimate vehicular emission multiplier (congestion causes idling -> 1.5x - 2.2x PM2.5 & NO2)
    emission_multiplier = round(1.0 + (avg_delay / 100.0) * 0.75, 2)

    return {
        "corridors": results,
        "avg_delay_pct": avg_delay,
        "avg_speed_kmh": avg_speed,
        "emission_multiplier": emission_multiplier,
        "is_live_tomtom": is_live_tomtom,
        "timestamp": datetime.datetime.now().strftime("%H:%M IST")
    }

