import streamlit as st

from src.config.content import (
    ABOUT_TEXT,
    HERO_TEXT,
    METHODOLOGY_TEXT,
    SUPPORT_TEXT,
)
from src.ui.token_estimator import token_estimator
from src.ui.utils import reduce_top_padding


def render_header() -> None:

    reduce_top_padding()

    st.html("""
    <div style="background: #00BF63; padding: 10px; border-radius: 10px; margin-bottom: 0px;">
        <p align="center" style="color: white; margin: 0;">📣 EcoLogits is joining CodeCarbon non-profit ! <a href="https://www.linkedin.com/posts/genai-impact_grande-nouvelle-pour-un-numérique-plus-activity-7420053917440376832-QBEw/" target="_blank" style="color: white; text-decoration: underline; font-weight: bold;">Full announcement here</a></p>
    </div>
    """)

    st.html(HERO_TEXT)

    _, col_info, col_method, col_token_estimator, col_support, _ = st.columns([1, 0.50, 0.50, 0.50, 0.50, 1])

    with col_info:

        @st.dialog(title="ℹ️ More informations about the calculator", width="medium")
        def calculator_info():
            st.markdown(ABOUT_TEXT, unsafe_allow_html=True)

        if st.button("ℹ️ About", width="stretch"):
            calculator_info()

    with col_method:

        @st.dialog(title="📖 About the methodology", width="large")
        def methodology_info():
            st.markdown(METHODOLOGY_TEXT, unsafe_allow_html=True)

        if st.button("📖 Methodology", width="stretch"):
            methodology_info()

    with col_token_estimator:

        @st.dialog(title="🪙 Tokens estimator", width="medium")
        def token_estimator_info():
            token_estimator()

        if st.button("🪙 Tokens ?", width="stretch"):
            token_estimator_info()

    with col_support:

        @st.dialog(title="🩷 Support us !", width="medium")
        def support_info():
            st.markdown(SUPPORT_TEXT, unsafe_allow_html=True)

        if st.button("🩷 Support us !", width="stretch"):
            support_info()

    st.divider()
