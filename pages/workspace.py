import streamlit as st
from components.layout import render_topbar

def _workspace_card(icon, title, body):
    st.markdown(f"<div class='workspace-card'><div class='icon-box'>{icon}</div><h3>{title}</h3><p>{body}</p></div>", unsafe_allow_html=True)

def render_workspace():
    render_topbar()
    st.markdown("<div class='workspace-title'><h1>Choose a Workspace</h1><p>Select a module to continue.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        _workspace_card("📈", "GTN Forecasting", "Guided workflow for data intake, forecasting, outputs, scenario simulation, and AI commentary.")
        if st.button("Open GTN Forecasting →", use_container_width=True):
            st.session_state.workspace = "GTN Forecasting"
            st.session_state.page = "Home"
            st.rerun()
    with c2:
        _workspace_card("🧪", "Scenario Simulator", "Explore price, volume, rebate, and payer mix sensitivities after forecast generation.")
        if st.button("Open Scenario Simulator →", disabled=not st.session_state.forecast_ready, use_container_width=True):
            st.session_state.page = "Scenario Simulator"
            st.rerun()
    with c3:
        _workspace_card("💬", "AI Copilot", "Ask natural-language questions about forecast drivers, risk, and interpretation.")
        if st.button("Open AI Copilot →", disabled=not st.session_state.forecast_ready, use_container_width=True):
            st.session_state.page = "AI Copilot"
            st.rerun()
