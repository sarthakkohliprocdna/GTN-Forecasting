import streamlit as st
from components.layout import page_header, next_button
from ai.groq_client import generate_ai_summary

def render_copilot():
    page_header("AI Copilot", "Ask conversational questions about GTN forecast drivers, risks, scenarios, and model performance.")
    if not st.session_state.forecast_ready:
        st.warning("Generate a forecast before using the AI Copilot.")
        next_button("Go to Forecast Engine →", "Forecast Engine", disabled=not st.session_state.data_loaded)
        return
    question = st.text_input("Ask a question", value="Summarize the key drivers and risks in the GTN forecast.")
    if st.button("Generate AI Commentary", type="primary", use_container_width=True):
        context = {"question": question, "brand": st.session_state.selected_brand, "champion_models": st.session_state.champion_df.to_dict("records") if st.session_state.champion_df is not None else [], "forecast_summary": st.session_state.forecast_df[["gross_sales","total_gtn","net_sales","gtn_pct"]].describe().to_dict() if st.session_state.forecast_df is not None else {}, "scenario_results": st.session_state.scenario_results}
        with st.spinner("Generating commentary..."):
            answer = generate_ai_summary(str(context))
        st.markdown(f"<div class='ai-answer'><h3>AI Commentary</h3><p>{answer}</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='tip-box'><strong>Example questions</strong><br>Why did GTN increase? Which deduction bucket has the highest risk? How should Finance interpret the forecast? What does the scenario imply?</div>", unsafe_allow_html=True)
    next_button("Review Model Zoo →", "Model Zoo")
