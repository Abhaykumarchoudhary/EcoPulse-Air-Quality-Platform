"""
Sidebar Navigation and Filter Controls for EcoPulse.
Matches the dark navy theme, brand logo, nav buttons, filters, and reset button.
"""
import os
import streamlit as st
from config import AVAILABLE_DATES, DEFAULT_DATE
from data.stations import STATIONS
from data.live_api import load_env_credentials

def render_sidebar():
    import os
    with st.sidebar:
        # Brand Logo & Title with crisp vector pulse emblem
        st.markdown("""
        <div class="sidebar-brand-container">
            <div class="sidebar-logo-circle">
                <svg viewBox="0 0 40 40" width="34" height="34" fill="none">
                    <circle cx="20" cy="20" r="18" fill="url(#brandGrad)" stroke="#14b8a6" stroke-width="1.5"/>
                    <circle cx="20" cy="20" r="13" stroke="#14b8a6" stroke-width="0.8" stroke-dasharray="2 3" opacity="0.4"/>
                    <path d="M 8 20 H 12.5 L 14.8 14.5 L 17.5 24.5 L 20.8 10 L 23.8 27 L 26.2 16.5 L 28 20 H 32" stroke="url(#pulseGradBrand)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="20.8" cy="10" r="1.8" fill="#5eead4"/>
                    <defs>
                        <linearGradient id="brandGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#0f766e"/>
                            <stop offset="50%" stop-color="#115e59"/>
                            <stop offset="100%" stop-color="#042f2e"/>
                        </linearGradient>
                        <linearGradient id="pulseGradBrand" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#2dd4bf"/>
                            <stop offset="50%" stop-color="#ffffff"/>
                            <stop offset="100%" stop-color="#5eead4"/>
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            <div class="sidebar-brand-text-box">
                <div class="sidebar-brand-title">Eco<span>Pulse</span></div>
                <div class="sidebar-brand-subtitle">AQ &amp; CARBON INTELLIGENCE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Options
        if "active_nav" not in st.session_state:
            st.session_state["active_nav"] = "Overview"
            
        nav_items = [
            ("Overview", "🏞️"),
            ("Air Quality", "🍃"),
            ("Carbon", "📊"),
            ("Combined Insights", "🔗"),
            ("About", "ℹ️")
        ]
        
        for item_name, icon in nav_items:
            is_active = (st.session_state["active_nav"] == item_name)
            active_cls = "active" if is_active else ""
            btn_key = f"nav_btn_{item_name.lower().replace(' ', '_')}"
            
            # Using button styled via CSS
            if st.button(f"{icon}  {item_name}", key=btn_key, use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state["active_nav"] = item_name
                st.rerun()

        # Data Source Selector (Live API vs Benchmark Dataset)
        st.markdown("<div class='sidebar-section-title'>DATA STREAM</div>", unsafe_allow_html=True)
        if "data_mode" not in st.session_state:
            st.session_state["data_mode"] = "Live"

        data_mode_sel = st.radio(
            "Data Source",
            ["Live Satellite & Ground APIs", "Benchmark Dataset (Jan 2025)"],
            index=0 if st.session_state["data_mode"] == "Live" else 1,
            key="radio_data_mode",
            label_visibility="collapsed"
        )
        st.session_state["data_mode"] = "Live" if "Live" in data_mode_sel else "Benchmark"

        if st.session_state["data_mode"] == "Live":
            st.markdown("""
            <div class="sidebar-live-card">
                <div class="title"><span class="pulse-dot-green"></span> Live Stream Active</div>
                <div class="meta">Connected to Open-Meteo CAMS, ERA5 &amp; 12 Ground Stations.</div>
            </div>
            """, unsafe_allow_html=True)
            
            c_ref1, c_ref2 = st.columns([60, 40])
            with c_ref1:
                if st.button("🔄 Refresh", key="btn_refresh_live", use_container_width=True):
                    st.cache_data.clear()
                    st.rerun()
            with c_ref2:
                st.markdown("<div style='font-size:11px; color:#10b981; padding-top:6px; font-weight:600;'>● Online</div>", unsafe_allow_html=True)

            with st.expander("⚙️ API Keys & Live Feeds", expanded=False):
                load_env_credentials()
                has_waqi = bool(st.session_state.get("waqi_token") or os.environ.get("WAQI_API_TOKEN"))
                has_firms = bool(st.session_state.get("firms_key") or os.environ.get("NASA_FIRMS_MAP_KEY"))
                has_openaq = bool(st.session_state.get("openaq_key") or os.environ.get("OPENAQ_API_KEY"))
                has_tomtom = bool(st.session_state.get("tomtom_key") or os.environ.get("TOMTOM_API_KEY"))
                has_ogd = bool(os.environ.get("DATA_GOV_IN_API_KEY"))

                waqi_badge = '<span style="color:#34d399;">✓ Live Active (23 CPCB Stations)</span>' if has_waqi else '<span style="color:#94a3b8;">Not set</span>'
                firms_badge = '<span style="color:#34d399;">✓ Live Active (VIIRS Satellites)</span>' if has_firms else '<span style="color:#94a3b8;">Reference Mode</span>'
                openaq_badge = '<span style="color:#34d399;">✓ Connected (.env)</span>' if has_openaq else '<span style="color:#94a3b8;">Optional</span>'
                tomtom_badge = '<span style="color:#34d399;">✓ Connected (.env)</span>' if has_tomtom else '<span style="color:#94a3b8;">Corridor Model</span>'
                ogd_badge = '<span style="color:#34d399;">✓ Connected (.env)</span>' if has_ogd else '<span style="color:#94a3b8;">Fallback</span>'

                st.markdown(f"""
                <div style="font-size:11px; color:#cbd5e1; line-height:1.6; margin-bottom: 8px;">
                    <strong>Open-Meteo Weather:</strong> <span style="color:#34d399;">✓ Live (Free)</span><br>
                    <strong>WAQI CPCB Ground:</strong> {waqi_badge}<br>
                    <strong>NASA FIRMS Fires:</strong> {firms_badge}<br>
                    <strong>OpenAQ v3 Feed:</strong> {openaq_badge}<br>
                    <strong>TomTom Traffic:</strong> {tomtom_badge}<br>
                    <strong>data.gov.in CPCB:</strong> {ogd_badge}
                </div>
                """, unsafe_allow_html=True)
                
                # 1. WAQI Token (Instant free access to all Delhi CPCB stations)
                curr_waqi = st.session_state.get("waqi_token") or os.environ.get("WAQI_API_TOKEN", "")
                waqi_input = st.text_input(
                    "WAQI Token (Real CPCB Live)",
                    value=curr_waqi,
                    type="password",
                    key="input_waqi_token",
                    help="Free instant key from https://aqicn.org/data-platform/token/ for all 40+ Delhi CPCB stations."
                )
                if waqi_input != st.session_state.get("waqi_token", ""):
                    st.session_state["waqi_token"] = waqi_input
                    st.cache_data.clear()
                    st.rerun()

                # 2. NASA FIRMS Map Key
                curr_firms = st.session_state.get("firms_key") or os.environ.get("NASA_FIRMS_MAP_KEY", "")
                firms_input = st.text_input(
                    "NASA FIRMS Map Key",
                    value=curr_firms,
                    type="password",
                    key="input_firms_key",
                    help="Active fire detection key from https://firms.modaps.eosdis.nasa.gov/api/map_key/"
                )
                if firms_input != st.session_state.get("firms_key", ""):
                    st.session_state["firms_key"] = firms_input
                    st.cache_data.clear()
                    st.rerun()

                # 3. TomTom Key
                curr_tomtom = st.session_state.get("tomtom_key") or os.environ.get("TOMTOM_API_KEY", "")
                tomtom_input = st.text_input(
                    "TomTom API Key",
                    value=curr_tomtom,
                    type="password",
                    key="input_tomtom_key",
                    help="Traffic key from https://developer.tomtom.com/"
                )
                if tomtom_input != st.session_state.get("tomtom_key", ""):
                    st.session_state["tomtom_key"] = tomtom_input
                    st.cache_data.clear()
                    st.rerun()

                # 4. OpenAQ v3 Key
                curr_openaq = st.session_state.get("openaq_key") or os.environ.get("OPENAQ_API_KEY", "")
                openaq_input = st.text_input(
                    "OpenAQ Key (Optional)",
                    value=curr_openaq,
                    type="password",
                    key="input_openaq_key",
                    help="Free key from https://explore.openaq.org/register"
                )
                if openaq_input != st.session_state.get("openaq_key", ""):
                    st.session_state["openaq_key"] = openaq_input
                    st.cache_data.clear()
                    st.rerun()

                # 3. Upload custom CPCB CSV
                st.markdown("<div style='font-size:11px; font-weight:600; color:#94a3b8; margin-top:10px;'>Upload CPCB CSV:</div>", unsafe_allow_html=True)
                uploaded_csv = st.file_uploader(
                    "Drop CPCB CSV",
                    type=["csv"],
                    key="upl_cpcb_csv",
                    label_visibility="collapsed"
                )
                if uploaded_csv is not None:
                    os.makedirs(os.path.join("data", "raw"), exist_ok=True)
                    csv_target = os.path.join("data", "raw", "cpcb_stations.csv")
                    with open(csv_target, "wb") as f:
                        f.write(uploaded_csv.getbuffer())
                    st.success("Loaded CPCB CSV!")
                    st.cache_data.clear()
                    st.rerun()

        st.markdown("<div class='sidebar-section-title'>FILTERS</div>", unsafe_allow_html=True)
        
        current_nav = st.session_state["active_nav"]
        filters_disabled = False
        if current_nav == "Carbon":
            filters_disabled = True
            st.markdown("<div style='font-size:11px; font-style:italic; color:#94a3b8; margin-top:-6px; margin-bottom:12px; line-height:1.4;'>Date, Area and Station are greyed out here. This page uses its own filters.</div>", unsafe_allow_html=True)
        elif current_nav in ["Combined Insights", "About"]:
            filters_disabled = True
            st.markdown("<div style='font-size:11px; font-style:italic; color:#94a3b8; margin-top:-6px; margin-bottom:12px; line-height:1.4;'>Global filters disabled on this page.</div>", unsafe_allow_html=True)

        # Date Filter
        if "filter_date" not in st.session_state:
            st.session_state["filter_date"] = DEFAULT_DATE
        date_sel = st.selectbox(
            "Date",
            AVAILABLE_DATES,
            index=AVAILABLE_DATES.index(st.session_state["filter_date"]) if st.session_state["filter_date"] in AVAILABLE_DATES else len(AVAILABLE_DATES)-1,
            disabled=filters_disabled,
            key="sel_filter_date"
        )
        if not filters_disabled:
            st.session_state["filter_date"] = date_sel
        
        # Area Filter
        area_options = ["All Delhi-NCR", "Central Delhi", "East Delhi", "North Delhi", "South Delhi", "Noida", "Gurugram"]
        if "filter_area" not in st.session_state:
            st.session_state["filter_area"] = "All Delhi-NCR"
        area_sel = st.selectbox(
            "Area",
            area_options,
            index=area_options.index(st.session_state["filter_area"]),
            disabled=filters_disabled,
            key="sel_filter_area"
        )
        if not filters_disabled:
            st.session_state["filter_area"] = area_sel
        
        # Station Filter
        st_names = ["All stations"] + [s["name"] for s in STATIONS]
        if "filter_station" not in st.session_state:
            st.session_state["filter_station"] = "All stations"
        station_sel = st.selectbox(
            "Station",
            st_names,
            index=st_names.index(st.session_state["filter_station"]),
            disabled=filters_disabled,
            key="sel_filter_station"
        )
        if not filters_disabled:
            st.session_state["filter_station"] = station_sel
        
        # Reset Filters Button
        if st.button("Reset filters", key="btn_reset_filters", disabled=filters_disabled, use_container_width=True):
            st.session_state["filter_date"] = DEFAULT_DATE
            st.session_state["filter_area"] = "All Delhi-NCR"
            st.session_state["filter_station"] = "All stations"
            st.rerun()
            
        st.markdown("""
        <div style="margin-top: 60px; font-size: 11px; color: #475569; padding-top: 20px; border-top: 1px solid #1e293b;">
            Final Year Project · v1.0
        </div>
        """, unsafe_allow_html=True)
