"""
About View (Wireframe 5).
Features 'How EcoPulse works' 4-step pipeline, Data sources table,
Limitations list, Team credits (Abhay Kumar Choudhary and team),
and Action buttons (GitHub repository, Download report).
"""
import os
import streamlit as st

def render_about_page():
    # Top Header
    st.markdown(
        '<div class="top-header-bar" style="margin-bottom: 14px;">'
        '<div class="header-title-box"><h1>About</h1></div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Top Card: How EcoPulse works
    pipeline_html = (
        '<div class="content-box-card" style="padding: 20px 24px; margin-bottom: 16px;">'
        '<div class="card-title-text" style="margin-bottom: 12px;">How EcoPulse works</div>'
        '<div class="pipeline-flow-container">'
        '<div class="pipeline-step-card pipeline-step-teal">'
        '<div class="pipeline-step-icon">🛰️</div>'
        '<div class="pipeline-step-title">Collect</div>'
        '<div class="pipeline-step-subtitle" style="font-size:11.5px; line-height:1.4;">'
        'Download MAIAC AOD, CPCB, OpenAQ and Open-Meteo data'
        '</div></div>'
        '<div class="pipeline-arrow">→</div>'
        '<div class="pipeline-step-card pipeline-step-white">'
        '<div class="pipeline-step-icon">❇️</div>'
        '<div class="pipeline-step-title">Fuse</div>'
        '<div class="pipeline-step-subtitle" style="font-size:11.5px; line-height:1.4;">'
        'QA-mask AOD and match it to stations by day and cell'
        '</div></div>'
        '<div class="pipeline-arrow">→</div>'
        '<div class="pipeline-step-card pipeline-step-teal">'
        '<div class="pipeline-step-icon">📈</div>'
        '<div class="pipeline-step-title">Predict</div>'
        '<div class="pipeline-step-subtitle" style="font-size:11.5px; line-height:1.4;">'
        'RF/XGBoost estimates PM₂.₅; gap-fill covers cloudy days'
        '</div></div>'
        '<div class="pipeline-arrow">→</div>'
        '<div class="pipeline-step-card pipeline-step-white">'
        '<div class="pipeline-step-icon">🗺️</div>'
        '<div class="pipeline-step-title">Map</div>'
        '<div class="pipeline-step-subtitle" style="font-size:11.5px; line-height:1.4;">'
        'Render a 1 km daily grid with forecasts and anomalies'
        '</div></div>'
        '</div></div>'
    )
    st.markdown(pipeline_html, unsafe_allow_html=True)
    
    # Middle Row: Data sources (Left) & Limitations (Right)
    col_sources, col_limits = st.columns([58, 42])
    
    with col_sources:
        sources_html = (
            '<div class="content-box-card" style="height: 100%; margin-bottom: 16px;">'
            '<div class="card-title-text" style="margin-bottom: 14px;">Data sources</div>'
            '<div style="font-size: 11px; font-weight: 700; color: #64748b; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; margin-bottom: 8px; display: grid; grid-template-columns: 2fr 3fr 2fr;">'
            '<span>Source</span><span>What it gives</span><span>Link</span>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 2fr 3fr 2fr; padding: 7px 0; font-size: 12.5px; border-bottom: 1px solid #f1f5f9; color: #1e293b;">'
            '<span style="font-weight: 600;">MODIS MAIAC</span>'
            '<span style="color: #475569;">1 km daily AOD</span>'
            '<span><a href="https://earthdata.nasa.gov" target="_blank" style="color: #0f766e; text-decoration: none;">NASA Earthdata</a></span>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 2fr 3fr 2fr; padding: 7px 0; font-size: 12.5px; border-bottom: 1px solid #f1f5f9; color: #1e293b;">'
            '<span style="font-weight: 600;">CPCB</span>'
            '<span style="color: #475569;">Station PM₂.₅ readings</span>'
            '<span><a href="https://cpcb.nic.in" target="_blank" style="color: #0f766e; text-decoration: none;">cpcb.nic.in</a></span>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 2fr 3fr 2fr; padding: 7px 0; font-size: 12.5px; border-bottom: 1px solid #f1f5f9; color: #1e293b;">'
            '<span style="font-weight: 600;">OpenAQ</span>'
            '<span style="color: #475569;">Extra station data</span>'
            '<span><a href="https://openaq.org" target="_blank" style="color: #0f766e; text-decoration: none;">openaq.org</a></span>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 2fr 3fr 2fr; padding: 7px 0; font-size: 12.5px; border-bottom: 1px solid #f1f5f9; color: #1e293b;">'
            '<span style="font-weight: 600;">Open-Meteo</span>'
            '<span style="color: #475569;">Wind, BLH, temperature, humidity</span>'
            '<span><a href="https://open-meteo.com" target="_blank" style="color: #0f766e; text-decoration: none;">open-meteo.com</a></span>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 2fr 3fr 2fr; padding: 7px 0; font-size: 12.5px; border-bottom: 1px solid #f1f5f9; color: #1e293b;">'
            '<span style="font-weight: 600;">NASA FIRMS</span>'
            '<span style="color: #475569;">Active VIIRS/MODIS fire hotspots</span>'
            '<span><a href="https://firms.modaps.eosdis.nasa.gov" target="_blank" style="color: #0f766e; text-decoration: none;">firms.modaps...</a></span>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 2fr 3fr 2fr; padding: 7px 0; font-size: 12.5px; border-bottom: 1px solid #f1f5f9; color: #1e293b;">'
            '<span style="font-weight: 600;">Climate TRACE</span>'
            '<span style="color: #475569;">Sector emissions</span>'
            '<span><a href="https://climatetrace.org" target="_blank" style="color: #0f766e; text-decoration: none;">climatetrace.org</a></span>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 2fr 3fr 2fr; padding: 7px 0; font-size: 12.5px; color: #1e293b;">'
            '<span style="font-weight: 600;">TomTom Traffic</span>'
            '<span style="color: #475569;">Delhi corridor congestion delays</span>'
            '<span><a href="https://developer.tomtom.com" target="_blank" style="color: #0f766e; text-decoration: none;">tomtom.com</a></span>'
            '</div></div>'
        )
        st.markdown(sources_html, unsafe_allow_html=True)
        
    with col_limits:
        limits_html = (
            '<div class="content-box-card" style="height: 100%; margin-bottom: 16px;">'
            '<div class="card-title-text" style="margin-bottom: 14px;">Limitations</div>'
            '<ul style="font-size: 13px; color: #475569; line-height: 1.85; padding-left: 20px; margin: 0;">'
            '<li>Few ground stations for validation</li>'
            '<li>Many days with missing AOD (cloud, haze)</li>'
            '<li>Emissions data is monthly and coarse</li>'
            '<li>Simulator is sensitivity-only</li>'
            '</ul></div>'
        )
        st.markdown(limits_html, unsafe_allow_html=True)

    # Read Technical Report files for direct download
    report_html_path = os.path.join("docs", "ECOPULSE_TECHNICAL_REPORT.html")
    report_md_path = os.path.join("docs", "ECOPULSE_TECHNICAL_REPORT.md")
    
    report_html_data = ""
    if os.path.exists(report_html_path):
        with open(report_html_path, "r", encoding="utf-8") as f:
            report_html_data = f.read()

    report_md_data = ""
    if os.path.exists(report_md_path):
        with open(report_md_path, "r", encoding="utf-8") as f:
            report_md_data = f.read()

    # Bottom Row: Team Credits & Action Buttons
    with st.container(border=True):
        c_team, c_actions = st.columns([52, 48])
        with c_team:
            st.markdown("""
            <div style="font-size: 13.5px; color: #1e293b; margin-bottom: 4px;">
                <strong>Engineering Team:</strong> Abhay Kumar Choudhary &amp; Research Team
            </div>
            <div style="font-size: 12px; color: #64748b;">
                <strong>Capstone Project:</strong> Satellite-Fused Air Quality &amp; Carbon Intelligence · Delhi-NCR
            </div>
            """, unsafe_allow_html=True)
            
        with c_actions:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.link_button(
                    "★ GitHub Repo",
                    url="https://github.com/Abhaykumarchoudhary/EcoPulse-Air-Quality-Platform",
                    use_container_width=True
                )
            with col_b2:
                st.download_button(
                    label="📥 Technical Report",
                    data=report_html_data or report_md_data,
                    file_name="EcoPulse_Technical_Report_v2.1.html",
                    mime="text/html",
                    use_container_width=True,
                    help="Download complete technical documentation, mathematical formulation, and model validation benchmarks."
                )

