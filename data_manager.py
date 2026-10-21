"""
Smart City & District Dashboard - Data Management & Simulation Module
Provides authentic, comprehensive telemetry for all 36 districts of Maharashtra.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

ALL_DISTRICTS_LABEL = "All Districts (Maharashtra Overview)"

# Geographic Center of Maharashtra
CITY_CENTER = {"lat": 19.6633, "lon": 75.3003, "name": "Maharashtra State Center"}

# Complete Official 36 Districts of Maharashtra with realistic demographics and metrics
ZONES = {
    ALL_DISTRICTS_LABEL: {
        "lat": 19.6633,
        "lon": 75.3003,
        "zoom": 7,
        "population": 126000000,
        "area_sqkm": 307713,
        "smart_nodes": 4850,
        "base_aqi": 62,
        "base_traffic": 54,
        "base_power_mwh": 34500,
        "base_water_ml": 18500,
        "description": "Comprehensive statewide telemetry covering all 36 administrative districts across Maharashtra."
    },
    # Konkan Division
    "Mumbai City": {
        "lat": 18.9388, "lon": 72.8354, "zoom": 12,
        "population": 3145000, "area_sqkm": 157, "smart_nodes": 420,
        "base_aqi": 82, "base_traffic": 78, "base_power_mwh": 2850, "base_water_ml": 980,
        "description": "Financial capital of India, historic island city, heritage business district, and maritime gateway."
    },
    "Mumbai Suburban": {
        "lat": 19.1136, "lon": 72.8697, "zoom": 12,
        "population": 9356000, "area_sqkm": 446, "smart_nodes": 580,
        "base_aqi": 94, "base_traffic": 84, "base_power_mwh": 4600, "base_water_ml": 1850,
        "description": "High-density residential and commercial zone encompassing Bandra, Andheri, BKC, and Sanjay Gandhi National Park."
    },
    "Thane": {
        "lat": 19.2183, "lon": 72.9781, "zoom": 12,
        "population": 8100000, "area_sqkm": 4214, "smart_nodes": 360,
        "base_aqi": 78, "base_traffic": 72, "base_power_mwh": 2900, "base_water_ml": 820,
        "description": "Major industrial manufacturing hub, metropolitan urban extension, and lake city."
    },
    "Palghar": {
        "lat": 19.6967, "lon": 72.7699, "zoom": 11,
        "population": 3000000, "area_sqkm": 5344, "smart_nodes": 180,
        "base_aqi": 52, "base_traffic": 44, "base_power_mwh": 1200, "base_water_ml": 280,
        "description": "Coastal and tribal district housing Tarapur Atomic Power Station and industrial clusters."
    },
    "Raigad": {
        "lat": 18.6414, "lon": 72.8722, "zoom": 11,
        "population": 2630000, "area_sqkm": 7152, "smart_nodes": 210,
        "base_aqi": 58, "base_traffic": 56, "base_power_mwh": 1450, "base_water_ml": 310,
        "description": "Maritime industrial belt featuring JNPT container port, Navi Mumbai expansion, and Konkan coastlines."
    },
    "Ratnagiri": {
        "lat": 16.9902, "lon": 73.3120, "zoom": 11,
        "population": 1615000, "area_sqkm": 8208, "smart_nodes": 140,
        "base_aqi": 34, "base_traffic": 32, "base_power_mwh": 650, "base_water_ml": 180,
        "description": "Coastal Konkan heartland known for Alphonso mango orchards, fisheries, and ports."
    },
    "Sindhudurg": {
        "lat": 16.1158, "lon": 73.6934, "zoom": 11,
        "population": 850000, "area_sqkm": 5207, "smart_nodes": 110,
        "base_aqi": 28, "base_traffic": 25, "base_power_mwh": 380, "base_water_ml": 120,
        "description": "Eco-tourism haven with pristine beaches, Western Ghats forests, and historic sea forts."
    },

    # Pune Division (Western Maharashtra)
    "Pune": {
        "lat": 18.5204, "lon": 73.8567, "zoom": 12,
        "population": 9420000, "area_sqkm": 15643, "smart_nodes": 520,
        "base_aqi": 76, "base_traffic": 78, "base_power_mwh": 4100, "base_water_ml": 1250,
        "description": "Oxford of the East, leading IT and automotive manufacturing powerhouse."
    },
    "Satara": {
        "lat": 17.6805, "lon": 74.0183, "zoom": 11,
        "population": 3000000, "area_sqkm": 10480, "smart_nodes": 160,
        "base_aqi": 38, "base_traffic": 40, "base_power_mwh": 880, "base_water_ml": 290,
        "description": "Historic Maratha capital, home to Kaas UNESCO plateau, Koyna hydroelectric complex, and sugarcane cooperatives."
    },
    "Sangli": {
        "lat": 16.8524, "lon": 74.5815, "zoom": 11,
        "population": 2820000, "area_sqkm": 8572, "smart_nodes": 150,
        "base_aqi": 42, "base_traffic": 45, "base_power_mwh": 920, "base_water_ml": 310,
        "description": "Turmeric city of India, major grape & sugar export belt along the Krishna river basin."
    },
    "Solapur": {
        "lat": 17.6599, "lon": 75.9064, "zoom": 11,
        "population": 4320000, "area_sqkm": 14895, "smart_nodes": 190,
        "base_aqi": 56, "base_traffic": 52, "base_power_mwh": 1350, "base_water_ml": 420,
        "description": "Textile and chadder capital, crucial transport interchange between Maharashtra and Karnataka."
    },
    "Kolhapur": {
        "lat": 16.7050, "lon": 74.2433, "zoom": 11,
        "population": 3880000, "area_sqkm": 7685, "smart_nodes": 190,
        "base_aqi": 46, "base_traffic": 54, "base_power_mwh": 1250, "base_water_ml": 380,
        "description": "Agricultural, foundry, sugar processing, and historic temple center situated on the Panchganga river."
    },

    # Nashik Division (Northern Maharashtra)
    "Nashik": {
        "lat": 19.9975, "lon": 73.7898, "zoom": 11,
        "population": 6100000, "area_sqkm": 15530, "smart_nodes": 290,
        "base_aqi": 54, "base_traffic": 58, "base_power_mwh": 2100, "base_water_ml": 580,
        "description": "Wine capital of India, pilgrimage hub on the Godavari, and defense aeronautics (HAL) center."
    },
    "Dhule": {
        "lat": 20.9042, "lon": 74.7749, "zoom": 11,
        "population": 2050000, "area_sqkm": 8063, "smart_nodes": 130,
        "base_aqi": 48, "base_traffic": 42, "base_power_mwh": 740, "base_water_ml": 210,
        "description": "Key textile center and highway crossroad junction of NH-3, NH-6, and NH-211."
    },
    "Jalgaon": {
        "lat": 21.0077, "lon": 75.5626, "zoom": 11,
        "population": 4230000, "area_sqkm": 11765, "smart_nodes": 180,
        "base_aqi": 58, "base_traffic": 48, "base_power_mwh": 1220, "base_water_ml": 360,
        "description": "Banana and gold capital, micro-irrigation hub (Jain Irrigation), and pulse production belt."
    },
    "Nandurbar": {
        "lat": 21.3739, "lon": 74.2403, "zoom": 11,
        "population": 1650000, "area_sqkm": 5035, "smart_nodes": 100,
        "base_aqi": 36, "base_traffic": 30, "base_power_mwh": 480, "base_water_ml": 160,
        "description": "Northern tribal district renowned for wind energy farms in the Satpura mountain ranges."
    },
    "Ahilyanagar": {
        "lat": 19.0952, "lon": 74.7496, "zoom": 11,
        "population": 4540000, "area_sqkm": 17048, "smart_nodes": 210,
        "base_aqi": 52, "base_traffic": 50, "base_power_mwh": 1400, "base_water_ml": 410,
        "description": "Largest district by land area, pioneer in the Indian cooperative sugar movement and Shirdi pilgrimage corridor."
    },

    # Chhatrapati Sambhajinagar Division (Marathwada)
    "Chhatrapati Sambhajinagar": {
        "lat": 19.8762, "lon": 75.3433, "zoom": 11,
        "population": 3700000, "area_sqkm": 10107, "smart_nodes": 260,
        "base_aqi": 66, "base_traffic": 60, "base_power_mwh": 1650, "base_water_ml": 480,
        "description": "Industrial and tourism center with DMIC AURIC Smart City, auto/pharma clusters, and Ajanta-Ellora caves."
    },
    "Jalna": {
        "lat": 19.8410, "lon": 75.8864, "zoom": 11,
        "population": 1960000, "area_sqkm": 7718, "smart_nodes": 130,
        "base_aqi": 58, "base_traffic": 44, "base_power_mwh": 890, "base_water_ml": 190,
        "description": "Steel re-rolling capital, hybrid seed production hub, and sweet lime trade center."
    },
    "Beed": {
        "lat": 18.9891, "lon": 75.7601, "zoom": 11,
        "population": 2585000, "area_sqkm": 10693, "smart_nodes": 140,
        "base_aqi": 46, "base_traffic": 38, "base_power_mwh": 810, "base_water_ml": 220,
        "description": "Central Marathwada district with major wind energy installations, Bindusara river, and Parli power station."
    },
    "Parbhani": {
        "lat": 19.2686, "lon": 76.7708, "zoom": 11,
        "population": 1836000, "area_sqkm": 6511, "smart_nodes": 120,
        "base_aqi": 44, "base_traffic": 36, "base_power_mwh": 620, "base_water_ml": 180,
        "description": "Agricultural university center (VNMKV) specializing in cotton, pulses, and Godavari irrigation."
    },
    "Hingoli": {
        "lat": 19.7196, "lon": 77.1477, "zoom": 11,
        "population": 1177000, "area_sqkm": 4526, "smart_nodes": 95,
        "base_aqi": 32, "base_traffic": 28, "base_power_mwh": 390, "base_water_ml": 130,
        "description": "Turmeric hub and site of India's upcoming LIGO gravitational-wave observatory in Aundha Nagnath."
    },
    "Nanded": {
        "lat": 19.1383, "lon": 77.3210, "zoom": 11,
        "population": 3360000, "area_sqkm": 10528, "smart_nodes": 170,
        "base_aqi": 50, "base_traffic": 46, "base_power_mwh": 1020, "base_water_ml": 310,
        "description": "Pilgrimage destination (Hazur Sahib), Godavari river corridor, and regional educational center."
    },
    "Latur": {
        "lat": 18.4088, "lon": 76.5604, "zoom": 11,
        "population": 2455000, "area_sqkm": 7157, "smart_nodes": 150,
        "base_aqi": 48, "base_traffic": 44, "base_power_mwh": 860, "base_water_ml": 240,
        "description": "Major soybean and pulse market in South Marathwada, Marathwada Rail Coach Factory hub."
    },
    "Dharashiv": {
        "lat": 18.1856, "lon": 76.0419, "zoom": 11,
        "population": 1660000, "area_sqkm": 7569, "smart_nodes": 115,
        "base_aqi": 38, "base_traffic": 34, "base_power_mwh": 540, "base_water_ml": 170,
        "description": "Historic hill district with Tuljabhavani temple, wind turbine farms, and solar parks."
    },

    # Amravati Division (West Vidarbha)
    "Amravati": {
        "lat": 20.9374, "lon": 77.7796, "zoom": 11,
        "population": 2890000, "area_sqkm": 12210, "smart_nodes": 180,
        "base_aqi": 48, "base_traffic": 48, "base_power_mwh": 960, "base_water_ml": 290,
        "description": "Cultural center of Vidarbha, Melghat Tiger Reserve sanctuary, and textile growth park."
    },
    "Akola": {
        "lat": 20.7002, "lon": 77.0082, "zoom": 11,
        "population": 1814000, "area_sqkm": 5429, "smart_nodes": 140,
        "base_aqi": 54, "base_traffic": 46, "base_power_mwh": 780, "base_water_ml": 210,
        "description": "Cotton City of Vidarbha, oil mills center, and Dr. PDKV Agricultural University campus."
    },
    "Yavatmal": {
        "lat": 20.3888, "lon": 78.1204, "zoom": 11,
        "population": 2772000, "area_sqkm": 13582, "smart_nodes": 140,
        "base_aqi": 40, "base_traffic": 36, "base_power_mwh": 760, "base_water_ml": 240,
        "description": "Cotton and teakwood forest belt with extensive wildlife reserves along the Wardha river."
    },
    "Buldhana": {
        "lat": 20.5292, "lon": 76.1843, "zoom": 11,
        "population": 2586000, "area_sqkm": 9661, "smart_nodes": 135,
        "base_aqi": 42, "base_traffic": 36, "base_power_mwh": 720, "base_water_ml": 230,
        "description": "Site of the unique Lonar meteorite crater lake and Shegaon pilgrimage center."
    },
    "Washim": {
        "lat": 20.1110, "lon": 77.1332, "zoom": 11,
        "population": 1200000, "area_sqkm": 5155, "smart_nodes": 95,
        "base_aqi": 34, "base_traffic": 30, "base_power_mwh": 390, "base_water_ml": 130,
        "description": "Centuries-old historical center with Balaji shrine and fertile soybean-cotton cultivation."
    },

    # Nagpur Division (East Vidarbha)
    "Nagpur": {
        "lat": 21.1458, "lon": 79.0882, "zoom": 11,
        "population": 4650000, "area_sqkm": 9892, "smart_nodes": 340,
        "base_aqi": 68, "base_traffic": 66, "base_power_mwh": 2400, "base_water_ml": 680,
        "description": "Winter capital of Maharashtra, Orange City, geographic zero milestone of India, and MIHAN cargo hub."
    },
    "Wardha": {
        "lat": 20.7453, "lon": 78.6022, "zoom": 11,
        "population": 1300000, "area_sqkm": 6309, "smart_nodes": 110,
        "base_aqi": 38, "base_traffic": 32, "base_power_mwh": 510, "base_water_ml": 150,
        "description": "Gandhian heritage center (Sevagram Ashram) and national cotton trading node."
    },
    "Chandrapur": {
        "lat": 19.9615, "lon": 79.2961, "zoom": 11,
        "population": 2200000, "area_sqkm": 11443, "smart_nodes": 160,
        "base_aqi": 84, "base_traffic": 52, "base_power_mwh": 1600, "base_water_ml": 310,
        "description": "Black Gold City known for coal mining, major thermal power generation, and Tadoba National Park."
    },
    "Bhandara": {
        "lat": 21.1714, "lon": 79.6548, "zoom": 11,
        "population": 1200000, "area_sqkm": 3895, "smart_nodes": 105,
        "base_aqi": 36, "base_traffic": 30, "base_power_mwh": 420, "base_water_ml": 140,
        "description": "Brass City of Maharashtra with extensive lake networks and paddy rice cultivation along Wainganga."
    },
    "Gondia": {
        "lat": 21.4624, "lon": 80.1961, "zoom": 11,
        "population": 1322000, "area_sqkm": 5431, "smart_nodes": 105,
        "base_aqi": 32, "base_traffic": 28, "base_power_mwh": 430, "base_water_ml": 140,
        "description": "Rice City with rich bamboo and tendu leaf forests bordering Madhya Pradesh and Chhattisgarh."
    },
    "Gadchiroli": {
        "lat": 20.1809, "lon": 80.0018, "zoom": 11,
        "population": 1073000, "area_sqkm": 14412, "smart_nodes": 95,
        "base_aqi": 26, "base_traffic": 22, "base_power_mwh": 360, "base_water_ml": 130,
        "description": "Forest-dense eastern border district along Pranhita and Godavari rivers, rich in mineral and eco resources."
    }
}

# Landmark Points of Interest (POIs) across major Maharashtra districts
POI_DATA = [
    # Hospitals & Tertiary Healthcare
    {
        "id": "HOSP-MUM",
        "name": "KEM Hospital & Seth GS Medical College",
        "category": "Hospital",
        "zone": "Mumbai City",
        "lat": 19.0022, "lon": 72.8431,
        "status": "Operational",
        "metric_label": "ICU Bed Capacity",
        "metric_value": "92% (High Readiness)",
        "contact": "Emergency: 022-24107000",
        "info": "Premier public tertiary referral teaching hospital serving over 1.8 million patients annually."
    },
    {
        "id": "HOSP-PUN",
        "name": "Sassoon General Hospital & BJ Medical College",
        "category": "Hospital",
        "zone": "Pune",
        "lat": 18.5283, "lon": 73.8741,
        "status": "Operational",
        "metric_label": "Emergency Beds",
        "metric_value": "94% Available",
        "contact": "Emergency: 020-26128000",
        "info": "Historic multi-specialty government hospital with regional trauma response and neonatal ICU."
    },
    {
        "id": "HOSP-NAG",
        "name": "Government Medical College & Hospital (GMCH)",
        "category": "Hospital",
        "zone": "Nagpur",
        "lat": 21.1345, "lon": 79.0963,
        "status": "Operational",
        "metric_label": "Trauma Readiness",
        "metric_value": "100% Prepared",
        "contact": "Emergency: 0712-2744671",
        "info": "Largest public hospital in Central India catering to Maharashtra, MP, and Chhattisgarh patients."
    },
    {
        "id": "HOSP-KOL",
        "name": "Chhatrapati Pramila Tai Raje (CPR) Civil Hospital",
        "category": "Hospital",
        "zone": "Kolhapur",
        "lat": 16.6980, "lon": 74.2310,
        "status": "Operational",
        "metric_label": "Bed Capacity",
        "metric_value": "89% (Optimal)",
        "contact": "Desk: 0231-2641011",
        "info": "Premier government hospital catering to southern Maharashtra and northern Karnataka."
    },
    {
        "id": "HOSP-NAS",
        "name": "Nashik District Civil & Super-Specialty Hospital",
        "category": "Hospital",
        "zone": "Nashik",
        "lat": 20.0012, "lon": 73.7845,
        "status": "Operational",
        "metric_label": "Emergency Response",
        "metric_value": "7 mins Average",
        "contact": "Desk: 0253-2573111",
        "info": "District headquarters hospital with 24/7 cardiac catheterization and telemedicine dispatch."
    },
    {
        "id": "HOSP-CSN",
        "name": "Government Medical College & Hospital (Ghati)",
        "category": "Hospital",
        "zone": "Chhatrapati Sambhajinagar",
        "lat": 19.8860, "lon": 75.3210,
        "status": "Operational",
        "metric_label": "ICU Bed Capacity",
        "metric_value": "88% Ready",
        "contact": "Desk: 0240-2402412",
        "info": "Marathwada regional tertiary healthcare center with burn care and trauma specialization."
    },

    # Universities & Higher Education
    {
        "id": "EDU-MUM",
        "name": "University of Mumbai (Vidyanagari Kalina Campus)",
        "category": "School",
        "zone": "Mumbai Suburban",
        "lat": 19.0760, "lon": 72.8680,
        "status": "Operational",
        "metric_label": "Campus Solar Offset",
        "metric_value": "82% Clean Power",
        "contact": "Admin: 022-26543000",
        "info": "Sprawling 240-acre research campus featuring Jawaharlal Nehru Library and nanoscience center."
    },
    {
        "id": "EDU-PUN",
        "name": "Savitribai Phule Pune University (SPPU)",
        "category": "School",
        "zone": "Pune",
        "lat": 18.5529, "lon": 73.8260,
        "status": "Operational",
        "metric_label": "Campus Green Cover",
        "metric_value": "411 Acres (Optimal)",
        "contact": "Admin: 020-25690062",
        "info": "Premier multi-disciplinary university leading botanical and urban atmospheric research."
    },
    {
        "id": "EDU-NAG",
        "name": "RTM Nagpur University Campus",
        "category": "School",
        "zone": "Nagpur",
        "lat": 21.1490, "lon": 79.0620,
        "status": "Operational",
        "metric_label": "IoT Sensor Lab",
        "metric_value": "Active (32 Nodes)",
        "contact": "Admin: 0712-2525471",
        "info": "Centennial university driving Central India agricultural and environmental IoT studies."
    },
    {
        "id": "EDU-KOL",
        "name": "Shivaji University Smart Campus",
        "category": "School",
        "zone": "Kolhapur",
        "lat": 16.6780, "lon": 74.2540,
        "status": "Operational",
        "metric_label": "Solar Energy Yield",
        "metric_value": "4.2 MW Peak",
        "contact": "Admin: 0231-2609000",
        "info": "Green-certified university campus with lake ecosystem conservation and robotics incubation."
    },

    # Traffic Sensors & Arterial Expressways
    {
        "id": "TRF-MUM",
        "name": "Bandra-Worli Sea Link & Coastal Road Node",
        "category": "Traffic Sensor",
        "zone": "Mumbai City",
        "lat": 19.0250, "lon": 72.8180,
        "status": "Moderate",
        "metric_label": "Flow Rate",
        "metric_value": "4,820 Veh/hr (Speed 62 km/h)",
        "contact": "Traffic Police: 103",
        "info": "High-capacity freeway monitoring system with automated tidal flow and incident cameras."
    },
    {
        "id": "TRF-PUN",
        "name": "Yashwantrao Chavan Expressway (Urse Toll Node)",
        "category": "Traffic Sensor",
        "zone": "Pune",
        "lat": 18.7240, "lon": 73.6810,
        "status": "Smooth",
        "metric_label": "Expressway Flow",
        "metric_value": "3,650 Veh/hr (Speed 84 km/h)",
        "contact": "Highway Police Control",
        "info": "India's pioneer 6-lane access-controlled concrete expressway with weigh-in-motion."
    },
    {
        "id": "TRF-NAG",
        "name": "Hindu Hrudaysamrat Balasaheb Thackeray Samruddhi Mahamarg Node",
        "category": "Traffic Sensor",
        "zone": "Nagpur",
        "lat": 21.0850, "lon": 79.0120,
        "status": "Smooth",
        "metric_label": "Interchange Flow",
        "metric_value": "2,400 Veh/hr (Speed 105 km/h)",
        "contact": "MSRDC Highway Ops",
        "info": "701 km Super Communication Expressway terminal node connecting Nagpur directly with Mumbai."
    },
    {
        "id": "TRF-NAS",
        "name": "Nashik Dwarka Circle Multi-Highway Junction",
        "category": "Traffic Sensor",
        "zone": "Nashik",
        "lat": 19.9880, "lon": 73.8010,
        "status": "Moderate",
        "metric_label": "Intersection Volume",
        "metric_value": "3,100 Veh/hr (Speed 34 km/h)",
        "contact": "City Traffic Branch",
        "info": "Major arterial rotary connecting Mumbai-Agra NH-3 with Pune-Nashik highway."
    },

    # Waste Management & Resource Recovery
    {
        "id": "WST-MUM",
        "name": "Kanjurmarg Integrated Waste Management Facility",
        "category": "Waste Point",
        "zone": "Mumbai Suburban",
        "lat": 19.1350, "lon": 72.9380,
        "status": "Operational",
        "metric_label": "Bioreactor Processing",
        "metric_value": "3,200 Tons/day Clean Processed",
        "contact": "MCGM Solid Waste Management",
        "info": "Modern scientific sanitary landfill with automated leachate treatment and methane capture."
    },
    {
        "id": "WST-PUN",
        "name": "Uruli Devachi Bio-CNG & Resource Recovery Plant",
        "category": "Waste Point",
        "zone": "Pune",
        "lat": 18.4720, "lon": 73.9850,
        "status": "Operational",
        "metric_label": "Bio-CNG Generation",
        "metric_value": "4,500 kg/day Clean Fuel",
        "contact": "PMC Waste Department",
        "info": "Converts municipal vegetable and organic refuse into compressed biogas for Pune PMPML buses."
    },
    {
        "id": "WST-NAG",
        "name": "Bhandewadi Waste-to-Energy Processing Plant",
        "category": "Waste Point",
        "zone": "Nagpur",
        "lat": 21.1390, "lon": 79.1620,
        "status": "Operational",
        "metric_label": "Energy Recovery",
        "metric_value": "11.5 MW Electricity Yield",
        "contact": "NMC Sanitation Bureau",
        "info": "Refuse-derived fuel (RDF) thermal processing plant diverting 800 tons/day from dumping grounds."
    },

    # Clean Power & Major Substations
    {
        "id": "PWR-SAT",
        "name": "Koyna Hydroelectric Power Complex Stage IV",
        "category": "Electricity Hub",
        "zone": "Satara",
        "lat": 17.4020, "lon": 73.7540,
        "status": "Optimal",
        "metric_label": "Hydro Generation",
        "metric_value": "1,960 MW (Peak Reserve)",
        "contact": "MahaGenco Dispatch",
        "info": "Largest completed hydroelectric plant in India with underground powerhouse servicing statewide peak loads."
    },
    {
        "id": "PWR-CHA",
        "name": "Chandrapur 400kV Mega Grid Transmission Hub",
        "category": "Electricity Hub",
        "zone": "Chandrapur",
        "lat": 19.9820, "lon": 79.3140,
        "status": "Operational",
        "metric_label": "Grid Throughput",
        "metric_value": "3,340 MW Base Dispatch",
        "contact": "MahaTransco State Dispatch",
        "info": "Super-grid switchyard transmitting base electrical power across Maharashtra with FACTS compensation."
    },
    {
        "id": "PWR-DHU",
        "name": "Sakri 125MW Mega Solar Photovoltaic Park",
        "category": "Electricity Hub",
        "zone": "Dhule",
        "lat": 20.9850, "lon": 74.3210,
        "status": "Optimal",
        "metric_label": "Clean Solar Infeed",
        "metric_value": "118 MW Peak Sunlight",
        "contact": "MahaGenco Clean Energy",
        "info": "Utility-scale crystalline silicon solar installation feeding clean power into Western Maharashtra."
    },

    # Water Reservoirs & Potable Water Filtration
    {
        "id": "WTR-THA",
        "name": "Bhatsa Dam & Pise-Panjrapur Water Treatment Plant",
        "category": "Water Facility",
        "zone": "Thane",
        "lat": 19.3240, "lon": 73.1680,
        "status": "Operational",
        "metric_label": "Purified Volume",
        "metric_value": "1,365 ML/day (99.9% Purity)",
        "contact": "MCGM Water Department",
        "info": "One of Asia's largest water treatment complexes supplying drinking water across the Mumbai-Thane region."
    },
    {
        "id": "WTR-PUN",
        "name": "Khadakwasla Dam & Parvati Water Works",
        "category": "Water Facility",
        "zone": "Pune",
        "lat": 18.4350, "lon": 73.7620,
        "status": "Optimal",
        "metric_label": "Storage Level",
        "metric_value": "92.4% Full (Secure)",
        "contact": "Irrigation & Water Department",
        "info": "Major upstream freshwater reservoir ensuring uninterrupted drinking water supply to Pune city."
    },
    {
        "id": "WTR-SOL",
        "name": "Ujani (Bhimanagar) Dam Regional Water Reservoir",
        "category": "Water Facility",
        "zone": "Solapur",
        "lat": 18.0750, "lon": 75.1180,
        "status": "Optimal",
        "metric_label": "Gross Storage",
        "metric_value": "117 TMC (Full Reservoir)",
        "contact": "Water Resources Dept",
        "info": "Massive reservoir supporting agriculture, power plants, and potable pipeline schemes in Solapur."
    },
    {
        "id": "WTR-CSN",
        "name": "Jayakwadi (Nath Sagar) Dam & Headworks",
        "category": "Water Facility",
        "zone": "Chhatrapati Sambhajinagar",
        "lat": 19.4930, "lon": 75.3850,
        "status": "Optimal",
        "metric_label": "Live Capacity",
        "metric_value": "100% Live Storage",
        "contact": "Godavari Basin Water Authority",
        "info": "Lifeline of Marathwada on the Godavari river supplying water to cities, agriculture, and industries."
    }
]

def get_zones():
    """Return all available zone names, with state overview at index 0 and 36 districts sorted alphabetically."""
    districts_only = sorted([k for k in ZONES.keys() if k != ALL_DISTRICTS_LABEL])
    return [ALL_DISTRICTS_LABEL] + districts_only

def get_zone_metadata(zone_name):
    """Retrieve metadata dict for selected district or state overview."""
    return ZONES.get(zone_name, ZONES[ALL_DISTRICTS_LABEL])

def get_pois(zone_name=ALL_DISTRICTS_LABEL, categories=None):
    """Filter POIs by district and category list, ensuring every district has civic telemetry."""
    pois = POI_DATA.copy()
    if zone_name != ALL_DISTRICTS_LABEL:
        pois = [p for p in pois if p["zone"] == zone_name]
        # If district doesn't have custom static landmark POIs in POI_DATA, generate standard district facilities
        if not pois and zone_name in ZONES:
            z_meta = ZONES[zone_name]
            lat, lon = z_meta["lat"], z_meta["lon"]
            pois = [
                {
                    "id": f"HLTH-{zone_name[:3].upper()}",
                    "name": f"{zone_name} District Civil & Emergency Hospital",
                    "category": "Hospital",
                    "zone": zone_name,
                    "lat": lat + 0.008, "lon": lon - 0.006,
                    "status": "Operational",
                    "metric_label": "ICU Bed Capacity",
                    "metric_value": "88% Ready",
                    "contact": f"Health Helpline: 108",
                    "info": f"Primary district public healthcare and emergency response facility for {zone_name}."
                },
                {
                    "id": f"EDU-{zone_name[:3].upper()}",
                    "name": f"{zone_name} Government Polytechnic & STEM College",
                    "category": "School",
                    "zone": zone_name,
                    "lat": lat - 0.007, "lon": lon + 0.009,
                    "status": "Operational",
                    "metric_label": "Campus Solar Offset",
                    "metric_value": "78% Clean Energy",
                    "contact": f"Admin: {zone_name}",
                    "info": f"Public educational campus equipped with smart environmental IoT monitoring."
                },
                {
                    "id": f"TRF-{zone_name[:3].upper()}",
                    "name": f"{zone_name} Central Highway Junction (NH Bypass)",
                    "category": "Traffic Sensor",
                    "zone": zone_name,
                    "lat": lat + 0.005, "lon": lon + 0.012,
                    "status": "Smooth",
                    "metric_label": "Traffic Flow",
                    "metric_value": f"{int(z_meta['base_traffic'] * 35):,} Veh/hr",
                    "contact": f"Mobility Center: {zone_name}",
                    "info": f"Smart highway intersection connecting {zone_name} with statewide arterial corridors."
                },
                {
                    "id": f"PWR-{zone_name[:3].upper()}",
                    "name": f"{zone_name} 132kV MSEDCL Smart Substation",
                    "category": "Electricity Hub",
                    "zone": zone_name,
                    "lat": lat - 0.011, "lon": lon - 0.008,
                    "status": "Operational",
                    "metric_label": "Substation Load",
                    "metric_value": f"{z_meta['base_power_mwh'] / 24:.1f} MW Active",
                    "contact": "MSEDCL Grid Dispatch",
                    "info": f"Smart automated distribution grid controlling feeder loads across {zone_name}."
                },
                {
                    "id": f"WTR-{zone_name[:3].upper()}",
                    "name": f"{zone_name} Municipal Water Treatment & Storage Works",
                    "category": "Water Facility",
                    "zone": zone_name,
                    "lat": lat + 0.012, "lon": lon - 0.011,
                    "status": "Optimal",
                    "metric_label": "Water Quality Index",
                    "metric_value": "99.8% Purity",
                    "contact": "Municipal Water Works",
                    "info": f"Potable water purification and reservoir supply network servicing {zone_name}."
                },
                {
                    "id": f"WST-{zone_name[:3].upper()}",
                    "name": f"{zone_name} Solid Waste & Organic Composting Station",
                    "category": "Waste Point",
                    "zone": zone_name,
                    "lat": lat - 0.009, "lon": lon + 0.015,
                    "status": "Operational",
                    "metric_label": "Diversion Rate",
                    "metric_value": "85.2% Recycled",
                    "contact": "Municipal Sanitation",
                    "info": f"Integrated waste sorting and composting depot servicing {zone_name}."
                }
            ]
    if categories:
        pois = [p for p in pois if p["category"] in categories]
    return pois

def generate_hourly_time_series(zone_name=ALL_DISTRICTS_LABEL, days=7, seed=42):
    """
    Generate realistic hourly time series data for the selected district or state over N days.
    Includes AQI, Temperature, Humidity, Electricity, Water, and Traffic.
    """
    np.random.seed(seed)
    total_hours = days * 24
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=total_hours - 1)

    timestamps = [start_time + timedelta(hours=i) for i in range(total_hours)]
    hours = np.array([t.hour for t in timestamps])
    day_of_week = np.array([t.weekday() for t in timestamps])
    is_weekend = (day_of_week >= 5).astype(int)

    meta = get_zone_metadata(zone_name)
    base_aqi = meta["base_aqi"]
    base_traffic = meta["base_traffic"]
    base_power = meta["base_power_mwh"]
    base_water = meta["base_water_ml"]

    # Diurnal Temperature Curve (°C)
    diurnal_temp = 5.2 * np.sin((hours - 8) * (2 * np.pi / 24))
    temperatures = np.round(26.0 + diurnal_temp + np.random.normal(0, 0.6, total_hours), 1)

    # Relative Humidity (%)
    humidity = np.round(np.clip(60.0 - diurnal_temp * 2.8 + np.random.normal(0, 2.0, total_hours), 30.0, 90.0), 0)

    # Traffic Congestion Index (0-100)
    morning_peak = np.exp(-((hours - 9) ** 2) / 3.0)
    evening_peak = np.exp(-((hours - 18.5) ** 2) / 3.5)
    traffic_profile = (0.28 + 0.45 * morning_peak + 0.52 * evening_peak) * (1 - 0.22 * is_weekend)
    traffic = (base_traffic / 55.0) * traffic_profile + np.random.normal(0, 3.5, total_hours)
    traffic = np.round(np.clip(traffic, 12.0, 95.0), 1)

    # AQI (0 to 300)
    aqi_diurnal = 14 * np.exp(-((hours - 9) ** 2) / 4.0) + 16 * np.exp(-((hours - 19) ** 2) / 5.0)
    aqi = base_aqi + aqi_diurnal + np.random.normal(0, 5.0, total_hours)
    day_wave = 8 * np.sin(np.linspace(0, days * np.pi, total_hours))
    aqi = np.round(np.clip(aqi + day_wave, 18.0, 220.0), 0)

    # Electricity Consumption (MWh)
    biz_hours_mult = 1.0 + 0.38 * np.exp(-((hours - 14) ** 2) / 18.0)
    power_hourly_base = base_power / 24.0
    power = power_hourly_base * biz_hours_mult * (1 - 0.12 * is_weekend) + np.random.normal(0, power_hourly_base * 0.03, total_hours)
    power = np.round(np.clip(power, power_hourly_base * 0.65, power_hourly_base * 1.6), 2)

    # Water Consumption (Mega Liters / ML)
    water_morning = np.exp(-((hours - 8) ** 2) / 2.5)
    water_evening = np.exp(-((hours - 20) ** 2) / 3.0)
    water_hourly_base = base_water / 24.0
    water = water_hourly_base * (0.65 + 0.7 * water_morning + 0.55 * water_evening) + np.random.normal(0, water_hourly_base * 0.04, total_hours)
    water = np.round(np.clip(water, water_hourly_base * 0.45, water_hourly_base * 2.0), 2)

    # Waste Generation (Tons per hour)
    waste_base = (meta["population"] / 126000000.0) * 3200.0 if zone_name == ALL_DISTRICTS_LABEL else (meta["population"] / 3000000.0) * 90.0
    waste = waste_base * (0.55 + 0.65 * np.exp(-((hours - 12) ** 2) / 16.0)) + np.random.normal(0, 2.0, total_hours)
    waste = np.round(np.clip(waste, 5.0, 4800.0), 1)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "date": [t.strftime("%Y-%m-%d") for t in timestamps],
        "hour": hours,
        "temperature_c": temperatures,
        "humidity_pct": humidity,
        "aqi": aqi,
        "traffic_index": traffic,
        "electricity_mwh": power,
        "water_ml": water,
        "waste_tons": waste,
        "zone": zone_name
    })
    return df

def get_waste_composition(zone_name=ALL_DISTRICTS_LABEL):
    """Return categorized waste breakdown data for the selected district or state."""
    meta = get_zone_metadata(zone_name)
    pop_ratio = meta["population"] / 126000000.0 if zone_name == ALL_DISTRICTS_LABEL else meta["population"] / 3500000.0

    multiplier = 28000 if zone_name == ALL_DISTRICTS_LABEL else 1200
    categories = [
        {"category": "Organic & Food Compost", "percentage": 45.0, "tons_per_day": round(multiplier * 0.45 * pop_ratio, 1), "color": "#10B981"},
        {"category": "Paper & Cardboard", "percentage": 23.0, "tons_per_day": round(multiplier * 0.23 * pop_ratio, 1), "color": "#3B82F6"},
        {"category": "Plastics & Packaging", "percentage": 16.0, "tons_per_day": round(multiplier * 0.16 * pop_ratio, 1), "color": "#F59E0B"},
        {"category": "Glass & Metals", "percentage": 7.5, "tons_per_day": round(multiplier * 0.075 * pop_ratio, 1), "color": "#06B6D4"},
        {"category": "Consumer E-Waste", "percentage": 5.5, "tons_per_day": round(multiplier * 0.055 * pop_ratio, 1), "color": "#8B5CF6"},
        {"category": "Special Disposal & Medical", "percentage": 3.0, "tons_per_day": round(multiplier * 0.03 * pop_ratio, 1), "color": "#F43F5E"}
    ]
    return pd.DataFrame(categories)

def get_area_comparison_metrics():
    """Return latest comparative summary metrics across all 36 districts of Maharashtra."""
    zone_keys = sorted([k for k in ZONES.keys() if k != ALL_DISTRICTS_LABEL])
    records = []
    for k in zone_keys:
        meta = ZONES[k]
        records.append({
            "zone": k,
            "population": meta["population"],
            "area_sqkm": meta["area_sqkm"],
            "smart_nodes": meta["smart_nodes"],
            "electricity_mwh": meta["base_power_mwh"],
            "water_ml": meta["base_water_ml"],
            "avg_aqi": meta["base_aqi"],
            "traffic_index": meta["base_traffic"],
            "waste_tons_day": round(meta["population"] * 0.00065, 1)
        })
    return pd.DataFrame(records)

def get_realtime_kpis(zone_name=ALL_DISTRICTS_LABEL, simulation_offset=0):
    """
    Generate instantaneous KPI metrics and deltas for the top overview bar.
    Takes simulation_offset to simulate live fluctuation when refreshed.
    """
    meta = get_zone_metadata(zone_name)
    jitter = np.sin(simulation_offset) * 2.0

    aqi_val = int(np.clip(meta["base_aqi"] + jitter * 1.2, 15, 220))
    if aqi_val <= 50:
        aqi_status = "Good"
        aqi_color = "#10B981"
    elif aqi_val <= 100:
        aqi_status = "Moderate"
        aqi_color = "#F59E0B"
    elif aqi_val <= 150:
        aqi_status = "Unhealthy for Sensitive"
        aqi_color = "#F97316"
    else:
        aqi_status = "Unhealthy"
        aqi_color = "#EF4444"

    traffic_val = int(np.clip(meta["base_traffic"] + jitter * 1.8, 15, 95))
    if traffic_val < 38:
        traffic_status = "Free Flowing"
        traffic_color = "#10B981"
    elif traffic_val < 65:
        traffic_status = "Moderate Flow"
        traffic_color = "#3B82F6"
    else:
        traffic_status = "Brisk Congestion"
        traffic_color = "#F59E0B"

    temp_val = round(26.2 + np.cos(simulation_offset) * 1.5, 1)
    humidity_val = int(58 - np.cos(simulation_offset) * 3)

    power_val = round(meta["base_power_mwh"] * (1 + jitter * 0.008), 1)
    water_val = round(meta["base_water_ml"] * (1 + jitter * 0.006), 1)
    waste_daily = round(meta["population"] * 0.00065, 1)

    return {
        "zone": zone_name,
        "population": meta["population"],
        "smart_nodes": meta["smart_nodes"],
        "aqi": aqi_val,
        "aqi_status": aqi_status,
        "aqi_color": aqi_color,
        "traffic_index": traffic_val,
        "traffic_status": traffic_status,
        "traffic_color": traffic_color,
        "temp_c": temp_val,
        "humidity_pct": humidity_val,
        "power_mwh": power_val,
        "water_ml": water_val,
        "waste_daily_tons": waste_daily,
        "active_alerts": [
            {"severity": "info", "text": f"🌿 Environmental Monitoring: Air quality index across {zone_name} is currently {aqi_val} ({aqi_status})."},
            {"severity": "info", "text": "⚡ Grid Stability: MahaGenco and MSEDCL distribution networks reporting nominal frequency across all 36 districts."},
            {"severity": "info", "text": "🚦 Transit & Logistics: State expressways (Samruddhi Mahamarg, Mumbai-Pune Expressway) running at smooth transit velocities."}
        ]
    }
