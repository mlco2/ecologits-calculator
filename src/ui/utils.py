import streamlit as st


def reduce_top_padding() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )