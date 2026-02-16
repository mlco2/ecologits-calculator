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


def format_energy(energy_value: float, energy_unit=Energy(value=0.0).unit) -> Quantity:
    val = q(energy_value, energy_unit)
    if val < q("1 kWh"):
        val = val.to("Wh")
    if val < q("1 Wh"):
        val = val.to("mWh")
    return val


def format_gwp(gwp_value: float, gwp_unit=GWP(value=0.0).unit) -> Quantity:
    val = q(gwp_value, gwp_unit)
    if val < q("1 kgCO2eq"):
        val = val.to("gCO2eq")
    if val < q("1 gCO2eq"):
        val = val.to("mgCO2eq")
    return val


def format_adpe(adpe_value: float, adpe_unit=ADPe(value=0.0).unit) -> Quantity:
    val = q(adpe_value, adpe_unit)
    if val < q("1 kgSbeq"):
        val = val.to("gSbeq")
    if val < q("1 gSbeq"):
        val = val.to("mgSbeq")
    if val < q("1 mgSbeq"):
        val = val.to("µgSbeq")
    return val


def format_pe(pe_value: float, pe_unit=PE(value=0.0).unit) -> Quantity:
    val = q(pe_value, pe_unit)
    if val < q("1 MJ"):
        val = val.to("kJ")
    return val


def format_wcf(wcf_value: float, wcf_unit=WCF(value=0.0).unit) -> Quantity:
    val = q(wcf_value, wcf_unit)
    if val < q("1 L"):
        val = val.to("mL")
    return val


def format_impacts(impacts: Impacts) -> tuple[QImpacts, Usage, Embodied]:
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
