"""
Air Quality: Fused Map View (Wireframe 2a).
Interactive 1 km Leaflet map with layer selection, opacity slider, basemap toggle,
ranked polluted stations list, and bottom timeline scrubber player.
"""
import streamlit as st
from components.map_view import render_leaflet_fused_map
from data.grid import DEFAULT_GRID
from data.stations import get_most_polluted_stations, STATIONS
from data.live_api import (
    fetch_live_delhi_air_quality,
    fetch_live_delhi_weather,
    fetch_live_station_readings,
    fetch_live_satellite_fires,
    fetch_delhi_traffic_congestion,
    generate_live_grid
)
from config import AVAILABLE_DATES

def render_fused_map_view():
    is_live = (st.session_state.get("data_mode", "Live") == "Live")
    fires = fetch_live_satellite_fires()
    traffic = fetch_delhi_traffic_congestion()
    
    if is_live:
        aq = fetch_live_delhi_air_quality()
        weather = fetch_live_delhi_weather()
        stations = fetch_live_station_readings()
        active_grid = generate_live_grid(DEFAULT_GRID, aq["pm2_5"], aq["aod"], weather)
        
        # Sort stations by pm25 descending for top polluted list
        sorted_st = sorted(stations, key=lambda s: s["pm25"], reverse=True)
        top_stations = sorted_st[:6]
    else:
        active_grid = DEFAULT_GRID
        weather = {"wind_speed": 5.4, "wind_direction": 290}
        stations = fetch_live_station_readings()
        sorted_st = sorted(stations, key=lambda s: s["pm25"], reverse=True)
        top_stations = sorted_st[:6]
    
    # Build real CSV export data from 1,024 active grid cells
    import pandas as pd
    export_rows = []
    for c in active_grid:
        export_rows.append({
            "cell_id": c.get("cell_id"),
            "latitude": c.get("center_lat"),
            "longitude": c.get("center_lon"),
            "pm25_ug_m3": c.get("pm25"),
            "satellite_aod": c.get("aod"),
            "uncertainty_sigma_ug_m3": c.get("sigma"),
            "category": c.get("category"),
            "is_gap_filled": c.get("is_gap_filled", False),
            "nearest_monitoring_station": c.get("nearest_station"),
            "lat_min": c.get("lat_min"),
            "lat_max": c.get("lat_max"),
            "lon_min": c.get("lon_min"),
            "lon_max": c.get("lon_max")
        })
    export_df = pd.DataFrame(export_rows)
    export_csv_bytes = export_df.to_csv(index=False).encode('utf-8')

    col_map, col_controls = st.columns([72, 28])
    
    # Session state initialization for map view
    if "selected_station" not in st.session_state:
        st.session_state["selected_station"] = "Anand Vihar"
    if "layer_option" not in st.session_state:
        st.session_state["layer_option"] = "Fused 1 km Grid (Crisp)"
    if "map_opacity" not in st.session_state:
        st.session_state["map_opacity"] = 65
    if "basemap_theme" not in st.session_state:
        st.session_state["basemap_theme"] = "OpenStreetMap (Real Streets)"
    if "show_stations" not in st.session_state:
        st.session_state["show_stations"] = True
    if "show_anomalies" not in st.session_state:
        st.session_state["show_anomalies"] = True
    if "show_wind" not in st.session_state:
        st.session_state["show_wind"] = True
    if "show_fires" not in st.session_state:
        st.session_state["show_fires"] = True
    if "timeline_date_idx" not in st.session_state:
        st.session_state["timeline_date_idx"] = len(AVAILABLE_DATES) - 1
    if "timeline_playing" not in st.session_state:
        st.session_state["timeline_playing"] = False

    # Right Controls Panel (Wireframe 2a Right Side)
    with col_controls:
        # Layers Card
        st.markdown("""
        <div class="content-box-card" style="padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 12px;">Map Layers</div>
        </div>
        """, unsafe_allow_html=True)
        
        layer_options = [
            "Original Base Map (Clean)",
            "Fused 1 km Grid (Crisp)",
            "Smooth Continuous Surface",
            "Raw MODIS AOD",
            "Gap-filled only",
            "Wind Flow Vectors"
        ]
        curr_layer = st.session_state["layer_option"] if st.session_state["layer_option"] in layer_options else layer_options[0]
        layer_choice = st.radio(
            "Layer Selection",
            layer_options,
            index=layer_options.index(curr_layer),
            label_visibility="collapsed",
            key="radio_layer"
        )
        st.session_state["layer_option"] = layer_choice
        
        # Checkboxes
        c_st = st.checkbox("Numeric Station Pins", value=st.session_state["show_stations"], key="chk_stations")
        c_an = st.checkbox("Anomaly Hotspot Flags", value=st.session_state["show_anomalies"], key="chk_anomalies")
        c_wind = st.checkbox("Wind Flow Streamlines", value=st.session_state["show_wind"], key="chk_wind")
        c_fires = st.checkbox(f"🔥 Active Satellite Fires ({len(fires)})", value=st.session_state["show_fires"], key="chk_fires")
        st.session_state["show_stations"] = c_st
        st.session_state["show_anomalies"] = c_an
        st.session_state["show_wind"] = c_wind
        st.session_state["show_fires"] = c_fires
        
        # Opacity Slider
        st.markdown("<div style='font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase; margin-top:12px;'>SURFACE OPACITY</div>", unsafe_allow_html=True)
        opacity_val = st.slider(
            "Opacity",
            min_value=10,
            max_value=100,
            value=st.session_state["map_opacity"],
            step=5,
            label_visibility="collapsed",
            key="slider_opacity"
        )
        st.session_state["map_opacity"] = opacity_val
        
        # Basemap Dropdown
        basemap_options = [
            "OpenStreetMap (Real Streets)",
            "Esri World Street Map",
            "Satellite + Roads (Hybrid)",
            "Topographic",
            "Dark Matter"
        ]
        curr_base = st.session_state["basemap_theme"] if st.session_state["basemap_theme"] in basemap_options else basemap_options[0]
        basemap = st.selectbox(
            "Basemap Style",
            basemap_options,
            index=basemap_options.index(curr_base),
            key="select_basemap"
        )
        st.session_state["basemap_theme"] = basemap

        # Most Polluted Stations Card
        st.markdown("""
        <div class="content-box-card" style="padding: 16px; margin-top: 14px;">
            <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 12px;">Most polluted stations</div>
        </div>
        """, unsafe_allow_html=True)
        
        for idx, st_item in enumerate(top_stations, 1):
            dot_color = "#ef4444" if st_item["pm25"] >= 121 else "#f97316"
            is_active = (st_item["name"] == st.session_state["selected_station"])
            active_bg = "background: #f1f5f9; font-weight:700;" if is_active else ""
            
            c_label, c_btn = st.columns([8, 2])
            with c_label:
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding: 6px 8px; border-radius:6px; font-size:13px; color:#1e293b; {active_bg}">
                    <span><strong>{idx}</strong> {st_item['name']} <strong>{st_item['pm25']}</strong></span>
                    <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:{dot_color};"></span>
                </div>
                """, unsafe_allow_html=True)
            with c_btn:
                if st.button("📍", key=f"btn_st_{st_item['id']}", help=f"Focus on {st_item['name']}"):
                    st.session_state["selected_station"] = st_item["name"]
                    st.rerun()

        # Traffic & Arterial Congestion Telemetry Card
        st.markdown(f"""
        <div class="content-box-card" style="padding: 14px; margin-top: 14px; margin-bottom: 8px; border-left: 3px solid #3b82f6;">
            <div style="font-size: 13px; font-weight: 700; color: #0f172a; display:flex; justify-content:space-between; align-items:center;">
                <span>🚗 Traffic Congestion</span>
                <span style="font-size:10px; font-weight:600; color:{'#10b981' if traffic.get('is_live_tomtom') else '#64748b'};">
                    {'● TomTom Live' if traffic.get('is_live_tomtom') else '● Delhi Corridor Model'}
                </span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:11px; color:#475569;">
                <span>Avg Congestion Delay:</span>
                <b style="color:{'#dc2626' if traffic['avg_delay_pct'] > 40 else '#d97706'};">+{traffic['avg_delay_pct']}%</b>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:4px; font-size:11px; color:#475569;">
                <span>Corridor Speed:</span>
                <b>{traffic['avg_speed_kmh']} km/h</b>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:4px; font-size:11px; color:#475569;">
                <span>Idling Emission Impact:</span>
                <b style="color:#b91c1c;">{traffic['emission_multiplier']}x factor</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Data Export Card in Sidebar
        cur_date_str = AVAILABLE_DATES[st.session_state["timeline_date_idx"]]
        cur_date_slug = cur_date_str.lower().replace(" ", "_").replace("(", "").replace(")", "")
        st.markdown("""
        <div class="content-box-card" style="padding: 16px; margin-top: 14px; margin-bottom: 8px;">
            <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">Export Surface Data</div>
            <p style="font-size: 11.5px; color: #64748b; line-height: 1.45; margin-bottom: 10px;">
                Export all 1,024 1 km grid cells with machine learning PM₂.₅ estimates, satellite AOD, and uncertainty (±σ).
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="📥 Download 1 km Grid (CSV)",
            data=export_csv_bytes,
            file_name=f"ecopulse_delhi_1km_grid_{cur_date_slug}.csv",
            mime="text/csv",
            use_container_width=True,
            key="btn_export_grid_csv_sidebar"
        )

    # Left Map Panel
    with col_map:
        layer_key_map = {
            "Original Base Map (Clean)": "original",
            "Fused 1 km Grid (Crisp)": "fused",
            "Smooth Continuous Surface": "smooth",
            "Raw MODIS AOD": "aod",
            "Gap-filled only": "gap_filled",
            "Wind Flow Vectors": "wind"
        }
        active_layer_code = layer_key_map.get(st.session_state["layer_option"], "fused")
        
        basemap_code_map = {
            "OpenStreetMap (Real Streets)": "streets",
            "Esri World Street Map": "positron",
            "Positron (Light Retina)": "positron",
            "Satellite + Roads (Hybrid)": "satellite_hybrid",
            "Topographic": "topographic",
            "Dark Matter": "dark_matter",
            "Dark Matter (Neon)": "dark_matter",
            "OpenStreetMap": "streets"
        }
        active_basemap_code = basemap_code_map.get(st.session_state["basemap_theme"], "positron")
        
        render_leaflet_fused_map(
            grid_cells=active_grid,
            active_layer=active_layer_code,
            show_stations=st.session_state["show_stations"],
            show_anomalies=st.session_state["show_anomalies"],
            opacity=st.session_state["map_opacity"] / 100.0,
            basemap_theme=active_basemap_code,
            selected_station_name=st.session_state["selected_station"],
            height=540,
            is_overview=False,
            stations=stations,
            wind_data=weather,
            show_wind=st.session_state["show_wind"],
            fire_hotspots=fires,
            show_fires=st.session_state["show_fires"]
        )

    # Bottom Bar: Timeline Player (Wireframe 2a Bottom)
    st.markdown("""
    <div class="content-box-card" style="padding: 12px 20px; margin-top: 14px; margin-bottom: 10px;">
    </div>
    """, unsafe_allow_html=True)
    
    t_play, t_slider, t_date, t_speed, t_dl = st.columns([6, 52, 14, 10, 18])
    
    with t_play:
        play_label = "⏸" if st.session_state["timeline_playing"] else "▶"
        if st.button(play_label, key="btn_play_timeline", help="Play/Pause timeline animation"):
            st.session_state["timeline_playing"] = not st.session_state["timeline_playing"]
            st.rerun()
            
    with t_slider:
        selected_idx = st.slider(
            "Timeline Scrubber",
            min_value=0,
            max_value=len(AVAILABLE_DATES) - 1,
            value=st.session_state["timeline_date_idx"],
            label_visibility="collapsed",
            key="timeline_scrubber"
        )
        st.session_state["timeline_date_idx"] = selected_idx
        
    with t_date:
        st.markdown(f"""
        <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:6px 10px; font-size:12px; font-weight:600; text-align:center; color:#0f172a;">
            {cur_date_str}
        </div>
        """, unsafe_allow_html=True)
        
    with t_speed:
        st.selectbox("Speed", ["1x", "0.5x", "2x"], index=0, label_visibility="collapsed", key="sel_speed")
        
    with t_dl:
        st.download_button(
            label="📥 Export CSV",
            data=export_csv_bytes,
            file_name=f"ecopulse_delhi_1km_grid_{cur_date_slug}.csv",
            mime="text/csv",
            key="btn_dl_csv_timeline",
            help="Download all 1,024 1 km cells as CSV"
        )
