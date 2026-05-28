import streamlit as st

WORKFLOW_STEPS = ["Home", "Data Intake", "Forecast Engine", "Outputs", "Scenario Simulator", "AI Copilot", "Model Zoo"]

def init_state():
    defaults = {
        "authenticated": False,
        "page": "Login",
        "workspace": None,
        "data_loaded": False,
        "data_mode": "Not loaded",
        "actuals_df": None,
        "forecast_ready": False,
        "forecast_results": None,
        "forecast_df": None,
        "champion_df": None,
        "selected_brand": "All Brands",
        "scenario_results": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
