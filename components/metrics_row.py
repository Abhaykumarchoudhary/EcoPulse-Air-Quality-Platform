"""
Key Metrics Row Component for EcoPulse.
Renders 4 metric cards with vertical accent stripes on the left: Orange, Red, Amber, Teal.
Matches wireframe reference image layout and iconography.
"""
import streamlit as st

def render_overview_metrics(
    mean_pm25: float = 112.0,
    pct_change: float = 8.0,
    most_polluted_area: str = "Anand Vihar",
    most_polluted_val: int = 186,
    most_polluted_status: str = "Very Poor",
    anomaly_days: int = 3,
    r2_score: float = 0.78
):
    col1, col2, col3, col4 = st.columns(4)
    
    # 1. MEAN PM2.5 (12 JAN)
    with col1:
        c1_html = (
            '<div class="metric-card-wrapper border-accent-orange">'
            '<div class="metric-header">'
            '<span class="metric-label">MEAN PM₂.₅ (12 JAN)</span>'
            '<span class="metric-icon">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/>'
            '<path d="M9.6 4.6A2 2 0 1 1 11 8H2"/>'
            '<path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>'
            '</svg>'
            '</span>'
            '</div>'
            f'<div class="metric-value">{int(mean_pm25)} <span style="font-size:18px; font-weight:600; color:#334155;">µg/m³</span></div>'
            f'<div class="metric-subtext change-red">▲ {abs(pct_change):.0f}% vs previous day</div>'
            '</div>'
        )
        st.markdown(c1_html, unsafe_allow_html=True)
        
    # 2. MOST POLLUTED AREA
    with col2:
        c2_html = (
            '<div class="metric-card-wrapper border-accent-red">'
            '<div class="metric-header">'
            '<span class="metric-label">MOST POLLUTED AREA</span>'
            '<span class="metric-icon">'
            '<svg width="16" height="18" viewBox="0 0 16 20" fill="none">'
            '<circle cx="8" cy="6" r="5" fill="#ef4444"/>'
            '<circle cx="6.5" cy="4.5" r="1.5" fill="#fca5a5"/>'
            '<line x1="8" y1="11" x2="8" y2="19" stroke="#94a3b8" stroke-width="1.8" stroke-linecap="round"/>'
            '</svg>'
            '</span>'
            '</div>'
            f'<div class="metric-value" style="font-size:23px; font-weight:700; margin-top:2px;">{most_polluted_area}</div>'
            f'<div class="metric-subtext">{most_polluted_val} µg/m³ · {most_polluted_status}</div>'
            '</div>'
        )
        st.markdown(c2_html, unsafe_allow_html=True)
        
    # 3. ANOMALY DAYS THIS MONTH
    with col3:
        c3_html = (
            '<div class="metric-card-wrapper border-accent-amber">'
            '<div class="metric-header">'
            '<span class="metric-label">ANOMALY DAYS THIS MONTH</span>'
            '<span class="metric-icon">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
            '<line x1="12" y1="9" x2="12" y2="13"/>'
            '<line x1="12" y1="17" x2="12.01" y2="17"/>'
            '</svg>'
            '</span>'
            '</div>'
            f'<div class="metric-value">{anomaly_days}</div>'
            '<div class="metric-subtext">Deviation above 3σ</div>'
            '</div>'
        )
        st.markdown(c3_html, unsafe_allow_html=True)
        
    # 4. MODEL ACCURACY (R²)
    with col4:
        c4_html = (
            '<div class="metric-card-wrapper border-accent-teal">'
            '<div class="metric-header">'
            '<span class="metric-label">MODEL ACCURACY (R²)</span>'
            '<span class="metric-icon">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#db2777" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="10" stroke="#db2777" fill="#fdf2f8"/>'
            '<circle cx="12" cy="12" r="6" stroke="#db2777"/>'
            '<circle cx="12" cy="12" r="2" fill="#db2777"/>'
            '</svg>'
            '</span>'
            '</div>'
            f'<div class="metric-value">{r2_score:.2f}</div>'
            '<div class="metric-subtext">Leave-one-station-out</div>'
            '</div>'
        )
        st.markdown(c4_html, unsafe_allow_html=True)
