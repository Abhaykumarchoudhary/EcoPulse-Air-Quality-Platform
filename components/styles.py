"""
CSS styles for EcoPulse.
Injects pixel-perfect custom styles into Streamlit to replicate the wireframe v2.1 design.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global Font & Reset */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

/* App Background & Typography */
.stApp {
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

[data-testid="stMain"] div[data-testid="stRadio"] label,
[data-testid="stMain"] div[data-testid="stRadio"] p,
[data-testid="stMain"] div[data-testid="stCheckbox"] label,
[data-testid="stMain"] div[data-testid="stCheckbox"] p,
[data-testid="stMain"] div[data-testid="stSelectbox"] label,
[data-testid="stMain"] div[data-testid="stSlider"] label,
[data-testid="stMain"] p {
    color: #1e293b !important;
    font-weight: 500 !important;
}

/* Header & Sidebar Controls - Zero height to eliminate vacant top void */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
    min-height: 0px !important;
    max-height: 0px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    overflow: visible !important;
    z-index: 99999 !important;
    pointer-events: none !important;
}
header[data-testid="stHeader"] * {
    pointer-events: auto !important;
}
#MainMenu, footer {
    visibility: hidden;
}

/* Sidebar Collapsed Re-Open Floating Logo Control */
[data-testid="stExpandSidebarButton"],
button[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[data-testid="baseButton-header"][aria-label="Expand sidebar"],
button[data-testid="baseButton-header"][aria-label="Open sidebar"],
button[aria-label="Expand sidebar"],
button[aria-label="Open sidebar"],
button[data-testid="stSidebarCollapseButton"][aria-expanded="false"] {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 9999999 !important;
    background: #0d1527 !important;
    color: #ffffff !important;
    border: 1.5px solid #14b8a6 !important;
    border-radius: 9999px !important;
    height: 42px !important;
    min-width: 42px !important;
    padding: 4px 14px 4px 6px !important;
    box-shadow: 0 4px 16px rgba(15, 118, 110, 0.4), 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    cursor: pointer !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 8px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    pointer-events: auto !important;
    text-decoration: none !important;
}

/* Hide Streamlit's default double-arrow icon and material symbol text */
[data-testid="stExpandSidebarButton"] svg,
button[data-testid="stExpandSidebarButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="collapsedControl"] svg,
button[aria-label="Expand sidebar"] svg,
button[aria-label="Open sidebar"] svg,
[data-testid="stExpandSidebarButton"] span,
button[data-testid="stExpandSidebarButton"] span,
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
button[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {
    display: none !important;
}

/* EcoPulse Glowing Pulse Emblem Logo on Left */
[data-testid="stExpandSidebarButton"]::before,
button[data-testid="stExpandSidebarButton"]::before,
[data-testid="stSidebarCollapsedControl"]::before,
[data-testid="collapsedControl"]::before,
button[aria-label="Expand sidebar"]::before,
button[aria-label="Open sidebar"]::before {
    content: "" !important;
    display: inline-block !important;
    width: 30px !important;
    height: 30px !important;
    flex-shrink: 0 !important;
    background-image: url("data:image/svg+xml;utf8,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2040%2040%22%20width%3D%2240%22%20height%3D%2240%22%20fill%3D%22none%22%3E%0A%20%20%3Cdefs%3E%0A%20%20%20%20%3ClinearGradient%20id%3D%22bgGrad%22%20x1%3D%220%25%22%20y1%3D%220%25%22%20x2%3D%22100%25%22%20y2%3D%22100%25%22%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%220%25%22%20stop-color%3D%22%230f766e%22/%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%2250%25%22%20stop-color%3D%22%23115e59%22/%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%22100%25%22%20stop-color%3D%22%23042f2e%22/%3E%0A%20%20%20%20%3C/linearGradient%3E%0A%20%20%20%20%3ClinearGradient%20id%3D%22pulseGrad%22%20x1%3D%220%25%22%20y1%3D%220%25%22%20x2%3D%22100%25%22%20y2%3D%220%25%22%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%220%25%22%20stop-color%3D%22%232dd4bf%22/%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%2250%25%22%20stop-color%3D%22%23ffffff%22/%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%22100%25%22%20stop-color%3D%22%235eead4%22/%3E%0A%20%20%20%20%3C/linearGradient%3E%0A%20%20%20%20%3Cfilter%20id%3D%22glow%22%20x%3D%22-20%25%22%20y%3D%22-20%25%22%20width%3D%22140%25%22%20height%3D%22140%25%22%3E%0A%20%20%20%20%20%20%3CfeDropShadow%20dx%3D%220%22%20dy%3D%220%22%20stdDeviation%3D%221.5%22%20flood-color%3D%22%232dd4bf%22%20flood-opacity%3D%220.6%22/%3E%0A%20%20%20%20%3C/filter%3E%0A%20%20%3C/defs%3E%0A%20%20%3Ccircle%20cx%3D%2220%22%20cy%3D%2220%22%20r%3D%2218%22%20fill%3D%22url%28%23bgGrad%29%22%20stroke%3D%22%2314b8a6%22%20stroke-width%3D%221.5%22/%3E%0A%20%20%3Ccircle%20cx%3D%2220%22%20cy%3D%2220%22%20r%3D%2213%22%20stroke%3D%22%2314b8a6%22%20stroke-width%3D%220.8%22%20stroke-dasharray%3D%222%203%22%20opacity%3D%220.4%22/%3E%0A%20%20%3Cpath%20d%3D%22M%208%2020%20H%2012.5%20L%2014.8%2014.5%20L%2017.5%2024.5%20L%2020.8%2010%20L%2023.8%2027%20L%2026.2%2016.5%20L%2028%2020%20H%2032%22%20stroke%3D%22url%28%23pulseGrad%29%22%20stroke-width%3D%222.2%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%20filter%3D%22url%28%23glow%29%22/%3E%0A%20%20%3Ccircle%20cx%3D%2220.8%22%20cy%3D%2210%22%20r%3D%221.8%22%20fill%3D%22%235eead4%22/%3E%0A%3C/svg%3E") !important;
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    filter: drop-shadow(0 0 4px rgba(45, 212, 191, 0.4)) !important;
}

/* EcoPulse Wordmark + Slide Chevron */
[data-testid="stExpandSidebarButton"]::after,
button[data-testid="stExpandSidebarButton"]::after,
[data-testid="stSidebarCollapsedControl"]::after,
[data-testid="collapsedControl"]::after,
button[aria-label="Expand sidebar"]::after,
button[aria-label="Open sidebar"]::after {
    content: "EcoPulse ❯" !important;
    font-size: 13.5px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    letter-spacing: -0.01em !important;
    white-space: nowrap !important;
}

/* Hover: Interactive Slide Right & Glowing Effect */
[data-testid="stExpandSidebarButton"]:hover,
button[data-testid="stExpandSidebarButton"]:hover,
[data-testid="stSidebarCollapsedControl"]:hover,
[data-testid="collapsedControl"]:hover,
button[aria-label="Expand sidebar"]:hover,
button[aria-label="Open sidebar"]:hover {
    background: #111d38 !important;
    border-color: #2dd4bf !important;
    box-shadow: 0 6px 24px rgba(20, 184, 166, 0.55), 0 0 16px rgba(45, 212, 191, 0.35) !important;
    transform: translateX(4px) !important;
}

/* Active / Click effect */
[data-testid="stExpandSidebarButton"]:active,
button[data-testid="stExpandSidebarButton"]:active,
[data-testid="stSidebarCollapsedControl"]:active,
[data-testid="collapsedControl"]:active {
    transform: scale(0.96) !important;
}

/* Inside Sidebar Collapse Button */
[data-testid="stSidebarCollapseButton"] button,
button[aria-label="Collapse sidebar"],
[data-testid="stSidebarHeader"] button {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    padding: 6px 8px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebarCollapseButton"] button:hover,
button[aria-label="Collapse sidebar"]:hover,
[data-testid="stSidebarHeader"] button:hover {
    background: #0f766e !important;
    border-color: #14b8a6 !important;
    color: #ffffff !important;
    transform: scale(1.05) !important;
}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarHeader"] button svg {
    color: #cbd5e1 !important;
    fill: currentColor !important;
    stroke: currentColor !important;
}

/* Ultra-smooth Sidebar Slide Transition & Full Width Layout */
section[data-testid="stSidebar"]:not([data-collapsed="true"]) {
    background-color: #0d1527 !important;
    color: #e2e8f0 !important;
    border-right: 1px solid #1e293b !important;
    min-width: 270px !important;
    max-width: 320px !important;
    width: 300px !important;
    z-index: 1000 !important;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), margin-left 0.35s cubic-bezier(0.16, 1, 0.3, 1), width 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

/* When sidebar is put aside / collapsed: take 0 width so right side expands to 100% full page */
section[data-testid="stSidebar"][data-collapsed="true"],
section[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0px !important;
    min-width: 0px !important;
    max-width: 0px !important;
    padding: 0px !important;
    margin: 0px !important;
    border: none !important;
    flex: 0 0 0px !important;
    overflow: hidden !important;
    visibility: hidden !important;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), margin-left 0.35s cubic-bezier(0.16, 1, 0.3, 1), width 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

/* Main content area takes 100% full width */
[data-testid="stMain"],
.stMain {
    width: 100% !important;
    max-width: 100% !important;
    flex: 1 1 100% !important;
    transition: width 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

/* Remove unnecessary vacant top space & expand main block container to full width */
.block-container,
[data-testid="stMainBlockContainer"],
.stMainBlockContainer {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
    width: 100% !important;
}

/* When sidebar is collapsed, top padding accommodates the floating EcoPulse logo pill cleanly */
div.stAppViewContainer:has(section[data-testid="stSidebar"][data-collapsed="true"]) .block-container,
div.stAppViewContainer:has(section[data-testid="stSidebar"][data-collapsed="true"]) [data-testid="stMainBlockContainer"],
div.stAppViewContainer:has(section[data-testid="stSidebar"][aria-expanded="false"]) .block-container,
div.stAppViewContainer:has(section[data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stMainBlockContainer"] {
    padding-top: 3.5rem !important;
}

/* Streamlit Bordered Container Styling to match wireframe cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    margin-bottom: 14px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    padding: 16px 18px !important;
}
section[data-testid="stSidebar"] div.stSelectbox label,
section[data-testid="stSidebar"] div.stDateInput label {
    color: #94a3b8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #1a233a !important;
    border: 1px solid #334155 !important;
    color: #f8fafc !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #f8fafc !important;
}
section[data-testid="stSidebar"] div[data-baseweb="popover"] {
    background-color: #1a233a !important;
}

/* Sidebar Brand */
.sidebar-brand-container {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 0 20px 0;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 20px;
}
.sidebar-logo-circle {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.sidebar-brand-text-box {
    display: flex;
    flex-direction: column;
}
.sidebar-brand-title {
    font-size: 21px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.sidebar-brand-title span {
    color: #2dd4bf;
}
.sidebar-brand-subtitle {
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #64748b;
    margin-top: 3px;
}

/* Custom Nav Links in Sidebar */
.nav-item-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    color: #94a3b8;
    text-decoration: none;
    margin-bottom: 6px;
    transition: all 0.15s ease;
    cursor: pointer;
}
.nav-item-btn:hover {
    background: #1e293b;
    color: #ffffff;
}
.nav-item-btn.active {
    background: #0f766e !important;
    color: #ffffff !important;
    font-weight: 600;
}

/* Filters Header */
.sidebar-section-title {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 24px 0 12px 0;
}

/* Reset Filters Outline Button */
.reset-filter-btn {
    border: 1px solid #0f766e;
    color: #2dd4bf;
    background: transparent;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    text-align: center;
    width: 100%;
    margin-top: 14px;
    cursor: pointer;
    transition: all 0.2s;
}
.reset-filter-btn:hover {
    background: rgba(15, 118, 110, 0.15);
    color: #5eead4;
}

/* Top Bar / Header */
.top-header-bar {
    display: flex !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    margin-top: 0px !important;
    margin-bottom: 10px !important;
    padding: 0 !important;
}
.header-title-box {
    margin: 0 !important;
    padding: 0 !important;
}
.header-title-box h1 {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.15 !important;
}
.header-title-box p {
    font-size: 13px !important;
    color: #64748b !important;
    margin: 3px 0 0 0 !important;
    padding: 0 !important;
    line-height: 1.25 !important;
}
.header-badges-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-top: 2px;
}
.badge-demo {
    background: #e2e8f0;
    color: #475569;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 500;
}
.badge-date {
    font-size: 12px;
    color: #64748b;
}
.badge-location {
    background: #ffffff;
    border: 1px solid #10b981;
    color: #047857;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Card Container Wrappers */
[data-testid="stMain"] div[data-testid="stVerticalBlock"]:has(.map-card-header),
[data-testid="stMain"] div[data-testid="stVerticalBlock"]:has(.sparkline-card-header),
[data-testid="stMain"] div[data-testid="stVerticalBlock"]:has(.about-card-content),
[data-testid="stMain"] div[data-testid="stVerticalBlock"]:has(.pipeline-flow-container),
[data-testid="stMain"] div[data-testid="stVerticalBlock"].st-emotion-cache-1s3lgy2,
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    padding: 16px 18px !important;
    margin-bottom: 14px !important;
}

/* Metric Cards with Accent Left Borders */
.metric-card-wrapper {
    background: #ffffff;
    border-radius: 8px;
    padding: 15px 18px 14px 18px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    border: 1px solid #e2e8f0;
    height: 100%;
    position: relative;
    overflow: hidden;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.metric-card-wrapper:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-1px);
}
.border-accent-orange { border-left: 4px solid #f97316 !important; }
.border-accent-red    { border-left: 4px solid #ef4444 !important; }
.border-accent-amber  { border-left: 4px solid #eab308 !important; }
.border-accent-teal   { border-left: 4px solid #0f766e !important; }

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.metric-label {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.metric-icon {
    font-size: 15px;
    color: #94a3b8;
}
.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.1;
    margin-bottom: 6px;
}
.metric-subtext {
    font-size: 12px;
    color: #64748b;
    font-weight: 500;
}
.metric-subtext.change-red {
    color: #dc2626;
    font-weight: 600;
}

/* White Content Container Card */
.content-box-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    border: 1px solid #e2e8f0;
    margin-bottom: 20px;
}
.card-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}
.card-title-text {
    font-size: 17px;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 6px;
}
.card-actions-row {
    display: flex;
    align-items: center;
    gap: 8px;
}
.pill-btn-small {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    color: #475569;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
}
.pill-btn-small:hover {
    background: #e2e8f0;
}
.help-circle-btn {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 1px solid #cbd5e1;
    color: #64748b;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    background: #f8fafc;
}

/* Sub-Navigation Tabs (Air Quality Subviews) */
.subnav-tabs-container {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}
.subnav-tab-pill {
    padding: 8px 18px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: #475569;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.15s ease;
}
.subnav-tab-pill:hover {
    border-color: #0f766e;
    color: #0f766e;
}
.subnav-tab-pill.active {
    background: #0f766e !important;
    border-color: #0f766e !important;
    color: #ffffff !important;
}

/* Alert Banners */
.alert-banner-amber {
    background: #fffbeb;
    border: 1.5px solid #f59e0b;
    border-radius: 8px;
    padding: 12px 16px;
    color: #92400e;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Pipeline Diagram Stepper */
.pipeline-flow-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 14px 0;
}
.pipeline-step-card {
    flex: 1;
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.pipeline-step-teal {
    background: #ccfbf1;
    border: 1.5px solid #14b8a6;
}
.pipeline-step-white {
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
}
.pipeline-step-icon {
    font-size: 18px;
    margin-bottom: 4px;
}
.pipeline-step-title {
    font-size: 14px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2px;
}
.pipeline-step-subtitle {
    font-size: 12px;
    color: #475569;
}
.pipeline-arrow {
    font-size: 20px;
    color: #0f766e;
    font-weight: 800;
}

/* Footer Attribution */
.app-footer-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #64748b;
    padding-top: 14px;
    border-top: 1px solid #e2e8f0;
    margin-top: 12px;
}
.app-footer-row a {
    color: #0f766e;
    text-decoration: none;
    font-weight: 600;
}

/* Primary Button Styling */
button[kind="primary"], .btn-teal-primary {
    background-color: #0f766e !important;
    border-color: #0f766e !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
button[kind="primary"]:hover, .btn-teal-primary:hover {
    background-color: #115e59 !important;
}

/* Secondary / Outline Button */
button[kind="secondary"], .btn-outline {
    border: 1px solid #cbd5e1 !important;
    background-color: #ffffff !important;
    color: #334155 !important;
    border-radius: 8px !important;
}

/* Leaflet Map Hatch Pattern CSS */
.leaflet-container {
    border-radius: 8px;
}

/* Live API Badges and Telemetry Bar */
.badge-live {
    background: #ecfdf5 !important;
    border: 1px solid #10b981 !important;
    color: #047857 !important;
    padding: 4px 12px !important;
    border-radius: 9999px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 7px !important;
}

.pulse-dot-green {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    animation: pulseLiveGreen 1.8s infinite;
}

@keyframes pulseLiveGreen {
    0% {
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    }
    70% {
        box-shadow: 0 0 0 7px rgba(16, 185, 129, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
    }
}

.live-telemetry-strip {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
    padding: 8px 14px;
    margin-bottom: 14px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 12.5px;
    color: #166534;
}

.live-telemetry-strip .item-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-weight: 500;
}

.live-telemetry-strip .item-chip strong {
    font-weight: 700;
    color: #14532d;
}

.sidebar-live-card {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 8px;
    padding: 10px 12px;
    margin-top: 8px;
    margin-bottom: 12px;
}

.sidebar-live-card .title {
    font-size: 12px;
    font-weight: 700;
    color: #34d399;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
}

.sidebar-live-card .meta {
    font-size: 10.5px;
    color: #94a3b8;
    line-height: 1.35;
}

/* ========================================================================= */
/* ECOPULSE RESPONSIVE DESIGN & MOBILE BREAKPOINTS                           */
/* Fluid adaptation across Desktop (>1024px), Tablet (768-1024px), & Mobile (<768px) */
/* ========================================================================= */

/* General Fluid Adjustments */
img, svg, iframe, .element-container {
    max-width: 100% !important;
}

[data-testid="stPlotlyChart"], .js-plotly-plot, .plot-container {
    width: 100% !important;
    max-width: 100% !important;
}

/* TABLET BREAKPOINT (max-width: 1024px) */
@media (max-width: 1024px) {
    .block-container,
    [data-testid="stMainBlockContainer"],
    .stMainBlockContainer {
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        padding-top: 0.85rem !important;
        padding-bottom: 1.5rem !important;
    }

    .top-header-bar {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
    }

    .header-badges-row {
        flex-wrap: wrap !important;
        gap: 6px !important;
    }

    /* Metric cards: 2x2 grid on tablet */
    div[data-testid="stHorizontalBlock"]:has(.metric-card-wrapper) {
        flex-wrap: wrap !important;
        gap: 12px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.metric-card-wrapper) > [data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:has(.metric-card-wrapper) > div[data-testid="column"] {
        min-width: calc(50% - 8px) !important;
        flex: 1 1 calc(50% - 8px) !important;
        margin-bottom: 4px !important;
    }

    .metric-value {
        font-size: 24px !important;
    }
}

/* MOBILE LANDSCAPE & TABLET PORTRAIT (max-width: 860px) */
@media (max-width: 860px) {
    /* Stack multi-column layout blocks to single column */
    div[data-testid="stHorizontalBlock"]:not(:has(.metric-card-wrapper)):not(:has(button[key^="btn_subtab_"])) {
        flex-wrap: wrap !important;
        gap: 14px !important;
    }
    div[data-testid="stHorizontalBlock"]:not(:has(.metric-card-wrapper)):not(:has(button[key^="btn_subtab_"])) > [data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:not(:has(.metric-card-wrapper)):not(:has(button[key^="btn_subtab_"])) > div[data-testid="column"] {
        min-width: 100% !important;
        width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 6px !important;
    }

    /* Air Quality subtabs: wrap 2 per row */
    div[data-testid="stHorizontalBlock"]:has(button[key^="btn_subtab_"]) {
        flex-wrap: wrap !important;
        gap: 6px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(button[key^="btn_subtab_"]) > [data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:has(button[key^="btn_subtab_"]) > div[data-testid="column"] {
        min-width: calc(50% - 4px) !important;
        flex: 1 1 calc(50% - 4px) !important;
        margin-bottom: 4px !important;
    }
}

/* SMARTPHONE & NARROW SCREENS (max-width: 768px) */
@media (max-width: 768px) {
    .block-container,
    [data-testid="stMainBlockContainer"],
    .stMainBlockContainer {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 0.75rem !important;
        padding-bottom: 1.25rem !important;
    }

    /* Sidebar Mobile Overlay */
    section[data-testid="stSidebar"]:not([data-collapsed="true"]) {
        min-width: 260px !important;
        max-width: 86vw !important;
        width: 86vw !important;
        box-shadow: 0 0 35px rgba(0, 0, 0, 0.6) !important;
        z-index: 100000 !important;
    }

    /* Floating Re-Open Sidebar Control Pill */
    [data-testid="stExpandSidebarButton"],
    button[data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    button[data-testid="baseButton-header"][aria-label="Expand sidebar"],
    button[data-testid="baseButton-header"][aria-label="Open sidebar"],
    button[aria-label="Expand sidebar"],
    button[aria-label="Open sidebar"],
    button[data-testid="stSidebarCollapseButton"][aria-expanded="false"] {
        top: 8px !important;
        left: 8px !important;
        height: 36px !important;
        min-width: 36px !important;
        padding: 3px 10px 3px 5px !important;
        font-size: 12px !important;
    }
    [data-testid="stExpandSidebarButton"]::before,
    button[data-testid="stExpandSidebarButton"]::before {
        width: 24px !important;
        height: 24px !important;
    }
    [data-testid="stExpandSidebarButton"]::after,
    button[data-testid="stExpandSidebarButton"]::after {
        font-size: 12px !important;
        content: "EcoPulse" !important;
    }

    /* Top Header Bar */
    .top-header-bar {
        margin-bottom: 8px !important;
    }
    .header-title-box h1 {
        font-size: 18px !important;
    }
    .header-title-box p {
        font-size: 11.5px !important;
    }
    .header-badges-row {
        gap: 5px !important;
        padding-top: 0 !important;
    }
    .badge-demo,
    .badge-date,
    .badge-location,
    .badge-live {
        font-size: 10.5px !important;
        padding: 2.5px 8px !important;
    }

    /* Content Cards */
    .content-box-card {
        padding: 12px 14px !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
    }
    .card-header-row {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 6px !important;
        margin-bottom: 10px !important;
    }
    .card-title-text {
        font-size: 14.5px !important;
    }
    .card-actions-row {
        width: 100% !important;
        justify-content: flex-start !important;
        flex-wrap: wrap !important;
    }

    /* Stepper: Responsive Vertical Flow on Mobile */
    .pipeline-flow-container {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 6px !important;
        padding: 6px 0 !important;
    }
    .pipeline-step-card {
        width: 100% !important;
        flex: none !important;
        padding: 10px 12px !important;
    }
    .pipeline-step-title {
        font-size: 13px !important;
    }
    .pipeline-step-subtitle {
        font-size: 11px !important;
    }
    .pipeline-arrow {
        transform: rotate(90deg) !important;
        margin: 0 auto !important;
        font-size: 16px !important;
        line-height: 1 !important;
    }

    /* Subnav Tabs: Touch Horizontal Scroll */
    .subnav-tabs-container {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        flex-wrap: nowrap !important;
        padding-bottom: 6px !important;
        gap: 8px !important;
        scrollbar-width: none !important;
    }
    .subnav-tabs-container::-webkit-scrollbar {
        display: none !important;
    }
    .subnav-tab-pill {
        white-space: nowrap !important;
        font-size: 11.5px !important;
        padding: 6px 12px !important;
        flex-shrink: 0 !important;
    }

    /* Telemetry strip */
    .live-telemetry-strip {
        font-size: 11px !important;
        padding: 8px 10px !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 4px !important;
    }
    .live-telemetry-strip .item-chip {
        font-size: 11px !important;
    }

    /* Tables & DataFrames */
    [data-testid="stDataFrame"],
    [data-testid="stTable"],
    div.stDataFrame {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        max-width: 100% !important;
    }

    /* Metric Cards Typography */
    .metric-card-wrapper {
        padding: 12px 14px !important;
    }
    .metric-value {
        font-size: 22px !important;
        margin-bottom: 3px !important;
    }
    .metric-label {
        font-size: 10px !important;
    }
    .metric-subtext {
        font-size: 11px !important;
    }
}

/* ULTRA COMPACT PHONES (max-width: 480px) */
@media (max-width: 480px) {
    .block-container,
    [data-testid="stMainBlockContainer"],
    .stMainBlockContainer {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 0.5rem !important;
    }

    /* Stack metric cards to 1 column on tiny screens */
    div[data-testid="stHorizontalBlock"]:has(.metric-card-wrapper) > [data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:has(.metric-card-wrapper) > div[data-testid="column"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 8px !important;
    }

    /* Air Quality subtabs: single button stack on very small screens */
    div[data-testid="stHorizontalBlock"]:has(button[key^="btn_subtab_"]) > [data-testid="stColumn"],
    div[data-testid="stHorizontalBlock"]:has(button[key^="btn_subtab_"]) > div[data-testid="column"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Alert Banners */
    .alert-banner-amber {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 6px !important;
        font-size: 11.5px !important;
        padding: 8px 12px !important;
    }

    /* Footer */
    .app-footer-row {
        flex-direction: column !important;
        gap: 4px !important;
        text-align: center !important;
        font-size: 10.5px !important;
    }
}
</style>
"""
