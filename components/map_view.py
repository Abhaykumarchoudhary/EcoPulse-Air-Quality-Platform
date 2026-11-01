"""
Interactive Leaflet-based Geospatial Map Component for EcoPulse.
High-resolution 1 km PM2.5 gridded surface with Retina basemaps,
smooth contour heat surface, animated wind flow vectors, floating inspection HUD,
numeric station pins, pulsing radar hotspots, and quick landmark camera fly-to controls.
"""
import json
from typing import List, Dict, Any, Optional
import streamlit.components.v1 as components
from config import DELHI_CENTER, AQI_CATEGORIES, NCR_BOUNDS
from data.stations import STATIONS

def _safe_json_dumps(obj: Any) -> str:
    def _default(o):
        if hasattr(o, "item"):
            return o.item()
        if hasattr(o, "tolist"):
            return o.tolist()
        return str(o)
    return json.dumps(obj, default=_default)

def render_leaflet_fused_map(
    grid_cells: List[Dict[str, Any]],
    active_layer: str = "fused",         # "fused", "smooth", "aod", "gap_filled", "wind", "heat"
    show_stations: bool = True,
    show_anomalies: bool = True,
    opacity: float = 0.75,
    basemap_theme: str = "positron",     # "positron", "dark_matter", "satellite_hybrid", "topographic", "streets"
    selected_station_name: str = "Anand Vihar",
    height: int = 560,
    is_overview: bool = False,
    stations: Optional[List[Dict[str, Any]]] = None,
    wind_data: Optional[Dict[str, Any]] = None,
    show_wind: bool = False
):
    """
    Renders ultra-high quality Leaflet map with Retina basemaps, dual discrete/smooth modes,
    live wind flow streamlines, floating inspection HUD, and numeric station badges.
    """
    grid_json = _safe_json_dumps(grid_cells)
    active_stations = stations if (stations and len(stations) > 0) else STATIONS
    stations_json = _safe_json_dumps(active_stations)
    categories_json = _safe_json_dumps(AQI_CATEGORIES)
    wind_info = wind_data or {"wind_speed": 5.4, "wind_direction": 290}
    wind_json = _safe_json_dumps(wind_info)
    bounds_json = _safe_json_dumps(NCR_BOUNDS)
    
    # Normalize basemap theme key
    theme_key = basemap_theme.lower()
    if theme_key in ["light", "default"]:
        theme_key = "positron"
    elif theme_key in ["dark", "dark matter"]:
        theme_key = "dark_matter"
    elif theme_key in ["satellite", "hybrid"]:
        theme_key = "satellite_hybrid"
    elif theme_key in ["topo", "topographic"]:
        theme_key = "topographic"
    
    # Normalize layer key
    layer_key = active_layer.lower()
    if "smooth" in layer_key or "contour" in layer_key:
        layer_mode = "smooth"
    elif "aod" in layer_key:
        layer_mode = "aod"
    elif "gap" in layer_key:
        layer_mode = "gap_filled"
    elif "wind" in layer_key:
        layer_mode = "wind"
    else:
        layer_mode = "fused"

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
        <style>
            * {{ box-sizing: border-box; }}
            body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0f172a; overflow: hidden; }}
            #map-container {{ position: relative; width: 100%; height: {height}px; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1); border: 1px solid #cbd5e1; }}
            #map {{ width: 100%; height: 100%; }}
            
            /* Glassmorphic Floating HUD (Inspection Card) */
            .map-hud {{
                position: absolute;
                top: 14px;
                left: 14px;
                z-index: 1000;
                background: rgba(15, 23, 42, 0.88);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 10px;
                padding: 10px 14px;
                color: #ffffff;
                min-width: 260px;
                box-shadow: 0 12px 30px rgba(0,0,0,0.3);
                transition: all 0.2s ease;
                pointer-events: none;
            }}
            .hud-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid rgba(255, 255, 255, 0.12);
                padding-bottom: 6px;
                margin-bottom: 6px;
            }}
            .hud-title-box {{
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .hud-live-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #10b981;
                box-shadow: 0 0 8px #10b981;
                animation: pulse-dot 2s infinite;
            }}
            @keyframes pulse-dot {{
                0% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.4; transform: scale(0.85); }}
                100% {{ opacity: 1; transform: scale(1); }}
            }}
            .hud-title {{
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.3px;
                color: #f8fafc;
            }}
            .hud-coords {{
                font-size: 10.5px;
                color: #94a3b8;
                font-family: monospace;
            }}
            .hud-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 6px 12px;
            }}
            .hud-item {{
                display: flex;
                flex-direction: column;
            }}
            .hud-label {{
                font-size: 9.5px;
                font-weight: 600;
                color: #94a3b8;
                letter-spacing: 0.4px;
                text-transform: uppercase;
            }}
            .hud-val {{
                font-size: 13px;
                font-weight: 700;
                color: #f1f5f9;
            }}
            .hud-val-tag {{
                display: inline-block;
                padding: 1px 6px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 700;
                margin-top: 1px;
            }}

            /* Quick-Jump Landmark Navigation Bar */
            .map-quick-nav {{
                position: absolute;
                top: 14px;
                right: 14px;
                z-index: 1000;
                display: flex;
                gap: 6px;
                background: rgba(255, 255, 255, 0.92);
                backdrop-filter: blur(8px);
                padding: 4px 6px;
                border-radius: 8px;
                border: 1px solid #cbd5e1;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            .nav-chip {{
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 600;
                color: #1e293b;
                cursor: pointer;
                transition: all 0.15s ease;
                outline: none;
            }}
            .nav-chip:hover {{
                background: #0f766e;
                color: #ffffff;
                border-color: #0f766e;
                transform: translateY(-1px);
            }}
            .nav-chip.reset-chip {{
                background: #f1f5f9;
                color: #475569;
            }}
            .nav-chip.reset-chip:hover {{
                background: #334155;
                color: #ffffff;
            }}

            /* Map Legend Bottom Left */
            .map-legend-box {{
                position: absolute;
                bottom: 18px;
                left: 18px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.96);
                backdrop-filter: blur(10px);
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 10px 14px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.12);
                font-size: 11px;
                color: #1e293b;
            }}
            .legend-title {{
                font-weight: 700;
                font-size: 11.5px;
                margin-bottom: 6px;
                color: #0f172a;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .legend-swatches {{
                display: flex;
                height: 12px;
                border-radius: 3px;
                overflow: hidden;
                margin-bottom: 4px;
                border: 1px solid #cbd5e1;
            }}
            .legend-swatch {{
                width: 28px;
                height: 100%;
            }}
            .legend-swatch-hatch {{
                width: 30px;
                height: 100%;
                background: repeating-linear-gradient(
                    45deg,
                    #94a3b8,
                    #94a3b8 2px,
                    #e2e8f0 2px,
                    #e2e8f0 6px
                );
            }}
            .legend-scale-labels {{
                display: flex;
                justify-content: space-between;
                font-size: 9.5px;
                color: #64748b;
                font-weight: 600;
                margin-bottom: 3px;
            }}
            .legend-subnote {{
                font-size: 9.5px;
                color: #64748b;
            }}

            /* Zoom level badge */
            .zoom-level-label {{
                position: absolute;
                bottom: 18px;
                right: 18px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 3px 8px;
                font-size: 11px;
                color: #475569;
                font-weight: 600;
            }}

            /* Custom Station Pin Badges */
            .station-pin-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
                cursor: pointer;
            }}
            .station-pin-badge {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                color: #ffffff;
                font-weight: 800;
                font-size: 11px;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid #ffffff;
                box-shadow: 0 4px 10px rgba(0,0,0,0.35);
                transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
                z-index: 2;
            }}
            .station-pin-container:hover .station-pin-badge {{
                transform: scale(1.22);
            }}
            .station-pin-name {{
                font-size: 10px;
                font-weight: 700;
                color: #0f172a;
                background: rgba(255, 255, 255, 0.96);
                padding: 1.5px 6px;
                border-radius: 4px;
                border: 1px solid #cbd5e1;
                margin-top: 2px;
                white-space: nowrap;
                box-shadow: 0 2px 5px rgba(0,0,0,0.12);
                z-index: 2;
            }}
            
            /* Pulsing Radar Ring on Worst Hotspot */
            .radar-ripple {{
                position: absolute;
                top: 0;
                left: 0;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                border: 2px solid #ef4444;
                animation: ripple 2.2s cubic-bezier(0, 0.2, 0.8, 1) infinite;
                pointer-events: none;
                z-index: 1;
            }}
            .radar-ripple.delayed {{
                animation-delay: 1.1s;
            }}
            @keyframes ripple {{
                0% {{ transform: scale(0.9); opacity: 0.95; }}
                100% {{ transform: scale(2.6); opacity: 0; }}
            }}

            /* Wind vector arrow marker */
            .wind-arrow-wrap {{
                display: flex;
                align-items: center;
                justify-content: center;
                pointer-events: none;
                transition: transform 0.3s ease;
            }}
            .wind-arrow-icon {{
                color: rgba(14, 165, 233, 0.85);
                filter: drop-shadow(0 0 2px rgba(255,255,255,0.7));
            }}

            /* Leaflet popup customization */
            .leaflet-popup-content-wrapper {{
                background: #ffffff;
                border-radius: 10px;
                padding: 4px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                border: 1px solid #e2e8f0;
            }}
            .custom-cell-popup {{
                padding: 6px 8px;
                font-family: inherit;
            }}
            .popup-station-name {{
                font-size: 14px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 3px;
            }}
            .popup-pm-val {{
                font-size: 20px;
                font-weight: 800;
                color: #ef4444;
                margin-bottom: 2px;
            }}
            .popup-category {{
                font-size: 12px;
                font-weight: 600;
                color: #64748b;
                margin-bottom: 6px;
            }}
            .popup-meta {{
                font-size: 11px;
                color: #475569;
                border-top: 1px solid #f1f5f9;
                padding-top: 4px;
                display: flex;
                flex-direction: column;
                gap: 2px;
            }}
        </style>
    </head>
    <body>
        <div id="map-container">
            <div id="map"></div>

            <!-- Floating Glassmorphism Inspection HUD -->
            <div class="map-hud" id="map-hud">
                <div class="hud-header">
                    <div class="hud-title-box">
                        <span class="hud-live-dot"></span>
                        <span class="hud-title" id="hud-title">Delhi-NCR 1 km Surface</span>
                    </div>
                    <span class="hud-coords" id="hud-coords">28.614°N, 77.209°E</span>
                </div>
                <div class="hud-grid">
                    <div class="hud-item">
                        <span class="hud-label">Estimated PM₂.₅</span>
                        <span class="hud-val" id="hud-pm">Hover over map</span>
                    </div>
                    <div class="hud-item">
                        <span class="hud-label">Satellite AOD</span>
                        <span class="hud-val" id="hud-aod">--</span>
                    </div>
                    <div class="hud-item">
                        <span class="hud-label">Model Sigma</span>
                        <span class="hud-val" id="hud-sigma">--</span>
                    </div>
                    <div class="hud-item">
                        <span class="hud-label">Data Ingestion</span>
                        <span class="hud-val" id="hud-source">--</span>
                    </div>
                </div>
            </div>

            <!-- Quick Landmark Navigation Bar -->
            <div class="map-quick-nav">
                <button class="nav-chip" onclick="flyToLoc(28.6468, 77.3160, 12, 'Anand Vihar')">📍 Anand Vihar</button>
                <button class="nav-chip" onclick="flyToLoc(28.7328, 77.1706, 12, 'Jahangirpuri')">📍 Jahangirpuri</button>
                <button class="nav-chip" onclick="flyToLoc(28.6304, 77.2177, 12, 'Central Delhi')">📍 Connaught Pl</button>
                <button class="nav-chip" onclick="flyToLoc(28.5562, 77.1000, 12, 'IGI Airport')">📍 IGI Airport</button>
                <button class="nav-chip reset-chip" onclick="flyToLoc(28.6139, 77.2090, 10, 'Delhi-NCR')">🔄 NCR Full</button>
            </div>

            <!-- Bottom Left Legend -->
            <div class="map-legend-box">
                <div class="legend-title">
                    <span>PM<sub>2.5</sub> (µg/m³) · 1 km Surface</span>
                </div>
                <div class="legend-swatches">
                    <div class="legend-swatch" style="background:#22c55e;" title="0-30 Good"></div>
                    <div class="legend-swatch" style="background:#84cc16;" title="31-60 Satisfactory"></div>
                    <div class="legend-swatch" style="background:#eab308;" title="61-90 Moderate"></div>
                    <div class="legend-swatch" style="background:#f97316;" title="91-120 Poor"></div>
                    <div class="legend-swatch" style="background:#ef4444;" title="121-250 Very Poor"></div>
                    <div class="legend-swatch" style="background:#7f1d1d;" title="250+ Severe"></div>
                    <div class="legend-swatch-hatch" title="Gap-filled model"></div>
                </div>
                <div class="legend-scale-labels">
                    <span>0</span><span>30</span><span>60</span><span>90</span><span>120</span><span>250+</span>
                </div>
                <div class="legend-subnote">Hatched = Gap-filled (Cloud/Haze) · Hover for pixel telemetry</div>
            </div>

            <div class="zoom-level-label" id="zoom-label">Delhi · Zoom 10</div>
        </div>

        <!-- SVG Patterns for Gap-fill Hatching -->
        <svg width="0" height="0" style="position:absolute;">
            <defs>
                <pattern id="gapfill-hatch" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
                    <line x1="0" y1="0" x2="0" y2="8" stroke="#0f172a" stroke-width="2.5" opacity="0.65" />
                </pattern>
            </defs>
        </svg>

        <script>
            var center = {DELHI_CENTER};
            var map = L.map('map', {{
                center: center,
                zoom: 10,
                zoomControl: true,
                attributionControl: false
            }});

            map.on('zoomend', function() {{
                document.getElementById('zoom-label').innerText = 'Delhi · Zoom ' + map.getZoom();
            }});

            // High-Resolution & Retina Basemap Providers
            var basemaps = {{
                "positron": L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                    maxZoom: 20,
                    subdomains: 'abcd',
                    detectRetina: true,
                    attribution: '&copy; CARTO'
                }}),
                "dark_matter": L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                    maxZoom: 20,
                    subdomains: 'abcd',
                    detectRetina: true,
                    attribution: '&copy; CARTO'
                }}),
                "satellite_hybrid": L.layerGroup([
                    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
                        maxZoom: 19,
                        detectRetina: true,
                        attribution: 'Esri Satellite'
                    }}),
                    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
                        maxZoom: 19,
                        detectRetina: true,
                        attribution: 'Esri Reference'
                    }})
                ]),
                "topographic": L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
                    maxZoom: 18,
                    detectRetina: true,
                    attribution: 'Esri Topo'
                }}),
                "streets": L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    maxZoom: 19,
                    detectRetina: true,
                    attribution: 'OSM'
                }})
            }};

            var requestedTheme = "{theme_key}";
            var activeBasemapLayer = basemaps[requestedTheme] || basemaps["positron"];
            activeBasemapLayer.addTo(map);

            var gridData = {grid_json};
            var stationsData = {stations_json};
            var windInfo = {wind_json};
            var ncrBounds = {bounds_json};
            var layerMode = "{layer_mode}";
            var layerOpacity = {opacity};
            var showStations = {"true" if show_stations else "false"};
            var showAnomalies = {"true" if show_anomalies else "false"};
            var selectedStation = "{selected_station_name}";

            var hudTitle = document.getElementById('hud-title');
            var hudCoords = document.getElementById('hud-coords');
            var hudPm = document.getElementById('hud-pm');
            var hudAod = document.getElementById('hud-aod');
            var hudSigma = document.getElementById('hud-sigma');
            var hudSource = document.getElementById('hud-source');

            // Fly to landmark function
            window.flyToLoc = function(lat, lon, zoom, name) {{
                map.flyTo([lat, lon], zoom, {{ duration: 1.2, easeLinearity: 0.25 }});
                hudTitle.innerText = name;
                hudCoords.innerText = lat.toFixed(3) + '°N, ' + lon.toFixed(3) + '°E';
            }};

            // 1. Smooth Heatmap Mode via Leaflet-Heat
            if (layerMode === "smooth") {{
                var heatPoints = gridData.map(function(cell) {{
                    return [cell.center_lat, cell.center_lon, Math.min(1.0, cell.pm25 / 235.0)];
                }});
                L.heatLayer(heatPoints, {{
                    radius: 36,
                    blur: 24,
                    maxZoom: 14,
                    max: 1.0,
                    gradient: {{
                        0.15: '#22c55e',
                        0.30: '#84cc16',
                        0.48: '#eab308',
                        0.65: '#f97316',
                        0.85: '#ef4444',
                        1.0: '#7f1d1d'
                    }}
                }}).addTo(map);
            }}

            // 2. High-Resolution Discrete 1 km Grid Cells (if not purely smooth)
            var highlightedRect = null;
            gridData.forEach(function(cell) {{
                var bounds = [[cell.lat_min, cell.lon_min], [cell.lat_max, cell.lon_max]];
                var fillColor = cell.color;
                var fillOpacity = (layerMode === "smooth") ? 0.05 : layerOpacity;
                var strokeColor = (layerMode === "smooth") ? "transparent" : "#ffffff";
                var strokeWidth = (layerMode === "smooth") ? 0 : 0.35;

                if (layerMode === "aod") {{
                    var aodVal = cell.aod;
                    fillColor = aodVal > 0.85 ? "#b91c1c" : aodVal > 0.60 ? "#f97316" : aodVal > 0.35 ? "#eab308" : "#22c55e";
                }} else if (layerMode === "gap_filled") {{
                    if (!cell.is_gap_filled) {{
                        fillOpacity = 0.06;
                    }} else {{
                        fillColor = "#ef4444";
                        fillOpacity = 0.85;
                    }}
                }}

                var rect = L.rectangle(bounds, {{
                    color: strokeColor,
                    weight: strokeWidth,
                    fillColor: fillColor,
                    fillOpacity: fillOpacity
                }}).addTo(map);

                // Gap-filled subtle hatch pattern overlay
                if (cell.is_gap_filled && layerMode !== "smooth") {{
                    L.rectangle(bounds, {{
                        color: "transparent",
                        weight: 0,
                        fillColor: "#0f172a",
                        fillOpacity: 0.22
                    }}).addTo(map);
                }}

                // Hover interaction: Live update HUD
                rect.on('mouseover', function(e) {{
                    rect.setStyle({{ color: '#38bdf8', weight: 2.0 }});
                    rect.bringToFront();
                    
                    hudTitle.innerText = cell.nearest_station;
                    hudCoords.innerText = cell.center_lat.toFixed(3) + '°N, ' + cell.center_lon.toFixed(3) + '°E';
                    hudPm.innerHTML = `<span class="hud-val-tag" style="background:${{cell.bg_color}}; color:${{cell.text_color}};">${{cell.pm25}} µg/m³ (${{cell.category}})</span>`;
                    hudAod.innerText = cell.aod + ' (MCD19A2)';
                    hudSigma.innerText = '± ' + (cell.sigma || 14.2) + ' µg/m³';
                    hudSource.innerText = cell.is_gap_filled ? 'Gap-Filled (RF Model)' : 'MODIS Satellite Fused';
                }});

                rect.on('mouseout', function(e) {{
                    rect.setStyle({{ color: strokeColor, weight: strokeWidth }});
                }});

                // Interactive Popup
                var popupHtml = `
                    <div class="custom-cell-popup">
                        <div class="popup-station-name">${{cell.nearest_station}} (1 km Cell)</div>
                        <div class="popup-pm-val" style="color:${{cell.color}};">${{cell.pm25}} µg/m³</div>
                        <div class="popup-category">${{cell.category}} Air Quality</div>
                        <div class="popup-meta">
                            <span>🛰️ MODIS MAIAC AOD: <strong>${{cell.aod}}</strong></span>
                            <span>🎯 Uncertainty: <strong>± ${{cell.sigma || 14.2}} µg/m³</strong></span>
                            <span>📡 Data: <strong>${{cell.is_gap_filled ? 'Gap-Filled Model' : 'Satellite AOD Fused'}}</strong></span>
                        </div>
                    </div>
                `;
                rect.bindPopup(popupHtml);
            }});

            // 3. Live Wind Streamlines & Vectors
            if (layerMode === "wind" || { "true" if show_wind else "false" }) {{
                var windDir = windInfo.wind_direction || 290;
                var windSpd = windInfo.wind_speed || 5.4;
                var arrowSvg = `
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="transform: rotate(${{windDir + 90}}deg);">
                        <path d="M12 2L19 21L12 17L5 21L12 2Z" fill="#0284c7" stroke="#ffffff" stroke-width="1.2" opacity="0.85"/>
                    </svg>
                `;
                
                // Place 25 vector indicators across the domain
                var latSpan = ncrBounds.lat_max - ncrBounds.lat_min;
                var lonSpan = ncrBounds.lon_max - ncrBounds.lon_min;
                for (var r_idx = 1; r_idx <= 5; r_idx++) {{
                    for (var c_idx = 1; c_idx <= 5; c_idx++) {{
                        var wLat = ncrBounds.lat_min + (r_idx / 6) * latSpan;
                        var wLon = ncrBounds.lon_min + (c_idx / 6) * lonSpan;
                        
                        var windIcon = L.divIcon({{
                            html: arrowSvg,
                            className: 'wind-arrow-wrap',
                            iconSize: [24, 24],
                            iconAnchor: [12, 12]
                        }});
                        
                        var windMarker = L.marker([wLat, wLon], {{ icon: windIcon, interactive: false }}).addTo(map);
                    }}
                }}
            }}

            // 4. Station Markers with Numeric Badges & Radar Rings
            if (showStations) {{
                stationsData.forEach(function(st) {{
                    var isWorst = st.is_worst;
                    var isTarget = (st.name === selectedStation);
                    var markerColor = st.pm25 >= 121 ? "#ef4444" : st.pm25 >= 91 ? "#f97316" : "#eab308";
                    
                    var badgeHtml = `
                        <div class="station-pin-container ${{isWorst ? 'worst-station' : ''}}">
                            ${{isWorst ? '<div class="radar-ripple"></div><div class="radar-ripple delayed"></div>' : ''}}
                            <div class="station-pin-badge" style="background:${{markerColor}};">
                                <span class="station-pin-val">${{st.pm25}}</span>
                            </div>
                            <div class="station-pin-name">${{st.name}}</div>
                        </div>
                    `;

                    var pinIcon = L.divIcon({{
                        html: badgeHtml,
                        className: 'station-badge-icon',
                        iconSize: [36, 44],
                        iconAnchor: [18, 22]
                    }});

                    var marker = L.marker([st.lat, st.lon], {{ icon: pinIcon, zIndexOffset: isWorst ? 1000 : 500 }}).addTo(map);

                    marker.on('click', function() {{
                        map.flyTo([st.lat, st.lon], 12, {{ duration: 1.2 }});
                        hudTitle.innerText = st.name + ' (CPCB Sensor)';
                        hudCoords.innerText = st.lat.toFixed(3) + '°N, ' + st.lon.toFixed(3) + '°E';
                        hudPm.innerHTML = `<span class="hud-val-tag" style="background:#fee2e2; color:#991b1b;">${{st.pm25}} µg/m³ (${{st.status}})</span>`;
                        hudAod.innerText = (st.aod || 0.48) + ' (Collocated)';
                        hudSigma.innerText = 'MAE ' + (st.loso_mae || 24.5) + ' µg/m³';
                        hudSource.innerText = st.source || 'CPCB Official Telemetry';
                    }});

                    var tooltipContent = `
                        <div style="font-family:sans-serif; padding:2px;">
                            <strong>${{st.name}}</strong><br>
                            PM₂.₅: <b>${{st.pm25}} µg/m³</b> (${{st.status}})<br>
                            <span style="font-size:10px; color:#64748b;">Source: ${{st.source}}</span>
                        </div>
                    `;
                    marker.bindTooltip(tooltipContent, {{ direction: 'top', offset: [0, -16] }});
                }});
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height + 25)

def render_combined_hotspot_map(
    grid_cells: List[Dict[str, Any]],
    hotspots: List[Dict[str, Any]],
    sector_filter: str = "All",
    height: int = 400
):
    """
    Renders Hotspot Map for Combined Insights (Wireframe 4).
    Overlays purple emission hotspot diamonds/squares sized by emissions tonnage
    over the high-resolution 1 km PM2.5 grid surface on a crisp Retina basemap.
    """
    grid_json = _safe_json_dumps(grid_cells)
    
    if sector_filter != "All":
        filtered_hotspots = [h for h in hotspots if h["sector"] == sector_filter]
    else:
        filtered_hotspots = hotspots
        
    hotspots_json = _safe_json_dumps(filtered_hotspots)
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; font-family: -apple-system, sans-serif; }}
            #hotspot-map {{ width: 100%; height: {height}px; border-radius: 12px; z-index: 1; border: 1px solid #cbd5e1; }}
            
            .hotspot-marker {{
                background: linear-gradient(135deg, #8b5cf6, #6d28d9);
                border: 2px solid #ffffff;
                box-shadow: 0 4px 14px rgba(109, 40, 217, 0.6);
                transform: rotate(45deg);
                border-radius: 4px;
                transition: transform 0.2s ease;
            }}
            .hotspot-marker:hover {{
                transform: rotate(45deg) scale(1.2);
            }}
            .hotspot-legend {{
                position: absolute;
                bottom: 16px;
                left: 16px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(8px);
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 11px;
                font-weight: 700;
                color: #334155;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div id="hotspot-map"></div>
        <div class="hotspot-legend">◆ Climate TRACE Emission Hotspot · Sized by kt CO₂e</div>
        <script>
            var map = L.map('hotspot-map', {{
                center: {DELHI_CENTER},
                zoom: 10,
                zoomControl: true,
                attributionControl: false
            }});
            
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                maxZoom: 20,
                subdomains: 'abcd',
                detectRetina: true,
                attribution: '&copy; CARTO'
            }}).addTo(map);

            var gridData = {grid_json};
            var hotspotsData = {hotspots_json};

            // Draw faded 1km grid background
            gridData.forEach(function(cell) {{
                var bounds = [[cell.lat_min, cell.lon_min], [cell.lat_max, cell.lon_max]];
                L.rectangle(bounds, {{
                    color: "transparent",
                    weight: 0,
                    fillColor: cell.color,
                    fillOpacity: 0.32
                }}).addTo(map);
            }});

            // Draw Emission Hotspots as glowing purple diamonds
            hotspotsData.forEach(function(hs) {{
                var size = hs.marker_size;
                var diamondIcon = L.divIcon({{
                    className: 'hotspot-marker',
                    iconSize: [size, size],
                    iconAnchor: [size/2, size/2]
                }});

                var marker = L.marker([hs.lat, hs.lon], {{ icon: diamondIcon }}).addTo(map);
                marker.bindPopup(`
                    <div style="font-family:sans-serif; padding:4px;">
                        <div style="font-weight:700; font-size:14px; color:#0f172a;">${{hs.name}}</div>
                        <div style="font-size:12px; color:#7c3aed; font-weight:600; margin:2px 0;">Sector: ${{hs.sector}}</div>
                        <div style="font-size:12px; color:#475569;">Annual CO₂e: <strong>${{hs.emissions_kt.toLocaleString()}} kt</strong></div>
                    </div>
                `);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height + 25)
