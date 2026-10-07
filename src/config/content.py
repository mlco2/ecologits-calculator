from pathlib import Path

import streamlit as st

_CONTENT_DIR = Path(__file__).parent / "content"


@st.cache_data
def _load(filename: str) -> str:
    """Load a content file from the content directory and cache the result."""
    return (_CONTENT_DIR / filename).read_text(encoding="utf-8")


HOW_TO_TEXT = _load("how_to.html")
TOKEN_ESTIMATOR_TEXT = _load("token_estimator.md")
ABOUT_TEXT = _load("about.md")
SUPPORT_TEXT = _load("support.md")
METHODOLOGY_TEXT = _load("methodology.md")
CITATION_TEXT = _load("citation.bib")
LICENCE_TEXT = _load("licence.html")


CITATION_LABEL = "BibTeX citation for EcoLogits Calculator and the EcoLogits library:"
