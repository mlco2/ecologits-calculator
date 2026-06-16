from html import escape

import pandas as pd
import streamlit as st


def render_environment_card(
    *,
    title: str,
    value: str,
    emoji: str = "",
    unit: str = "",
    subtext: str = "",
) -> None:
    st.html(
        render_environment_card_html(
            title=title,
            value=value,
            emoji=emoji,
            unit=unit,
            subtext=subtext,
        )
    )


def render_environment_card_html(
    *,
    title: str,
    value: str,
    emoji: str = "",
    unit: str = "",
    subtext: str = "",
) -> str:
    unit_html = f'<span class="environment-card-unit">{escape(unit)}</span>' if unit else ""
    subtext_html = (
        f'<p class="environment-card-subtext">{escape(subtext)}</p>' if subtext else ""
    )

    return f"""
        <div class="environment-card">
            <div class="environment-card-header">
                <span class="environment-card-icon">{escape(emoji)}</span>
                <span class="environment-card-title">{escape(title)}</span>
            </div>
            <div class="environment-card-value">
                <span class="environment-card-number">{escape(value)}</span>
                {unit_html}
            </div>
            {subtext_html}
        </div>
        """


def render_model_selector(
    df: pd.DataFrame, col_provider, col_model, key_suffix: str = ""
) -> tuple[str, str]:
    with col_provider:
        providers_clean = sorted(df["provider_clean"].unique())
        # Default to OpenAI if available
        default_index = providers_clean.index("Anthropic") if "Anthropic" in providers_clean else 0

        provider = st.selectbox(
            label="Provider",
            options=providers_clean,
            index=default_index,
            key=f"provider_select_{key_suffix}",
        )

    with col_model:
        models_clean = sorted(
            [
                x
                for x in df["name_clean"].unique()
                if x in df[df["provider_clean"] == provider]["name_clean"].unique()
            ]
        )
        default_model_index = models_clean.index("Claude sonnet 4 6") if "Claude sonnet 4 6" in models_clean else 0
        model = st.selectbox(label="Model", options=models_clean, key=f"model_select_{key_suffix}", index=default_model_index)

    return provider, model


def display_model_warnings(impacts) -> None:
    """Display warning messages based on model characteristics."""
    if len(impacts.warnings) == 1:
        st.warning(impacts.warnings[0].message, icon="⚠️")
    elif len(impacts.warnings) == 2:
        st.warning(
            f"{impacts.warnings[0].message.split(',')[0]} and {impacts.warnings[1].message.split(',')[0].lower()}, {impacts.warnings[0].message.split(',')[1]}",
            icon="⚠️",
        )


def display_electricity_mix_warnings(electricity_mix) -> None:
    """Display warning messages based on electricity mix characteristics."""
    if electricity_mix and electricity_mix.has_warnings:
        warning_messages = [str(warning) for warning in electricity_mix.warnings]
        if len(warning_messages) == 1:
            st.warning(warning_messages[0], icon="⚠️")
        else:
            # Combine multiple warnings into a single message
            combined_message = "\n".join([f"• {msg}" for msg in warning_messages])
            st.warning(f"Electricity mix warnings:\n{combined_message}", icon="⚠️")
