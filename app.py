import streamlit as st

from src.config.content import (
    CITATION_LABEL,
    CITATION_TEXT,
    LICENCE_TEXT,
)
from src.ui.header import render_header
from src.ui.calculator import calculator_mode
from src.ui.company import company_mode
from src.ui.expert import expert_mode
from src.ui.expert_company import expert_company_mode
from src.ui.token_estimator import token_estimator

_MODES = ["😀 Standard", "🤓 Expert"]

def main():

    st.set_page_config(layout="wide", page_title="EcoLogits Calculator", page_icon="🧮")

    with open("src/ui/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


    render_header()


    _, col_selector, col_modes, _ = st.columns([1, 1.65, 0.35, 1])

    with col_selector:
            st.space(size=1)
            mode = st.pills(
                label="Select the mode",
                options=["🧮 Calculator", "🏢 Company Mode", "🪙 Tokens estimator"],
                default="🧮 Calculator",
                width="stretch",
                label_visibility="collapsed"
            )

    if mode == "🧮 Calculator":
        calculator_mode_selection = col_modes.radio(
            "Calculator mode",
            _MODES,
            index=0,
            label_visibility="collapsed",
            width="stretch"
        )
        if calculator_mode_selection == "🤓 Expert":
            expert_mode()
        else:
            calculator_mode()

    elif mode == "🏢 Company Mode":
        company_mode_selection = col_modes.radio(
            "Company mode",
            _MODES,
            index=0,
            label_visibility="collapsed",
            width="stretch"
        )
        if company_mode_selection == "🤓 Expert":
            expert_company_mode()
        else:
            company_mode()

    elif mode == "🪙 Tokens estimator":
        token_estimator()


    with st.expander("📚 Citation"):
        st.html(CITATION_LABEL)
        st.code(CITATION_TEXT, language="bibtex")

    st.html(LICENCE_TEXT)


if __name__ == "__main__":
    main()
