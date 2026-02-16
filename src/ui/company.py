import logging

import streamlit as st

from ecologits.electricity_mix_repository import electricity_mixes
from ecologits.tracers.utils import llm_impacts

from src.config.constants import COUNTRY_CODES
from src.core.formatting import format_impacts
from src.core.latency_estimator import latency_estimator
from src.repositories.electricity_mix import (
    format_country_name,
)
from src.repositories.models import load_models
from src.ui.components import display_model_warnings, render_model_selector
from src.ui.impacts import (
    display_impacts,
)


def company_mode():
    # st.expander("How to use this calculator?", expanded=False).markdown(HOW_TO_TEXT)

    with st.container(border=True):
        df = load_models(filter_main=True)

        col1, col2, col3 = st.columns(3)

        provider, model = render_model_selector(df, col1, col2, key_suffix="comp")

        n_employees = col3.number_input(
            label="Number of employees using AI tools",
            min_value=1,
            max_value=10000,
            value=100,
            step=1,
            help="This is the number of employees in your company using AI tools on a regular basis. If you are unsure, you can start with an estimate and adjust later as you gather more data.",
        )

        output_method = col1.pills(
            label="Calculation basis",
            options=["Daily pages", "Daily tokens"],
            default="Daily pages",
            selection_mode="single",
            help="A page refers to a page of content (approx. 500 words) - for tokens, jump to the dedicated tab to learn more.",
        )

        if output_method == "Daily pages":
            output_tokens = col2.slider(
                label="Daily pages (per person)",
                min_value=1,
                max_value=100,
                step=1,
                value=5,
            )
            output_tokens_count = output_tokens * 1000 * n_employees  # approx. 1000 tokens per page
        else:
            output_tokens = col2.selectbox(
                label="Daily tokens (per person)",
                options=[1000, 5000, 10000, 50000, 100000, 500000, 1000000],
                index=2,
            )
            output_tokens_count = output_tokens * n_employees

        time_horizon_label = col3.pills(
            label="Time horizon",
            options=["Daily", "Weekly", "Monthly", "Yearly"],
            default="Yearly",
            selection_mode="single",
        )

        try:
            # Map labels to number of days
            time_horizon_mapping = {
                "Daily": 1,
                "Weekly": 5,
                "Monthly": 22,
                "Yearly": 260,
            }
            time_horizon = time_horizon_mapping[time_horizon_label]
        except KeyError:
            st.error("Invalid time horizon selected. Please choose a valid option.")
            return

        dc_location = st.selectbox(
            label="Provider location",
            options=[c[1] for c in COUNTRY_CODES],
            format_func=format_country_name,
            index=0,
            help="If you dont know, the WORLD average is a good first approximate.",
        )

        electricity_mix = electricity_mixes.find_electricity_mix(dc_location)

        # WARNING DISPLAY
        provider_raw = df[(df["provider_clean"] == provider) & (df["name_clean"] == model)][
            "provider"
        ].values[0]
        model_raw = df[(df["provider_clean"] == provider) & (df["name_clean"] == model)][
            "name"
        ].values[0]

        display_model_warnings(df, provider, model)

    try:
        estimated_latency = latency_estimator.estimate(
            provider=provider_raw,
            model_name=model_raw,
            output_tokens=output_tokens_count * time_horizon,
        )
        impacts = llm_impacts(
            provider=provider_raw,
            model_name=model_raw,
            output_token_count=output_tokens_count * time_horizon,
            request_latency=estimated_latency,
            electricity_mix_zone=electricity_mix.zone,
        )

        impacts, _, _ = format_impacts(impacts)

        with st.container(border=True):
            st.markdown(
                f"<h5 align = 'center'>Estimated environmental impacts of using</h5>"
                f"<h4 align = 'center'>{model} ({provider})</h4>"
                f"<p align = 'center'><i>on a {time_horizon_label.lower()} basis in my company</i></p>",
                unsafe_allow_html=True,
            )
            display_impacts(impacts)

    except Exception as e:
        st.error("Could not find the model in the repository. Please try another model.")
        raise e

    _, col2, _ = st.columns(3)
    with col2:
        pdf_report = st.button(
            "Generate PDF report",
            type="primary",
            width="stretch",
            help="Download a PDF report summarizing the estimated environmental impacts of your organization.",
        )
    if pdf_report:
        st.info("PDF report generation is not yet implemented. Stay tuned!", icon="🧑‍🔧")
        logging.info("PDF report generation requested, but not yet implemented.")
