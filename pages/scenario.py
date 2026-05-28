import streamlit as st
import pandas as pd
import plotly.express as px
from components.layout import page_header, next_button, kpi_card
from models.forecast_engine import DEDUCTIONS

def render_scenario():
    page_header("Scenario Simulator", "Adjust business assumptions and review directional impact on GTN and Net Sales.")
    if not st.session_state.forecast_ready or st.session_state.forecast_df is None:
        st.warning("Generate a forecast before running scenarios.")
        next_button("Go to Forecast Engine →", "Forecast Engine", disabled=not st.session_state.data_loaded)
        return
    base = st.session_state.forecast_df.copy()
    left, right = st.columns([1, 1.35])
    with left:
        st.markdown("<div class='card'><div class='step-number'>4</div><h3>Configure Scenario</h3><p>Adjust assumptions to estimate directional impact on GTN and Net Sales.</p></div>", unsafe_allow_html=True)
        price = st.slider("Price Increase %", -5, 20, 3)
        volume = st.slider("Volume Growth %", -15, 25, 5)
        rebate = st.slider("Rebate Change %", -10, 20, 2)
        medicaid = st.slider("Medicaid Mix Impact %", -10, 20, 1)
    scenario = base.copy()
    scenario["gross_sales"] *= (1 + price/100) * (1 + volume/100)
    scenario["rebates"] *= (1 + rebate/100)
    scenario["medicaid"] *= (1 + medicaid/100)
    scenario["total_gtn"] = scenario[DEDUCTIONS].sum(axis=1)
    scenario["net_sales"] = scenario["gross_sales"] - scenario["total_gtn"]
    scenario["gtn_pct"] = scenario["total_gtn"] / scenario["gross_sales"]
    with right:
        base_net, scenario_net = base["net_sales"].sum(), scenario["net_sales"].sum()
        delta = scenario_net - base_net
        a,b,c = st.columns(3)
        with a: kpi_card("Base Net Sales", f"${base_net/1e6:,.1f}M")
        with b: kpi_card("Scenario Net Sales", f"${scenario_net/1e6:,.1f}M")
        with c: kpi_card("Net Sales Impact", f"${delta/1e6:,.1f}M")
        plot_df = pd.concat([base.assign(Scenario="Base"), scenario.assign(Scenario="Adjusted")])
        fig = px.line(plot_df, x="month", y="net_sales", color="Scenario", title="Base vs Scenario Net Sales")
        fig.update_layout(template="plotly_white", height=420)
        st.plotly_chart(fig, use_container_width=True)
    st.session_state.scenario_results = {"price": price, "volume": volume, "rebate": rebate, "medicaid": medicaid, "base_net_sales": base["net_sales"].sum(), "scenario_net_sales": scenario["net_sales"].sum(), "impact": scenario["net_sales"].sum() - base["net_sales"].sum()}
    next_button("Continue to AI Copilot →", "AI Copilot")
