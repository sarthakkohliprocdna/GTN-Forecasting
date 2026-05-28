import base64
from pathlib import Path
import streamlit as st
from components.state import WORKFLOW_STEPS

PROCDNA_LOGO = Path("assets/procdna_logo.png")
VIIV_LOGO = Path("assets/viiv_logo.png")

def _image_b64(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")

def logo_html(path: Path, max_width: int) -> str:
    b64 = _image_b64(path)
    if not b64:
        return ""
    return f'<img src="data:image/png;base64,{b64}" style="max-width:{max_width}px; height:auto;" />'

def set_page(page: str):
    st.session_state.page = page
    st.rerun()

def render_topbar():
    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand-lockup">
                {logo_html(PROCDNA_LOGO, 124)}
                <span class="brand-x">×</span>
                {logo_html(VIIV_LOGO, 100)}
            </div>
            <div class="topbar-right">
                <span class="app-badge">AI-Assisted GTN Forecasting</span>
                <span class="workspace-badge">Demo Workspace</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _is_available(step):
    if step in ["Home", "Data Intake", "Model Zoo"]:
        return True
    if step == "Forecast Engine":
        return st.session_state.data_loaded
    return st.session_state.forecast_ready

def render_stepper():
    st.markdown("<div class='workflow-wrapper'><div class='workflow-label'>Guided workflow</div>", unsafe_allow_html=True)
    cols = st.columns(len(WORKFLOW_STEPS))
    for idx, step in enumerate(WORKFLOW_STEPS):
        with cols[idx]:
            active = st.session_state.page == step
            button_type = "primary" if active else "secondary"
            if st.button(f"{idx + 1}  {step}", key=f"nav_{step}", disabled=not _is_available(step), type=button_type, use_container_width=True):
                set_page(step)
    st.markdown("</div>", unsafe_allow_html=True)

def page_header(title: str, subtitle: str):
    st.markdown(f"<div class='page-header'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)

def status_panel():
    if not st.session_state.data_loaded:
        next_step = "Load data"
    elif not st.session_state.forecast_ready:
        next_step = "Run forecast engine"
    else:
        next_step = "Review outputs"
    st.markdown(
        f"""
        <div class="status-card">
            <h3>Workflow Status</h3>
            <div class="status-row"><span>Data</span><strong>{st.session_state.data_mode}</strong></div>
            <div class="status-row"><span>Forecast</span><strong>{"Generated" if st.session_state.forecast_ready else "Not Run"}</strong></div>
            <div class="status-row"><span>Next Step</span><strong>{next_step}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def next_button(label: str, target_page: str, disabled: bool = False):
    left, right = st.columns([5, 1.6])
    with right:
        if st.button(label, disabled=disabled, use_container_width=True):
            set_page(target_page)

def kpi_card(label, value, note=None):
    note_html = f"<small>{note}</small>" if note else ""
    st.markdown(f"<div class='kpi-card'><span>{label}</span><strong>{value}</strong>{note_html}</div>", unsafe_allow_html=True)
