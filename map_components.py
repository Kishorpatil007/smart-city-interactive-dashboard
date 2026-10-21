"""
Smart City Dashboard - Interactive Folium Map Builder
Creates dynamic, styled maps with district perimeters, clustered markers, and humanized HTML popups
for all 36 districts of Maharashtra.
"""

import folium
from folium import plugins
from data_manager import get_pois, get_zone_metadata, ZONES, CITY_CENTER, ALL_DISTRICTS_LABEL

CATEGORY_STYLES = {
    "Hospital": {
        "color": "red",
        "icon": "plus",
        "prefix": "fa",
        "badge_bg": "#EF4444",
        "emoji": "🏥"
    },
    "School": {
        "color": "purple",
        "icon": "graduation-cap",
        "prefix": "fa",
        "badge_bg": "#8B5CF6",
        "emoji": "🏫"
    },
    "Traffic Sensor": {
        "color": "orange",
        "icon": "car",
        "prefix": "fa",
        "badge_bg": "#F59E0B",
        "emoji": "🚦"
    },
    "Waste Point": {
        "color": "green",
        "icon": "recycle",
        "prefix": "fa",
        "badge_bg": "#10B981",
        "emoji": "♻️"
    },
    "Electricity Hub": {
        "color": "blue",
        "icon": "bolt",
        "prefix": "fa",
        "badge_bg": "#2563EB",
        "emoji": "⚡"
    },
    "Water Facility": {
        "color": "cadetblue",
        "icon": "tint",
        "prefix": "fa",
        "badge_bg": "#0284C7",
        "emoji": "💧"
    }
}

# Division-wise color mapping for Maharashtra's 36 districts
ZONE_COLORS = {
    # Konkan (Coastal Blue)
    "Mumbai City": "#0284C7", "Mumbai Suburban": "#0284C7", "Thane": "#0284C7",
    "Palghar": "#0284C7", "Raigad": "#0284C7", "Ratnagiri": "#0284C7", "Sindhudurg": "#0284C7",
    # Pune Division (Royal Blue)
    "Pune": "#2563EB", "Satara": "#2563EB", "Sangli": "#2563EB", "Solapur": "#2563EB", "Kolhapur": "#2563EB",
    # Nashik Division (Emerald Green)
    "Nashik": "#10B981", "Dhule": "#10B981", "Jalgaon": "#10B981", "Nandurbar": "#10B981", "Ahilyanagar": "#10B981",
    # Marathwada (Amber)
    "Chhatrapati Sambhajinagar": "#F59E0B", "Jalna": "#F59E0B", "Beed": "#F59E0B", "Parbhani": "#F59E0B",
    "Hingoli": "#F59E0B", "Nanded": "#F59E0B", "Latur": "#F59E0B", "Dharashiv": "#F59E0B",
    # West Vidarbha / Amravati (Purple)
    "Amravati": "#8B5CF6", "Akola": "#8B5CF6", "Yavatmal": "#8B5CF6", "Buldhana": "#8B5CF6", "Washim": "#8B5CF6",
    # East Vidarbha / Nagpur (Rose Pink)
    "Nagpur": "#EC4899", "Wardha": "#EC4899", "Chandrapur": "#EC4899", "Bhandara": "#EC4899",
    "Gondia": "#EC4899", "Gadchiroli": "#EC4899"
}

TILE_PRESETS = {
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
}

def create_smart_city_map(
    selected_zone=ALL_DISTRICTS_LABEL,
    selected_categories=None,
    map_tile="Clean Civic Light",
    show_zones=True,
    enable_clustering=True
):
    """
    Generate an interactive Folium map centered on the selected district or entire state of Maharashtra.
    """
    zone_meta = get_zone_metadata(selected_zone)
    center_lat = zone_meta["lat"]
    center_lon = zone_meta["lon"]
    zoom_start = zone_meta["zoom"]

    # Resolve tile URL and attribution (no API key required)
    if map_tile in TILE_PRESETS:
        preset = TILE_PRESETS[map_tile]
        tile_url = preset["tiles"]
        tile_attr = preset["attr"]
    elif "dark" in str(map_tile).lower():
        tile_url = TILE_PRESETS["Subtle Dark"]["tiles"]
        tile_attr = TILE_PRESETS["Subtle Dark"]["attr"]
    elif "positron" in str(map_tile).lower() or "civic" in str(map_tile).lower():
        tile_url = TILE_PRESETS["Clean Civic Light"]["tiles"]
        tile_attr = TILE_PRESETS["Clean Civic Light"]["attr"]
    elif map_tile == "OpenStreetMap":
        tile_url = "OpenStreetMap"
        tile_attr = None
    else:
        tile_url = map_tile
        tile_attr = None

    # Initialize Base Map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles=tile_url,
        attr=tile_attr,
        control_scale=True,
        prefer_canvas=True
    )

    # Add Fullscreen button
    plugins.Fullscreen(position="topright", force_separate_button=True).add_to(m)

    # Draw District Boundaries across Maharashtra
    if show_zones:
        zone_group = folium.FeatureGroup(name="Maharashtra District Rings", show=True)
        for z_name, z_data in ZONES.items():
            if z_name == ALL_DISTRICTS_LABEL:
                continue
            z_color = ZONE_COLORS.get(z_name, "#2563EB")
            is_active_zone = (selected_zone == z_name)
            
            # Scaled radius in meters for state / district view
            radius_m = 16000 if selected_zone == ALL_DISTRICTS_LABEL else (14000 if is_active_zone else 8000)

            folium.Circle(
                location=[z_data["lat"], z_data["lon"]],
                radius=radius_m,
                color=z_color,
                weight=3 if is_active_zone else 1.2,
                fill=True,
                fill_color=z_color,
                fill_opacity=0.22 if is_active_zone else 0.08,
                tooltip=f"<b>{z_name} District</b><br>Population: {z_data['population']:,}<br>AQI: {z_data['base_aqi']} | Mobility: {z_data['base_traffic']}%",
                popup=folium.Popup(
                    f"""
                    <div style="font-family: 'Inter', -apple-system, sans-serif; min-width: 220px; padding: 4px;">
                        <h4 style="margin: 0 0 6px 0; color: {z_color}; font-size: 14px;">{z_name} District</h4>
                        <p style="font-size: 12px; margin: 2px 0; color: #334155;"><b>Area:</b> {z_data['area_sqkm']} km²</p>
                        <p style="font-size: 12px; margin: 2px 0; color: #334155;"><b>Population:</b> {z_data['population']:,} residents</p>
                        <p style="font-size: 12px; margin: 2px 0; color: #334155;"><b>Telemetry Nodes:</b> {z_data['smart_nodes']}</p>
                        <p style="font-size: 12px; margin: 2px 0; color: #334155;"><b>Air Quality (AQI):</b> {z_data['base_aqi']}</p>
                        <p style="font-size: 11px; color: #64748B; margin-top: 6px; line-height: 1.4;">{z_data['description']}</p>
                    </div>
                    """,
                    max_width=280
                )
            ).add_to(zone_group)

        zone_group.add_to(m)

    # Filter POIs
    pois = get_pois(zone_name=selected_zone, categories=selected_categories)

    # Create marker container (either Cluster or FeatureGroup)
    if enable_clustering:
        marker_container = plugins.MarkerCluster(
            name="Civic Facilities & Services",
            overlay=True,
            control=True,
            options={"maxClusterRadius": 40}
        )
    else:
        marker_container = folium.FeatureGroup(name="Civic Facilities & Services", show=True)

    # Populate POI Markers
    for poi in pois:
        style = CATEGORY_STYLES.get(poi["category"], {
            "color": "blue",
            "icon": "info-sign",
            "prefix": "glyphicon",
            "badge_bg": "#2563EB",
            "emoji": "📍"
        })

        status_color = "#10B981" if poi["status"] in ["Operational", "Optimal", "Smooth"] else (
            "#EF4444" if poi["status"] in ["Congested", "High Load"] else "#F59E0B"
        )

        popup_html = f"""
        <div style="font-family: 'Inter', -apple-system, sans-serif; min-width: 230px; border-radius: 8px; color: #1E293B;">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #E2E8F0; padding-bottom: 6px; margin-bottom: 8px;">
                <span style="font-size: 16px; margin-right: 6px;">{style['emoji']}</span>
                <span style="font-size: 11px; font-weight: 600; background: {style['badge_bg']}; color: white; padding: 2px 8px; border-radius: 12px;">{poi['category']}</span>
            </div>
            <h4 style="margin: 0 0 4px 0; font-size: 13px; font-weight: 700; color: #0F172A;">{poi['name']}</h4>
            <div style="font-size: 11px; color: #64748B; margin-bottom: 8px;">📍 District: <b>{poi['zone']}</b></div>
            
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px; margin-bottom: 8px;">
                <div style="font-size: 11px; color: #475569;"><b>Service Status:</b> 
                    <span style="color: {status_color}; font-weight: 600; margin-left: 4px;">● {poi['status']}</span>
                </div>
                <div style="font-size: 11px; color: #475569; margin-top: 3px;">
                    <b>{poi['metric_label']}:</b> <span style="font-weight: 600; color: #0F172A;">{poi['metric_value']}</span>
                </div>
            </div>
            
            <p style="font-size: 11px; line-height: 1.4; color: #475569; margin: 0 0 6px 0;">{poi['info']}</p>
            <div style="font-size: 10px; color: #94A3B8; border-top: 1px dashed #CBD5E1; padding-top: 4px;">
                📞 Contact: <b>{poi['contact']}</b>
            </div>
        </div>
        """

        folium.Marker(
            location=[poi["lat"], poi["lon"]],
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=f"{style['emoji']} <b>{poi['name']}</b> ({poi['status']})",
            icon=folium.Icon(
                color=style["color"],
                icon=style["icon"],
                prefix=style["prefix"]
            )
        ).add_to(marker_container)

    marker_container.add_to(m)

    # Add Layer Control
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    return m
