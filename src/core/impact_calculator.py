from ecologits.impacts.modeling import GWP, PE, WCF, ADPe, Embodied, Energy, Usage
from ecologits.tracers.utils import ImpactsOutput, llm_impacts
from ecologits.utils.range_value import RangeValue

from src.config.scenarios import Scenario


def compute_scenario_impacts(
    scenario: Scenario,
    provider: str,
    model_name: str,
) -> ImpactsOutput:
    if scenario.modality == "text":
        return llm_impacts(
            provider=provider,
            model_name=model_name,
            output_token_count=scenario.output_token_count or 0,
            request_latency=float("inf"),
        )

    return _mock_video_impacts(scenario, provider=provider, model_name=model_name)


def _mock_video_impacts(
    scenario: Scenario,
    provider: str,
    model_name: str,
) -> ImpactsOutput:
    # Temporary prototype values until the calculator depends on the EcoLogits video estimator.
    width, height = (int(part) for part in (scenario.resolution or "1280x720").split("x"))
    duration = scenario.duration or 5
    pixel_ratio = (width * height) / (1280 * 720)
    audio_ratio = 1.15 if scenario.with_audio else 1.0
    provider_ratio = 1.08 if provider in {"openai", "google"} else 1.0
    model_ratio = 0.95 if "fast" in model_name else 1.0
    scale = pixel_ratio * duration / 5 * audio_ratio * provider_ratio * model_ratio

    energy_value = RangeValue(min=0.035 * scale, max=0.09 * scale)
    gwp_value = RangeValue(min=0.012 * scale, max=0.04 * scale)
    adpe_value = RangeValue(min=0.00000003 * scale, max=0.00000011 * scale)
    pe_value = RangeValue(min=0.45 * scale, max=1.4 * scale)
    wcf_value = RangeValue(min=0.018 * scale, max=0.12 * scale)

    energy = Energy(value=energy_value)
    gwp = GWP(value=gwp_value)
    adpe = ADPe(value=adpe_value)
    pe = PE(value=pe_value)
    wcf = WCF(value=wcf_value)

    usage = Usage(energy=energy, gwp=gwp, adpe=adpe, pe=pe, wcf=wcf)
    embodied = Embodied(
        gwp=GWP(value=RangeValue(min=0.001 * scale, max=0.004 * scale)),
        adpe=ADPe(value=RangeValue(min=0.000000005 * scale, max=0.00000002 * scale)),
        pe=PE(value=RangeValue(min=0.05 * scale, max=0.18 * scale)),
    )

    return ImpactsOutput(
        energy=energy,
        gwp=GWP(value=gwp.value + embodied.gwp.value),
        adpe=ADPe(value=adpe.value + embodied.adpe.value),
        pe=PE(value=pe.value + embodied.pe.value),
        wcf=wcf,
        usage=usage,
        embodied=embodied,
    )
