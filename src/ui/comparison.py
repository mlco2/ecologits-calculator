import plotly.graph_objects as go
import streamlit as st

from ecologits.tracers.utils import llm_impacts

from src.core.formatting import format_impacts
from src.core.latency_estimator import latency_estimator
from src.repositories.models import load_models
from src.ui.components import render_model_selector


def model_comparison_mode():
    df = load_models(filter_main=True)
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        st.markdown("<h3 align='center'>Model A</h3>", unsafe_allow_html=True)
        provider_1, model_1 = render_model_selector(df, col1, col1, key_suffix="arena_a")
        provider_raw_1 = df[(df["provider_clean"] == provider_1) & (df["name_clean"] == model_1)][
            "provider"
        ].values[0]
        model_raw_1 = df[(df["provider_clean"] == provider_1) & (df["name_clean"] == model_1)][
            "name"
        ].values[0]

        try:
            estimated_latency_1 = latency_estimator.estimate(
                provider=provider_raw_1,
                model_name=model_raw_1,
                output_tokens=250,
            )
            impacts_1 = llm_impacts(
                provider=provider_raw_1,
                model_name=model_raw_1,
                output_token_count=250,
                request_latency=estimated_latency_1,
            )

            impacts_1, _, _ = format_impacts(impacts_1)

        except Exception as e:
            st.error(f"Error estimating impacts for model A: {e}")
            impacts_1 = None

    with col3:
        st.markdown("<h3 align='center'>Model B</h3>", unsafe_allow_html=True)
        provider_2, model_2 = render_model_selector(df, col3, col3, key_suffix="arena_b")
        provider_raw_2 = df[(df["provider_clean"] == provider_2) & (df["name_clean"] == model_2)][
            "provider"
        ].values[0]
        model_raw_2 = df[(df["provider_clean"] == provider_2) & (df["name_clean"] == model_2)][
            "name"
        ].values[0]

        try:
            estimated_latency_2 = latency_estimator.estimate(
                provider=provider_raw_2,
                model_name=model_raw_2,
                output_tokens=250,
            )
            impacts_2 = llm_impacts(
                provider=provider_raw_2,
                model_name=model_raw_2,
                output_token_count=250,
                request_latency=estimated_latency_2,
            )

            impacts_2, _, _ = format_impacts(impacts_2)

        except Exception as e:
            st.error(f"Error estimating impacts for model B: {e}")
            impacts_2 = None

    with col2:
        st.markdown("<h3 align='center'>Impacts comparison</h3>", unsafe_allow_html=True)

        comparison_metric = st.pills(
            label="Select the metric to compare",
            options=["ENERGY", "GWP", "ADPE", "PE", "WCF"],
            default="ENERGY",
            key="comparison_pills",
            width="stretch",
        )

        value_1 = impacts_1.__dict__[comparison_metric.lower()]
        value_2 = impacts_2.__dict__[comparison_metric.lower()]
        value_2 = value_2.to(value_1.units)

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                y=[comparison_metric],
                x=[value_1 * -1] if impacts_1 else [0],
                name=f"{model_raw_1} ({provider_raw_1})",
                marker_color="#0B3B36",
                orientation="h",
                text=[f"{abs(value_1):.2f}"] if impacts_1 else ["N/A"],
                textposition="inside",
                textfont={"color": "white", "size": 20},
            )
        )
        fig.add_trace(
            go.Bar(
                y=[comparison_metric],
                x=[value_2] if impacts_2 else [0],
                name=f"{model_raw_2} ({provider_raw_2})",
                marker_color="#00BF63",
                orientation="h",
                text=[f"{value_2:.2f}"] if impacts_2 else ["N/A"],
                textposition="inside",
                textfont={"color": "white", "size": 20},
            )
        )
        fig.update_layout(
            barmode="relative",
            bargap=0.0,
            bargroupgap=0,
            yaxis={"title": "", "showticklabels": False},
            xaxis={"title": "", "showticklabels": False},
            legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "center", "x": 0.5},
            height=250,
            margin={"l": 20, "r": 20, "t": 20, "b": 20},
        )
        st.plotly_chart(fig, width="stretch")

        st.space(10)
        st.markdown(
            "<p align='center'><i>Values are estimated for a request with 250 output tokens.</i></p>"
            "<p align='center'><i>To understand how the environmental impacts are computed go to the Methodology tab.</i></p>",
            unsafe_allow_html=True,
        )
