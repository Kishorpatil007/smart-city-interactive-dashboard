# 🏙️ Smart City Interactive Dashboard

A high-performance, accessible, and human-centered Smart City telemetry and urban operations dashboard built using three core libraries:

- 🎨 **Streamlit** – Clean modern interface, session state, dynamic filters, and user interaction
- 🗺️ **Folium** – Interactive geospatial community map, district perimeters, clusters, and HTML popups
- 📊 **Plotly** – Accessible data charts, multi-variable time series, health thresholds, and donut visualizations

---

## 🌟 Key Features

### 1. 🏙️ City Overview & Live Telemetry
- **Key Performance Indicators (KPIs):** Real-time monitoring of:
  - 👥 **Total Population** (1.65M across city districts)
  - 🌐 **Connected Nodes** (1,280 IoT nodes active)
  - 🌿 **Air Quality Index (AQI)** with health status indicator (Good / Moderate / Unhealthy)
  - 🚦 **Traffic Mobility Index** (%) and commuter flow status
  - ⚡ **Electricity Consumption** (MWh/day) & 💧 **Water Supply Flow** (ML/day)
- **Live Civic Dispatch Bulletin:** Dynamic updates for air quality, traffic routing, and renewable microgrid efficiency.
- **Live Telemetry Refresh:** "Refresh Live Telemetry" button to simulate real-time sensor updates.

### 2. 🗺️ Interactive Community Map (Folium)
- **Geographic Exploration:** Explores 6 distinct urban districts:
  - *Downtown & Civic Center*
  - *Green Valley & Eco-Park*
  - *University & Innovation District*
  - *Harbor & Logistics Hub*
  - *Tech Corridor & Business Park*
  - *South Garden Residential*
- **Facility Markers with Rich HTML Popups:**
  - 🏥 **Hospitals / Emergency Centers:** Bed occupancy, trauma readiness, drone blood dispatch.
  - 🏫 **Schools & Universities:** Solar offset, indoor air purification index.
  - 🚦 **Traffic Nodes:** Vehicles/hour, average speed, adaptive signaling status.
  - 🗑️ **Waste & Recycling Hubs:** Pneumatic collection fill levels, biomethane yield.
  - ⚡ **Clean Energy Substations:** Solar output, battery storage state-of-charge.
  - 💧 **Water Filtration & Reservoirs:** Treatment volumes, purity index, pressure ratings.
- **Geospatial Controls:** Toggle smart zone perimeter rings, marker clustering, and switch between *CartoDB dark_matter*, *CartoDB positron*, and *OpenStreetMap* basemaps.

### 3. 📈 Data Visualizations (Plotly)
- 📊 **Electricity Consumption by Area:** Bar chart comparing districts against the municipal benchmark.
- 📈 **Air Quality Index (AQI) Over Time:** Spline line chart with colored background bands (Good, Moderate, Unhealthy for Sensitive, Unhealthy) and 24-hour moving averages.
- 🥧 **Waste Segregation & Recovery:** Donut chart breakdown (Organic, Paper, Plastic, E-Waste, Hazardous) with daily tonnage calculations.
- 📊 **Traffic Congestion by District:** Color-coded congestion indices against smooth flow and heavy congestion benchmarks.
- 📈 **Water Consumption vs Target:** Daily water flow compared to sustainability conservation targets.
- 🌡️ **Microclimate Dynamics:** Dual-axis chart tracking hourly temperature (°C) and relative humidity (%).
- 🚦 **24-Hour Diurnal Traffic Curve:** Rush-hour visualization highlighting morning and evening peak intervals.

### 4. 🎛️ Streamlit User Controls
- **District / Area Dropdown:** Seamlessly filter the entire dashboard to a specific neighborhood or view citywide aggregates.
- **Date Picker & Horizon:** Switch between *Past 24 Hours*, *Past 7 Days*, and *Past 30 Days*.
- **Category Multi-Select:** Filter visible infrastructure types on both the map and the data directory.
- **CSV Data Export:** One-click download of the active district's time-series telemetry.

---

## 📁 Project Architecture

```
PIMV MINI PROJECT/
│
├── app.py                   # Main Streamlit application and layout
├── data_manager.py          # Smart city data generator, POIs, and IoT simulator
├── map_components.py        # Folium interactive geospatial map builder
├── chart_components.py      # Plotly interactive dark-themed visualizer
├── run_dashboard.bat        # Windows 1-click batch launcher
├── requirements.txt         # Core dependencies
├── README.md                # Project documentation and demo guide
└── .streamlit/
    └── config.toml          # Dark-tech theme configuration
```

---

## 🚀 How to Run

### Option 1: One-Click Windows Batch Launcher
Double-click `run_dashboard.bat` in the project root directory.

### Option 2: Command Line
Open your terminal in `c:\PIMV MINI PROJECT` and run:

```bash
python -m streamlit run app.py
```

The application will start immediately and be accessible at:
👉 **`http://localhost:8501`**

---

## 📋 Technical & Architecture Overview

| Requirement | Project Implementation | Status |
| :--- | :--- | :---: |
| **Library 1: Streamlit** | Glassmorphic interface, session state, sidebar controls, metric cards, tabs | ✅ Full |
| **Library 2: Folium** | Geospatial map, zone circles, clustered markers, styled HTML popups, layer toggle | ✅ Full |
| **Library 3: Plotly** | 7 interactive charts (line, bar, donut, dual-axis, threshold bands) | ✅ Full |
| **User Interaction** | District selector, date & horizon controls, category filter, simulation pulse | ✅ Full |
| **Data Export** | Instant CSV telemetry export button | ✅ Full |
| **Aesthetics** | Cyber-modern dark tech theme, glowing status indicators, responsive layout | ✅ Full |
