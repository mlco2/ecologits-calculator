from dataclasses import dataclass

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


def format_energy(energy_value: float, energy_unit: str | None = None) -> Quantity:
    if energy_unit is None:
        energy_unit = Energy(value=0.0).unit
    val = q(energy_value, energy_unit)
    return auto_scale(val, THRESHOLDS["energy"])


def format_gwp(gwp_value: float, gwp_unit: str | None = None) -> Quantity:
    if gwp_unit is None:
        gwp_unit = GWP(value=0.0).unit
    val = q(gwp_value, gwp_unit)
    return auto_scale(val, THRESHOLDS["gwp"])


def format_adpe(adpe_value: float, adpe_unit: str | None = None) -> Quantity:
    if adpe_unit is None:
        adpe_unit = ADPe(value=0.0).unit
    val = q(adpe_value, adpe_unit)
    return auto_scale(val, THRESHOLDS["adpe"])


def format_pe(pe_value: float, pe_unit: str | None = None) -> Quantity:
    if pe_unit is None:
        pe_unit = PE(value=0.0).unit
    val = q(pe_value, pe_unit)
    return auto_scale(val, THRESHOLDS["pe"])


def format_wcf(wcf_value: float, wcf_unit: str | None = None) -> Quantity:
    if wcf_unit is None:
        wcf_unit = WCF(value=0.0).unit
    val = q(wcf_value, wcf_unit)
    return auto_scale(val, THRESHOLDS["wcf"])


def format_impacts(impacts: Impacts | ImpactsOutput) -> tuple[QImpacts, Usage, Embodied]:
    if isinstance(impacts.energy.value, float):
        return (
            QImpacts(
                energy=format_energy(impacts.energy.value),
                gwp=format_gwp(impacts.gwp.value),
                adpe=format_adpe(impacts.adpe.value),
                pe=format_pe(impacts.pe.value),
                wcf=format_wcf(impacts.wcf.value),
            ),
            impacts.usage,
            impacts.embodied,
        )

    else:
        energy = format_energy(impacts.energy.value.mean)
        gwp = format_gwp(impacts.gwp.value.mean)
        adpe = format_adpe(impacts.adpe.value.mean)
        pe = format_pe(impacts.pe.value.mean)
        wcf = format_wcf(impacts.wcf.value.mean)

        return (
            QImpacts(
                energy=energy,
                energy_min=format_energy(impacts.energy.value.min).to(energy.units),
                energy_max=format_energy(impacts.energy.value.max).to(energy.units),
                gwp=gwp,
                gwp_min=format_gwp(impacts.gwp.value.min).to(gwp.units),
                gwp_max=format_gwp(impacts.gwp.value.max).to(gwp.units),
                adpe=adpe,
                adpe_min=format_adpe(impacts.adpe.value.min).to(adpe.units),
                adpe_max=format_adpe(impacts.adpe.value.max).to(adpe.units),
                pe=pe,
                pe_min=format_pe(impacts.pe.value.min).to(pe.units),
                pe_max=format_pe(impacts.pe.value.max).to(pe.units),
                wcf=wcf,
                wcf_min=format_wcf(impacts.wcf.value.min).to(wcf.units),
                wcf_max=format_wcf(impacts.wcf.value.max).to(wcf.units),
                ranges=True,
            ),
            impacts.usage,
            impacts.embodied,
        )
