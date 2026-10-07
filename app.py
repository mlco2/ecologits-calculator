from pathlib import Path

import streamlit as st

from src.config.content import (
    CITATION_LABEL,
    CITATION_TEXT,
    HOW_TO_TEXT,
    LICENCE_TEXT,
)
from src.ui.pages.about import about_page
from src.ui.pages.calculator import calculator_mode
from src.ui.pages.company import company_mode
from src.ui.pages.expert import expert_mode
from src.ui.pages.expert_company import expert_company_mode
from src.ui.pages.methodology import methodology_page
from src.ui.pages.model_comparison import model_comparison_page
from src.ui.pages.support import support_page

ROOT = Path(__file__).resolve().parent


def _render_announcement() -> None:
    st.html(
        """
        <div class="announcement">
            <strong>EcoLogits now supports AI-generated videos 🎬.
            <a href="https://ecologits.ai/blog/" target="_blank">
                Read our blog post.
            </a></strong>
        </div>
        """
    )


def _render_calculator() -> None:
    _render_announcement()
    st.html(HOW_TO_TEXT)

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
        expert_enabled = st.toggle(
            "Expert mode",
            key="is_expert",
            help="Configure advanced inputs for a more detailed impact estimate.",
        )

    if company_enabled:
        expert_company_mode() if expert_enabled else company_mode()
    else:
        expert_mode() if expert_enabled else calculator_mode()


def _about_page(calculator_page: st.Page | None = None) -> None:
    about_page(calculator_page=calculator_page)


def _methodology_page() -> None:
    methodology_page()


def _support_page() -> None:
    support_page()


def _render_footer() -> None:
    with st.container(key="app_footer"):
        licence, citation = st.columns(
            [2.5, 0.8],
            gap="large",
            vertical_alignment="center",
        )

        with licence:
            with st.container(key="footer_licence"):
                st.html(f'<div class="footer-licence">{LICENCE_TEXT}</div>')

        with citation:
            with st.container(
                key="footer_citation",
                horizontal=True,
                horizontal_alignment="right",
            ):
                with st.popover(
                    "Cite EcoLogits",
                    icon=":material/format_quote:",
                    width="content",
                ):
                    st.html(CITATION_LABEL)
                    st.code(CITATION_TEXT, language="bibtex")

        st.html('<hr class="footer-divider">')

        brand, about, links = st.columns(
            [1.1, 1.4, 0.8],
            gap="large",
            vertical_alignment="center",
        )

        with brand:
            with st.container(key="footer_brand"):
                st.image(str(ROOT / "assets/logo.png"), width=220)

        with about:
            with st.container(key="footer_about"):
                st.markdown(
                    """
                    **Making the environmental footprint of generative AI visible.**

                    EcoLogits is an open-source project developed by
                    [CodeCarbon](https://codecarbon.io/); visit
                    [ecologits.ai](https://ecologits.ai/) to discover our other projects.
                    """
                )

        with links:
            with st.container(key="footer_links"):
                st.markdown(
                    """
                    **Follow the project**

                    - [GitHub](https://github.com/mlco2/ecologits)
                    - [LinkedIn](https://www.linkedin.com/company/ecologits/)
                    - [Discord](https://discord.gg/7KPzAfcN)
                    """
                )


def main():
    st.set_page_config(
        layout="wide",
        page_title="EcoLogits Calculator",
        page_icon="🧮",
        initial_sidebar_state="collapsed",
    )

    with open(ROOT / "src/ui/components/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    st.logo(
        str(ROOT / "assets/ecologits-logo.png"),
        size="small",
        link="https://ecologits.ai/",
    )

    calculator_nav_page = st.Page(_render_calculator, title="Calculator", url_path="", default=True)

    def _about_nav_page() -> None:
        _about_page(calculator_page=calculator_nav_page)

    page = st.navigation(
        [
            calculator_nav_page,
            st.Page(
                model_comparison_page,
                title="Model comparison",
                icon=":material/compare_arrows:",
                url_path="model-comparison",
            ),
            st.Page(_about_nav_page, title="About us", url_path="about"),
            st.Page(_methodology_page, title="Methodology", url_path="methodology"),
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
    _render_footer()


if __name__ == "__main__":
    main()
