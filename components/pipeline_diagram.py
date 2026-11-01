"""
Pipeline Stepper Diagram and Project Footer Component for EcoPulse.
Directly matches Wireframe 1 reference layout.
"""
import streamlit as st

def render_pipeline_stepper():
    pipeline_html = (
        '<div style="padding: 2px 4px;">'
        '<div class="pipeline-flow-container">'
        '<div class="pipeline-step-card pipeline-step-teal">'
        '<div class="pipeline-step-icon">🛰️</div>'
        '<div class="pipeline-step-title">Collect</div>'
        '<div class="pipeline-step-subtitle">AOD, CPCB, weather</div>'
        '</div>'
        '<div class="pipeline-arrow">→</div>'
        '<div class="pipeline-step-card pipeline-step-white">'
        '<div class="pipeline-step-icon">❇️</div>'
        '<div class="pipeline-step-title">Fuse</div>'
        '<div class="pipeline-step-subtitle">Collocate and QA-mask</div>'
        '</div>'
        '<div class="pipeline-arrow">→</div>'
        '<div class="pipeline-step-card pipeline-step-teal">'
        '<div class="pipeline-step-icon">📈</div>'
        '<div class="pipeline-step-title">Predict</div>'
        '<div class="pipeline-step-subtitle">RF/XGBoost + gap-fill</div>'
        '</div>'
        '<div class="pipeline-arrow">→</div>'
        '<div class="pipeline-step-card pipeline-step-white">'
        '<div class="pipeline-step-icon">🗺️</div>'
        '<div class="pipeline-step-title">Map</div>'
        '<div class="pipeline-step-subtitle">1 km PM₂.₅ grid</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(pipeline_html, unsafe_allow_html=True)
