"""
Top Header Component for EcoPulse.
Renders title, subtitle, demo data chip, date, and Delhi-NCR pin badge.
"""
import streamlit as st

def render_top_header(title: str, subtitle: str, date_str: str = "12 Jan 2025", is_live: bool = False):
    badge_html = (
        '<span class="badge-live"><span class="pulse-dot-green"></span>LIVE API</span>'
        if is_live else
        '<span class="badge-demo">Demo data</span>'
    )
    
    st.markdown(f"""
    <div class="top-header-bar">
        <div class="header-title-box">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div class="header-badges-row">
            {badge_html}
            <span class="badge-date">Data through: {date_str}</span>
            <span class="badge-location">📍 Delhi-NCR</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
