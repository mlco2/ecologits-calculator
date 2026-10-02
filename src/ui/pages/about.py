import streamlit as st


def about_page(calculator_page: st.Page | None = None) -> None:
    with st.container(key="about_page"):
        # Hero
        with st.container(horizontal_alignment="center"):
            st.badge(
                "Open-source project by CodeCarbon",
                icon=":material/eco:",
                color="green",
            )
            st.title("Making the footprint of generative AI visible", text_alignment="center")
            st.markdown(
                "EcoLogits Calculator raises awareness on the environmental "
                "impacts of AI inference — energy, carbon, water — with "
                "transparent, open methodology.",
                text_alignment="center",
            )
            with st.container(horizontal=True, horizontal_alignment="center"):
                if st.button(
                    "Try the calculator",
                    type="primary",
                    icon=":material/calculate:",
                ):
                    if calculator_page is not None:
                        st.switch_page(calculator_page)
                st.link_button(
                    "Star on GitHub",
                    url="https://github.com/mlco2/ecologits",
                    icon=":material/star:",
                )
                st.link_button(
                    "Join the discussion",
                    url="https://github.com/mlco2/ecologits/discussions/45",
                    icon=":material/forum:",
                )

        pillars = st.columns(3)
        with pillars[0].container(border=True):
            st.markdown(":material/visibility:")
            st.subheader("Raise awareness")
            st.caption(
                "Training gets attention, inference at scale often dominates. "
                "We make per-request impacts tangible."
            )
        with pillars[1].container(border=True):
            st.markdown(":material/science:")
            st.subheader("Stay rigorous")
            st.caption(
                "Bottom-up estimates from model architecture, hardware and "
                "electricity mix. Hypotheses are public and reviewable."
            )
        with pillars[2].container(border=True):
            st.markdown(":material/groups:")
            st.subheader("Build in the open")
            st.caption(
                "Built with EcoLogits, Boavizta and Data For Good. "
                "Free, open-source, community-driven."
            )

        st.info(
            "Inference impacts for large language models can largely outweigh "
            "training impacts once deployed at scale. That is why this "
            "calculator focuses on the request level.",
            icon=":material/lightbulb:",
        )

        st.header("Questions, answered", icon=":material/forum:")
        estimate_tab, reduce_tab, project_tab = st.tabs(
            ["How we estimate", "Reduce your footprint", "Project and contact"]
        )

        with estimate_tab:
            with st.expander(
                "How do you assess closed-source models?",
                icon=":material/model_training:",
                expanded=True,
            ):
                st.write(
                    "Impacts are derived from model architecture and parameter "
                    "count. For closed models we estimate counts from public "
                    "signals: leaked GPT-4 architecture scaled by pricing for "
                    "GPT-4-Turbo and GPT-4o, and benchmark-parity assumptions "
                    "for Claude-era models. Approximations, fully disclosed in "
                    "open code."
                )
            with st.expander(
                "Which models and providers are supported?",
                icon=":material/hub:",
            ):
                st.write(
                    "LLMs through major API providers today, with embeddings, "
                    "image, video and multimodal support on the roadmap."
                )
                st.link_button(
                    "See supported providers",
                    url="https://ecologits.ai/providers/",
                    icon=":material/open_in_new:",
                )
            with st.expander(
                "EcoLogits vs CodeCarbon?",
                icon=":material/compare_arrows:",
            ):
                st.write(
                    "EcoLogits estimates generative AI used through API "
                    "providers. CodeCarbon measures energy and GHG of compute "
                    "you run yourself. Deploying locally? Use CodeCarbon for "
                    "measured numbers."
                )

        with reduce_tab:
            tips = st.columns(2)
            with tips[0].container(border=True):
                st.markdown(":material/park:")
                st.subheader("Be frugal")
                st.markdown(
                    "- Question the need for AI, then GenAI\n"
                    "- Prefer small, specialized models\n"
                    "- Restrict scope and limit usage"
                )
            with tips[1].container(border=True):
                st.markdown(":material/memory:")
                st.subheader("Optimize serving")
                st.markdown(
                    "- Quantize models\n"
                    "- Use inference optimization tricks\n"
                    "- Fine-tune small models over generalists"
                )
            infra = st.columns(2)
            with infra[0].container(border=True):
                st.markdown(":material/cloud:")
                st.subheader("Choose clean infra")
                st.markdown(
                    "- Run in low-carbon, efficient regions "
                    "([electricitymaps.com](https://app.electricitymaps.com/map))\n"
                    "- Avoid buying new GPUs when existing capacity fits"
                )
            with infra[1].container(border=True):
                st.markdown(":material/monitoring:")
                st.subheader("Measure continuously")
                st.markdown(
                    "- Evaluate before, during and after\n"
                    "- Track with [EcoLogits](https://github.com/mlco2/ecologits) "
                    "or [CodeCarbon](https://github.com/mlco2/codecarbon)"
                )

        with project_tab:
            cols = st.columns(3)
            with cols[0].container(border=True):
                st.markdown(":material/volunteer_activism:")
                st.subheader("Contribute")
                st.caption(
                    "Feedback, discussions and pull requests welcome on "
                    "EcoLogits and this calculator."
                )
                st.link_button(
                    "Contribute on GitHub",
                    url="https://github.com/mlco2/ecologits/discussions/45",
                    icon=":material/open_in_new:",
                )
            with cols[1].container(border=True):
                st.markdown(":material/handshake:")
                st.subheader("Acknowledgements")
                st.caption(
                    "Thanks to Data For Good and Boavizta for tools, "
                    "best practices and LCA expertise."
                )
                st.link_button(
                    "Contact CodeCarbon",
                    url="https://codecarbon.io/contact/",
                    icon=":material/open_in_new:",
                )
            with cols[2].container(border=True):
                st.markdown(":material/chat:")
                st.subheader("Contact")
                st.caption(
                    "General questions: GitHub thread. Chat: Discord. Licensed CC BY-SA 4.0."
                )
                st.link_button(
                    "Join our Discord",
                    url="https://discord.gg/7KPzAfcN",
                    icon=":material/open_in_new:",
                )
