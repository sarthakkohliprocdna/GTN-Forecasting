import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.layout import page_header, next_button, kpi_card
from models.forecast_engine import DEDUCTIONS

def render_outputs():
    page_header("Forecast Outputs", "Review GTN forecast, Net Sales forecast, GTN %, and champion model performance.")
    if not st.session_state.forecast_ready or st.session_state.forecast_df is None:
        st.warning("Run the Forecast Engine before reviewing outputs.")
        next_button("Go to Forecast Engine →", "Forecast Engine", disabled=not st.session_state.data_loaded)
        return
    df = st.session_state.forecast_df.copy()
    gross, gtn, net = df["gross_sales"].sum(), df["total_gtn"].sum(), df["net_sales"].sum()
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Forecast Gross Sales", f"${gross/1e6:,.1f}M")
    with c2: kpi_card("Forecast GTN", f"${gtn/1e6:,.1f}M")
    with c3: kpi_card("Forecast GTN %", f"{gtn/gross:.1%}")
    with c4: kpi_card("Forecast Net Sales", f"${net/1e6:,.1f}M")
    left, right = st.columns([1.3, 1])
    with left:
        chart_df = df.melt(id_vars=["month"], value_vars=["gross_sales", "total_gtn", "net_sales"], var_name="Metric", value_name="Value")
        fig = px.line(chart_df, x="month", y="Value", color="Metric", title="12-Month Forecast")
        fig.update_layout(template="plotly_white", height=430)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        latest = df.iloc[-1]
        fig = go.Figure(go.Waterfall(name="GTN Rollup", orientation="v", measure=["absolute"] + ["relative"]*len(DEDUCTIONS) + ["total"], x=["Gross Sales"] + DEDUCTIONS + ["Net Sales"], y=[latest["gross_sales"]] + [-latest[d] for d in DEDUCTIONS] + [latest["net_sales"]]))
        fig.update_layout(title="Latest Month GTN Waterfall", template="plotly_white", height=430)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("### Champion Model Summary")
    st.dataframe(st.session_state.champion_df, use_container_width=True)
    next_button("Continue to Scenario Simulator →", "Scenario Simulator")
