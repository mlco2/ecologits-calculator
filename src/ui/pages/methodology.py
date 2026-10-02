import streamlit as st


def methodology_page() -> None:
    with st.container(key="methodology_page"):
        # Hero
        with st.container(horizontal_alignment="center"):
            st.badge(
                "Transparent and open methodology",
                icon=":material/science:",
                color="green",
            )
            st.title("How we estimate impacts", text_alignment="center")
            st.markdown(
                "A bottom-up methodology to estimate the energy consumption "
                "and environmental impacts of an AI request — from model "
                "architecture, hardware and electricity mix.",
                text_alignment="center",
            )
            with st.container(horizontal=True, horizontal_alignment="center"):
                st.link_button(
                    "EcoLogits documentation",
                    url="https://ecologits.ai/methodology/",
                    type="primary",
                    icon=":material/menu_book:",
                )
                st.link_button(
                    "Boavizta resources",
                    url="https://boavizta.org/",
                    icon=":material/open_in_new:",
                )

        # Model
        st.header("The impact model", icon=":material/functions:")
        st.caption(
            "Impacts of one inference split into usage (electricity) and "
            "embodied (manufacturing, transport, extraction) phases."
        )
        with st.container(border=True):
            st.latex(r"I_{request} = I_{request}^u + I_{request}^e")
            st.latex(
                r"I_{request} = E_{request} \times F_{em} + "
                r"\frac{\Delta T}{\Delta L} \times I_{server}^e"
            )
        legend = st.columns(2)
        with legend[0].container(border=True):
            st.markdown(":material/bolt:")
            st.subheader("Usage phase")
            st.markdown(
                "- $E_{request}$: server and cooling energy\n"
                "- $F_{em}$: electricity mix by country and time"
            )
        with legend[1].container(border=True):
            st.markdown(":material/memory:")
            st.subheader("Embodied phase")
            st.markdown(
                "- $\\Delta T / \\Delta L$: compute time over hardware lifetime\n"
                "- $I_{server}^e$: embodied impacts of the server"
            )

        # Multi-criteria
        st.header("Four impact dimensions", icon=":material/eco:")
        criteria = st.columns(4)
        with criteria[0].container(border=True):
            st.markdown(":material/cloud:")
            st.subheader("Carbon")
            st.caption("Global Warming Potential in kgCO2eq.")
        with criteria[1].container(border=True):
            st.markdown(":material/diamond:")
            st.subheader("Metals")
            st.caption("Abiotic depletion (ADPe) in kgSbeq.")
        with criteria[2].container(border=True):
            st.markdown(":material/bolt:")
            st.subheader("Energy")
            st.caption("Primary energy (PE) in MJ.")
        with criteria[3].container(border=True):
            st.markdown(":material/water_drop:")
            st.subheader("Water")
            st.caption("Water consumption footprint (WCF).")

        # Principles, data, hypotheses
        st.header("Principles, data and hypotheses", icon=":material/fact_check:")
        tabs = st.tabs(["Principles", "Data sources", "Hypotheses"])
        with tabs[0]:
            st.write(
                "Bottom-up modeling: from low-level physical components up to "
                "the software level of one inference. Life Cycle Assessment "
                "(LCA) proxies cover both usage and embodied phases."
            )
            st.link_button(
                "Server footprint, beyond carbon",
                url="https://boavizta.org/en/blog/empreinte-de-la-fabrication-d-un-serveur",
                icon=":material/open_in_new:",
            )
            st.link_button(
                "Boavizta API documentation",
                url="https://doc.api.boavizta.org/",
                icon=":material/open_in_new:",
            )
        with tabs[1]:
            st.markdown(
                "- [ML.ENERGY Leaderboard](https://ml.energy/leaderboard): "
                "GPU energy and latency by architecture and output tokens\n"
                "- [Boavizta API](https://github.com/Boavizta/boaviztapi): "
                "server embodied impacts and base consumption\n"
                "- [Our World in Data](https://ourworldindata.org), "
                "[ADEME Base Empreinte](https://base-empreinte.ademe.fr) and "
                "[WRI](https://www.wri.org): electricity mix per country"
            )
        with tabs[2]:
            st.warning(
                "We estimate undisclosed proprietary model architectures "
                "from public signals. Approximations, fully disclosed.",
                icon=":material/warning:",
            )
            st.markdown(
                "- Production setup: quantized models on data-center servers "
                "and GPUs such as H100\n"
                "- Electricity mixes are yearly averages\n"
                "- Excluded for now: idle cloud resources, buildings, network, "
                "end-user devices"
            )

        # Equivalents
        st.header("Everyday equivalents", icon=":material/compare_arrows:")
        st.caption(
            "Reference points for standard use cases, computed from request "
            "impacts — or scaled to 1% of the planet daily for a year."
        )
        per_request, scaled = st.tabs(["Per request", "At planetary scale"])
        with per_request:
            with st.expander(
                "Walking or running distance",
                icon=":material/directions_walk:",
                expanded=True,
            ):
                st.write(
                    "Request energy vs. human effort (70 kg person, "
                    "[runningtools.com](https://www.runningtools.com/energyusage.htm)): "
                    "walking 196 kJ/km at 3 km/h, running 294 kJ/km at 10 km/h."
                )
            with st.expander(
                "Electric vehicle distance", icon=":material/ev_station:"
            ):
                st.write(
                    "Request energy vs. EV consumption of 0.17 kWh/km "
                    "([selectra.info](https://selectra.info/energie/actualites/insolite/consommation-vehicules-electriques-france-2040), "
                    "[tesla.com](https://www.tesla.com/fr_fr/support/power-consumption))."
                )
            with st.expander("Streaming time", icon=":material/play_circle:"):
                st.write(
                    "Request GHG vs. video streaming: 1 kgCO2eq is 15.6 h "
                    "([impactco2.fr](https://impactco2.fr/outils/comparateur?value=1&comparisons=streamingvideo))."
                )
        with scaled:
            with st.container(border=True):
                st.latex(
                    r"I_{scaled} = I_{request} \times "
                    r"[1\% \text{ of 8B people}] \times 365 \text{ days}"
                )
            with st.expander(
                "Wind turbines or nuclear plants",
                icon=":material/wind_power:",
                expanded=True,
            ):
                st.write(
                    "Scaled energy vs. a 2 MW turbine (4.2 GWh/year, "
                    "[ecologie.gouv.fr](https://www.ecologie.gouv.fr/eolien-terrestre)) "
                    "and a 900 MW nuclear plant (6 TWh/year)."
                )
            with st.expander(
                "Ireland electricity consumption", icon=":material/public:"
            ):
                st.write(
                    "Scaled energy vs. Ireland: 33 TWh/year for 5M people "
                    "([wikipedia.org](https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption))."
                )
            with st.expander("Paris to New York flights", icon=":material/flight:"):
                st.write(
                    "Scaled GHG vs. a Paris-NYC return flight: 1,770 kgCO2eq "
                    "per passenger at 100 passengers per flight "
                    "([impactco2.fr](https://impactco2.fr/outils/comparateur?value=1&comparisons=&equivalent=avion-pny))."
                )

        st.info(
            "Motivated to help test and improve this methodology? We would "
            "love to hear from you.",
            icon=":material/lightbulb:",
        )
        with st.container(horizontal=True, horizontal_alignment="center"):
            st.link_button(
                "Contact us",
                url="https://codecarbon.io/",
                type="primary",
                icon=":material/mail:",
            )
