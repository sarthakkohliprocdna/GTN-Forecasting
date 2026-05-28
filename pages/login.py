import streamlit as st
from components.layout import logo_html, PROCDNA_LOGO, VIIV_LOGO

def render_login():
    st.markdown(
        f"""
        <div class="login-page">
            <div class="login-left-panel">
                <div class="login-brand-logo">{logo_html(PROCDNA_LOGO, 150)}</div>
                <h1>Forecast GTN with clarity.</h1>
                <h2>Explain. Simulate. Decide.</h2>
                <p>An AI-assisted forecasting workspace for Pharma Finance teams to model GTN deductions, benchmark forecasting approaches, simulate scenarios, and generate executive-ready explanations.</p>
                <div class="login-footer">© 2026 ProcDNA. Demo environment.</div>
            </div>
            <div class="login-right-panel">
                <div class="login-form-card">
                    <div class="login-logo-row">{logo_html(PROCDNA_LOGO, 118)}{logo_html(VIIV_LOGO, 92)}</div>
                    <h3>Login to Your Account</h3>
                    <p>Please enter your details.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="login-form-overlay">', unsafe_allow_html=True)
    st.text_input("Email Address", value="admin@gtnforecast.com")
    st.text_input("Password", value="password123", type="password")
    if st.button("Sign In →", use_container_width=True):
        st.session_state.authenticated = True
        st.session_state.page = "Workspace"
        st.rerun()
    st.caption("Dev note: use admin@gtnforecast.com and password123")
    st.markdown("</div>", unsafe_allow_html=True)
