"""
Plotly Chart Generators for EcoPulse.
Configured with modern clean typography, custom palettes, and exact wireframe layouts.
"""
import plotly.graph_objects as go
from typing import List, Dict, Any

def get_base_layout(height: int = 340):
    """Clean minimal Plotly layout template."""
    return go.Layout(
        height=height,
        margin=dict(l=40, r=20, t=25, b=35),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Inter, sans-serif", size=12, color="#475569"),
        hoverlabel=dict(bgcolor="#0f172a", font_size=12, font_family="Inter", font_color="#ffffff"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            linecolor="#cbd5e1",
            tickcolor="#cbd5e1",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            linecolor="#cbd5e1",
            tickcolor="#cbd5e1",
            zeroline=False
        )
    )

def render_overview_sparkline(past_days: List[int] = [95, 108, 102, 118, 112], forecast_days: List[int] = [128, 145, 119]):
    """
    Renders compact sparkline for Wireframe 1 'Next 3 days' card.
    Past line is navy, today has a vertical divider, future has colored dots.
    """
    fig = go.Figure()
    
    x_past = ["-4d", "-3d", "-2d", "Yesterday", "Today"]
    x_future = ["Today", "+1d", "+2d", "+3d"]
    y_future = [past_days[-1]] + forecast_days
    
    # Historical past line
    fig.add_trace(go.Scatter(
        x=x_past,
        y=past_days,
        mode="lines+markers",
        line=dict(color="#0f172a", width=2.5),
        marker=dict(size=6, color="#0f172a"),
        name="Past",
        hoverinfo="y"
    ))
    
    # Forecast line
    fig.add_trace(go.Scatter(
        x=x_future,
        y=y_future,
        mode="lines+markers",
        line=dict(color="#0f766e", width=2, dash="dot"),
        marker=dict(size=8, color=["#0f172a", "#f97316", "#ef4444", "#14b8a6"]),
        name="Forecast",
        hoverinfo="y"
    ))
    
    # Vertical line at Today
    fig.add_shape(
        type="line",
        x0="Today",
        x1="Today",
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="#94a3b8", width=1.5, dash="dash")
    )
    fig.add_annotation(
        x="Today",
        y=0.04,
        yref="paper",
        text="Today",
        showarrow=False,
        font=dict(size=10, color="#64748b")
    )
    
    layout = get_base_layout(height=170)
    layout.update(
        showlegend=False,
        margin=dict(l=25, r=15, t=10, b=25),
        xaxis=dict(showgrid=False, linecolor="#e2e8f0"),
        yaxis=dict(showgrid=True, gridcolor="#f8fafc", title=None)
    )
    fig.update_layout(layout)
    return fig

def render_3day_forecast_chart(historical: List[Dict[str, Any]], forecast: List[Dict[str, Any]]):
    """
    Renders 3-day forecast chart with AQI color background bands, uncertainty cone,
    and Today vertical separator matching Wireframe 2b.
    """
    fig = go.Figure()
    
    # Background AQI Bands
    # Very Poor: 121 to 250
    fig.add_hrect(y0=121, y1=240, fillcolor="#fee2e2", opacity=0.45, line_width=0,
                  annotation_text="Very Poor band", annotation_position="top left",
                  annotation_font=dict(color="#991b1b", size=10))
    # Poor: 91 to 121
    fig.add_hrect(y0=91, y1=121, fillcolor="#ffedd5", opacity=0.45, line_width=0,
                  annotation_text="Poor band", annotation_position="top left",
                  annotation_font=dict(color="#9a3412", size=10))
    # Moderate: 60 to 91
    fig.add_hrect(y0=60, y1=91, fillcolor="#fef9c3", opacity=0.4, line_width=0,
                  annotation_text="Moderate band", annotation_position="top left",
                  annotation_font=dict(color="#854d0e", size=10))
    
    # Uncertainty cone for forecast (upper & lower bounds)
    f_x = [f["day_label"] for f in forecast]
    f_upper = [f["upper"] for f in forecast]
    f_lower = [f["lower"] for f in forecast]
    f_pred = [f["predicted"] for f in forecast]
    
    # Shaded uncertainty band
    fig.add_trace(go.Scatter(
        x=f_x + f_x[::-1],
        y=f_upper + f_lower[::-1],
        fill="toself",
        fillcolor="rgba(20, 184, 166, 0.22)",
        line=dict(color="rgba(255,255,255,0)"),
        hoverinfo="skip",
        name="Uncertainty band",
        showlegend=False
    ))
    
    # Past 7 days (solid navy line)
    h_x = [h["day_label"] for h in historical]
    h_y = [h["observed"] for h in historical]
    
    fig.add_trace(go.Scatter(
        x=h_x,
        y=h_y,
        mode="lines+markers",
        name="Observed (last 7 days)",
        line=dict(color="#0f172a", width=2.5),
        marker=dict(size=6, color="#0f172a"),
        hovertemplate="Observed: %{y} µg/m³<extra></extra>"
    ))
    
    # Connect last historical point to forecast
    bridge_x = [h_x[-1]] + f_x
    bridge_y = [h_y[-1]] + f_pred
    
    fig.add_trace(go.Scatter(
        x=bridge_x,
        y=bridge_y,
        mode="lines+markers",
        name="Forecast (next 3 days)",
        line=dict(color="#0f766e", width=2.5, dash="dash"),
        marker=dict(size=7, color="#0f766e"),
        hovertemplate="Predicted: %{y} µg/m³<extra></extra>"
    ))
    
    # Today vertical divider
    today_x = h_x[-1]
    fig.add_shape(
        type="line",
        x0=today_x,
        x1=today_x,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="#64748b", width=1.5, dash="dot")
    )
    fig.add_annotation(
        x=today_x,
        y=0.06,
        yref="paper",
        text="Today",
        showarrow=False,
        xanchor="left",
        font=dict(color="#0f172a", size=11, family="Inter")
    )
    
    layout = get_base_layout(height=320)
    layout.update(
        showlegend=False,
        yaxis=dict(title="PM₂.₅ (µg/m³)", range=[55, 230]),
        xaxis=dict(showgrid=False)
    )
    fig.update_layout(layout)
    return fig

def render_obs_vs_pred_timeseries(series: List[Dict[str, Any]]):
    """
    Renders multi-week observed vs predicted time series with red anomaly dots
    and range slider matching Wireframe 2b bottom chart.
    """
    x_dates = [d["date"] for d in series]
    y_pred = [d["predicted"] for d in series]
    y_obs = [d["observed"] for d in series]
    
    anomalies = [d for d in series if d.get("anomaly")]
    anom_x = [d["date"] for d in anomalies]
    anom_y = [d["observed"] for d in anomalies]
    anom_sigma = [d["sigma"] for d in anomalies]
    
    fig = go.Figure()
    
    # Predicted series (teal line)
    fig.add_trace(go.Scatter(
        x=x_dates,
        y=y_pred,
        mode="lines",
        name="Predicted",
        line=dict(color="#0f766e", width=2),
        hovertemplate="Predicted: %{y} µg/m³<extra></extra>"
    ))
    
    # Observed series (navy line)
    fig.add_trace(go.Scatter(
        x=x_dates,
        y=y_obs,
        mode="lines",
        name="Observed",
        line=dict(color="#0f172a", width=2.2),
        hovertemplate="Observed: %{y} µg/m³<extra></extra>"
    ))
    
    # Anomaly points (red 8px dots)
    fig.add_trace(go.Scatter(
        x=anom_x,
        y=anom_y,
        mode="markers",
        name="Anomaly days",
        marker=dict(size=8, color="#ef4444", symbol="circle", line=dict(color="#b91c1c", width=1.5)),
        hovertemplate="⚠️ Anomaly: %{y} µg/m³ (Dev: +%{text}σ)<extra></extra>",
        text=anom_sigma
    ))
    
    layout = get_base_layout(height=280)
    layout.update(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(
            rangeslider=dict(visible=True, thickness=0.08, bgcolor="#f1f5f9"),
            type="date"
        ),
        yaxis=dict(title="PM₂.₅ (µg/m³)")
    )
    fig.update_layout(layout)
    return fig

def render_scatter_obs_vs_pred(points: List[Dict[str, Any]]):
    """
    Observed vs Predicted scatter plot (R^2 = 0.78) with teal dots, 40% opacity,
    and 1:1 dashed line for Wireframe 2c.
    """
    x_obs = [p["observed"] for p in points]
    y_pred = [p["predicted"] for p in points]
    
    fig = go.Figure()
    
    # 1:1 Reference Line
    fig.add_trace(go.Scatter(
        x=[40, 260],
        y=[40, 260],
        mode="lines",
        name="1:1 line",
        line=dict(color="#94a3b8", width=1.5, dash="dash"),
        hoverinfo="skip"
    ))
    
    # Scatter points (teal dots, 40% opacity)
    fig.add_trace(go.Scatter(
        x=x_obs,
        y=y_pred,
        mode="markers",
        name="Stations",
        marker=dict(
            size=7,
            color="rgba(15, 118, 110, 0.45)",
            line=dict(color="#0f766e", width=0.5)
        ),
        hovertemplate="Obs: %{x} µg/m³<br>Pred: %{y} µg/m³<extra></extra>"
    ))
    
    layout = get_base_layout(height=280)
    layout.update(
        showlegend=False,
        xaxis=dict(title="Observed PM₂.₅ (µg/m³)", range=[35, 265]),
        yaxis=dict(title="Predicted PM₂.₅ (µg/m³)", range=[35, 265])
    )
    fig.update_layout(layout)
    return fig

def render_loso_bar_chart(station_errors: List[Dict[str, Any]]):
    """
    Leave-one-station-out (LOSO) error horizontal bar chart.
    Worst station in amber, others in teal.
    """
    sorted_errors = sorted(station_errors, key=lambda x: x["mae"])
    x_vals = [e["mae"] for e in sorted_errors]
    y_labels = [e["station"] for e in sorted_errors]
    colors = [e["color"] for e in sorted_errors]
    
    fig = go.Figure(go.Bar(
        x=x_vals,
        y=y_labels,
        orientation="h",
        marker=dict(color=colors),
        hovertemplate="%{y}: MAE %{x} µg/m³<extra></extra>"
    ))
    
    layout = get_base_layout(height=280)
    layout.update(
        showlegend=False,
        xaxis=dict(title="MAE (µg/m³)"),
        yaxis=dict(autorange="reversed")
    )
    fig.update_layout(layout)
    return fig

def render_shap_bar_chart(shap_data: List[Dict[str, Any]]):
    """
    SHAP importance horizontal bar chart.
    AOD bar in teal, others in slate grey.
    """
    sorted_shap = sorted(shap_data, key=lambda x: x["importance"])
    x_vals = [s["importance"] for s in sorted_shap]
    y_labels = [s["feature"] for s in sorted_shap]
    colors = [s["color"] for s in sorted_shap]
    
    fig = go.Figure(go.Bar(
        x=x_vals,
        y=y_labels,
        orientation="h",
        marker=dict(color=colors),
        hovertemplate="%{y}: Relative SHAP %{x:.2f}<extra></extra>"
    ))
    
    layout = get_base_layout(height=280)
    layout.update(
        showlegend=False,
        xaxis=dict(title="Mean |SHAP value|"),
        yaxis=dict(autorange="reversed")
    )
    fig.update_layout(layout)
    return fig

def render_carbon_sector_ranking(sectors_data: List[Dict[str, Any]], selected_sector: str = "Power"):
    """
    Horizontal bar chart for Carbon 'Emissions by sector'.
    Selected sector in orange/amber, other sectors in teal.
    """
    # Sort descending by emissions
    sorted_data = sorted(sectors_data, key=lambda x: x["emissions_mt"], reverse=False)
    
    y_labels = []
    x_vals = []
    colors = []
    
    for s in sorted_data:
        is_sel = (s["sector"] == selected_sector)
        y_labels.append(f"{s['sector']} (selected)" if is_sel else s["sector"])
        x_vals.append(s["emissions_mt"])
        colors.append("#f59e0b" if is_sel else "#0f766e")
        
    fig = go.Figure(go.Bar(
        x=x_vals,
        y=y_labels,
        orientation="h",
        marker=dict(color=colors),
        hovertemplate="%{y}: %{x:.1f} Mt CO₂e<extra></extra>"
    ))
    
    layout = get_base_layout(height=260)
    layout.update(
        showlegend=False,
        margin=dict(l=40, r=20, t=10, b=30),
        xaxis=dict(title="Emissions (Mt CO₂e)", gridcolor="#f1f5f9"),
        yaxis=dict(autorange="reversed")
    )
    fig.update_layout(layout)
    return fig

def render_carbon_trend_forecast(forecast_dict: Dict[str, Any], selected_models: List[str] = ["Prophet", "XGBoost", "Naive"]):
    """
    Past emissions and multi-model forecast with shaded grey forecast period area.
    Navy solid = history · teal dashed = Prophet · purple dashed = XGBoost · grey dotted = naive
    """
    fig = go.Figure()
    
    hx = forecast_dict["history_x"]
    hy = forecast_dict["history_y"]
    fx = forecast_dict["forecast_x"]
    
    # 1. Shaded Grey Forecast Period
    # From "2023" to "2024 Q4"
    fig.add_vrect(
        x0="2023",
        x1="2024 Q4",
        fillcolor="#f1f5f9",
        opacity=0.7,
        layer="below",
        line_width=0,
        annotation_text="forecast period",
        annotation_position="top right",
        annotation_font=dict(size=10, color="#64748b")
    )
    
    # 2. Historical line (Navy solid)
    fig.add_trace(go.Scatter(
        x=hx,
        y=hy,
        mode="lines+markers",
        name="History",
        line=dict(color="#0f172a", width=2.5),
        marker=dict(size=5, color="#0f172a"),
        hovertemplate="%{x}: %{y:.1f} Mt<extra>History</extra>"
    ))
    
    # 3. Model projections
    if "Prophet" in selected_models:
        fig.add_trace(go.Scatter(
            x=fx,
            y=forecast_dict["prophet_y"],
            mode="lines",
            name="Prophet",
            line=dict(color="#0f766e", width=2.2, dash="dash"),
            hovertemplate="%{x}: %{y:.1f} Mt<extra>Prophet</extra>"
        ))
        
    if "XGBoost" in selected_models:
        fig.add_trace(go.Scatter(
            x=fx,
            y=forecast_dict["xgboost_y"],
            mode="lines",
            name="XGBoost",
            line=dict(color="#8b5cf6", width=2.2, dash="dash"),
            hovertemplate="%{x}: %{y:.1f} Mt<extra>XGBoost</extra>"
        ))
        
    if "Naive" in selected_models:
        fig.add_trace(go.Scatter(
            x=fx,
            y=forecast_dict["naive_y"],
            mode="lines",
            name="Naive",
            line=dict(color="#94a3b8", width=2, dash="dot"),
            hovertemplate="%{x}: %{y:.1f} Mt<extra>Naive</extra>"
        ))
        
    layout = get_base_layout(height=260)
    layout.update(
        showlegend=False,
        margin=dict(l=40, r=20, t=10, b=30),
        xaxis=dict(showgrid=False),
        yaxis=dict(title="Mt CO₂e", gridcolor="#f8fafc")
    )
    fig.update_layout(layout)
    return fig

def render_carbon_coal_scenario(scenario_data: Dict[str, Any]):
    """
    What-if reduce coal chart.
    Grey line = baseline · green line = scenario
    """
    qx = scenario_data["quarters"]
    base_y = scenario_data["baseline"]
    scen_y = scenario_data["scenario"]
    
    fig = go.Figure()
    
    # Baseline (Grey line)
    fig.add_trace(go.Scatter(
        x=qx,
        y=base_y,
        mode="lines+markers",
        name="Baseline",
        line=dict(color="#94a3b8", width=2),
        marker=dict(size=5, color="#94a3b8"),
        hovertemplate="Baseline: %{y} Mt<extra></extra>"
    ))
    
    # Scenario (Green line)
    fig.add_trace(go.Scatter(
        x=qx,
        y=scen_y,
        mode="lines+markers",
        name="Scenario",
        line=dict(color="#16a34a", width=2.5),
        marker=dict(size=6, color="#16a34a"),
        hovertemplate="Scenario (-%{text}% coal): %{y} Mt<extra></extra>",
        text=[scenario_data["reduction_pct"]] * len(qx)
    ))
    
    layout = get_base_layout(height=220)
    layout.update(
        showlegend=False,
        margin=dict(l=35, r=20, t=10, b=30),
        xaxis=dict(showgrid=False),
        yaxis=dict(title="Mt CO₂e", gridcolor="#f8fafc")
    )
    fig.update_layout(layout)
    return fig

def render_combined_dual_axis(monthly_data: List[Dict[str, Any]]):
    """
    Dual-axis chart: Monthly PM2.5 and emissions side by side. Blue shading marks winter.
    Navy line = PM2.5 (left axis) · amber line = emissions (right axis)
    """
    months = [d["month"] for d in monthly_data]
    pm_vals = [d["pm25"] for d in monthly_data]
    em_vals = [d["emissions"] for d in monthly_data]
    
    fig = go.Figure()
    
    # Blue shading for winter months (Jan 2023 - Feb 2023, Nov 2023 - Feb 2024, Nov 2024 - Dec 2024)
    # Winter block 1
    fig.add_vrect(
        x0="Jan 2023", x1="Feb 2023",
        fillcolor="rgba(219, 234, 254, 0.45)",
        layer="below", line_width=0,
        annotation_text="Winter", annotation_position="top left",
        annotation_font=dict(size=10, color="#1e40af")
    )
    # Winter block 2
    fig.add_vrect(
        x0="Nov 2023", x1="Feb 2024",
        fillcolor="rgba(219, 234, 254, 0.45)",
        layer="below", line_width=0,
        annotation_text="Winter", annotation_position="top left",
        annotation_font=dict(size=10, color="#1e40af")
    )
    # Winter block 3
    fig.add_vrect(
        x0="Nov 2024", x1="Dec 2024",
        fillcolor="rgba(219, 234, 254, 0.45)",
        layer="below", line_width=0,
        annotation_text="Winter", annotation_position="top left",
        annotation_font=dict(size=10, color="#1e40af")
    )
    
    # Left axis: PM2.5 (Navy line)
    fig.add_trace(go.Scatter(
        x=months,
        y=pm_vals,
        name="PM₂.₅",
        mode="lines+markers",
        line=dict(color="#0f172a", width=2.2),
        marker=dict(size=5, color="#0f172a"),
        hovertemplate="PM₂.₅: %{y} µg/m³<extra></extra>",
        yaxis="y1"
    ))
    
    # Right axis: Emissions (Amber line)
    fig.add_trace(go.Scatter(
        x=months,
        y=em_vals,
        name="Emissions",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=2.2),
        marker=dict(size=5, color="#f59e0b"),
        hovertemplate="Emissions: %{y:.1f} Mt CO₂e<extra></extra>",
        yaxis="y2"
    ))
    
    layout = get_base_layout(height=290)
    layout.update(
        showlegend=False,
        margin=dict(l=45, r=45, t=15, b=35),
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(
            title=dict(text="PM₂.₅ (µg/m³)", font=dict(color="#0f172a")),
            tickfont=dict(color="#0f172a"),
            gridcolor="#f1f5f9"
        ),
        yaxis2=dict(
            title=dict(text="Emissions (Mt CO₂e)", font=dict(color="#f59e0b")),
            tickfont=dict(color="#f59e0b"),
            overlaying="y",
            side="right",
            showgrid=False
        )
    )
    fig.update_layout(layout)
    return fig

def render_combined_seasonal_pattern(seasonal_data: List[Dict[str, Any]]):
    """
    Seasonal pattern: Average PM2.5 for each month. Darker bars are winter months.
    """
    months = [d["month"] for d in seasonal_data]
    pm_vals = [d["pm25"] for d in seasonal_data]
    colors = [d["color"] for d in seasonal_data]
    
    fig = go.Figure(go.Bar(
        x=months,
        y=pm_vals,
        marker=dict(color=colors),
        hovertemplate="%{x}: %{y} µg/m³<extra></extra>"
    ))
    
    layout = get_base_layout(height=260)
    layout.update(
        showlegend=False,
        margin=dict(l=35, r=15, t=10, b=30),
        xaxis=dict(showgrid=False),
        yaxis=dict(title="Mean PM₂.₅ (µg/m³)", gridcolor="#f8fafc")
    )
    fig.update_layout(layout)
    return fig
