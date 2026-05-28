import streamlit as st
import plotly.express as px
from components.layout import page_header, status_panel, next_button
from models.forecast_engine import run_forecast

def render_forecast_engine():
    page_header("Forecast Engine", "Benchmark multiple forecasting models and select the champion model for each GTN component.")
    if not st.session_state.data_loaded or st.session_state.actuals_df is None:
        st.warning("Load data before running the forecast engine.")
        next_button("Go to Data Intake →", "Data Intake")
        return
    brands = ["All Brands"] + sorted(st.session_state.actuals_df["brand"].dropna().unique().tolist())
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown("<div class='card'><div class='step-number'>2</div><h3>Run Champion Model Selection</h3><p>The engine benchmarks candidate models by GTN component, evaluates WMAPE, bias, and stability, and generates a 12-month forecast.</p></div>", unsafe_allow_html=True)
        selected_brand = st.selectbox("Forecast Brand", brands)
        st.session_state.selected_brand = selected_brand
        if st.button("Run Forecast Engine", type="primary", use_container_width=True):
            with st.spinner("Benchmarking model zoo and generating forecasts..."):
                results = run_forecast(st.session_state.actuals_df, brand=selected_brand, horizon=12)
                st.session_state.forecast_results = results
                st.session_state.forecast_df = results["forecast_df"]
                st.session_state.champion_df = results["champion_df"]
                st.session_state.forecast_ready = True
            st.success("Forecast generated successfully.")
        if st.session_state.forecast_ready and st.session_state.champion_df is not None:
            st.markdown("### Champion Models")
            st.dataframe(st.session_state.champion_df, use_container_width=True)
            fig = px.bar(st.session_state.champion_df, x="GTN Component", y="WMAPE", color="Champion Model", title="Champion Model WMAPE by Component")
            fig.update_layout(template="plotly_white", height=430)
            st.plotly_chart(fig, use_container_width=True)
    with right:
        status_panel()
        st.markdown("<div class='tip-box'><strong>Model selection</strong><br>Each component can use a different model depending on its historical pattern.</div>", unsafe_allow_html=True)
    next_button("Continue to Outputs →", "Outputs", disabled=not st.session_state.forecast_ready)
