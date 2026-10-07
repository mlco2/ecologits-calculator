from dataclasses import dataclass
from math import floor, log10

from ecologits.impacts.modeling import (
    GWP,
    PE,
    WCF,
    ADPe,
    Embodied,
    Energy,
    Impacts,
    Usage,
)
from ecologits.tracers.utils import ImpactsOutput
from pint import Quantity

from src.core.units import q


@dataclass
class QImpacts:
    energy: Quantity
    gwp: Quantity
    adpe: Quantity
    pe: Quantity
    wcf: Quantity
    ranges: bool = False
    energy_min: Quantity | None = None
    energy_max: Quantity | None = None
    gwp_min: Quantity | None = None
    gwp_max: Quantity | None = None
    adpe_min: Quantity | None = None
    adpe_max: Quantity | None = None
    pe_min: Quantity | None = None
    pe_max: Quantity | None = None
    wcf_min: Quantity | None = None
    wcf_max: Quantity | None = None


# Thresholds for automatic unit scaling
THRESHOLDS: dict[str, list[tuple[Quantity, str]]] = {
    "energy": [
        (q("1 kWh"), "Wh"),
        (q("1 Wh"), "mWh"),
    ],
    "gwp": [
        (q("1 kgCO2eq"), "gCO2eq"),
        (q("1 gCO2eq"), "mgCO2eq"),
    ],
    "adpe": [
        (q("1 kgSbeq"), "gSbeq"),
        (q("1 gSbeq"), "mgSbeq"),
        (q("1 mgSbeq"), "µgSbeq"),
    ],
    "pe": [
        (q("1 MJ"), "kJ"),
    ],
    "wcf": [
        (q("1 L"), "mL"),
    ],
}


def format_number(value: float, sig: int = 3) -> str:
    """Format with sig significant digits, never in scientific notation.

    Unlike f"{value:.{sig}g}", very small or very large values render as
    plain decimals (e.g. "0.00000000123" instead of "1.23e-09").
    """
    if value != value or value in (float("inf"), float("-inf")):
        return str(value)
    if value == 0:
        return "0"
    order = floor(log10(abs(value)))
    decimals = min(max(0, (sig - 1) - order), 24)
    text = f"{value:.{decimals}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def auto_scale(value: Quantity, thresholds: list[tuple[Quantity, str]]) -> Quantity:
    """Scale a quantity to an appropriate unit based on thresholds.

    Parameters
    ----------
    value : Quantity
        The quantity to scale.
    thresholds : list[tuple[Quantity, str]]
        List of (threshold, target_unit) tuples. Applied sequentially; if the
        value is below a threshold, it is converted to that unit and the next
        threshold is checked with the converted value.

    Returns:
    -------
    Quantity
        The scaled quantity in the appropriate unit.
    """
    for limit, unit in thresholds:
        if value < limit:
            value = value.to(unit)
    return value


_DEFAULT_UNIT_CLS = {
    "energy": Energy,
    "gwp": GWP,
    "adpe": ADPe,
    "pe": PE,
    "wcf": WCF,
}

_LARGE_SCALE: dict[str, tuple[Quantity, str]] = {
    "energy": (q("1000 kWh"), "MWh"),
    "gwp": (q("1000 kgCO2eq"), "tCO2eq"),
    "adpe": (q("1000 kgSbeq"), "tSbeq"),
    "pe": (q("1000 MJ"), "GJ"),
    "wcf": (q("1000 L"), "kL"),
}

_CRITERIA = ("energy", "gwp", "adpe", "pe", "wcf")


def _format(kind: str, value: float, unit: str | None = None) -> Quantity:
    if unit is None:
        unit = _DEFAULT_UNIT_CLS[kind](value=0.0).unit
    val = q(value, unit)
    limit, target = _LARGE_SCALE[kind]
    if val >= limit:
        val = val.to(target)
    return auto_scale(val, THRESHOLDS[kind])


def format_energy(energy_value: float, energy_unit: str | None = None) -> Quantity:
    return _format("energy", energy_value, energy_unit)


def format_gwp(gwp_value: float, gwp_unit: str | None = None) -> Quantity:
    return _format("gwp", gwp_value, gwp_unit)


def format_adpe(adpe_value: float, adpe_unit: str | None = None) -> Quantity:
    return _format("adpe", adpe_value, adpe_unit)


def format_pe(pe_value: float, pe_unit: str | None = None) -> Quantity:
    return _format("pe", pe_value, pe_unit)


def format_wcf(wcf_value: float, wcf_unit: str | None = None) -> Quantity:
    return _format("wcf", wcf_value, wcf_unit)


def format_impacts(impacts: Impacts | ImpactsOutput) -> tuple[QImpacts, Usage, Embodied]:
    if isinstance(impacts, ImpactsOutput) and impacts.has_errors:
        errors = "; ".join(str(error) for error in impacts.errors)
        raise ValueError(f"Unable to calculate impacts: {errors}")

    if isinstance(impacts.energy.value, float):
        return (
            QImpacts(
                **{kind: _format(kind, getattr(impacts, kind).value) for kind in _CRITERIA}  # type: ignore[arg-type]
            ),
            impacts.usage,
            impacts.embodied,
        )

    else:
        values = {kind: getattr(impacts, kind).value for kind in _CRITERIA}
        means = {kind: _format(kind, values[kind].mean) for kind in _CRITERIA}
        kwargs: dict = {"ranges": True}
        for kind in _CRITERIA:
            kwargs[kind] = means[kind]
            kwargs[f"{kind}_min"] = _format(kind, values[kind].min).to(means[kind].units)
            kwargs[f"{kind}_max"] = _format(kind, values[kind].max).to(means[kind].units)
        return (
            QImpacts(**kwargs),  # type: ignore[arg-type]
            impacts.usage,
            impacts.embodied,
        )
