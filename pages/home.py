import streamlit as st
from components.layout import page_header, status_panel, next_button

def render_home():
    page_header("AI-Assisted GTN Forecasting", "A guided workflow to load GTN data, benchmark forecasting models, generate outputs, simulate scenarios, and explain results.")
    left, right = st.columns([1.5, 1])
    with left:
        for num, title, body in [
            ("1", "Load GTN Data", "Use the demo dataset or upload historical GTN actuals in the required template format."),
            ("2", "Run Forecast Engine", "Benchmark models by GTN component and select champion models using accuracy, bias, and stability."),
            ("3", "Review, Simulate, Explain", "Review outputs, run what-if scenarios, and generate AI-assisted commentary."),
        ]:
            st.markdown(f"<div class='card'><div class='step-number'>{num}</div><h3>{title}</h3><p>{body}</p></div>", unsafe_allow_html=True)
    with right:
        status_panel()
    next_button("Start Workflow →", "Data Intake")
