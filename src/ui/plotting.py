import plotly.graph_objects as go
import streamlit as st


def range_plot(mean_val, min_val, max_val, unit):
    fig = go.Figure()

    # Background bar
    fig.add_trace(
        go.Bar(
            x=[max_val],
            y=[""],
            orientation="h",
            marker={"color": "#0B3B36"},
            showlegend=False,
            hoverinfo="skip",
        )
    )

    # Vertical line
    fig.add_shape(
        type="line",
        x0=mean_val,
        y0=-1,
        x1=mean_val,
        y1=1,
        line={"color": "#00BF63", "width": 3, "dash": "solid"},
        # name="Average"
    )

    # Add labels
    for val, pos, text in zip(
        [max_val, min_val] * 2,
        [0.85, 0.85, 1.6, 1.6],
        ["Max", "Min", f"{max_val:.3g} {unit}", f"{min_val:.3g} {unit}"], strict=False,
    ):
        fig.add_annotation(
            x=val, y=-pos, text=text, showarrow=False, font={"color": "black", "size": 16}
        )

    # fig.add_annotation(
    #     x=mean_val,
    #     y=1.65,
    #     text=f"{mean_val:.3g} {unit}",
    #     showarrow=False,
    #     font=dict(color="black", size=35),
    # )

    # Layout adjustments
    fig.update_layout(
        height=160,
        width=400,
        xaxis={"range": [min_val, max_val], "showgrid": False, "showticklabels": False},
        yaxis={"showticklabels": False},
        plot_bgcolor="white",
        margin={"l": 100, "r": 100, "t": 0, "b": 20},
        showlegend=False,
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, width="stretch", config={'displayModeBar': False})
