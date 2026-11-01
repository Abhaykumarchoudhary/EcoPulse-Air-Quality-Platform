"""
About View (Wireframe 5).
Features 'How EcoPulse works' 4-step pipeline, Data sources table,
Limitations list, Team credits (Abhay Kumar Choudhary and team),
and Action buttons (GitHub repository, Download report).
"""
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
            '<div style="display: grid; grid-template-columns: 2fr 3fr 2fr; padding: 7px 0; font-size: 12.5px; color: #1e293b;">'
            '<span style="font-weight: 600;">Climate TRACE</span>'
            '<span style="color: #475569;">Sector emissions</span>'
            '<span><a href="https://climatetrace.org" target="_blank" style="color: #0f766e; text-decoration: none;">climatetrace.org</a></span>'
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

    # Bottom Row: Team Credits & Action Buttons (Wireframe 5 Bottom)
    footer_html = (
        '<div class="content-box-card" style="padding: 16px 24px; margin-top: 4px; display: flex; justify-content: space-between; align-items: center;">'
        '<div>'
        '<div style="font-size: 13px; color: #1e293b; margin-bottom: 3px;">'
        '<strong>Team</strong> · Abhay Kumar Choudhary and team'
        '</div>'
        '<div style="font-size: 13px; color: #64748b;">'
        '<strong>Guide</strong> · [Guide name]'
        '</div></div>'
        '<div style="display: flex; gap: 12px; align-items: center;">'
        '<a href="https://github.com" target="_blank" style="background:#0f766e; color:#ffffff; padding:8px 18px; border-radius:6px; font-size:13px; font-weight:600; text-decoration:none;">GitHub repository</a>'
        '<a href="#" style="background:#ffffff; border:1px solid #0f766e; color:#0f766e; padding:8px 18px; border-radius:6px; font-size:13px; font-weight:600; text-decoration:none;">Download report</a>'
        '</div></div>'
    )
    st.markdown(footer_html, unsafe_allow_html=True)
