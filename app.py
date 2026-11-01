"""
EcoPulse: A Satellite-Fused Air Quality and Carbon Intelligence Platform.
Main Streamlit application entry point.
"""
import streamlit as st

# Configure wide layout matching wireframes (1440x900 laptop, Streamlit wide layout)
st.set_page_config(
    page_title="EcoPulse · Satellite-Fused AQ & Carbon Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

from components.styles import CUSTOM_CSS
from components.sidebar import render_sidebar
from views.overview import render_overview_page
from views.air_quality_main import render_air_quality_page
from views.carbon import render_carbon_page
from views.combined_insights import render_combined_insights_page
from views.about import render_about_page

# Inject custom wireframe-matched styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Render Dark Navy Navigation Sidebar
render_sidebar()

# Page Routing
current_page = st.session_state.get("active_nav", "Overview")

if current_page == "Overview":
    render_overview_page()
elif current_page == "Air Quality":
    render_air_quality_page()
elif current_page == "Carbon":
    render_carbon_page()
elif current_page == "Combined Insights":
    render_combined_insights_page()
elif current_page == "About":
    render_about_page()
