"""
Air Quality: Model Performance View (Wireframe 2c).
Features Model Comparison Table with highlighted fusion row,
Observed vs Predicted 1:1 scatter plot, LOSO Per-station error bars with amber worst station,
SHAP feature importances, and bottom gap-fill missing AOD banner.
"""
import streamlit as st
from utils.chart_helpers import (
    render_scatter_obs_vs_pred,
    render_loso_bar_chart,
    render_shap_bar_chart
)
from data.model_metrics import (
    MODEL_COMPARISON,
    STATION_LOSO_ERRORS,
    SHAP_IMPORTANCE,
    SCATTER_POINTS
)

def render_model_perf_view():
    # Top Card: Model Comparison Table
    st.markdown("""
    <div class="content-box-card" style="margin-bottom: 20px;">
        <div class="card-header-row" style="margin-bottom: 12px;">
            <div class="card-title-text">
                Model comparison <span class="help-circle-btn">?</span>
            </div>
            <div class="card-actions-row">
                <span class="pill-btn-small">CSV</span>
            </div>
        </div>
        
        <div style="font-size: 11px; font-weight: 700; color: #64748b; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 4px; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;">
            <span>Model</span>
            <span style="text-align:right;">R²</span>
            <span style="text-align:right;">RMSE</span>
            <span style="text-align:right;">MAE</span>
        </div>
    """, unsafe_allow_html=True)
    
    for row in MODEL_COMPARISON:
        if row["is_best"]:
            # Highlighted in soft teal background
            st.markdown(f"""
            <div style="background: #ccfbf1; border-radius: 6px; padding: 10px 8px; margin: 4px 0; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; font-size: 13.5px; font-weight: 700; color: #0f766e; border-left: 3px solid #0f766e;">
                <span>{row['name']}</span>
                <span style="text-align:right;">{row['r2']:.2f}</span>
                <span style="text-align:right;">{row['rmse']:.1f}</span>
                <span style="text-align:right;">{row['mae']:.1f}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="padding: 8px 8px; border-bottom: 1px solid #f1f5f9; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; font-size: 13px; color: #334155;">
                <span>{row['name']}</span>
                <span style="text-align:right;">{row['r2']:.2f}</span>
                <span style="text-align:right;">{row['rmse']:.1f}</span>
                <span style="text-align:right;">{row['mae']:.1f}</span>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Middle Row: 3 Charts Side by Side
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 8px; padding-bottom: 4px;">
            <div class="card-header-row" style="margin-bottom: 4px;">
                <div class="card-title-text" style="font-size: 14px;">
                    Observed vs predicted <span class="help-circle-btn" title="Scatter: Each dot is one station-day. Dots near the dashed line mean accurate predictions.">?</span>
                </div>
            </div>
            <div style="font-size: 11px; color: #475569; margin-bottom: 4px;">
                Each dot is one station-day. Dots near the dashed line mean accurate predictions.
            </div>
            <div style="font-size: 10.5px; color: #94a3b8;">
                teal dots, 40% opacity · dashed grey 1:1 line
            </div>
        </div>
        """, unsafe_allow_html=True)
        scatter_fig = render_scatter_obs_vs_pred(SCATTER_POINTS)
        st.plotly_chart(scatter_fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 8px; padding-bottom: 4px;">
            <div class="card-header-row" style="margin-bottom: 4px;">
                <div class="card-title-text" style="font-size: 14px;">
                    Per-station error (LOSO) <span class="help-circle-btn">?</span>
                </div>
            </div>
            <div style="font-size: 11px; color: #64748b;">
                teal bars, worst station in amber<br>&nbsp;
            </div>
        </div>
        """, unsafe_allow_html=True)
        loso_fig = render_loso_bar_chart(STATION_LOSO_ERRORS)
        st.plotly_chart(loso_fig, use_container_width=True, config={"displayModeBar": False})

    with col3:
        st.markdown("""
        <div class="content-box-card" style="margin-bottom: 8px; padding-bottom: 4px;">
            <div class="card-header-row" style="margin-bottom: 4px;">
                <div class="card-title-text" style="font-size: 14px;">
                    SHAP importance <span class="help-circle-btn">?</span>
                </div>
            </div>
            <div style="font-size: 11px; color: #64748b;">
                AOD bar teal, others slate grey<br>&nbsp;
            </div>
        </div>
        """, unsafe_allow_html=True)
        shap_fig = render_shap_bar_chart(SHAP_IMPORTANCE)
        st.plotly_chart(shap_fig, use_container_width=True, config={"displayModeBar": False})

    # Bottom Gap-Fill Alert Banner
    st.markdown("""
    <div class="alert-banner-amber" style="margin-top: 14px;">
        <span>Share of days with missing AOD: 38%. Handled by the gap-fill model.</span>
        <span class="help-circle-btn">?</span>
    </div>
    """, unsafe_allow_html=True)
