# EcoPulse: A Satellite-Fused Air Quality and Carbon Intelligence Platform

An end-to-end geospatial ML pipeline that fuses satellite AOD, ground PM₂.₅, meteorology and emissions data into a continuous 1 km daily PM₂.₅ surface for Delhi-NCR, with forecasting, anomaly detection, carbon analytics and an interactive dashboard.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Objective](#objective)
3. [Quick Start & Installation](#quick-start--installation)
4. [Methodology](#methodology)
5. [Tech Stack](#tech-stack)
6. [Expected Outcomes](#expected-outcomes)
7. [Deployment](#deployment)

---

## Problem Statement

- **Ground stations are sparse.** CPCB monitoring stations give accurate PM₂.₅, but they cover only a small part of Delhi-NCR, leaving large areas unmonitored.
- **Satellite AOD is not PM₂.₅.** Aerosol Optical Depth (AOD) has continuous spatial coverage, but it measures the whole atmospheric column rather than ground-level PM₂.₅. It is also missing on many days because of cloud and haze.
- **Emissions are studied in isolation.** Emission inventories are coarse and are usually analysed separately from air quality.
- **No unified pipeline exists.** Nothing currently fuses these sources into a single, continuous, validated picture.

## Objective

Build an end-to-end geospatial ML pipeline that fuses satellite AOD, ground PM₂.₅, meteorology and emissions data to:

- estimate a continuous **1 km gridded daily PM₂.₅ surface** for Delhi-NCR,
- **forecast** it,
- **detect anomalies**, and
- deliver everything through **one interactive dashboard**.

---

## Quick Start & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ecopulse.git
cd ecopulse
```

### 2. Set up virtual environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment credentials (Optional)
Copy `.env.example` to `.env` and optionally add free API keys for live CPCB station streaming:
```bash
cp .env.example .env
```
*(The dashboard gracefully falls back to bundled real-world benchmark data and Open-Meteo feeds if no custom tokens are provided).*

### 5. Launch the application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## Methodology

### 1. Data Ingestion and Preprocessing

**Sources**

| Data | Source |
|------|--------|
| Satellite AOD (1 km) | MODIS MAIAC AOD (MCD19A2) |
| Ground PM₂.₅ | CPCB and OpenAQ stations |
| Meteorology | Open-Meteo / ERA5 (temperature, humidity, wind, boundary-layer height) |
| Emissions | Monthly sector emissions from Climate TRACE / EDGAR |

**Cleaning**

- QA-bit masking of AOD pixels
- Spatiotemporal collocation of AOD with stations
- Feature engineering

**Tooling:** Dask, Xarray and Rasterio for raster processing.

### 2. AOD-PM₂.₅ Fusion Model

- **Model:** Random Forest / XGBoost, using AOD plus meteorology and time features to predict ground PM₂.₅.
- **Baselines:** weather-only and AOD-only linear models.
- **Gap-filling:** a second model without AOD, used on days when AOD is missing.
- **Output:** a gridded daily PM₂.₅ surface.

### 3. Validation

- **Method:** leave-one-station-out cross-validation (GroupKFold by station).
- **Metrics:** R², RMSE and MAE for all models.
- **Interpretation:** SHAP to quantify the contribution of AOD relative to meteorology.

### 4. Forecasting and Anomaly Detection

- **Forecast:** 1-3 day PM₂.₅ forecast from lagged fused values plus forecast weather.
- **Anomalies:** residual-based flagging, where days deviating beyond 2-3σ are flagged. Isolation Forest is an optional second method.

### 5. Carbon Module

- **Sector trends:** Prophet / XGBoost versus a seasonal naive baseline, evaluated per sector.
- **Scenario:** a trend-based what-if for scenarios such as a 20% coal reduction, labelled *indicative*.
- **Combined Insights:** monthly correlation with PM₂.₅, presented as *indicative* and *not causal*.

### 6. Scenario Simulator

A sensitivity analysis that perturbs the model's real inputs (wind speed, boundary-layer height, temperature) and shows the resulting change in predicted PM₂.₅.

### 7. Dashboard

Built with **Streamlit + Folium/Plotly**, with three tabs:

1. **Air Quality:** fused map, forecast, anomalies
2. **Carbon:** sector trends and scenarios
3. **Combined Insights:** emissions vs PM₂.₅ relationships

---

## Tech Stack

| Area | Tools |
|------|-------|
| Raster / geospatial processing | Dask, Xarray, Rasterio |
| Modelling | Random Forest, XGBoost, scikit-learn |
| Forecasting | XGBoost, Prophet |
| Explainability | SHAP |
| Anomaly detection | Residual-based (2-3σ), Isolation Forest |
| Dashboard | Streamlit, Folium, Plotly |

---

## Expected Outcomes

- A validated 1 km daily PM₂.₅ surface with reported R², RMSE and MAE
- A quantified comparison of what satellite AOD adds beyond weather alone
- A working forecast and anomaly detection module
- A unified, interactive decision-support dashboard

---

## Deployment

### Streamlit Community Cloud (Recommended Free Hosting)
1. Push this repository to your GitHub account.
2. Visit [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
3. Click **"New app"**, select your repository, branch (`main`), and set the main file path to `app.py`.
4. (Optional) Under **Advanced settings > Secrets**, you can securely provide your `WAQI_API_TOKEN` and `OPENAQ_API_KEY` without exposing them in public code.
5. Click **"Deploy!"** to get a live, publicly accessible URL for your platform.

---

## Notes and Limitations

- Carbon scenarios and emissions-PM₂.₅ correlations are **indicative only** and do not imply causation.
- AOD is unavailable on cloudy or hazy days, so the AOD-free model is used for gap-filling.

