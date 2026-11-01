"""
Combined Insights View (Wireframe 4 - Scrolling Page).
Features Dual-Axis Monthly PM2.5 vs Emissions with winter shading,
Pearson Correlation Heatmap table, 12-Month Seasonal Profile,
and Point Emission Hotspots Map with sector filter chips.
"""
import streamlit as st
from components.header import render_top_header
from utils.chart_helpers import (
    render_combined_dual_axis,
    render_combined_seasonal_pattern
)
from components.map_view import render_combined_hotspot_map
from data.combined_data import (
    MONTHLY_DUAL_AXIS,
    CORRELATION_HEATMAP,
    SEASONAL_PATTERN,
    EMISSION_HOTSPOTS
)
from data.grid import DEFAULT_GRID

def render_combined_insights_page():
    # Top Header
    render_top_header(
        title="Combined Insights",
        subtitle="Empirical relationships and spatial overlaps between greenhouse gas emissions and ambient PM₂.₅",
        date_str="Dec 2024"
    )
    
    # Top Alert Banner (Wireframe 4)
    st.markdown("""
    <div class="alert-banner-amber">
        <span>Correlation is indicative, not causal. Emissions data is monthly and coarse.</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 1: PM2.5 and emissions by month (Dual Axis)
    st.markdown("""
    <div class="content-box-card" style="margin-bottom: 0px; padding-bottom: 6px;">
        <div class="card-header-row">
            <div class="card-title-text">
                PM₂.₅ and emissions by month <span class="help-circle-btn" title="Dual-axis chart: Monthly PM₂.₅ and emissions side by side. Blue shading marks winter.">?</span>
            </div>
        </div>
        <div style="font-size: 11.5px; color: #64748b; margin-top: -10px; margin-bottom: 6px;">
            Dual-axis chart: Monthly PM₂.₅ and emissions side by side. Blue shading marks winter.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_dual = render_combined_dual_axis(MONTHLY_DUAL_AXIS)
    st.plotly_chart(fig_dual, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown("""
    <div style="font-size: 11px; color: #64748b; text-align: center; margin-top: -12px; margin-bottom: 20px;">
        Navy line = PM₂.₅ (left axis) · amber line = emissions (right axis)
    </div>
    """, unsafe_allow_html=True)

    # Middle Row: Correlation Heatmap (Left) & Seasonal Pattern (Right)
    col_corr, col_season = st.columns([48, 52])
    
    with col_corr:
        corr_html = (
            '<div class="content-box-card" style="margin-bottom: 0px; padding-bottom: 12px; height: 100%;">'
            '<div class="card-header-row" style="margin-bottom: 14px;">'
            '<div class="card-title-text">'
            'Correlation heatmap <span class="help-circle-btn" title="Pearson correlation coefficient between monthly sector emissions and ground PM2.5.">?</span>'
            '</div></div>'
            '<div style="border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; margin-bottom: 14px;">'
            '<table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 13px;">'
            '<thead>'
            '<tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #64748b; font-size: 12px;">'
            '<th style="padding: 10px 8px; width: 20%;"></th>'
            '<th style="padding: 10px 8px;">Power</th>'
            '<th style="padding: 10px 8px;">Transport</th>'
            '<th style="padding: 10px 8px;">Industry</th>'
            '<th style="padding: 10px 8px;">Buildings</th>'
            '</tr></thead>'
            '<tbody>'
            '<tr>'
            '<td style="font-weight: 700; color: #475569; padding: 16px 8px; background: #f8fafc; border-right: 1px solid #e2e8f0;">PM₂.₅</td>'
            '<td style="background: #ef4444; color: #ffffff; font-weight: 800; font-size: 15px; padding: 16px 8px;">0.68</td>'
            '<td style="background: #ffedd5; color: #9a3412; font-weight: 700; font-size: 15px; padding: 16px 8px;">0.41</td>'
            '<td style="background: #fee2e2; color: #991b1b; font-weight: 700; font-size: 15px; padding: 16px 8px;">0.37</td>'
            '<td style="background: #bfdbfe; color: #1e40af; font-weight: 700; font-size: 15px; padding: 16px 8px;">-0.12</td>'
            '</tr></tbody></table></div>'
            '<div style="font-size: 11px; color: #64748b; text-align: center;">'
            'Blue = -1 · white: 0 · red: +1'
            '</div></div>'
        )
        st.markdown(corr_html, unsafe_allow_html=True)
        
    with col_season:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 0px; padding-bottom: 6px;">
            <div class="card-header-row">
                <div class="card-title-text">
                    Seasonal pattern <span class="help-circle-btn" title="Seasonal pattern: Average PM₂.₅ for each month. Darker bars are winter months.">?</span>
                </div>
            </div>
            <div style="font-size: 11.5px; color: #64748b; margin-top: -10px; margin-bottom: 6px;">
                Seasonal pattern: Average PM₂.₅ for each month. Darker bars are winter months.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        fig_season = render_combined_seasonal_pattern(SEASONAL_PATTERN)
        st.plotly_chart(fig_season, use_container_width=True, config={"displayModeBar": False})

    st.write("") # spacing

    # Bottom Card: Pollution and emission hotspots ?
    if "hotspot_filter" not in st.session_state:
        st.session_state["hotspot_filter"] = "All"
        
    st.markdown("""
    <div class="content-box-card" style="margin-top: 10px; margin-bottom: 0px; padding-bottom: 8px;">
        <div class="card-header-row">
            <div class="card-title-text">
                Pollution and emission hotspots <span class="help-circle-btn" title="Hotspot map: Fused PM₂.₅ with emission sources. Bigger diamonds mean larger emissions.">?</span>
            </div>
        </div>
        <div style="font-size: 11.5px; color: #64748b; margin-top: -10px; margin-bottom: 12px;">
            Hotspot map: Fused PM₂.₅ with emission sources. Bigger diamonds mean larger emissions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter Chips: [ All ], [ Power ], [ Industry ], [ Transport ]
    c_btn1, c_btn2, c_btn3, c_btn4, c_fill = st.columns([12, 14, 14, 16, 44])
    
    with c_btn1:
        if st.button("All", key="chip_all", type="primary" if st.session_state["hotspot_filter"] == "All" else "secondary", use_container_width=True):
            st.session_state["hotspot_filter"] = "All"
            st.rerun()
    with c_btn2:
        if st.button("Power", key="chip_power", type="primary" if st.session_state["hotspot_filter"] == "Power" else "secondary", use_container_width=True):
            st.session_state["hotspot_filter"] = "Power"
            st.rerun()
    with c_btn3:
        if st.button("Industry", key="chip_industry", type="primary" if st.session_state["hotspot_filter"] == "Industry" else "secondary", use_container_width=True):
            st.session_state["hotspot_filter"] = "Industry"
            st.rerun()
    with c_btn4:
        if st.button("Transport", key="chip_transport", type="primary" if st.session_state["hotspot_filter"] == "Transport" else "secondary", use_container_width=True):
            st.session_state["hotspot_filter"] = "Transport"
            st.rerun()

    # Leaflet Hotspot Map
    render_combined_hotspot_map(
        grid_cells=DEFAULT_GRID,
        hotspots=EMISSION_HOTSPOTS,
        sector_filter=st.session_state["hotspot_filter"],
        height=380
    )
