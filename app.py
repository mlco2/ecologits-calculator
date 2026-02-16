import streamlit as st

from src.config.content import (
    ABOUT_TEXT,
    CITATION_LABEL,
    CITATION_TEXT,
    HERO_TEXT,
    LICENCE_TEXT,
    METHODOLOGY_TEXT,
    SUPPORT_TEXT,
)
from src.ui.calculator import calculator_mode
from src.ui.company import company_mode
from src.ui.expert import expert_mode
from src.ui.token_estimator import token_estimator

st.set_page_config(layout="wide", page_title="EcoLogits Calculator", page_icon="🧮")

with open("src/ui/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


st.html("""
<div style="background: #00BF63; padding: 10px; border-radius: 10px; margin-bottom: 0px;">
    <p align="center" style="color: white; margin: 0;">📣 EcoLogits is joining CodeCarbon non-profit ! <a href="https://www.linkedin.com/posts/genai-impact_grande-nouvelle-pour-un-numérique-plus-activity-7420053917440376832-QBEw/" target="_blank" style="color: white; text-decoration: underline; font-weight: bold;">Full announcement here</a></p>
</div>
""")

st.html(HERO_TEXT)

tab_calculator, tab_expert, tab_company, tab_token, tab_method, tab_about, tab_support = st.tabs(
    [
        "🧮 Calculator",
        "🤓 Expert Mode",
        "🏢 Company Mode",
        "🪙 Tokens estimator",
        "📖 Methodology",
        "ℹ️ About",
        "🩷 Support us",
    ]
)

with tab_calculator:
    calculator_mode()

with tab_expert:
    expert_mode()

with tab_company:
    company_mode()

with tab_token:
    token_estimator()

with tab_method:
    st.write(METHODOLOGY_TEXT)

with tab_about:
    st.markdown(ABOUT_TEXT, unsafe_allow_html=True)

with tab_support:
    st.markdown(SUPPORT_TEXT, unsafe_allow_html=True)


with st.expander("📚 Citation"):
    st.html(CITATION_LABEL)
    st.code(CITATION_TEXT, language="bibtex")

st.html(LICENCE_TEXT)
