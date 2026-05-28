from pathlib import Path
import pandas as pd
import streamlit as st
from components.layout import page_header, status_panel, next_button
from utils.validators import validate_actuals
from utils.data_loader import load_actuals

def _load_demo_data():
    df = load_actuals("data/gtn_actuals.csv")
    st.session_state.actuals_df = df
    st.session_state.data_loaded = True
    st.session_state.data_mode = "Demo dataset"
    st.session_state.forecast_ready = False
    st.session_state.forecast_results = None
    st.session_state.forecast_df = None
    st.session_state.champion_df = None

def render_data_intake():
    page_header("Data Intake", "Start with the built-in demo dataset or upload historical GTN actuals using the required template.")
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown("<div class='card'><div class='step-number'>1</div><h3>Choose Data Source</h3><p>Use demo data for a walkthrough, or upload client GTN actuals. The system validates the file structure before forecasting.</p></div>", unsafe_allow_html=True)
        d1, d2, d3 = st.columns(3)
        for col, path, label, fname in [
            (d1, "templates/gtn_actuals_template.csv", "Download GTN Template", "gtn_actuals_template.csv"),
            (d2, "templates/forecast_drivers_template.csv", "Download Drivers Template", "forecast_drivers_template.csv"),
            (d3, "templates/contract_assumptions_template.csv", "Download Contract Template", "contract_assumptions_template.csv"),
        ]:
            with col:
                p = Path(path)
                if p.exists():
                    st.download_button(label, p.read_bytes(), file_name=fname, mime="text/csv", use_container_width=True)
        st.markdown("### Option 1: Use Demo Dataset")
        if st.button("Use Demo Dataset", type="primary", use_container_width=True):
            _load_demo_data()
            st.success("Demo dataset loaded successfully.")
        st.markdown("### Option 2: Upload Historical GTN Actuals")
        uploaded = st.file_uploader("Upload completed GTN actuals CSV", type=["csv"])
        if uploaded is not None:
            df = pd.read_csv(uploaded)
            valid, message = validate_actuals(df)
            if valid:
                df["month"] = pd.to_datetime(df["month"])
                st.session_state.actuals_df = df
                st.session_state.data_loaded = True
                st.session_state.data_mode = "Uploaded client data"
                st.session_state.forecast_ready = False
                st.success(message)
            else:
                st.error(message)
        if st.session_state.data_loaded and st.session_state.actuals_df is not None:
            st.markdown("### Data Preview")
            st.dataframe(st.session_state.actuals_df.head(10), use_container_width=True)
    with right:
        status_panel()
        st.markdown("<div class='tip-box'><strong>Next step</strong><br>Continue to the Forecast Engine once data is loaded.</div>", unsafe_allow_html=True)
    next_button("Continue to Forecast Engine →", "Forecast Engine", disabled=not st.session_state.data_loaded)
