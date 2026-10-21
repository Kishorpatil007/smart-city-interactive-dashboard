"""
Smart City Dashboard - Plotly Data Visualization Module
Provides clean, accessible, human-centered Plotly visualizations for city metrics.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Human-Centered Civic Palette
CHART_THEME = {
    "paper_bg": "#FFFFFF",
    "plot_bg": "#FFFFFF",
    "font_color": "#475569",
    "title_color": "#0F172A",
    "grid_color": "#F1F5F9",
    "line_color": "#E2E8F0",
    "accent_blue": "#2563EB",
    "accent_emerald": "#10B981",
    "accent_amber": "#F59E0B",
    "accent_purple": "#8B5CF6",
    "accent_rose": "#F43F5E",
    "accent_sky": "#0284C7"
}

def _apply_humanized_theme(fig, title="", height=380, show_legend=True):
    """Utility to apply uniform, clean, accessible styling to all Plotly figures."""
    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.02,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"size": 15, "color": CHART_THEME["title_color"], "family": "Inter, -apple-system, sans-serif", "weight": "bold"}
        },
        paper_bgcolor=CHART_THEME["paper_bg"],
        plot_bgcolor=CHART_THEME["plot_bg"],
        font={"color": CHART_THEME["font_color"], "family": "Inter, -apple-system, sans-serif"},
        height=height,
        margin={"l": 45, "r": 30, "t": 60, "b": 45},
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#64748B")
        ),
        xaxis=dict(
            gridcolor=CHART_THEME["grid_color"],
            linecolor=CHART_THEME["line_color"],
            tickfont=dict(color="#64748B", size=11)
        ),
        yaxis=dict(
            gridcolor=CHART_THEME["grid_color"],
            linecolor=CHART_THEME["line_color"],
            tickfont=dict(color="#64748B", size=11)
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#CBD5E1",
            font_size=12,
            font_color="#0F172A",
            font_family="Inter, -apple-system, sans-serif"
        )
    )
    return fig

def plot_electricity_by_area(area_df, selected_zone="All Districts (Maharashtra Overview)"):
    """
    Bar Chart: Electricity consumption across Maharashtra districts with average benchmark.
    """
    df = area_df.sort_values(by="electricity_mwh", ascending=False)
    colors = [
        "#D97706" if z == selected_zone else "#2563EB"
        for z in df["zone"]
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["zone"],
        y=df["electricity_mwh"],
        marker=dict(
            color=colors,
            line=dict(color="#1E40AF", width=1),
            opacity=0.92
        ),
        text=[f"{v:,.0f}" for v in df["electricity_mwh"]],
        textposition="outside",
        textfont=dict(color="#334155", size=9),
        hovertemplate="<b>%{x} District</b><br>⚡ Power: %{y:,.1f} MWh/day<br>Population: %{customdata:,}<extra></extra>",
        customdata=df["population"],
        name="Daily Usage"
    ))

    # Add Target / Sustainability Benchmark line
    avg_power = df["electricity_mwh"].mean()
    fig.add_hline(
        y=avg_power,
        line_dash="dot",
        line_color="#D97706",
        annotation_text=f"District Benchmark Mean ({avg_power:,.0f} MWh)",
        annotation_position="top right",
        annotation_font=dict(color="#D97706", size=10)
    )

    _apply_humanized_theme(fig, title="⚡ Electricity Consumption by District in Maharashtra (MWh / Day)", height=440, show_legend=False)
    fig.update_xaxes(tickangle=-45, tickfont=dict(size=9))
    return fig

def plot_aqi_over_time(hourly_df, zone_name):
    """
    Line Chart: AQI over time with soft, humanized safety threshold bands.
    """
    fig = go.Figure()

    # Safety Zone Background Shading with soft pastel tints
    fig.add_hrect(y0=0, y1=50, fillcolor="#10B981", opacity=0.06, line_width=0, annotation_text="Good (0-50)", annotation_position="top left", annotation_font_size=10, annotation_font_color="#047857")
    fig.add_hrect(y0=50, y1=100, fillcolor="#F59E0B", opacity=0.06, line_width=0, annotation_text="Moderate (51-100)", annotation_position="top left", annotation_font_size=10, annotation_font_color="#B45309")
    fig.add_hrect(y0=100, y1=150, fillcolor="#F97316", opacity=0.06, line_width=0, annotation_text="Unhealthy for Sensitive (101-150)", annotation_position="top left", annotation_font_size=10, annotation_font_color="#C2410C")
    fig.add_hrect(y0=150, y1=300, fillcolor="#EF4444", opacity=0.06, line_width=0, annotation_text="Unhealthy (>150)", annotation_position="top left", annotation_font_size=10, annotation_font_color="#B91C1C")

    # Main AQI Line
    fig.add_trace(go.Scatter(
        x=hourly_df["timestamp"],
        y=hourly_df["aqi"],
        mode="lines",
        line=dict(color="#0284C7", width=2.4, shape="spline"),
        name="AQI Index",
        fill="tozeroy",
        fillcolor="rgba(2, 132, 199, 0.07)",
        hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>🌿 Air Quality: <b>%{y:.0f}</b><br>Temp: %{customdata[0]}°C | Hum: %{customdata[1]}%<extra></extra>",
        customdata=np.stack((hourly_df["temperature_c"], hourly_df["humidity_pct"]), axis=-1)
    ))

    # Add 24-hr moving average trend
    if len(hourly_df) >= 24:
        ma_24 = hourly_df["aqi"].rolling(window=24, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=hourly_df["timestamp"],
            y=ma_24,
            mode="lines",
            line=dict(color="#E11D48", width=1.8, dash="dash"),
            name="24h Average"
        ))

    _apply_humanized_theme(fig, title=f"🌿 Air Quality Index (AQI) Trend & Health Thresholds — {zone_name}")
    fig.update_yaxes(range=[0, max(hourly_df["aqi"].max() + 15, 120)])
    return fig

def plot_waste_categories_pie(waste_df, zone_name):
    """
    Pie / Donut Chart: Waste categories distribution and tonnage with clean styling.
    """
    fig = go.Figure()
    total_tons = waste_df["tons_per_day"].sum()

    fig.add_trace(go.Pie(
        labels=waste_df["category"],
        values=waste_df["tons_per_day"],
        hole=0.58,
        marker=dict(
            colors=waste_df["color"],
            line=dict(color="#FFFFFF", width=2)
        ),
        textinfo="percent+label",
        textposition="outside",
        textfont=dict(size=11, color="#334155"),
        hovertemplate="<b>%{label}</b><br>Collected: %{value:,.1f} Tons/day<br>Share: %{percent}<extra></extra>",
        pull=[0.04 if "Organic" in c or "Paper" in c else 0 for c in waste_df["category"]]
    ))

    # Center label in donut hole
    fig.add_annotation(
        text=f"<b>{total_tons:,.0f}</b><br><span style='font-size:11px; color:#64748B;'>Tons/Day</span>",
        x=0.5, y=0.5,
        font_size=18,
        font_color="#0F172A",
        showarrow=False
    )

    _apply_humanized_theme(fig, title=f"♻️ Municipal Waste Segregation & Recovery ({zone_name})", show_legend=True)
    return fig

def plot_traffic_level_by_area(area_df, selected_zone="All Districts (Maharashtra Overview)"):
    """
    Bar Chart: Traffic mobility index (%) across all 36 districts of Maharashtra.
    """
    df = area_df.sort_values(by="traffic_index", ascending=False)
    def get_color(val, zone_name):
        if zone_name == selected_zone:
            return "#D97706"
        if val < 40:
            return "#10B981"
        elif val < 65:
            return "#3B82F6"
        return "#EF4444"

    colors = [get_color(v, z) for v, z in zip(df["traffic_index"], df["zone"])]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["zone"],
        y=df["traffic_index"],
        marker=dict(
            color=colors,
            line=dict(color="#CBD5E1", width=1)
        ),
        text=[f"{v}%" for v in df["traffic_index"]],
        textposition="outside",
        textfont=dict(color="#334155", size=9),
        hovertemplate="<b>%{x} District</b><br>🚦 Mobility Congestion Index: <b>%{y}%</b><extra></extra>",
        name="Congestion %"
    ))

    # Free flow and brisk threshold lines
    fig.add_hline(y=65, line_dash="dash", line_color="#D97706", annotation_text="Heavy Congestion (65%)", annotation_font_size=10, annotation_font_color="#D97706")
    fig.add_hline(y=40, line_dash="dash", line_color="#059669", annotation_text="Smooth Flow (40%)", annotation_font_size=10, annotation_font_color="#059669")

    _apply_humanized_theme(fig, title="🚦 Traffic Mobility Index across Maharashtra Districts (%)", height=440, show_legend=False)
    fig.update_xaxes(tickangle=-45, tickfont=dict(size=9))
    fig.update_yaxes(range=[0, 105])
    return fig

def plot_water_consumption_trend(hourly_df, zone_name):
    """
    Line & Bar Chart: Water consumption over time with conservation baseline.
    """
    daily_water = hourly_df.groupby("date")["water_ml"].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily_water["date"],
        y=daily_water["water_ml"],
        marker=dict(
            color="#38BDF8",
            line=dict(color="#0284C7", width=1)
        ),
        name="Daily Consumption (ML)",
        hovertemplate="<b>%{x}</b><br>💧 Water Consumed: <b>%{y:.1f} ML</b><extra></extra>"
    ))

    target_val = daily_water["water_ml"].mean() * 0.94
    fig.add_trace(go.Scatter(
        x=daily_water["date"],
        y=[target_val] * len(daily_water),
        mode="lines",
        line=dict(color="#059669", width=2.2, dash="dash"),
        name=f"Conservation Target ({target_val:.1f} ML)"
    ))

    _apply_humanized_theme(fig, title=f"💧 Water Consumption vs Sustainability Target — {zone_name}")
    return fig

def plot_temperature_and_humidity(hourly_df, zone_name):
    """
    Dual-axis Chart: Hourly temperature (°C) and relative humidity (%).
    """
    fig = go.Figure()

    # Temperature Trace
    fig.add_trace(go.Scatter(
        x=hourly_df["timestamp"],
        y=hourly_df["temperature_c"],
        mode="lines",
        line=dict(color="#EA580C", width=2.2),
        name="Temperature (°C)",
        hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>🌤️ Temp: %{y:.1f} °C<extra></extra>"
    ))

    # Humidity Trace (secondary y)
    fig.add_trace(go.Scatter(
        x=hourly_df["timestamp"],
        y=hourly_df["humidity_pct"],
        mode="lines",
        line=dict(color="#0284C7", width=2.0, dash="dot"),
        name="Humidity (%)",
        yaxis="y2",
        hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>💧 Humidity: %{y:.1f} %<extra></extra>"
    ))

    _apply_humanized_theme(fig, title=f"🌤️ Microclimate Tracking (Temperature & Humidity) — {zone_name}")
    
    # Configure secondary y-axis
    fig.update_layout(
        yaxis2=dict(
            title="Humidity (%)",
            title_font=dict(color="#0284C7"),
            tickfont=dict(color="#0284C7"),
            overlaying="y",
            side="right",
            showgrid=False
        )
    )
    fig.update_yaxes(title="Temperature (°C)")
    return fig

def plot_hourly_traffic_curve(hourly_df, zone_name):
    """
    Hourly Rush Hour Traffic Congestion Curve with friendly annotations.
    """
    hourly_avg = hourly_df.groupby("hour")["traffic_index"].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hourly_avg["hour"],
        y=hourly_avg["traffic_index"],
        mode="lines+markers",
        line=dict(color="#E11D48", width=2.6, shape="spline"),
        marker=dict(size=6, color="#FB7185", line=dict(color="#FFFFFF", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(225, 29, 72, 0.08)",
        name="Mobility Index",
        hovertemplate="<b>Hour: %{x}:00</b><br>🚦 Avg Congestion: %{y:.1f}%<extra></extra>"
    ))

    fig.add_vrect(x0=7.5, x1=9.5, fillcolor="#F59E0B", opacity=0.08, line_width=0, annotation_text="Morning Commute (8-9:30 AM)", annotation_position="top left", annotation_font_size=10, annotation_font_color="#B45309")
    fig.add_vrect(x0=17.0, x1=19.0, fillcolor="#F59E0B", opacity=0.08, line_width=0, annotation_text="Evening Commute (5-7 PM)", annotation_position="top left", annotation_font_size=10, annotation_font_color="#B45309")

    _apply_humanized_theme(fig, title=f"🚦 24-Hour Diurnal Commute Curve ({zone_name})", show_legend=False)
    fig.update_xaxes(title="Hour of Day (24-hour time)", tickmode="linear", tick0=0, dtick=2)
    fig.update_yaxes(title="Congestion Index (%)", range=[0, 100])
    return fig
