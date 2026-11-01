# EcoPulse Raw Data Directory

You can drop downloaded data files directly into this directory, and EcoPulse will automatically detect and load them:

### 1. Ground PM₂.₅ Station Data (`cpcb_stations.csv`)
Export from CPCB (https://airquality.cpcb.gov.in/AQI_India/) or OpenAQ.
Expected columns:
```csv
station_name,latitude,longitude,pm25,date_time
Anand Vihar,28.6468,77.3160,186,2025-01-12 10:00
Jahangirpuri,28.7328,77.1706,174,2025-01-12 10:00
Wazirpur,28.6998,77.1654,162,2025-01-12 10:00
...
```

### 2. Satellite AOD GeoTIFF / NetCDF (`satellite_aod/`)
Download MODIS MAIAC `MCD19A2.061` tiles from NASA AppEEARS covering Delhi-NCR:
- Coordinate bounds: `lat: 28.4 to 28.9, lon: 76.9 to 77.4`
- Place `.tif` or `.nc` files in `data/raw/satellite_aod/`

### 3. Sectoral Carbon Emissions (`climate_trace_delhi.csv`)
Download from Climate TRACE (https://climatetrace.org/data):
- Filter: India -> Delhi
- Contains monthly CO2e emissions by sector: Power, Manufacturing, Road Transport, Residential.
