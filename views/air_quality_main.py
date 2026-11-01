"""
Main Air Quality View Wrapper.
Hosts the sub-navigation pills:
1. Fused Map (Wireframe 2a)
2. Forecast & Anomalies (Wireframe 2b)
3. Model Performance (Wireframe 2c)
4. Scenario Simulator (Wireframe 2d)
"""
import streamlit as st
from components.header import render_top_header
from views.air_quality.fused_map import render_fused_map_view
from views.air_quality.forecast import render_forecast_view
from views.air_quality.model_perf import render_model_perf_view
from views.air_quality.simulator import render_simulator_view

import datetime

def render_air_quality_page():
    is_live = (st.session_state.get("data_mode", "Live") == "Live")
    date_display = datetime.datetime.now().strftime("%d %b %Y, %H:%M IST") if is_live else "12 Jan 2025"
    
    # Top Header
    render_top_header(
        title="Air Quality",
        subtitle="Fused PM₂.₅ from satellite AOD, stations and weather",
        date_str=date_display,
        is_live=is_live
    )
    
    # Subtabs State
    if "air_subtab" not in st.session_state:
        st.session_state["air_subtab"] = "Fused Map"
        
    subtabs = [
        "Fused Map",
        "Forecast & Anomalies",
        "Model Performance",
        "Scenario Simulator"
    ]
    
    # Render pill tabs using buttons in a row
    cols = st.columns([18, 25, 23, 23, 11])
    for idx, tab_name in enumerate(subtabs):
        with cols[idx]:
            is_active = (st.session_state["air_subtab"] == tab_name)
            btn_type = "primary" if is_active else "secondary"
            if st.button(tab_name, key=f"btn_subtab_{idx}", type=btn_type, use_container_width=True):
                st.session_state["air_subtab"] = tab_name
                st.rerun()
                
    st.write("") # spacing
    
    # Render Active Sub-View
    current_tab = st.session_state["air_subtab"]
    if current_tab == "Fused Map":
        render_fused_map_view()
    elif current_tab == "Forecast & Anomalies":
        render_forecast_view()
    elif current_tab == "Model Performance":
        render_model_perf_view()
    elif current_tab == "Scenario Simulator":
        render_simulator_view()
