import streamlit as st

from src.config.content import (
    CITATION_LABEL,
    CITATION_TEXT,
    LICENCE_TEXT,
)
from src.ui.calculator import calculator_mode
from src.ui.company import company_mode
from src.ui.expert import expert_mode
from src.ui.expert_company import expert_company_mode
from src.ui.header import render_header

_MODES = ["😀 Standard", "🤓 Expert"]


def main():

    st.set_page_config(layout="wide", page_title="EcoLogits Calculator", page_icon="🧮")

    with open("src/ui/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    render_header()

    _, col_selector, _ = st.columns([1, 2, 1])

    # Initialize session state for mode tracking
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "calculator"
    if "is_expert" not in st.session_state:
        st.session_state.is_expert = False

    with col_selector:
        st.space(size="xsmall")
        # Determine button label based on current mode
        if st.session_state.current_mode == "calculator":
            button_label = "🏢 Switch to **Company Mode**"
        else:
            button_label = "🧮 Switch to **Calculator Mode**"

        if st.button(button_label, use_container_width=True):
            if st.session_state.current_mode == "calculator":
                st.session_state.current_mode = "company"
            else:
                st.session_state.current_mode = "calculator"
            st.rerun()

    mode = st.session_state.current_mode

    # Expert mode toggle
    st.session_state.is_expert = st.toggle("🤓 Expert Mode", value=st.session_state.is_expert)

    if mode == "calculator":
        if st.session_state.is_expert:
            expert_mode()
        else:
            calculator_mode()

    elif mode == "company":
        if st.session_state.is_expert:
            expert_company_mode()
        else:
            company_mode()

    with st.expander("📚 Citation"):
        st.html(CITATION_LABEL)
        st.code(CITATION_TEXT, language="bibtex")

    st.html(LICENCE_TEXT)


if __name__ == "__main__":
    main()
