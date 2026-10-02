import streamlit as st


def support_page() -> None:
    with st.container(key="support_page"):
        # Hero
        with st.container(horizontal_alignment="center"):
            st.badge(
                "Volunteer-maintained since June 2024",
                icon=":material/favorite:",
                color="green",
            )
            st.title("Help keep this tool free and open", text_alignment="center")
            st.markdown(
                "At CodeCarbon, this calculator is developed and maintained "
                "entirely on a volunteer basis. Your support keeps it a free "
                "and open-source resource for the common good.",
                text_alignment="center",
            )
            with st.container(horizontal=True, horizontal_alignment="center"):
                st.link_button(
                    "Star on GitHub",
                    url="https://github.com/mlco2/ecologits",
                    type="primary",
                    icon=":material/star:",
                )
                st.link_button(
                    "Join our Discord",
                    url="https://discord.gg/7KPzAfcN",
                    icon=":material/chat:",
                )
                st.link_button(
                    "Follow on LinkedIn",
                    url="https://www.linkedin.com/company/ecologits/",
                    icon=":material/work:",
                )

        tiers = st.columns(3)
        with tiers[0].container(border=True):
            st.markdown(":material/bolt:")
            st.subheader("If you have 1 second")
            st.caption("Three quick ways to help the project.")
            st.markdown(
                "- Give a like to this space\n"
                "- Star the EcoLogits repository\n"
                "- Follow us on LinkedIn"
            )
            st.link_button(
                "Star the repository",
                url="https://github.com/mlco2/ecologits",
                icon=":material/open_in_new:",
            )
        with tiers[1].container(border=True):
            st.markdown(":material/forum:")
            st.subheader("If you have 5 minutes")
            st.caption("Share feedback and help the community.")
            st.markdown(
                "- Chat with us on Discord\n"
                "- Start a GitHub discussion\n"
                "- Message us on LinkedIn"
            )
            st.link_button(
                "Start a discussion",
                url="https://github.com/mlco2/ecologits/discussions/45",
                icon=":material/open_in_new:",
            )
        with tiers[2].container(border=True):
            st.markdown(":material/volunteer_activism:")
            st.subheader("If you have more to give")
            st.caption("Contribute code or join the mission.")
            st.markdown(
                "- Contribute to EcoLogits, the calculator or the API\n"
                "- Become an active CodeCarbon member"
            )
            st.link_button(
                "Become a member",
                url="https://codecarbon.io/",
                icon=":material/open_in_new:",
            )

        st.header("Contribute your way", icon=":material/handshake:")
        roles = st.columns(2)
        with roles[0].container(border=True):
            st.markdown(":material/person:")
            st.subheader("As an individual")
            st.caption("All open-source contributions are welcome.")
            st.markdown(
                "- Contribute to [EcoLogits](https://github.com/mlco2/ecologits), "
                "the [calculator](https://github.com/mlco2/ecologits-calculator) "
                "or the [API](https://github.com/mlco2/ecologits-api)\n"
                "- Become an active member of the "
                "[CodeCarbon](https://codecarbon.io/) nonprofit"
            )
            st.link_button(
                "Contribute on GitHub",
                url="https://github.com/mlco2/ecologits",
                icon=":material/open_in_new:",
            )
        with roles[1].container(border=True):
            st.markdown(":material/business:")
            st.subheader("As an organization")
            st.caption(
                "If this calculator brings value to your organization, "
                "customers or communities, help fund it."
            )
            st.markdown(
                "- Become a **sponsor**\n"
                "- Become a **benefactor member** as a public-sector body, "
                "nonprofit or university"
            )
            st.link_button(
                "Contact CodeCarbon",
                url="https://codecarbon.io/",
                icon=":material/open_in_new:",
            )
