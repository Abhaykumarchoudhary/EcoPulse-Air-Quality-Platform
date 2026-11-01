"""
Overview View (Wireframe 1).
Features Key Metrics Row, Fused PM2.5 Grid Preview with 'Open full map →' action,
Next 3 days sparkline, About project description, and 4-step ML pipeline flow.
All major sections are organized in distinct card containers matching the wireframe.
"""
import streamlit as st
from components.header import render_top_header
from components.metrics_row import render_overview_metrics
from components.pipeline_diagram import render_pipeline_stepper
from components.map_view import render_leaflet_fused_map
from utils.chart_helpers import render_overview_sparkline
from data.grid import DEFAULT_GRID, get_grid_stats
from data.anomalies import get_anomaly_count_month
from data.live_api import (
    fetch_live_delhi_air_quality,
    fetch_live_delhi_weather,
    fetch_live_station_readings,
    generate_live_grid
)
import datetime
import numpy as np

def render_overview_page():
    is_live = (st.session_state.get("data_mode", "Live") == "Live")
    
    if is_live:
        aq = fetch_live_delhi_air_quality()
        weather = fetch_live_delhi_weather()
        stations = fetch_live_station_readings()
        active_grid = generate_live_grid(DEFAULT_GRID, aq["pm2_5"], aq["aod"], weather)
        
        now = datetime.datetime.now()
        date_display = now.strftime("%d %b %Y, %H:%M IST")
        
        # Calculate live stats
        mean_pm = round(float(aq["pm2_5"]), 1)
        worst_st = next((s for s in stations if s["is_worst"]), stations[0])
        worst_area = worst_st["name"]
        worst_val = worst_st["pm25"]
        worst_status = worst_st["status"]
    else:
        stations = fetch_live_station_readings()
        active_grid = DEFAULT_GRID
        date_display = "12 Jan 2025"
        worst_st = next((s for s in stations if s.get("is_worst")), stations[0])
        worst_area = worst_st["name"]
        worst_val = worst_st["pm25"]
        worst_status = worst_st["status"]
        mean_pm = round(float(np.mean([s["pm25"] for s in stations])), 1)
        aq = None
        weather = None

    # Top Header
    render_top_header(
        title="Overview",
        subtitle="Satellite-fused air quality and carbon emissions for Delhi-NCR",
        date_str=date_display,
        is_live=is_live
    )
    
    # If Live Mode, render sleek Live Telemetry Strip
    if is_live and aq and weather:
        st.markdown(f"""
        <div class="live-telemetry-strip">
            <span class="item-chip">📡 <strong>Live Telemetry:</strong></span>
            <span class="item-chip">PM₂.₅: <strong>{aq['pm2_5']} µg/m³</strong></span>
            <span class="item-chip">Satellite AOD: <strong>{aq['aod']}</strong></span>
            <span class="item-chip">Temp: <strong>{weather['temperature']} °C</strong></span>
            <span class="item-chip">RH: <strong>{weather['humidity']}%</strong></span>
            <span class="item-chip">Wind: <strong>{weather['wind_speed']} km/h ({weather['wind_direction']}°)</strong></span>
            <span class="item-chip">BLH: <strong>{weather['boundary_layer_height']} m</strong></span>
            <span class="item-chip" style="color:#047857;">Source: <strong>{aq['source']}</strong></span>
        </div>
        """, unsafe_allow_html=True)
    
    # 4 Key Metric Cards Row (Each card has its own container with colored left accent)
    stats = get_grid_stats(active_grid)
    render_overview_metrics(
        mean_pm25=mean_pm,
        pct_change=8.0 if not is_live else round((mean_pm - 112.0) / 112.0 * 100, 1),
        most_polluted_area=worst_area,
        most_polluted_val=worst_val,
        most_polluted_status=worst_status,
        anomaly_days=get_anomaly_count_month(),
        r2_score=0.78
    )
    
    # Middle Row: Fused Map Container (Left 65%) and Next 3 Days + About Containers (Right 35%)
    col_map, col_info = st.columns([65, 35])
    
    with col_map:
        with st.container(border=True):
            st.markdown(
                '<div class="card-header-row map-card-header" style="margin-bottom: 8px;">'
                '<div class="card-title-text">'
                'Fused PM₂.₅ <span class="help-circle-btn" title="Continuous 1 km daily PM2.5 surface estimated by combining MODIS MAIAC satellite AOD, CPCB ground monitors, and weather features.">ℹ</span>'
                '</div>'
                '<div class="card-actions-row">'
                '<span class="pill-btn-small">CSV · PNG</span>'
                '<span class="help-circle-btn">?</span>'
                '</div></div>',
                unsafe_allow_html=True
            )
            
            # Leaflet Grid Map (Clean view without covering popups initially)
            render_leaflet_fused_map(
                grid_cells=active_grid,
                active_layer="fused",
                show_stations=True,
                show_anomalies=True,
                opacity=0.80,
                basemap_theme="positron",
                selected_station_name=None,
                height=350,
                is_overview=True,
                stations=stations,
                wind_data=weather if is_live else {"wind_speed": 5.4, "wind_direction": 290},
                show_wind=True
            )
            
            # 'Open full map →' button inside the map container at bottom right
            c_spacer, c_btn = st.columns([62, 38])
            with c_btn:
                if st.button("Open full map →", key="btn_open_full_map", type="primary", use_container_width=True):
                    st.session_state["active_nav"] = "Air Quality"
                    st.session_state["air_subtab"] = "Fused Map"
                    st.rerun()
                    
    with col_info:
        # Separate Container 1: Next 3 days sparkline
        with st.container(border=True):
            st.markdown(
                '<div class="card-header-row sparkline-card-header" style="margin-bottom: 2px;">'
                '<div class="card-title-text" style="font-size: 16px;">'
                'Next 3 days <span class="help-circle-btn" title="Mean PM₂.₅ for the last 4 days and the forecast for the next 3.">?</span>'
                '</div>'
                '<div class="card-actions-row">'
                '<span class="pill-btn-small">CSV · PNG</span>'
                '<span class="help-circle-btn">?</span>'
                '</div></div>'
                '<div style="font-size: 11.5px; color: #64748b; margin-top: -2px; margin-bottom: 4px;">'
                'Mean PM₂.₅ for the last 4 days and the forecast for the next 3.'
                '</div>',
                unsafe_allow_html=True
            )
            
            spark_fig = render_overview_sparkline()
            st.plotly_chart(spark_fig, use_container_width=True, config={"displayModeBar": False})
            
        # Separate Container 2: About this project
        with st.container(border=True):
            st.markdown(
                '<div class="about-card-content">'
                '<div class="card-title-text" style="font-size: 16px; margin-bottom: 8px;">About this project</div>'
                '<p style="font-size: 12.5px; color: #475569; line-height: 1.55; margin: 0;">'
                'EcoPulse fuses MODIS MAIAC satellite AOD with CPCB station readings and weather to estimate '
                'ground-level PM₂.₅ on a 1 km grid across Delhi-NCR. It forecasts the next 3 days, flags anomaly days, '
                'and links air quality to sector-level carbon emissions.'
                '</p></div>',
                unsafe_allow_html=True
            )

    # Separate Container 3: Bottom Pipeline Stepper
    with st.container(border=True):
        render_pipeline_stepper()

    # Footer Row below pipeline container
    st.markdown(
        '<div style="display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: #64748b; margin-top: 14px; margin-bottom: 12px; padding: 0 4px;">'
        '<span>Sources: NASA VIIRS (FIRMS), MODIS MAIAC, CPCB (WAQI/OGD), Open-Meteo, Climate TRACE, TomTom Traffic · Estimates, not official AQI</span>'
        '<a href="https://github.com/Abhaykumarchoudhary/EcoPulse-Air-Quality-Platform" target="_blank" style="color: #0f766e; text-decoration: none; font-weight: 600;">GitHub Repository ★</a>'
        '</div>',
        unsafe_allow_html=True
    )
