import streamlit as st

from components.state import init_state
from components.theme import load_theme
from components.layout import render_topbar, render_stepper
from pages.login import render_login
from pages.workspace import render_workspace
from pages.home import render_home
from pages.data_intake import render_data_intake
from pages.forecast_engine import render_forecast_engine
from pages.outputs import render_outputs
from pages.scenario import render_scenario
from pages.copilot import render_copilot
from pages.model_zoo import render_model_zoo

st.set_page_config(page_title="AI-Assisted GTN Forecasting", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

def render_shell():
    render_topbar()
    render_stepper()

def main():
    init_state()
    load_theme()

    if not st.session_state.authenticated:
        render_login()
        return

    if st.session_state.page == "Workspace":
        render_workspace()
        return

    render_shell()

    pages = {
        "Home": render_home,
        "Data Intake": render_data_intake,
        "Forecast Engine": render_forecast_engine,
        "Outputs": render_outputs,
        "Scenario Simulator": render_scenario,
        "AI Copilot": render_copilot,
        "Model Zoo": render_model_zoo,
    }
    pages.get(st.session_state.page, render_home)()

if __name__ == "__main__":
    main()
