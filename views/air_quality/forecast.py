"""
Air Quality: Forecast & Anomalies View (Wireframe 2b).
Features 3-day forecast with confidence interval bands and AQI categories,
Anomaly detection table with sigma thresholds and 'Show on map' action,
and long-term observed vs predicted time series with range slider.
"""
import streamlit as st
from utils.chart_helpers import render_3day_forecast_chart, render_obs_vs_pred_timeseries
from data.forecast_data import FORECAST_DATA_NCR, STATION_FORECASTS, LONG_TERM_SERIES
from data.live_api import fetch_live_forecast_data
from data.anomalies import ANOMALY_DAYS

def render_forecast_view():
    is_live = (st.session_state.get("data_mode", "Live") == "Live")
    col_fc, col_anom = st.columns([62, 38])
    
    # Top Left: 3-Day Forecast Card
    with col_fc:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 0px; padding-bottom: 8px;">
            <div class="card-header-row">
                <div class="card-title-text">
                    3-day forecast <span class="help-circle-btn">?</span>
                </div>
                <div class="card-actions-row">
                    <span class="pill-btn-small">CSV · PNG</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Station Selector
        fc_area = st.selectbox(
            "Forecast Region",
            ["All Delhi-NCR (mean)", "Anand Vihar", "Jahangirpuri"],
            label_visibility="collapsed",
            key="sel_forecast_region"
        )
        
        if is_live and fc_area == "All Delhi-NCR (mean)":
            live_fc = fetch_live_forecast_data()
            hist_data = live_fc.get("historical", FORECAST_DATA_NCR["historical"])
            fore_data = live_fc.get("forecast", FORECAST_DATA_NCR["forecast"])
        elif fc_area == "Anand Vihar" and "anand_vihar" in STATION_FORECASTS:
            hist_data = STATION_FORECASTS["anand_vihar"]["historical"]
            fore_data = STATION_FORECASTS["anand_vihar"]["forecast"]
        elif fc_area == "Jahangirpuri" and "jahangirpuri" in STATION_FORECASTS:
            hist_data = STATION_FORECASTS["jahangirpuri"]["historical"]
            fore_data = STATION_FORECASTS["jahangirpuri"]["forecast"]
        else:
            hist_data = FORECAST_DATA_NCR["historical"]
            fore_data = FORECAST_DATA_NCR["forecast"]
            
        fig_fc = render_3day_forecast_chart(hist_data, fore_data)
        st.plotly_chart(fig_fc, use_container_width=True, config={"displayModeBar": False})
        
        st.markdown("""
        <div style="font-size: 11px; color: #64748b; margin-top: -12px; margin-bottom: 16px;">
            PM₂.₅ (µg/m³) · solid navy = last 7 days · dashed teal = next 3 days
        </div>
        """, unsafe_allow_html=True)

    # Top Right: Anomaly Days Table
    with col_anom:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 12px;">
            <div class="card-header-row" style="margin-bottom: 4px;">
                <div class="card-title-text">
                    Anomaly days <span class="help-circle-btn" title="Anomaly table: Days when the actual value differed from the model's expectation by more than 3 standard deviations.">?</span>
                </div>
                <div class="card-actions-row">
                    <span class="pill-btn-small">CSV</span>
                </div>
            </div>
            <div style="font-size: 11.5px; color: #64748b; margin-top: -6px; margin-bottom: 10px;">
                Days when the actual value differed from the model's expectation by more than 3 standard deviations.
            </div>
            
            <div style="font-size: 11px; font-weight: 700; color: #64748b; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; margin-bottom: 6px; display: flex; justify-content: space-between;">
                <span>Date</span>
                <span>Observed</span>
                <span>Expected</span>
                <span>σ</span>
            </div>
        """, unsafe_allow_html=True)
        
        for anom in ANOMALY_DAYS:
            sigma_style = "font-weight: 800; color: #dc2626;" if anom["is_severe"] else "color: #334155;"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px 0; font-size: 12.5px; border-bottom: 1px solid #f1f5f9; color: #1e293b;">
                <span style="font-weight: 500;">{anom['date_str']}</span>
                <span>{anom['observed']}</span>
                <span>{anom['expected']}</span>
                <span style="{sigma_style}">{anom['sigma']}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 'Show on map' Action Button
        if st.button("Show on map", key="btn_show_anom_map", type="primary", use_container_width=True):
            st.session_state["air_subtab"] = "Fused Map"
            st.session_state["show_anomalies"] = True
            st.rerun()

    # Bottom: Observed vs Predicted Time Series Card
    st.markdown("""
    <div class="content-box-card" style="margin-top: 14px;">
        <div class="card-header-row" style="margin-bottom: 4px;">
            <div class="card-title-text">
                Observed vs predicted <span class="help-circle-btn" title="Observed vs predicted (time series): How closely the model tracks real station readings over time. Red dots mark anomaly days.">?</span>
            </div>
            <div class="card-actions-row">
                <span class="pill-btn-small">CSV · PNG</span>
            </div>
        </div>
        <div style="font-size: 12px; color: #64748b; margin-bottom: 6px;">
            How closely the model tracks real station readings over time. Red dots mark anomaly days.
        </div>
        <div style="font-size: 11px; color: #94a3b8; margin-bottom: 10px;">
            Navy = observed · teal = predicted · red 8 px dots = anomaly days
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    fig_ts = render_obs_vs_pred_timeseries(LONG_TERM_SERIES)
    st.plotly_chart(fig_ts, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown("""
    <div style="background: #f1f5f9; border-radius: 6px; padding: 6px 14px; font-size: 11px; color: #64748b; text-align: center; margin-top: -10px;">
        Range slider: zooms this chart only, never moves the global date
    </div>
    """, unsafe_allow_html=True)
