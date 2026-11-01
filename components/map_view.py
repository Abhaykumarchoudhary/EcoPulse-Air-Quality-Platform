"""
Interactive Leaflet-based Geospatial Map Component for EcoPulse.
High-resolution 1 km PM2.5 gridded surface with Retina basemaps,
smooth contour heat surface, animated wind flow streamlines, floating inspection HUD,
numeric station pins with dual radar pulses, quick landmark fly-to controls,
fullscreen toggle, and facility emission hotspot overlays.
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
    selected_station_name: Optional[str] = "Anand Vihar",
    height: int = 560,
    is_overview: bool = False,
    stations: Optional[List[Dict[str, Any]]] = None,
    wind_data: Optional[Dict[str, Any]] = None,
    show_wind: bool = False
):
    """
    Renders ultra-high quality Leaflet map with Retina basemaps, discrete 1km / smooth heat modes,
    live animated wind flow streamlines, collapsible glassmorphic HUD, full-screen toggle,
    quick landmark navigation, and CPCB station pins with pulsing radar rings.
    """
    grid_json = _safe_json_dumps(grid_cells)
    active_stations = stations if (stations and len(stations) > 0) else STATIONS
    stations_json = _safe_json_dumps(active_stations)
    categories_json = _safe_json_dumps(AQI_CATEGORIES)
    wind_info = wind_data or {"wind_speed": 5.4, "wind_direction": 290}
    wind_json = _safe_json_dumps(wind_info)
    bounds_json = _safe_json_dumps(NCR_BOUNDS)
    
    # Normalize basemap theme key
    theme_key = (basemap_theme or "positron").lower()
    if theme_key in ["light", "default", "positron (light retina)"]:
        theme_key = "positron"
    elif theme_key in ["dark", "dark matter", "dark_matter", "dark matter (neon)"]:
        theme_key = "dark_matter"
    elif theme_key in ["satellite", "hybrid", "satellite + roads (hybrid)", "satellite_hybrid"]:
        theme_key = "satellite_hybrid"
    elif theme_key in ["topo", "topographic"]:
        theme_key = "topographic"
    elif theme_key in ["streets", "openstreetmap"]:
        theme_key = "streets"
    
    # Normalize layer key
    layer_key = (active_layer or "fused").lower()
    if "smooth" in layer_key or "contour" in layer_key or "heat" in layer_key:
        layer_mode = "smooth"
    elif "aod" in layer_key:
        layer_mode = "aod"
    elif "gap" in layer_key:
        layer_mode = "gap_filled"
    elif "wind" in layer_key:
        layer_mode = "wind"
    else:
        layer_mode = "fused"

    sel_station_str = selected_station_name if selected_station_name else ""

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
            html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0b1120; overflow: hidden; }}
            
            #map-wrapper {{
                position: relative;
                width: 100%;
                height: {height}px;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25), 0 8px 10px -6px rgba(15, 23, 42, 0.15);
                border: 1px solid #cbd5e1;
            }}
            #map-wrapper.fullscreen {{
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                z-index: 999999 !important;
                border-radius: 0 !important;
                border: none !important;
            }}
            #map {{ width: 100%; height: 100%; background: #0f172a; }}
            
            /* Glassmorphic Floating HUD (Inspection Card) */
            .map-hud {{
                position: absolute;
                top: 14px;
                left: 14px;
                z-index: 1000;
                background: rgba(15, 23, 42, 0.90);
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 10px;
                padding: {'8px 12px' if is_overview else '10px 14px'};
                color: #ffffff;
                min-width: {'220px' if is_overview else '270px'};
                max-width: 320px;
                box-shadow: 0 16px 36px rgba(0,0,0,0.4);
                transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s ease;
                pointer-events: auto;
            }}
            .map-hud.collapsed .hud-body {{
                display: none;
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
                gap: 7px;
            }}
            .hud-live-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #10b981;
                box-shadow: 0 0 10px #10b981;
                animation: pulse-dot 2s infinite;
            }}
            @keyframes pulse-dot {{
                0% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.35; transform: scale(0.85); }}
                100% {{ opacity: 1; transform: scale(1); }}
            }}
            .hud-title {{
                font-size: {'11.5px' if is_overview else '12.5px'};
                font-weight: 700;
                letter-spacing: 0.2px;
                color: #f8fafc;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                max-width: 170px;
            }}
            .hud-actions {{
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            .hud-btn-toggle {{
                background: transparent;
                border: none;
                color: #94a3b8;
                font-size: 13px;
                font-weight: 700;
                cursor: pointer;
                padding: 0 4px;
                line-height: 1;
                border-radius: 4px;
            }}
            .hud-btn-toggle:hover {{
                color: #ffffff;
                background: rgba(255, 255, 255, 0.1);
            }}
            .hud-coords {{
                font-size: 10px;
                color: #94a3b8;
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
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
                font-size: 9px;
                font-weight: 600;
                color: #94a3b8;
                letter-spacing: 0.4px;
                text-transform: uppercase;
            }}
            .hud-val {{
                font-size: 12.5px;
                font-weight: 700;
                color: #f1f5f9;
            }}
            .hud-val-tag {{
                display: inline-block;
                padding: 2px 7px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 700;
                margin-top: 2px;
            }}

            /* Quick Action Toolbar Top Right */
            .map-top-bar {{
                position: absolute;
                top: 14px;
                right: 14px;
                z-index: 1000;
                display: flex;
                align-items: center;
                gap: 6px;
                flex-wrap: wrap;
                justify-content: flex-end;
            }}
            .map-btn-pill {{
                background: rgba(255, 255, 255, 0.94);
                backdrop-filter: blur(8px);
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 5px 9px;
                font-size: 11px;
                font-weight: 600;
                color: #1e293b;
                cursor: pointer;
                box-shadow: 0 3px 8px rgba(0,0,0,0.1);
                transition: all 0.15s ease;
                display: inline-flex;
                align-items: center;
                gap: 4px;
            }}
            .map-btn-pill:hover {{
                background: #0f766e;
                color: #ffffff;
                border-color: #0f766e;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25);
            }}
            .map-btn-pill.active {{
                background: #0f766e;
                color: #ffffff;
                border-color: #0f766e;
            }}

            /* Dropdown Basemap Menu inside Map */
            .basemap-menu-wrap {{
                position: relative;
                display: inline-block;
            }}
            .basemap-dropdown {{
                position: absolute;
                top: 100%;
                right: 0;
                margin-top: 4px;
                background: rgba(255, 255, 255, 0.97);
                backdrop-filter: blur(12px);
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 4px;
                min-width: 160px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                display: none;
                flex-direction: column;
                gap: 2px;
                z-index: 1010;
            }}
            .basemap-dropdown.show {{
                display: flex;
            }}
            .basemap-opt {{
                padding: 6px 10px;
                font-size: 11.5px;
                font-weight: 600;
                color: #1e293b;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.15s ease;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .basemap-opt:hover {{
                background: #f1f5f9;
                color: #0f766e;
            }}
            .basemap-opt.active {{
                background: #ccfbf1;
                color: #0f766e;
                font-weight: 700;
            }}

            /* Quick Landmark Bar */
            .landmark-bar {{
                position: absolute;
                top: 54px;
                right: 14px;
                z-index: 999;
                display: {'none' if is_overview else 'flex'};
                gap: 5px;
                flex-wrap: wrap;
                max-width: 480px;
                justify-content: flex-end;
            }}
            .landmark-chip {{
                background: rgba(255, 255, 255, 0.88);
                backdrop-filter: blur(6px);
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 3px 8px;
                font-size: 10.5px;
                font-weight: 600;
                color: #334155;
                cursor: pointer;
                transition: all 0.15s ease;
            }}
            .landmark-chip:hover {{
                background: #0f766e;
                color: #ffffff;
                border-color: #0f766e;
                transform: translateY(-1px);
            }}

            /* Map Legend Bottom Left */
            .map-legend-box {{
                position: absolute;
                bottom: 16px;
                left: 14px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: {'6px 10px' if is_overview else '8px 12px'};
                box-shadow: 0 4px 16px rgba(0,0,0,0.12);
                font-size: 11px;
                color: #1e293b;
                max-width: 320px;
            }}
            .legend-title {{
                font-weight: 700;
                font-size: 11px;
                margin-bottom: 4px;
                color: #0f172a;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}
            .legend-swatches {{
                display: flex;
                height: 10px;
                border-radius: 3px;
                overflow: hidden;
                margin-bottom: 3px;
                border: 1px solid #cbd5e1;
            }}
            .legend-swatch {{
                flex: 1;
                height: 100%;
            }}
            .legend-swatch-hatch {{
                width: 24px;
                height: 100%;
                background: repeating-linear-gradient(
                    45deg,
                    #64748b,
                    #64748b 2px,
                    #cbd5e1 2px,
                    #cbd5e1 5px
                );
            }}
            .legend-scale-labels {{
                display: flex;
                justify-content: space-between;
                font-size: 9px;
                color: #64748b;
                font-weight: 600;
                margin-bottom: 2px;
            }}
            .legend-subnote {{
                font-size: 9px;
                color: #64748b;
                display: {'none' if is_overview else 'block'};
            }}

            /* Telemetry & Zoom Label Bottom Right */
            .map-bottom-telemetry {{
                position: absolute;
                bottom: 16px;
                right: 14px;
                z-index: 1000;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .telemetry-chip {{
                background: rgba(255, 255, 255, 0.92);
                backdrop-filter: blur(8px);
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 3px 8px;
                font-size: 10.5px;
                color: #334155;
                font-weight: 600;
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
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
                box-shadow: 0 4px 12px rgba(0,0,0,0.35);
                transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
                z-index: 2;
            }}
            .station-pin-container:hover .station-pin-badge {{
                transform: scale(1.24);
                box-shadow: 0 6px 16px rgba(0,0,0,0.45);
            }}
            .station-pin-name {{
                font-size: 9.5px;
                font-weight: 700;
                color: #0f172a;
                background: rgba(255, 255, 255, 0.97);
                padding: 1px 5px;
                border-radius: 4px;
                border: 1px solid #cbd5e1;
                margin-top: 2px;
                white-space: nowrap;
                box-shadow: 0 2px 5px rgba(0,0,0,0.12);
                z-index: 2;
            }}
            
            /* Pulsing Radar Ring on Worst Hotspot / Anomaly */
            .radar-ripple {{
                position: absolute;
                top: 0;
                left: 0;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                border: 2.5px solid #ef4444;
                animation: ripple 2.2s cubic-bezier(0, 0.2, 0.8, 1) infinite;
                pointer-events: none;
                z-index: 1;
            }}
            .radar-ripple.delayed {{
                animation-delay: 1.1s;
            }}
            @keyframes ripple {{
                0% {{ transform: scale(0.9); opacity: 0.95; }}
                100% {{ transform: scale(2.8); opacity: 0; }}
            }}

            /* Animated Wind Streamlines */
            .wind-streamline {{
                pointer-events: none;
                animation: wind-flow 2.8s linear infinite;
            }}
            @keyframes wind-flow {{
                0% {{ transform: translate(0, 0) scale(0.9); opacity: 0.15; }}
                50% {{ opacity: 0.85; }}
                100% {{ transform: translate(var(--dx), var(--dy)) scale(1.05); opacity: 0; }}
            }}

            /* Leaflet popup styling */
            .leaflet-popup-content-wrapper {{
                background: #ffffff;
                border-radius: 10px;
                padding: 4px;
                box-shadow: 0 14px 30px rgba(0,0,0,0.22);
                border: 1px solid #e2e8f0;
            }}
            .custom-cell-popup {{
                padding: 6px 8px;
                font-family: inherit;
            }}
            .popup-station-name {{
                font-size: 13px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 2px;
            }}
            .popup-pm-val {{
                font-size: 19px;
                font-weight: 800;
                color: #ef4444;
                margin-bottom: 2px;
            }}
            .popup-category {{
                font-size: 11px;
                font-weight: 600;
                color: #64748b;
                margin-bottom: 5px;
            }}
            .popup-meta {{
                font-size: 10.5px;
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
        <div id="map-wrapper">
            <div id="map"></div>

            <!-- Floating Glassmorphic Inspection HUD -->
            <div class="map-hud" id="map-hud">
                <div class="hud-header">
                    <div class="hud-title-box">
                        <span class="hud-live-dot"></span>
                        <span class="hud-title" id="hud-title">Delhi-NCR 1 km Surface</span>
                    </div>
                    <div class="hud-actions">
                        <span class="hud-coords" id="hud-coords">28.614°N, 77.209°E</span>
                        <button class="hud-btn-toggle" onclick="toggleHud()" title="Collapse/Expand Telemetry">−</button>
                    </div>
                </div>
                <div class="hud-body" id="hud-body">
                    <div class="hud-grid">
                        <div class="hud-item">
                            <span class="hud-label">Estimated PM₂.₅</span>
                            <span class="hud-val" id="hud-pm">Hover over surface</span>
                        </div>
                        <div class="hud-item">
                            <span class="hud-label">Satellite AOD</span>
                            <span class="hud-val" id="hud-aod">--</span>
                        </div>
                        <div class="hud-item">
                            <span class="hud-label">Model Sigma (±σ)</span>
                            <span class="hud-val" id="hud-sigma">--</span>
                        </div>
                        <div class="hud-item">
                            <span class="hud-label">Data Ingestion</span>
                            <span class="hud-val" id="hud-source">--</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Top Action Toolbar -->
            <div class="map-top-bar">
                <!-- Basemap Switcher Menu -->
                <div class="basemap-menu-wrap">
                    <button class="map-btn-pill" onclick="toggleBasemapMenu()" id="btn-basemap">
                        🗺️ Basemap ▾
                    </button>
                    <div class="basemap-dropdown" id="basemap-dropdown">
                        <div class="basemap-opt" onclick="setBasemap('positron')">🏙️ Light Positron</div>
                        <div class="basemap-opt" onclick="setBasemap('dark_matter')">🌃 Dark Matter</div>
                        <div class="basemap-opt" onclick="setBasemap('satellite_hybrid')">🛰️ Satellite Hybrid</div>
                        <div class="basemap-opt" onclick="setBasemap('topographic')">⛰️ Topographic</div>
                        <div class="basemap-opt" onclick="setBasemap('streets')">🛣️ OpenStreetMap</div>
                    </div>
                </div>

                <!-- Layer Switcher Direct on Map -->
                <button class="map-btn-pill" onclick="toggleLayerSurface()" id="btn-layer-toggle" title="Switch Discrete 1km / Smooth Heat">
                    { "🔥 Smooth Heat" if layer_mode == "smooth" else "🟦 1 km Grid" }
                </button>

                <!-- Fullscreen Toggle -->
                <button class="map-btn-pill" onclick="toggleFullscreen()" title="Toggle Fullscreen">
                    ⛶ Expand
                </button>
            </div>

            <!-- Landmark Quick Navigation -->
            <div class="landmark-bar">
                <button class="landmark-chip" onclick="flyToLoc(28.6468, 77.3160, 13, 'Anand Vihar')">📍 Anand Vihar</button>
                <button class="landmark-chip" onclick="flyToLoc(28.7328, 77.1706, 13, 'Jahangirpuri')">📍 Jahangirpuri</button>
                <button class="landmark-chip" onclick="flyToLoc(28.6304, 77.2177, 13, 'Connaught Pl')">📍 Central Delhi</button>
                <button class="landmark-chip" onclick="flyToLoc(28.5562, 77.1000, 13, 'IGI Airport')">📍 IGI Airport</button>
                <button class="landmark-chip" onclick="flyToLoc(28.5300, 77.2700, 13, 'Okhla Hub')">📍 Okhla</button>
                <button class="landmark-chip" onclick="flyToLoc(28.4595, 77.0266, 13, 'Gurugram')">📍 Gurugram</button>
                <button class="landmark-chip" onclick="flyToLoc(28.5700, 77.3200, 13, 'Noida')">📍 Noida</button>
                <button class="landmark-chip" onclick="flyToLoc(28.6139, 77.2090, 10, 'Delhi-NCR')">🔄 NCR Full</button>
            </div>

            <!-- Bottom Left Legend -->
            <div class="map-legend-box">
                <div class="legend-title">
                    <span>PM<sub>2.5</sub> (µg/m³) · 1 km Surface</span>
                    <span style="font-weight:600; color:#0f766e; font-size:10px;">CPCB Scale</span>
                </div>
                <div class="legend-swatches">
                    <div class="legend-swatch" style="background:#10b981;" title="0-30 Good"></div>
                    <div class="legend-swatch" style="background:#84cc16;" title="31-60 Satisfactory"></div>
                    <div class="legend-swatch" style="background:#eab308;" title="61-90 Moderate"></div>
                    <div class="legend-swatch" style="background:#f97316;" title="91-120 Poor"></div>
                    <div class="legend-swatch" style="background:#ef4444;" title="121-250 Very Poor"></div>
                    <div class="legend-swatch" style="background:#7f1d1d;" title="250+ Severe"></div>
                    <div class="legend-swatch-hatch" title="Hatched: RF Gap-filled surface"></div>
                </div>
                <div class="legend-scale-labels">
                    <span>0</span><span>30</span><span>60</span><span>90</span><span>120</span><span>250+</span>
                </div>
                <div class="legend-subnote">Hatched = Gap-filled (Cloud/Haze) · Live cursor telemetry active</div>
            </div>

            <!-- Bottom Right Telemetry -->
            <div class="map-bottom-telemetry">
                <div class="telemetry-chip" id="wind-telemetry">
                    💨 {wind_info.get("wind_speed", 5.4)} m/s · {wind_info.get("wind_direction", 290)}° WNW
                </div>
                <div class="telemetry-chip" id="zoom-label">
                    Zoom 10
                </div>
            </div>
        </div>

        <script>
            var center = {DELHI_CENTER};
            var map = L.map('map', {{
                center: center,
                zoom: 10,
                zoomControl: true,
                attributionControl: false
            }});

            // Ensure crisp rendering across all screen resolutions and eliminate partial tile rendering
            setTimeout(function() {{ map.invalidateSize(); }}, 200);
            window.addEventListener('resize', function() {{ map.invalidateSize(); }});

            map.on('zoomend', function() {{
                document.getElementById('zoom-label').innerText = 'Zoom ' + map.getZoom();
            }});

            // Retina & High-Res Basemaps
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

            var currentBasemapKey = "{theme_key}";
            var activeBasemapLayer = basemaps[currentBasemapKey] || basemaps["positron"];
            activeBasemapLayer.addTo(map);

            window.setBasemap = function(key) {{
                if (basemaps[key]) {{
                    map.removeLayer(activeBasemapLayer);
                    activeBasemapLayer = basemaps[key];
                    activeBasemapLayer.addTo(map);
                    currentBasemapKey = key;
                    document.getElementById('basemap-dropdown').classList.remove('show');
                }}
            }};

            window.toggleBasemapMenu = function() {{
                var menu = document.getElementById('basemap-dropdown');
                menu.classList.toggle('show');
            }};

            document.addEventListener('click', function(e) {{
                var wrap = document.querySelector('.basemap-menu-wrap');
                if (wrap && !wrap.contains(e.target)) {{
                    document.getElementById('basemap-dropdown').classList.remove('show');
                }}
            }});

            window.toggleFullscreen = function() {{
                var el = document.getElementById('map-wrapper');
                el.classList.toggle('fullscreen');
                setTimeout(function() {{ map.invalidateSize(); }}, 250);
            }};

            window.toggleHud = function() {{
                var hud = document.getElementById('map-hud');
                hud.classList.toggle('collapsed');
            }};

            var gridData = {grid_json};
            var stationsData = {stations_json};
            var windInfo = {wind_json};
            var ncrBounds = {bounds_json};
            var layerMode = "{layer_mode}";
            var layerOpacity = {opacity};
            var showStations = {"true" if show_stations else "false"};
            var showAnomalies = {"true" if show_anomalies else "false"};
            var selectedStation = "{sel_station_str}";

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

            // 1. Smooth Heatmap Layer
            var heatLayer = null;
            var heatPoints = gridData.map(function(cell) {{
                return [cell.center_lat, cell.center_lon, Math.min(1.0, cell.pm25 / 240.0)];
            }});
            heatLayer = L.heatLayer(heatPoints, {{
                radius: 38,
                blur: 26,
                maxZoom: 14,
                max: 1.0,
                gradient: {{
                    0.12: '#10b981',
                    0.28: '#84cc16',
                    0.45: '#eab308',
                    0.65: '#f97316',
                    0.85: '#ef4444',
                    1.0: '#7f1d1d'
                }}
            }});

            if (layerMode === "smooth") {{
                heatLayer.addTo(map);
            }}

            // 2. Discrete 1 km Surface Rectangles
            var gridLayerGroup = L.layerGroup();
            gridData.forEach(function(cell) {{
                var bounds = [[cell.lat_min, cell.lon_min], [cell.lat_max, cell.lon_max]];
                var fillColor = cell.color;
                var fillOpacity = (layerMode === "smooth") ? 0.04 : layerOpacity;
                var strokeColor = (layerMode === "smooth") ? "transparent" : "#ffffff";
                var strokeWidth = (layerMode === "smooth") ? 0 : 0.35;

                if (layerMode === "aod") {{
                    var aodVal = cell.aod;
                    fillColor = aodVal > 0.85 ? "#b91c1c" : aodVal > 0.60 ? "#f97316" : aodVal > 0.35 ? "#eab308" : "#10b981";
                }} else if (layerMode === "gap_filled") {{
                    if (!cell.is_gap_filled) {{
                        fillOpacity = 0.05;
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
                }});

                // Gap-filled subtle hatch pattern overlay
                if (cell.is_gap_filled && layerMode !== "smooth") {{
                    L.rectangle(bounds, {{
                        color: "transparent",
                        weight: 0,
                        fillColor: "#0f172a",
                        fillOpacity: 0.20
                    }}).addTo(gridLayerGroup);
                }}

                // Hover interaction: Live update HUD
                rect.on('mouseover', function(e) {{
                    rect.setStyle({{ color: '#38bdf8', weight: 2.2 }});
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
                            <span>📡 Processing: <strong>${{cell.is_gap_filled ? 'Gap-Filled RF' : 'AOD Satellite Fused'}}</strong></span>
                        </div>
                    </div>
                `;
                rect.bindPopup(popupHtml);
                rect.addTo(gridLayerGroup);
            }});

            gridLayerGroup.addTo(map);

            // Toggle surface mode between Discrete and Smooth
            window.toggleLayerSurface = function() {{
                var btn = document.getElementById('btn-layer-toggle');
                if (map.hasLayer(heatLayer)) {{
                    map.removeLayer(heatLayer);
                    gridData.forEach(function(c) {{ /* restored */ }});
                    gridLayerGroup.eachLayer(function(l) {{
                        if (l.setStyle) {{
                            l.setStyle({{ fillOpacity: layerOpacity, weight: 0.35, color: '#ffffff' }});
                        }}
                    }});
                    btn.innerHTML = '🟦 1 km Grid';
                }} else {{
                    gridLayerGroup.eachLayer(function(l) {{
                        if (l.setStyle) {{
                            l.setStyle({{ fillOpacity: 0.04, weight: 0, color: 'transparent' }});
                        }}
                    }});
                    heatLayer.addTo(map);
                    btn.innerHTML = '🔥 Smooth Heat';
                }}
            }};

            // 3. Live Animated Wind Flow Streamlines
            if (layerMode === "wind" || { "true" if show_wind else "false" }) {{
                var windDir = windInfo.wind_direction || 290;
                var windSpd = windInfo.wind_speed || 5.4;
                var rad = (windDir * Math.PI) / 180.0;
                var dx = Math.round(-Math.sin(rad) * 28);
                var dy = Math.round(Math.cos(rad) * 28);

                var arrowSvg = `
                    <svg width="26" height="26" viewBox="0 0 26 26" fill="none" class="wind-streamline" style="--dx:${{dx}}px; --dy:${{dy}}px; transform: rotate(${{windDir + 90}}deg);">
                        <path d="M13 2L20 22L13 18L6 22L13 2Z" fill="#38bdf8" stroke="#ffffff" stroke-width="1.2" opacity="0.85"/>
                    </svg>
                `;
                
                var latSpan = ncrBounds.lat_max - ncrBounds.lat_min;
                var lonSpan = ncrBounds.lon_max - ncrBounds.lon_min;
                for (var r_idx = 1; r_idx <= 5; r_idx++) {{
                    for (var c_idx = 1; c_idx <= 5; c_idx++) {{
                        var wLat = ncrBounds.lat_min + (r_idx / 6) * latSpan;
                        var wLon = ncrBounds.lon_min + (c_idx / 6) * lonSpan;
                        
                        var windIcon = L.divIcon({{
                            html: arrowSvg,
                            className: 'wind-arrow-wrap',
                            iconSize: [26, 26],
                            iconAnchor: [13, 13]
                        }});
                        
                        L.marker([wLat, wLon], {{ icon: windIcon, interactive: false }}).addTo(map);
                    }}
                }}
            }}

            // 4. Station Markers with Numeric Badges & Dual Radar Ripples
            if (showStations) {{
                stationsData.forEach(function(st) {{
                    var isWorst = st.is_worst;
                    var isAnomaly = st.anomaly && showAnomalies;
                    var markerColor = st.pm25 >= 121 ? "#ef4444" : st.pm25 >= 91 ? "#f97316" : "#eab308";
                    
                    var badgeHtml = `
                        <div class="station-pin-container ${{isWorst ? 'worst-station' : ''}}">
                            ${{(isWorst || isAnomaly) ? '<div class="radar-ripple"></div><div class="radar-ripple delayed"></div>' : ''}}
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
                        map.flyTo([st.lat, st.lon], 13, {{ duration: 1.2 }});
                        hudTitle.innerText = st.name + ' (Ground Station)';
                        hudCoords.innerText = st.lat.toFixed(3) + '°N, ' + st.lon.toFixed(3) + '°E';
                        hudPm.innerHTML = `<span class="hud-val-tag" style="background:#fee2e2; color:#991b1b;">${{st.pm25}} µg/m³ (${{st.status}})</span>`;
                        hudAod.innerText = (st.aod || 0.48) + ' (Collocated)';
                        hudSigma.innerText = 'MAE ' + (st.loso_mae || 24.5) + ' µg/m³';
                        hudSource.innerText = st.source || 'CPCB Telemetry';
                    }});

                    var tooltipContent = `
                        <div style="font-family:sans-serif; padding:2px;">
                            <strong>${{st.name}}</strong><br>
                            PM₂.₅: <b>${{st.pm25}} µg/m³</b> (${{st.status}})<br>
                            <span style="font-size:10px; color:#64748b;">Telemetry: ${{st.source}}</span>
                        </div>
                    `;
                    marker.bindTooltip(tooltipContent, {{ direction: 'top', offset: [0, -16] }});
                }});
            }}

            // Auto-focus selected station if provided
            if (selectedStation) {{
                var targetSt = stationsData.find(function(s) {{ return s.name.toLowerCase() === selectedStation.toLowerCase(); }});
                if (targetSt) {{
                    setTimeout(function() {{
                        flyToLoc(targetSt.lat, targetSt.lon, 12, targetSt.name);
                    }}, 400);
                }}
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
    height: int = 420
):
    """
    Renders Enhanced Hotspot Map for Combined Insights.
    Overlays sector-coded glowing emission hotspots with thermal footprint rings,
    interactive facility telemetry HUD, fullscreen expander, and quick fly-to controls.
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
            * {{ box-sizing: border-box; }}
            body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0b1120; }}
            
            #hotspot-wrapper {{
                position: relative;
                width: 100%;
                height: {height}px;
                border-radius: 12px;
                overflow: hidden;
                border: 1px solid #cbd5e1;
                box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
            }}
            #hotspot-wrapper.fullscreen {{
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                z-index: 999999 !important;
                border-radius: 0 !important;
            }}
            #hotspot-map {{ width: 100%; height: 100%; background: #0f172a; }}
            
            /* Sector Coded Glowing Diamonds */
            .hotspot-marker {{
                border: 2px solid #ffffff;
                transform: rotate(45deg);
                border-radius: 4px;
                transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
                cursor: pointer;
            }}
            .hotspot-marker:hover {{
                transform: rotate(45deg) scale(1.35);
            }}
            .hotspot-power {{
                background: linear-gradient(135deg, #f59e0b, #d97706);
                box-shadow: 0 4px 14px rgba(217, 119, 6, 0.7);
            }}
            .hotspot-industry {{
                background: linear-gradient(135deg, #8b5cf6, #6d28d9);
                box-shadow: 0 4px 14px rgba(109, 40, 217, 0.7);
            }}
            .hotspot-transport {{
                background: linear-gradient(135deg, #0284c7, #0369a1);
                box-shadow: 0 4px 14px rgba(2, 132, 199, 0.7);
            }}
            .hotspot-waste {{
                background: linear-gradient(135deg, #10b981, #047857);
                box-shadow: 0 4px 14px rgba(16, 185, 129, 0.7);
            }}

            /* Quick Nav Bar */
            .hotspot-top-bar {{
                position: absolute;
                top: 14px;
                right: 14px;
                z-index: 1000;
                display: flex;
                gap: 5px;
            }}
            .hotspot-chip {{
                background: rgba(255, 255, 255, 0.94);
                backdrop-filter: blur(8px);
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 4px 9px;
                font-size: 11px;
                font-weight: 600;
                color: #334155;
                cursor: pointer;
                transition: all 0.15s ease;
            }}
            .hotspot-chip:hover {{
                background: #6d28d9;
                color: #ffffff;
                border-color: #6d28d9;
            }}

            /* Floating Legend */
            .hotspot-legend {{
                position: absolute;
                bottom: 16px;
                left: 14px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.96);
                backdrop-filter: blur(8px);
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 11px;
                color: #334155;
                box-shadow: 0 4px 12px rgba(0,0,0,0.12);
                max-width: 320px;
            }}
            .legend-item {{
                display: inline-flex;
                align-items: center;
                gap: 5px;
                margin-right: 10px;
                margin-top: 3px;
                font-size: 10.5px;
                font-weight: 600;
            }}
            .legend-badge {{
                width: 10px;
                height: 10px;
                transform: rotate(45deg);
                border-radius: 2px;
            }}
        </style>
    </head>
    <body>
        <div id="hotspot-wrapper">
            <div id="hotspot-map"></div>

            <div class="hotspot-top-bar">
                <button class="hotspot-chip" onclick="map.flyTo([28.5085, 77.3039], 13)">📍 Badarpur Hub</button>
                <button class="hotspot-chip" onclick="map.flyTo([28.5833, 77.5500], 13)">📍 Dadri NTPC</button>
                <button class="hotspot-chip" onclick="map.flyTo([28.7900, 77.0400], 13)">📍 Bawana Ind</button>
                <button class="hotspot-chip" onclick="map.flyTo([28.6139, 77.2090], 10)">🔄 NCR Full</button>
                <button class="hotspot-chip" onclick="toggleHotspotFullscreen()">⛶ Expand</button>
            </div>

            <div class="hotspot-legend">
                <div style="font-weight:700; color:#0f172a; margin-bottom:4px;">Climate TRACE Point Sources · kt CO₂e</div>
                <div>
                    <span class="legend-item"><span class="legend-badge" style="background:#f59e0b;"></span>Power</span>
                    <span class="legend-item"><span class="legend-badge" style="background:#8b5cf6;"></span>Industry</span>
                    <span class="legend-item"><span class="legend-badge" style="background:#0284c7;"></span>Transport</span>
                    <span class="legend-item"><span class="legend-badge" style="background:#10b981;"></span>Waste</span>
                </div>
            </div>
        </div>

        <script>
            var map = L.map('hotspot-map', {{
                center: {DELHI_CENTER},
                zoom: 10,
                zoomControl: true,
                attributionControl: false
            }});

            setTimeout(function() {{ map.invalidateSize(); }}, 200);
            window.addEventListener('resize', function() {{ map.invalidateSize(); }});

            window.toggleHotspotFullscreen = function() {{
                var el = document.getElementById('hotspot-wrapper');
                el.classList.toggle('fullscreen');
                setTimeout(function() {{ map.invalidateSize(); }}, 250);
            }};
            
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                maxZoom: 20,
                subdomains: 'abcd',
                detectRetina: true,
                attribution: '&copy; CARTO'
            }}).addTo(map);

            var gridData = {grid_json};
            var hotspotsData = {hotspots_json};

            // Draw faded 1km PM2.5 background surface
            gridData.forEach(function(cell) {{
                var bounds = [[cell.lat_min, cell.lon_min], [cell.lat_max, cell.lon_max]];
                L.rectangle(bounds, {{
                    color: "transparent",
                    weight: 0,
                    fillColor: cell.color,
                    fillOpacity: 0.30
                }}).addTo(map);
            }});

            // Draw emission hotspots with concentric plume rings
            hotspotsData.forEach(function(hs) {{
                var sec = (hs.sector || "Power").toLowerCase();
                var markerClass = sec.includes("ind") ? "hotspot-industry" : sec.includes("trans") ? "hotspot-transport" : sec.includes("waste") ? "hotspot-waste" : "hotspot-power";
                var color = sec.includes("ind") ? "#8b5cf6" : sec.includes("trans") ? "#0284c7" : sec.includes("waste") ? "#10b981" : "#f59e0b";

                // Concentric thermal plume footprint ring
                var radiusMeters = Math.min(6000, Math.max(1200, (hs.emissions_kt || 2000) * 0.7));
                L.circle([hs.lat, hs.lon], {{
                    radius: radiusMeters,
                    color: color,
                    weight: 1,
                    opacity: 0.45,
                    fillColor: color,
                    fillOpacity: 0.08
                }}).addTo(map);

                // Diamond icon
                var size = hs.marker_size || 24;
                var diamondIcon = L.divIcon({{
                    className: 'hotspot-marker ' + markerClass,
                    iconSize: [size, size],
                    iconAnchor: [size/2, size/2]
                }});

                var marker = L.marker([hs.lat, hs.lon], {{ icon: diamondIcon }}).addTo(map);
                marker.bindPopup(`
                    <div style="font-family:sans-serif; padding:4px;">
                        <div style="font-weight:700; font-size:14px; color:#0f172a;">${{hs.name}}</div>
                        <div style="font-size:12px; color:${{color}}; font-weight:700; margin:2px 0;">Sector: ${{hs.sector}}</div>
                        <div style="font-size:12px; color:#475569;">Annual CO₂e: <strong>${{hs.emissions_kt ? hs.emissions_kt.toLocaleString() : 'N/A'}} kt</strong></div>
                        <div style="font-size:10.5px; color:#64748b; margin-top:4px; border-top:1px solid #f1f5f9; padding-top:3px;">
                            Asset Source: Climate TRACE Facility Registry
                        </div>
                    </div>
                `);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height + 25)
