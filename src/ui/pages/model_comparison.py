from html import escape

import plotly.graph_objects as go
import streamlit as st

from src.config.scenarios import SCENARIOS
from src.core.formatting import format_impacts, format_number
from src.core.impact_calculator import compute_scenario_impacts
from src.core.units import q as _q
from src.repositories.models import load_models
from src.repositories.video_models import load_video_models
from src.ui.components.impacts import display_impacts

_COMPARISON_IMPACTS = ["Electricity", "Carbon Footprint", "Water", "Metals & Minerals"]
_MAX_MODELS = 4
_MODES = ["1 vs 1", "Model mapping"]

# Default selection for "Model mapping" as (provider, raw model name).
# Order matters: kept as listed when all are available for the task.
_DEFAULT_MAPPING_MODELS = [
    ("anthropic", "claude-fable-5-1"),
    ("openai", "gpt-6-astra"),
    ("mistralai", "zai-glm-5-3"),
    ("google_genai", "gemini-3.8-flash"),
]

# Impact label -> (QImpacts value attr, QImpacts min attr, QImpacts max attr, noun for sentences)
_DUEL_IMPACTS = {
    "Electricity": ("energy", "energy_min", "energy_max", "energy"),
    "Carbon Footprint": ("gwp", "gwp_min", "gwp_max", "carbon"),
    "Water": ("wcf", "wcf_min", "wcf_max", "water"),
    "Metals & Minerals": ("adpe", "adpe_min", "adpe_max", "metals & minerals"),
    "Fossil Fuels": ("pe", "pe_min", "pe_max", "fossil fuels"),
}

# EcoLogits charter greens
_TRACK_COLOR = "rgba(6, 37, 34, 0.08)"
_SMALL_COLOR = "rgba(0, 191, 99, 0.45)"
_LARGE_COLOR = "#087f4f"
_TICK_COLOR = "#062522"


def _scenario_context(scenario) -> str | None:
    if scenario.modality == "video":
        context = f"{scenario.resolution}, {scenario.duration}s"
        return context + (" with audio" if scenario.with_audio else "")
    if scenario.output_token_count is not None:
        return f"{scenario.output_token_count:,} output tokens"
    return None


def _load_scenario_models(scenario):
    if scenario.modality == "video":
        return load_video_models(
            resolution=scenario.resolution,
            duration=scenario.duration,
            with_audio=scenario.with_audio,
            extrapolate_resolution=scenario.extrapolate_resolution,
        )
    return load_models(filter_main=True)


def _compute_formatted(scenario, provider, model_name):
    return format_impacts(compute_scenario_impacts(scenario, provider, model_name))[0]


def _impact_values(q_impacts, impact_label):
    """Return (mean, min, max, unit) harmonized for one impact."""
    value_attr, min_attr, max_attr, _ = _DUEL_IMPACTS[impact_label]
    mean_q = getattr(q_impacts, value_attr)
    min_q = getattr(q_impacts, min_attr)
    max_q = getattr(q_impacts, max_attr)
    mean = float(mean_q.magnitude)
    unit = f"{mean_q.units:~}"
    if min_q is None or max_q is None:
        return mean, mean, mean, unit
    return mean, float(min_q.magnitude), float(max_q.magnitude), unit


def _base_magnitude(mean, unit):
    try:
        return float(_q(mean, unit).to_base_units().magnitude)
    except Exception:
        return mean


def _harmonize(a_vals, b_vals):
    """Convert both (mean, min, max, unit) to the unit of the largest mean."""
    a_mean, _, _, a_unit = a_vals
    b_mean, _, _, b_unit = b_vals

    target = (
        a_unit if _base_magnitude(a_mean, a_unit) >= _base_magnitude(b_mean, b_unit) else b_unit
    )

    def _convert(vals, target_unit):
        mean, vmin, vmax, unit = vals
        if unit == target_unit:
            return mean, vmin, vmax, target_unit
        try:
            mean = float(_q(mean, unit).to(target_unit).magnitude)
            vmin = float(_q(vmin, unit).to(target_unit).magnitude)
            vmax = float(_q(vmax, unit).to(target_unit).magnitude)
            return mean, vmin, vmax, target_unit
        except Exception:
            return vals

    return _convert(a_vals, target), _convert(b_vals, target)


def _split_provider_model(label: str) -> tuple[str, str]:
    """Split a 'Provider — Model' label into (provider, model)."""
    if " — " in label:
        provider, _, model = label.partition(" — ")
        return provider.strip(), model.strip()
    return "", label


def _render_duel_header(label_a, label_b, impact_label, a_vals, b_vals) -> None:
    _, _, _, noun = _DUEL_IMPACTS[impact_label]
    a_mean, _, _, unit = a_vals
    b_mean, _, _, _ = b_vals
    if a_mean <= b_mean:
        small_mean, large_mean = a_mean, b_mean
    else:
        small_mean, large_mean = b_mean, a_mean
    a_first = a_mean >= b_mean

    if small_mean <= 0 or large_mean <= 0:
        st.info("Comparison is not available for these values.", icon=":material/info:")
        return
    ratio = large_mean / small_mean
    if abs(ratio - 1) < 0.005:
        st.success(
            f"{label_a} and {label_b} have nearly identical {noun} impacts ({format_number(a_mean)} {unit}).",
            icon=":material/compare_arrows:",
        )
        return

    provider_a, model_a = _split_provider_model(label_a)
    provider_b, model_b = _split_provider_model(label_b)

    def _phrase(model: str, provider: str) -> str:
        if provider:
            return f"<b>{escape(model)}</b> from {escape(provider)}"
        return f"<b>{escape(model)}</b>"

    if a_first:
        sentence = (
            f"{_phrase(model_a, provider_a)} uses {format_number(ratio, 2)}× more {escape(noun)} "
            f"than {_phrase(model_b, provider_b)}"
        )
        arrow = "↑"
    else:
        sentence = (
            f"{_phrase(model_a, provider_a)} uses {format_number(ratio, 2)}× less {escape(noun)} "
            f"than {_phrase(model_b, provider_b)}"
        )
        arrow = "↓"

    st.html(
        f"""
        <div class="duel-header">
            <div class="duel-ratio">{arrow} {format_number(ratio, 2)}×</div>
            <div class="duel-sentence">{sentence}</div>
        </div>
        """
    )


def _render_duel_plot(label_a, label_b, impact_label, a_vals, b_vals) -> None:
    a_mean, a_min, a_max, unit = a_vals
    b_mean, b_min, b_max, _ = b_vals
    scale_max = max(a_max, b_max, a_mean, b_mean)
    if scale_max <= 0:
        st.info("No positive values to plot.", icon=":material/info:")
        return
    scale_max *= 1.04

    a_is_large = a_mean >= b_mean
    color_a = _LARGE_COLOR if a_is_large else _SMALL_COLOR
    color_b = _SMALL_COLOR if a_is_large else _LARGE_COLOR

    labels = [label_a, label_b]
    means = [a_mean, b_mean]
    mins = [min(a_min, a_mean), min(b_min, b_mean)]
    maxs = [max(a_max, a_mean), max(b_max, b_mean)]
    # Guarantee a visible stub: point estimates (min == max) get a thin
    # segment centered on the mean instead of a zero-width, invisible bar.
    min_width = scale_max * 0.02
    bases = []
    widths = []
    for mean, mn, mx in zip(means, mins, maxs, strict=True):
        if mx - mn >= min_width:
            bases.append(mn)
            widths.append(mx - mn)
        else:
            bases.append(max(0.0, mean - min_width / 2))
            widths.append(min_width)
    right_labels = [
        f"{format_number(m)} ± {format_number((mx - mn) / 2)} {unit}"
        if mx > mn
        else f"{format_number(m)} {unit}"
        for m, mn, mx in zip(means, mins, maxs, strict=True)
    ]

    fig = go.Figure()
    # Background track: full scale, light charter tint
    fig.add_trace(
        go.Bar(
            y=labels,
            x=[scale_max, scale_max],
            orientation="h",
            marker_color=_TRACK_COLOR,
            hoverinfo="skip",
            showlegend=False,
        )
    )
    # Uncertainty interval segments [min, max]
    fig.add_trace(
        go.Bar(
            y=labels,
            x=widths,
            base=bases,
            orientation="h",
            marker_color=[color_a, color_b],
            marker_line_width=0,
            customdata=[
                [format_number(means[0]), format_number(mins[0]), format_number(maxs[0])],
                [format_number(means[1]), format_number(mins[1]), format_number(maxs[1])],
            ],
            hovertemplate=(
                "%{y}<br>mean: %{customdata[0]} "
                + escape(unit)
                + "<br>range: %{customdata[1]}–%{customdata[2]} "
                + escape(unit)
                + "<extra></extra>"
            ),
            showlegend=False,
        )
    )
    # Mean ticks: dark vertical markers
    fig.add_trace(
        go.Scatter(
            x=means,
            y=labels,
            mode="markers",
            marker_symbol="line-ns",
            marker_line_color=_TICK_COLOR,
            marker_line_width=3,
            marker_size=22,
            hoverinfo="skip",
            showlegend=False,
        )
    )
    # Value annotations next to the mean tick (middle point).
    # The label on the dark green (larger) bar sits on the bar fill, so white.
    large_label = label_a if a_is_large else label_b
    for label, mean, text in zip(labels, means, right_labels, strict=True):
        fig.add_annotation(
            x=mean,
            y=label,
            text=text,
            xanchor="left",
            yanchor="middle",
            xshift=8,
            showarrow=False,
            font={"color": "white" if label == large_label else "#062522", "size": 12},
        )

    fig.update_layout(
        autosize=True,
        barmode="overlay",
        bargap=0.45,
        height=260,
        margin={"l": 220, "r": 170, "t": 12, "b": 60},
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={"color": "#062522"},
        xaxis={
            "range": [0, scale_max * 1.45],
            "title": f"{impact_label} ({unit})",
            "gridcolor": "rgba(6, 37, 34, 0.08)",
            "zeroline": False,
            "automargin": True,
        },
        yaxis={"autorange": "reversed", "showgrid": False, "automargin": True},
    )
    st.plotly_chart(fig, width="stretch", config={"responsive": True})


def _default_option_index(model_options, key: tuple[str, str], fallback: int) -> int:
    """Return the label index matching (provider, raw name), or fallback."""
    for index, (_, option_key) in enumerate(model_options.items()):
        if option_key == key:
            return index
    return fallback


def _one_vs_one(scenario, model_options) -> None:
    labels = list(model_options)
    default_a = _default_option_index(model_options, _DEFAULT_MAPPING_MODELS[0], 0)
    default_b = _default_option_index(
        model_options, _DEFAULT_MAPPING_MODELS[1], 1 if len(labels) > 1 else 0
    )
    col_a, col_b = st.columns(2)
    with col_a:
        label_a = st.selectbox("Model A", options=labels, index=default_a, key="compare_model_a")
    with col_b:
        label_b = st.selectbox("Model B", options=labels, index=default_b, key="compare_model_b")
    impact_label = st.pills(
        "Impact to compare",
        options=list(_DUEL_IMPACTS),
        default="Electricity",
        key="duel_impact",
    )
    if impact_label is None:
        st.info("Select an impact above to see the comparison.", icon=":material/info:")
        return
    if label_a == label_b:
        st.warning("Select two different models to compare.", icon=":material/warning:")
        return

    provider_a, name_a = model_options[label_a]
    provider_b, name_b = model_options[label_b]
    try:
        impacts_a = _compute_formatted(scenario, provider_a, name_a)
        impacts_b = _compute_formatted(scenario, provider_b, name_b)
    except ValueError as error:
        st.error(str(error))
        return

    a_vals, b_vals = _harmonize(
        _impact_values(impacts_a, impact_label),
        _impact_values(impacts_b, impact_label),
    )

    with st.container(border=True, key="duel_card"):
        _render_duel_header(label_a, label_b, impact_label, a_vals, b_vals)
        _render_duel_plot(label_a, label_b, impact_label, a_vals, b_vals)

    detail_a, detail_b = st.columns(2)
    with detail_a.container(border=True):
        st.subheader(label_a)
        display_impacts(impacts_output=impacts_a, impacts_to_display=_COMPARISON_IMPACTS)
    with detail_b.container(border=True):
        st.subheader(label_b)
        display_impacts(impacts_output=impacts_b, impacts_to_display=_COMPARISON_IMPACTS)


def _default_mapping_selection(model_options) -> list[str]:
    """Return default labels for model mapping, in _DEFAULT_MAPPING_MODELS order."""
    lookup = {(provider, name): label for label, (provider, name) in model_options.items()}
    selected = [lookup[key] for key in _DEFAULT_MAPPING_MODELS if key in lookup]
    if selected:
        return selected
    return list(model_options)[:2]


def _model_mapping(scenario, model_options) -> None:
    selected = st.multiselect(
        "Models to compare",
        options=list(model_options),
        default=_default_mapping_selection(model_options),
        max_selections=_MAX_MODELS,
        help="Select up to four models. Estimates use identical task settings.",
        key="compare_models",
    )
    if not selected:
        st.info(
            "Select at least one model above to see its estimated impacts.",
            icon=":material/info:",
        )
        return

    impact_label = st.pills(
        "Impact to map",
        options=list(_DUEL_IMPACTS),
        default="Carbon Footprint",
        key="mapping_impact",
    )

    results = []
    for label in selected:
        provider, model_name = model_options[label]
        try:
            impacts = _compute_formatted(scenario, provider, model_name)
            results.append({"label": label, "impacts": impacts, "error": None})
        except ValueError as error:
            results.append({"label": label, "impacts": None, "error": str(error)})

    successful = [r for r in results if r["impacts"] is not None]
    if impact_label is not None and successful:
        rows = []
        for result in successful:
            mean, vmin, vmax, unit = _impact_values(result["impacts"], impact_label)
            rows.append(
                {"label": result["label"], "mean": mean, "min": vmin, "max": vmax, "unit": unit}
            )
        target_unit = max(
            rows,
            key=lambda r: _base_magnitude(r["mean"], r["unit"]),
        )["unit"]
        mapped = []
        for row in rows:
            conv = {k: row[k] for k in ("label", "mean", "min", "max")}
            try:
                if row["unit"] != target_unit:
                    conv = {
                        "label": row["label"],
                        "mean": float(_q(row["mean"], row["unit"]).to(target_unit).magnitude),
                        "min": float(_q(row["min"], row["unit"]).to(target_unit).magnitude),
                        "max": float(_q(row["max"], row["unit"]).to(target_unit).magnitude),
                    }
            except Exception:
                pass
            mapped.append(conv)
        mapped.sort(key=lambda r: r["mean"])
        x_max = max(max(r["max"], r["mean"]) for r in mapped)
        if x_max <= 0:
            x_max = max(r["mean"] for r in mapped)
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                y=[r["label"] for r in mapped],
                x=[r["mean"] for r in mapped],
                orientation="h",
                marker_color=_LARGE_COLOR,
                error_x={
                    "type": "data",
                    "symmetric": False,
                    "array": [r["max"] - r["mean"] for r in mapped],
                    "arrayminus": [r["mean"] - r["min"] for r in mapped],
                    "color": _TICK_COLOR,
                    "thickness": 2,
                    "width": 6,
                },
                hovertemplate="%{y}<br>mean: %{customdata} "
                + escape(target_unit)
                + "<extra></extra>",
                customdata=[format_number(r["mean"]) for r in mapped],
                showlegend=False,
            )
        )
        fig.update_layout(
            autosize=True,
            height=max(220, 90 + 70 * len(mapped)),
            margin={"l": 220, "r": 40, "t": 60, "b": 60},
            plot_bgcolor="white",
            paper_bgcolor="white",
            font={"color": "#062522"},
            title={
                "text": f"{impact_label} by model ({target_unit})",
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis={
                "title": f"{impact_label} ({target_unit})",
                "range": [0, x_max * 1.25],
                "gridcolor": _TRACK_COLOR,
                "zeroline": False,
                "automargin": True,
            },
            yaxis={"autorange": "reversed", "automargin": True},
        )
        with st.container(border=True, key="mapping_chart"):
            st.plotly_chart(fig, width="stretch", config={"responsive": True})

    for result in results:
        if result["error"] is not None:
            st.error(f"{result['label']}: {result['error']}")


def model_comparison_page() -> None:
    with st.container(key="compare_header", horizontal_alignment="center"):
        st.title("Compare models", icon=":material/compare_arrows:", text_alignment="center")
        st.caption(
            "Same task, same settings — side-by-side estimated impacts "
            "to spot the most frugal model.",
            text_alignment="center",
        )
        with st.container(horizontal=True, horizontal_alignment="center"):
            mode = st.pills(
                "Comparison mode",
                options=_MODES,
                default="1 vs 1",
                key="compare_mode",
            )

    with st.container(border=True):
        scenario_label = st.selectbox(
            "Task",
            options=[scenario.label for scenario in SCENARIOS],
            key="compare_task",
        )
        scenario = next(s for s in SCENARIOS if s.label == scenario_label)
        models = _load_scenario_models(scenario)
        if models.empty:
            st.error("No compatible models are available for this task.")
            return
        model_options = {
            f"{row.provider_clean} — {row.name_clean}": (row.provider, row.name)
            for row in models.itertuples()
        }
        context = _scenario_context(scenario)
        if context:
            st.caption(f"Task settings: {context}")

    if mode == "Model mapping":
        _model_mapping(scenario, model_options)
    else:
        _one_vs_one(scenario, model_options)
