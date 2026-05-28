import pandas as pd
import streamlit as st
from components.layout import page_header
from models.model_registry import MODEL_ZOO

def render_model_zoo():
    page_header("Forecasting Model Zoo", "The platform benchmarks multiple forecasting approaches and selects the most appropriate strategy by GTN component.")
    df = pd.DataFrame(MODEL_ZOO)
    cols = st.columns(2)
    for idx, family in enumerate(df["family"].unique().tolist()):
        subset = df[df["family"] == family]
        items = "".join([f"<li><strong>{row['name']}</strong><br><span>{row['fit']}</span></li>" for _, row in subset.iterrows()])
        with cols[idx % 2]:
            st.markdown(f"<div class='card model-card'><h3>{family}</h3><ul>{items}</ul></div>", unsafe_allow_html=True)
    st.markdown("<div class='tip-box'>The goal is not to use every model blindly. The system benchmarks candidate approaches and selects champion models based on WMAPE, bias, stability, and business reasonability.</div>", unsafe_allow_html=True)
