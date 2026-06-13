import streamlit as st

from src.config.content import (
    ABOUT_TEXT,
    CITATION_LABEL,
    CITATION_TEXT,
    HOW_TO_TEXT,
    LICENCE_TEXT,
    METHODOLOGY_TEXT,
    SUPPORT_TEXT,
)
from src.ui.calculator import calculator_mode
from src.ui.company import company_mode
from src.ui.expert import expert_mode
from src.ui.expert_company import expert_company_mode
from src.ui.token_estimator import token_estimator


def _initialize_navigation_state() -> None:
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "calculator"
    if "company_mode" not in st.session_state:
        st.session_state.company_mode = False
    if "is_expert" not in st.session_state:
        st.session_state.is_expert = False


def _render_announcement() -> None:
    st.html(
        """
        <div class="announcement">
            EcoLogits is joining the CodeCarbon non-profit.
            <a href="https://www.linkedin.com/posts/genai-impact_grande-nouvelle-pour-un-numérique-plus-activity-7420053917440376832-QBEw/" target="_blank">
                Read the announcement
            </a>
        </div>
        """
    )


def _calculator_page() -> None:
    _render_calculator()


def _render_calculator() -> None:
    _render_announcement()
    st.expander("How to use this calculator?", expanded=False).markdown(HOW_TO_TEXT)

    with st.container(
        key="mode_toggles",
        horizontal=True,
        vertical_alignment="center",
        gap="small",
    ):
        company_enabled = st.toggle(
            "Company mode",
            key="company_mode",
            help="Estimate the environmental impact of AI usage across an organisation.",
        )
        st.toggle(
            "Expert mode",
            key="is_expert",
            help="Configure advanced inputs for a more detailed impact estimate.",
        )

    st.session_state.current_mode = "company" if company_enabled else "calculator"

    mode = st.session_state.current_mode

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


def _about_page() -> None:
    st.title("About us")
    st.markdown(ABOUT_TEXT, unsafe_allow_html=True)


def _methodology_page() -> None:
    st.title("Methodology")
    content = METHODOLOGY_TEXT.removeprefix("\n### 📖 Methodology\n")
    st.markdown(content, unsafe_allow_html=True)


def _token_estimator_page() -> None:
    st.title("Token estimator")
    token_estimator()


def _support_page() -> None:
    st.title("Support us")
    st.markdown(SUPPORT_TEXT, unsafe_allow_html=True)


def main():
    st.set_page_config(
        layout="wide",
        page_title="EcoLogits Calculator",
        page_icon="🧮",
        initial_sidebar_state="collapsed",
    )

    with open("src/ui/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    _initialize_navigation_state()
    st.logo(
        "assets/ecologits-logo.png",
        size="medium",
        link="https://ecologits.ai/",
    )

    page = st.navigation(
        [
            st.Page(_calculator_page, title="Calculator", url_path="", default=True),
            st.Page(_about_page, title="About us", url_path="about"),
            st.Page(_methodology_page, title="Methodology", url_path="methodology"),
            st.Page(
                _token_estimator_page,
                title="Token estimator",
                url_path="token-estimator",
            ),
            st.Page(
                _support_page,
                title="Support us",
                icon=":material/favorite:",
                url_path="support",
            ),
        ],
        position="top",
    )
    page.run()


if __name__ == "__main__":
    main()
