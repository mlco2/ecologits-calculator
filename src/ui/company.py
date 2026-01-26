import streamlit as st

from ecologits.electricity_mix_repository import electricity_mixes
from ecologits.tracers.utils import llm_impacts
from src.ui.impacts import (
    display_impacts,
)
from src.core.latency_estimator import latency_estimator
from src.core.formatting import format_impacts
from src.config.content import (
    WARNING_CLOSED_SOURCE,
    WARNING_MULTI_MODAL,
    WARNING_BOTH,
)
from src.repositories.electricity_mix import (
    format_country_name,
)
from src.config.constants import COUNTRY_CODES
from src.repositories.models import load_models
from src.ui.components import render_model_selector


def company_mode():
    # st.expander("How to use this calculator?", expanded=False).markdown(HOW_TO_TEXT)

    with st.container(border=True):
        df = load_models(filter_main=True)

        col1, col2, col3 = st.columns(3)

        provider, model = render_model_selector(df, col1, col2, key_suffix="comp")

        n_employees = col3.selectbox(
            label="Number of employees",
            options=[10, 50, 100, 500, 1000, 5000, 10000],
            index=2,
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
            output_tokens_count = (
                output_tokens * 1000 * n_employees
            )  # approx. 1000 tokens per page
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

        # Map labels to number of days
        time_horizon_mapping = {
            "Daily": 1,
            "Weekly": 5,
            "Monthly": 22,
            "Yearly": 260,
        }
        time_horizon = time_horizon_mapping[time_horizon_label]

        dc_location = st.selectbox(
            label="Provider location",
            options=[c[1] for c in COUNTRY_CODES],
            format_func=format_country_name,
            index=0,
            help="If you dont know, the WORLD average is a good first approximate.",
        )

        electricity_mix = electricity_mixes.find_electricity_mix(dc_location)

        # WARNING DISPLAY
        provider_raw = df[
            (df["provider_clean"] == provider) & (df["name_clean"] == model)
        ]["provider"].values[0]
        model_raw = df[
            (df["provider_clean"] == provider) & (df["name_clean"] == model)
        ]["name"].values[0]

        df_filtered = df[
            (df["provider_clean"] == provider) & (df["name_clean"] == model)
        ]

        if (
            df_filtered["warning_arch"].values[0]
            and not df_filtered["warning_multi_modal"].values[0]
        ):
            st.warning(WARNING_CLOSED_SOURCE, icon="⚠️")
        if (
            df_filtered["warning_multi_modal"].values[0]
            and not df_filtered["warning_arch"].values[0]
        ):
            st.warning(WARNING_MULTI_MODAL, icon="⚠️")
        if (
            df_filtered["warning_arch"].values[0]
            and df_filtered["warning_multi_modal"].values[0]
        ):
            st.warning(WARNING_BOTH, icon="⚠️")

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
                '<h3 align = "center">Environmental impacts</h3>',
                unsafe_allow_html=True,
            )
            display_impacts(impacts)

    except Exception as e:
        st.error(
            "Could not find the model in the repository. Please try another model."
        )
        raise e
