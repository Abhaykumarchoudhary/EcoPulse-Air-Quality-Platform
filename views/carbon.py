"""
Carbon View (Wireframe 3).
Features Sector Ranking, Multi-Model Trend & Forecasting (Prophet, XGBoost, Naive)
with shaded forecast period, Coal Reduction What-If Scenario, and Model Metrics Footer.
"""
import streamlit as st
from components.header import render_top_header
from utils.chart_helpers import (
    render_carbon_sector_ranking,
    render_carbon_trend_forecast,
    render_carbon_coal_scenario
)
from data.carbon_data import (
    SECTOR_EMISSIONS,
    get_sector_emissions,
    get_sector_forecast_data,
    calculate_coal_reduction_scenario
)

def render_carbon_page():
    # Top Header
    render_top_header(
        title="Carbon",
        subtitle="Sector-level greenhouse gas emissions and multi-model forecasting for Delhi-NCR",
        date_str="Dec 2024"
    )
    
    # State initialization for Carbon page
    if "carbon_sector" not in st.session_state:
        st.session_state["carbon_sector"] = "Power"
    if "carbon_years" not in st.session_state:
        st.session_state["carbon_years"] = (2015, 2024)
    if "carbon_models" not in st.session_state:
        st.session_state["carbon_models"] = ["Prophet", "XGBoost", "Naive"]
    if "coal_reduction_pct" not in st.session_state:
        st.session_state["coal_reduction_pct"] = 20

    f_col1, f_col2, f_col3 = st.columns([30, 38, 32])
    
    with f_col1:
        sec_idx = ["Power", "Transport", "Industry", "Buildings", "Waste"].index(st.session_state["carbon_sector"])
        sel_sec = st.selectbox(
            "Sector Filter",
            ["Power", "Transport", "Industry", "Buildings", "Waste"],
            index=sec_idx,
            format_func=lambda s: f"Sector · {s}",
            label_visibility="collapsed",
            key="sel_carbon_sec"
        )
        st.session_state["carbon_sector"] = sel_sec
        
    with f_col2:
        st.markdown("<div style='font-size:11px; font-weight:700; color:#64748b; margin-bottom:2px;'>Years 2015 — 2024</div>", unsafe_allow_html=True)
        years_range = st.slider(
            "Years Range",
            min_value=2015,
            max_value=2024,
            value=st.session_state["carbon_years"],
            label_visibility="collapsed",
            key="slider_carbon_years"
        )
        st.session_state["carbon_years"] = years_range
        
    with f_col3:
        sel_models = st.multiselect(
            "Models Selection",
            ["Prophet", "XGBoost", "Naive"],
            default=st.session_state["carbon_models"],
            format_func=lambda m: f"Model: {m}",
            label_visibility="collapsed",
            key="msel_carbon_models"
        )
        if sel_models:
            st.session_state["carbon_models"] = sel_models
            
    # Middle Row: Emissions by sector (Left) & Trend and forecast (Right)
    col_rank, col_trend = st.columns([48, 52])
    
    with col_rank:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 0px; padding-bottom: 6px;">
            <div class="card-header-row">
                <div class="card-title-text">
                    Emissions by sector <span class="help-circle-btn" title="Sector ranking: Total emissions per sector for the selected years.">?</span>
                </div>
            </div>
            <div style="font-size: 11.5px; color: #64748b; margin-top: -10px; margin-bottom: 8px;">
                Sector ranking: Total emissions per sector for the selected years.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        active_sector_data = get_sector_emissions(st.session_state["carbon_sector"])
        fig_rank = render_carbon_sector_ranking(active_sector_data, selected_sector=st.session_state["carbon_sector"])
        st.plotly_chart(fig_rank, use_container_width=True, config={"displayModeBar": False})
        
    with col_trend:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 0px; padding-bottom: 6px;">
            <div class="card-header-row">
                <div class="card-title-text">
                    Trend and forecast <span class="help-circle-btn" title="Trend and forecast: Past emissions and each model's forecast. The grey area is the forecast period.">?</span>
                </div>
            </div>
            <div style="font-size: 11.5px; color: #64748b; margin-top: -10px; margin-bottom: 8px;">
                Trend and forecast: Past emissions and each model's forecast. The grey area is the forecast period.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        forecast_dict = get_sector_forecast_data(sector=st.session_state["carbon_sector"])
        fig_trend = render_carbon_trend_forecast(forecast_dict, selected_models=st.session_state["carbon_models"])
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        
        st.markdown("""
        <div style="font-size: 11px; color: #64748b; text-align: center; margin-top: -10px;">
            Navy solid = history · teal dashed = Prophet · purple dashed = XGBoost · grey dotted = naive
        </div>
        """, unsafe_allow_html=True)

    st.write("") # spacing

    # Lower Card: What-if: reduce coal ?
    st.markdown("""
    <div class="content-box-card" style="margin-top: 10px; margin-bottom: 14px;">
        <div class="card-header-row">
            <div class="card-title-text">
                What-if: reduce coal <span class="help-circle-btn" title="Sensitivity scenario perturbing coal usage in Delhi-NCR power generation.">?</span>
            </div>
            <div>
                <span style="border: 1.5px solid #f59e0b; background: #fffbeb; color: #92400e; padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 700; letter-spacing: 0.05em;">INDICATIVE ONLY</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_whatif_ctrl, col_whatif_chart = st.columns([36, 64])
    
    with col_whatif_ctrl:
        st.selectbox("Coal Sector", ["Power"], format_func=lambda s: f"Sector · {s}", disabled=True, key="sel_whatif_sec")
        st.write("")
        st.markdown(f"<div style='font-size:13px; font-weight:600; color:#0f172a;'>Reduce coal by <span style='color:#0f766e; font-weight:800;'>{st.session_state['coal_reduction_pct']}%</span></div>", unsafe_allow_html=True)
        coal_slider = st.slider(
            "Coal Reduction Slider",
            min_value=0,
            max_value=50,
            value=st.session_state["coal_reduction_pct"],
            step=5,
            label_visibility="collapsed",
            key="slider_coal_pct"
        )
        st.session_state["coal_reduction_pct"] = coal_slider
        st.markdown("<div style='font-size:11px; color:#64748b;'>0–50%, steps of 5</div>", unsafe_allow_html=True)
        
    with col_whatif_chart:
        scen_calc = calculate_coal_reduction_scenario(st.session_state["coal_reduction_pct"])
        fig_coal = render_carbon_coal_scenario(scen_calc)
        st.plotly_chart(fig_coal, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style="font-size: 11px; color: #64748b; text-align: center; margin-top: -10px;">
            Grey line = baseline · green line = scenario
        </div>
        """, unsafe_allow_html=True)

    # Bottom Metrics Bar (Wireframe 3 Bottom)
    sec_metrics = forecast_dict["metrics"]
    st.markdown(f"""
    <div class="content-box-card" style="padding: 10px 18px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 12.5px; color: #475569;">
        <div>
            <strong>Metrics</strong> · Sector: <strong>{sec_metrics['sector']}</strong> · RMSE: <strong>{sec_metrics['rmse']}</strong> · MAE: <strong>{sec_metrics['mae']}</strong> · Best model: <strong style="color:#0f766e;">{sec_metrics['best_model']}</strong>
        </div>
        <div>
            <span class="pill-btn-small">CSV</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
