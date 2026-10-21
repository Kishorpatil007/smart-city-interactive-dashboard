"""
🏙️ Smart City Interactive Dashboard
Real-Time Telemetry & Urban Operations System
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import folium
import importlib

# Local project modules with dynamic reload support for Streamlit hot-reloading
import data_manager
import map_components
import chart_components

try:
    importlib.reload(data_manager)
    importlib.reload(map_components)
    importlib.reload(chart_components)
except Exception:
    pass

from data_manager import (
    get_zones,
    get_zone_metadata,
    get_pois,
    generate_hourly_time_series,
    get_waste_composition,
    get_area_comparison_metrics,
    get_realtime_kpis,
    POI_DATA
)

create_smart_city_map = getattr(map_components, "create_smart_city_map")
CATEGORY_STYLES = getattr(map_components, "CATEGORY_STYLES")
TILE_PRESETS = getattr(map_components, "TILE_PRESETS", {
    "Clean Civic Light": {
        "tiles": "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        "attr": "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors &copy; <a href='https://carto.com/attributions'>CARTO</a>"
    },
    "OpenStreetMap": {
        "tiles": "OpenStreetMap",
        "attr": None
    },
    "Subtle Dark": {
        "tiles": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        "attr": "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors &copy; <a href='https://carto.com/attributions'>CARTO</a>"
    }
})

from chart_components import (
    plot_electricity_by_area,
    plot_aqi_over_time,
    plot_waste_categories_pie,
    plot_traffic_level_by_area,
    plot_water_consumption_trend,
    plot_temperature_and_humidity,
    plot_hourly_traffic_curve
)

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & ACCESSIBLE CIVIC STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart City Interactive Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Clean, Humanized Civic Design CSS
st.markdown("""
<style>
    /* Clean Modern Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
    }

    /* Main Container Spacing */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Clean Civic Hero Header */
    .hero-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 6px 16px -2px rgba(15, 23, 42, 0.04);
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #64748B;
        font-size: 0.95rem;
        margin: 0;
        font-weight: 400;
    }

    /* Soft Civic Status Badge */
    .status-pill {
        display: inline-flex;
        align-items: center;
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #065F46;
        margin-top: 6px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
    }

    /* Modern Light Card Surfaces */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 4px 12px -2px rgba(15, 23, 42, 0.03);
        transition: all 0.2s ease-in-out;
        position: relative;
    }

    .metric-card:hover {
        border-color: #CBD5E1;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -2px rgba(15, 23, 42, 0.08);
    }

    .metric-icon-wrap {
        font-size: 1.6rem;
        margin-bottom: 8px;
    }

    .metric-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
        line-height: 1.2;
    }

    .metric-delta {
        font-size: 0.8rem;
        margin-top: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
        font-weight: 500;
    }

    /* Friendly Civic Bulletin Alert */
    .alert-banner {
        background: #EFF6FF;
        border-left: 4px solid #2563EB;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 24px;
        font-size: 0.88rem;
        color: #1E40AF;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Clean Light Tab Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 5px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        color: #64748B;
        border: none;
        background: transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #2563EB !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT
# -----------------------------------------------------------------------------
if "simulation_count" not in st.session_state:
    st.session_state["simulation_count"] = 0

if "last_refresh_time" not in st.session_state:
    st.session_state["last_refresh_time"] = datetime.now().strftime("%H:%M:%S")

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏙️ Dashboard Controls")

    # City / District Selector
    all_zones = get_zones()
    selected_zone = st.selectbox(
        "📍 Select District (Maharashtra)",
        options=all_zones,
        index=0,
        help="Choose any of the 36 districts of Maharashtra or view statewide overview."
    )

    # Date Picker & Time Period Horizon
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        selected_date = st.date_input(
            "📅 Date",
            value=date.today(),
            help="Anchor analysis date."
        )
    with col_date2:
        time_period = st.selectbox(
            "⏱️ Horizon",
            options=["Past 24 Hours", "Past 7 Days", "Past 30 Days"],
            index=1,
            help="Time series lookback range."
        )

    # Map Horizon to Days
    days_map = {"Past 24 Hours": 1, "Past 7 Days": 7, "Past 30 Days": 30}
    selected_days = days_map[time_period]

    # Data Category Filter
    st.markdown("---")
    st.markdown("#### 🗂️ Public Infrastructure Filters")
    available_categories = list(CATEGORY_STYLES.keys())
    selected_categories = st.multiselect(
        "Select Facility Types",
        options=available_categories,
        default=available_categories,
        help="Filter visible facilities on the interactive map and community directory."
    )

    # Map Appearance Customization
    st.markdown("---")
    st.markdown("#### 🗺️ Map Settings")
    map_tile_choice = st.selectbox(
        "Basemap Theme",
        options=list(TILE_PRESETS.keys()),
        index=0,
        help="Choose basemap style. Clean Civic Light and OpenStreetMap are free and do not require any API keys."
    )
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        show_zone_boundaries = st.checkbox("Show District Rings", value=True)
    with col_m2:
        enable_clustering = st.checkbox("Cluster Facilities", value=True)

    # Live Telemetry Refresh
    st.markdown("---")
    st.markdown("#### ⚡ Real-Time City Telemetry")
    if st.button("🔄 Refresh Live Telemetry", use_container_width=True):
        st.session_state["simulation_count"] += 1
        st.session_state["last_refresh_time"] = datetime.now().strftime("%H:%M:%S")
        st.toast("🌿 City sensor telemetry refreshed!", icon="🏙️")

    st.caption(f"Last Sensor Sync: **{st.session_state['last_refresh_time']}**")

    # Export Data Report Button
    st.markdown("---")
    export_df = generate_hourly_time_series(selected_zone, days=selected_days, seed=st.session_state["simulation_count"])
    csv_bytes = export_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Telemetry Report (CSV)",
        data=csv_bytes,
        file_name=f"smart_city_{selected_zone.lower().replace(' ', '_').replace('(', '').replace(')', '')}_{selected_days}d.csv",
        mime="text/csv",
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# 4. LOAD & PREPARE DATA
# -----------------------------------------------------------------------------
zone_meta = get_zone_metadata(selected_zone)
kpis = get_realtime_kpis(selected_zone, simulation_offset=st.session_state["simulation_count"])
hourly_df = generate_hourly_time_series(selected_zone, days=selected_days, seed=st.session_state["simulation_count"])
waste_df = get_waste_composition(selected_zone)
area_metrics_df = get_area_comparison_metrics()
filtered_pois = get_pois(zone_name=selected_zone, categories=selected_categories)

# -----------------------------------------------------------------------------
# 5. DASHBOARD MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="hero-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
        <div>
            <h1 class="hero-title">🏙️ Smart City Interactive Dashboard</h1>
            <p class="hero-subtitle">
                Civic Operations, Community Well-Being & Urban Sustainability • District: <b style="color:#2563EB;">{selected_zone}</b> • Date: <b style="color:#334155;">{selected_date}</b>
            </p>
        </div>
        <div>
            <div class="status-pill">
                <span class="status-dot"></span> City Services Active & Connected
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Live Civic Dispatch Banner
alerts = kpis["active_alerts"]
latest_alert = alerts[st.session_state["simulation_count"] % len(alerts)]["text"]
st.markdown(f"""
<div class="alert-banner">
    <span style="font-size: 1.25rem;">📢</span>
    <div><b>Civic Bulletin:</b> {latest_alert}</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. FEATURE 1: CITY OVERVIEW (KPI CARDS)
# -----------------------------------------------------------------------------
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap">👥</div>
        <div class="metric-label">Total Population</div>
        <div class="metric-value">{kpis['population'] / 1e6:.2f}M</div>
        <div class="metric-delta" style="color: #059669;">
            <span>↑ +1.2%</span> <span style="color: #64748B;">residents</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    num_districts = len(all_zones) - 1
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap">🌐</div>
        <div class="metric-label">Connected Nodes</div>
        <div class="metric-value">{kpis['smart_nodes']:,}</div>
        <div class="metric-delta" style="color: #2563EB;">
            <span>● {num_districts} Districts</span> <span style="color: #64748B;">All Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap">🌿</div>
        <div class="metric-label">Air Quality Index</div>
        <div class="metric-value" style="color: {kpis['aqi_color']};">{kpis['aqi']}</div>
        <div class="metric-delta" style="color: {kpis['aqi_color']};">
            <span>● {kpis['aqi_status']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap">🚦</div>
        <div class="metric-label">Traffic Mobility Index</div>
        <div class="metric-value" style="color: {kpis['traffic_color']};">{kpis['traffic_index']}%</div>
        <div class="metric-delta" style="color: {kpis['traffic_color']};">
            <span>● {kpis['traffic_status']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap">⚡ | 💧</div>
        <div class="metric-label">Power & Water / Day</div>
        <div class="metric-value">{kpis['power_mwh']:,.0f} <span style="font-size: 0.85rem; color: #64748B; font-weight: 500;">MWh</span></div>
        <div class="metric-delta" style="color: #0284C7;">
            <span>💧 {kpis['water_ml']:,.0f} ML</span> <span style="color: #64748B;">daily supply</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. TABBED NAVIGATION FOR COMPREHENSIVE EXPLORATION
# -----------------------------------------------------------------------------
tab_charts, tab_map, tab_sectors, tab_data = st.tabs([
    "📊 City Data Analysis (Plotly)",
    "🗺️ Interactive City Map (Folium)",
    "🚦 Mobility | 💧 Water | ♻️ Recycling Deep Dive",
    "📋 Infrastructure Directory & Telemetry"
])

# -----------------------------------------------------------------------------
# TAB 1: DATA VISUALIZATION - PLOTLY
# -----------------------------------------------------------------------------
with tab_charts:
    st.markdown("#### 📈 Dynamic Data Visualizations")
    st.caption("Interactive Plotly charts reacting seamlessly to district selection and time horizon.")

    # Row 1 of Charts: AQI Over Time & Electricity Consumption by Area
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        fig_aqi = plot_aqi_over_time(hourly_df, selected_zone)
        st.plotly_chart(fig_aqi, use_container_width=True)

    with row1_c2:
        fig_power = plot_electricity_by_area(area_metrics_df, selected_zone)
        st.plotly_chart(fig_power, use_container_width=True)

    st.markdown("---")

    # Row 2 of Charts: Waste Composition Donut & District Traffic Comparison
    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        fig_waste = plot_waste_categories_pie(waste_df, selected_zone)
        st.plotly_chart(fig_waste, use_container_width=True)

    with row2_c2:
        fig_traffic = plot_traffic_level_by_area(area_metrics_df, selected_zone)
        st.plotly_chart(fig_traffic, use_container_width=True)

    st.markdown("---")

    # Row 3 of Charts: Water Consumption Trends & Microclimate
    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        fig_water = plot_water_consumption_trend(hourly_df, selected_zone)
        st.plotly_chart(fig_water, use_container_width=True)

    with row3_c2:
        fig_climate = plot_temperature_and_humidity(hourly_df, selected_zone)
        st.plotly_chart(fig_climate, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: INTERACTIVE MAP - FOLIUM
# -----------------------------------------------------------------------------
with tab_map:
    st.markdown("#### 🗺️ Geospatial Community & Facilities Map (Folium)")
    st.caption("Explore city services, public healthcare, schools, transit corridors, and green utilities.")

    # Render Map Quick Stats Bar
    col_m_stat1, col_m_stat2, col_m_stat3, col_m_stat4 = st.columns(4)
    with col_m_stat1:
        st.info(f"📍 **Focus:** {selected_zone}")
    with col_m_stat2:
        st.info(f"🏥 **Facilities Displayed:** {len(filtered_pois)} Services")
    with col_m_stat3:
        st.info(f"📐 **Area Coverage:** {zone_meta['area_sqkm']} km²")
    with col_m_stat4:
        st.info(f"👥 **District Population:** {zone_meta['population']:,}")

    # Build Folium Map
    folium_map = create_smart_city_map(
        selected_zone=selected_zone,
        selected_categories=selected_categories,
        map_tile=map_tile_choice,
        show_zones=show_zone_boundaries,
        enable_clustering=enable_clustering
    )

    # Render Folium Map in Streamlit with Fallback
    try:
        from streamlit_folium import st_folium
        st_folium(folium_map, width="100%", height=520, returned_objects=[])
    except Exception as e:
        import streamlit.components.v1 as components
        components.html(folium_map._repr_html_(), height=520)

    # Map Legend & Category Key
    st.markdown("##### 📌 Facility Legend")
    legend_cols = st.columns(len(CATEGORY_STYLES))
    for idx, (cat_name, style) in enumerate(CATEGORY_STYLES.items()):
        with legend_cols[idx]:
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 3px solid {style['badge_bg']}; padding: 6px 10px; border-radius: 6px; font-size: 0.8rem; color: #334155;">
                <b>{style['emoji']} {cat_name}</b>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: MOBILITY | WATER | WASTE DEEP DIVE
# -----------------------------------------------------------------------------
with tab_sectors:
    st.markdown("#### 🚦 Commute Patterns | 💧 Water Sustainability | ♻️ Resource Recovery")
    st.caption("Urban management insights, community conservation, and diurnal curves.")

    col_sec1, col_sec2 = st.columns(2)
    with col_sec1:
        fig_rush = plot_hourly_traffic_curve(hourly_df, selected_zone)
        st.plotly_chart(fig_rush, use_container_width=True)

    with col_sec2:
        st.markdown("##### 💧 Fresh Water Reservoir & Storage Capacity")
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; color: #0F172A;">Municipal Main Reservoir Level</span>
                <span style="font-weight: 700; color: #059669; font-size: 1.05rem;">88.4% Capacity (Secure)</span>
            </div>
            <div style="background: #F1F5F9; height: 10px; border-radius: 6px; overflow: hidden; margin: 10px 0;">
                <div style="background: #0284C7; width: 88.4%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.82rem; color: #64748B; display: flex; justify-content: space-between;">
                <span>Total Safe Volume: 430 ML</span>
                <span>Current Supply Flow: 18.2 ML/hr</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### ♻️ Community Recycling & Clean Diversion")
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; color: #0F172A;">Landfill Diversion & Recovery Rate</span>
                <span style="font-weight: 700; color: #059669; font-size: 1.05rem;">87.6% Diverted</span>
            </div>
            <div style="background: #F1F5F9; height: 10px; border-radius: 6px; overflow: hidden; margin: 10px 0;">
                <div style="background: #10B981; width: 87.6%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.82rem; color: #64748B; display: flex; justify-content: space-between;">
                <span>Active Neighborhood Bins: Normal Fill (52%)</span>
                <span>Compost Generated: 14.8 T/day</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        stat_c1, stat_c2 = st.columns(2)
        with stat_c1:
            st.metric("Daily Waste Generated", f"{kpis['waste_daily_tons']:,.0f} Tons", delta="-3.5% vs benchmark", delta_color="inverse")
        with stat_c2:
            st.metric("Average Commute Speed", "39.2 km/h", delta="+3.8 km/h (Smooth)")

# -----------------------------------------------------------------------------
# TAB 4: INFRASTRUCTURE DIRECTORY & TELEMETRY
# -----------------------------------------------------------------------------
with tab_data:
    st.markdown("#### 📋 Civic Infrastructure & Community Services Directory")
    st.caption("Complete directory of hospitals, schools, transit corridors, and green utilities.")

    poi_table_data = []
    for p in filtered_pois:
        poi_table_data.append({
            "Facility ID": p["id"],
            "Facility Name": p["name"],
            "Category": p["category"],
            "District": p["zone"],
            "Service Status": p["status"],
            "Primary Metric": f"{p['metric_label']}: {p['metric_value']}",
            "Contact Helpline": p["contact"],
            "Coordinates": f"({p['lat']:.4f}, {p['lon']:.4f})"
        })

    poi_df = pd.DataFrame(poi_table_data)
    st.dataframe(
        poi_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Service Status": st.column_config.TextColumn(
                "Status",
                help="Current service readiness",
                width="small"
            )
        }
    )

    st.markdown("##### 📈 Recent Telemetry Sample (Hourly Urban Metrics)")
    st.dataframe(
        hourly_df.tail(10)[["timestamp", "temperature_c", "humidity_pct", "aqi", "traffic_index", "electricity_mwh", "water_ml"]].rename(
            columns={
                "timestamp": "Timestamp",
                "temperature_c": "Temp (°C)",
                "humidity_pct": "Humidity (%)",
                "aqi": "AQI",
                "traffic_index": "Mobility (%)",
                "electricity_mwh": "Power (MWh)",
                "water_ml": "Water (ML)"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

# -----------------------------------------------------------------------------
# 8. DASHBOARD FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
col_foot1, col_foot2 = st.columns([3, 1])
with col_foot1:
    st.caption("🏙️ **Smart City Interactive Dashboard** • Real-time civic telemetry powered by **Streamlit**, **Folium**, and **Plotly**.")
with col_foot2:
    st.caption(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
