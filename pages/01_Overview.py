# =========================
# HEATMAP STYLE DONUT (CLEANER MODEL)
# =========================

tq_val = len(tq_over)
rfi_val = len(rfi_over)

labels = ["TQ Not Responded", "RFI Not Responded"]
values = [tq_val, rfi_val]

# Heatmap-style gradient colours (professional engineering dashboard look)
colors = ["#2F80ED", "#EB5757"]  # blue → red (heat scale feel)

fig = go.Figure(
    data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.72,  # smaller inner circle = cleaner look
            marker=dict(colors=colors),
            textinfo="label+value+percent",
            hoverinfo="label+value"
        )
    ]
)

fig.update_layout(
    title="TQ vs RFI Not Responded (>7 Days)",
    paper_bgcolor="#0b1a2f",
    plot_bgcolor="#0b1a2f",
    font=dict(color="white"),
    margin=dict(t=40, b=10, l=10, r=10),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)