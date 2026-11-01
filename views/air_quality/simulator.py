"""
Air Quality: Scenario Simulator View (Wireframe 2d).
Sensitivity analysis tool perturbing wind speed, boundary-layer height, temperature,
and humidity with side-by-side Baseline vs Scenario maps and delta impact metrics.
"""
import streamlit as st
from components.map_view import render_leaflet_fused_map
from data.grid import DEFAULT_GRID
from data.scenario_engine import run_sensitivity_scenario
from data.live_api import (
    fetch_live_delhi_air_quality,
    fetch_live_delhi_weather,
    generate_live_grid
)
import datetime

def render_simulator_view():
    is_live = (st.session_state.get("data_mode", "Live") == "Live")
    
    if is_live:
        aq = fetch_live_delhi_air_quality()
        weather = fetch_live_delhi_weather()
        baseline_grid = generate_live_grid(DEFAULT_GRID, aq["pm2_5"], aq["aod"], weather)
        date_label = f"Live ({datetime.datetime.now().strftime('%H:%M IST')})"
    else:
        baseline_grid = DEFAULT_GRID
        weather = None
        date_label = "12 Jan 2025 (global)"

    # Top Warning Alert Banner
    st.markdown("""
    <div class="alert-banner-amber">
        <span>Sensitivity analysis, not an atmospheric chemistry simulation.</span>
        <span class="help-circle-btn">?</span>
    </div>
    """, unsafe_allow_html=True)
    
    # State initialization for simulator
    if "sim_wind" not in st.session_state:
        st.session_state["sim_wind"] = -15
    if "sim_blh" not in st.session_state:
        st.session_state["sim_blh"] = -10
    if "sim_temp" not in st.session_state:
        st.session_state["sim_temp"] = -1.0
    if "sim_hum" not in st.session_state:
        st.session_state["sim_hum"] = 10
    if "sim_run_count" not in st.session_state:
        st.session_state["sim_run_count"] = 1
        
    col_params, col_maps = st.columns([32, 68])
    
    # Left Panel: Parameters
    with col_params:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 12px; padding: 18px;">
            <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 14px;">Scenario Controls</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Date & Area inputs
        st.text_input("Date", value=date_label, disabled=True, key="sim_date_fixed")
        st.selectbox("Area", ["All Delhi-NCR (global)"], index=0, disabled=True, key="sim_area_fixed")
        
        if is_live and weather:
            st.markdown(f"""
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:6px; padding:8px 10px; margin-top:8px; margin-bottom:8px; font-size:11.5px; color:#166534; line-height:1.45;">
                <strong>Live Meteorological Reference:</strong><br>
                • Wind: {weather['wind_speed']} km/h ({weather['wind_direction']}°)<br>
                • BLH: {weather['boundary_layer_height']} m · Temp: {weather['temperature']} °C · RH: {weather['humidity']}%
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        
        # Slider 1: Wind speed (-50 to +50%)
        st.markdown("<div style='font-size:12px; font-weight:600; color:#334155; margin-bottom:2px;'>Wind speed · <span style='color:#0f766e;'>{}%</span> (-50 to +50%)</div>".format(st.session_state["sim_wind"]), unsafe_allow_html=True)
        w_val = st.slider("Wind speed", -50, 50, st.session_state["sim_wind"], step=5, label_visibility="collapsed", key="slider_wind")
        st.session_state["sim_wind"] = w_val
        
        # Slider 2: Boundary-layer height (-50 to +50%)
        st.markdown("<div style='font-size:12px; font-weight:600; color:#334155; margin-bottom:2px;'>Boundary-layer height · <span style='color:#0f766e;'>{}%</span></div>".format(st.session_state["sim_blh"]), unsafe_allow_html=True)
        b_val = st.slider("Boundary-layer height", -50, 50, st.session_state["sim_blh"], step=5, label_visibility="collapsed", key="slider_blh")
        st.session_state["sim_blh"] = b_val
        
        # Slider 3: Temperature (±5 °C)
        st.markdown("<div style='font-size:12px; font-weight:600; color:#334155; margin-bottom:2px;'>Temperature · <span style='color:#0f766e;'>{} °C</span> (±5 °C)</div>".format(st.session_state["sim_temp"]), unsafe_allow_html=True)
        t_val = st.slider("Temperature", -5.0, 5.0, float(st.session_state["sim_temp"]), step=0.5, label_visibility="collapsed", key="slider_temp")
        st.session_state["sim_temp"] = t_val
        
        # Slider 4: Humidity (±20%)
        st.markdown("<div style='font-size:12px; font-weight:600; color:#334155; margin-bottom:2px;'>Humidity · <span style='color:#0f766e;'>{}%</span> (±20%)</div>".format(st.session_state["sim_hum"]), unsafe_allow_html=True)
        h_val = st.slider("Humidity", -20, 20, st.session_state["sim_hum"], step=2, label_visibility="collapsed", key="slider_humidity")
        st.session_state["sim_hum"] = h_val
        
        st.write("")
        
        # Buttons
        if st.button("Run scenario", key="btn_run_sim", type="primary", use_container_width=True):
            st.session_state["sim_run_count"] += 1
            st.rerun()
            
        if st.button("Reset", key="btn_reset_sim", use_container_width=True):
            st.session_state["sim_wind"] = 0
            st.session_state["sim_blh"] = 0
            st.session_state["sim_temp"] = 0.0
            st.session_state["sim_hum"] = 0
            st.rerun()

    # Calculate Scenario Results
    sim_results = run_sensitivity_scenario(
        grid=baseline_grid,
        wind_pct=float(st.session_state["sim_wind"]),
        blh_pct=float(st.session_state["sim_blh"]),
        temp_delta=float(st.session_state["sim_temp"]),
        humidity_pct=float(st.session_state["sim_hum"])
    )

    # Right Panel: Side-by-side Baseline vs Scenario Maps
    with col_maps:
        col_base, col_scen = st.columns(2)
        
        with col_base:
            st.markdown("""
            <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 8px;">
                Baseline
            </div>
            """, unsafe_allow_html=True)
            render_leaflet_fused_map(
                grid_cells=sim_results["baseline_grid"],
                active_layer="fused",
                show_stations=False,
                show_anomalies=False,
                opacity=0.8,
                basemap_theme="light",
                height=320,
                is_overview=True
            )
            
        with col_scen:
            st.markdown("""
            <div style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 8px;">
                Scenario
            </div>
            """, unsafe_allow_html=True)
            render_leaflet_fused_map(
                grid_cells=sim_results["scenario_grid"],
                active_layer="fused",
                show_stations=False,
                show_anomalies=False,
                opacity=0.8,
                basemap_theme="light",
                height=320,
                is_overview=True
            )

        # Delta Result Card (Wireframe 2d Bottom)
        delta_val = sim_results["mean_delta"]
        pct_val = sim_results["pct_delta"]
        sign_str = "+" if delta_val >= 0 else ""
        delta_color = "#dc2626" if delta_val >= 0 else "#16a34a"
        
        st.markdown(f"""
        <div class="content-box-card" style="margin-top: 14px; padding: 18px 24px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 4px;">
                    CHANGE IN MEAN PM₂.₅
                </div>
                <div style="font-size: 28px; font-weight: 800; color: {delta_color}; line-height: 1;">
                    {sign_str}{delta_val} µg/m³ ({sign_str}{pct_val:.0f}%)
                </div>
            </div>
            <div style="font-size: 13px; color: #475569; font-weight: 500;">
                <strong>{sim_results['worsened_count']}</strong> areas worsened, <strong>{sim_results['improved_count']}</strong> improved
            </div>
        </div>
        """, unsafe_allow_html=True)
