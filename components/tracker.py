import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    # -------------------------
    # CLEAN DATA
    # -------------------------
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    df["age"] = (today - df["date sent"]).dt.days

    total = len(df)

    tq = df[df["doc type"].str.lower() == "tq"]
    rfi = df[df["doc type"].str.lower() == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])

    both_not = min(tq_not, rfi_not)

    tq_only = max(tq_not - both_not, 0)
    rfi_only = max(rfi_not - both_not, 0)

    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # percentages
    tq_only_pct = round((tq_only / total) * 100, 1) if total else 0
    both_pct = round((both_not / total) * 100, 1) if total else 0
    rfi_only_pct = round((rfi_only / total) * 100, 1) if total else 0

    # -------------------------
    # TITLE
    # -------------------------
    st.markdown("### 📊 Not Responded within 7 Days")

    left, right = st.columns([2.3, 1])

    # -------------------------
    # LEFT PANEL
    # -------------------------
    with left:

        fig = go.Figure()

        # circles
        fig.add_shape(type="circle", x0=0.0, y0=0.2, x1=1.2, y1=1.4,
                      fillcolor="rgba(59,130,246,0.35)", line_color="#3b82f6")

        fig.add_shape(type="circle", x0=0.7, y0=0.2, x1=1.9, y1=1.4,
                      fillcolor="rgba(168,85,247,0.35)", line_color="#a855f7")

        fig.add_shape(type="circle", x0=1.4, y0=0.2, x1=2.6, y1=1.4,
                      fillcolor="rgba(34,197,94,0.35)", line_color="#22c55e")

        # text annotations
        fig.add_annotation(
            x=0.6, y=0.8,
            text=f"TQ Only<br><b>{tq_only_pct}%</b><br>({tq_only})",
            showarrow=False,
            font=dict(color="white", size=16)
        )

        fig.add_annotation(
            x=1.3, y=0.8,
            text=f"Both TQ & RFI<br><b>{both_pct}%</b><br>({both_not})",
            showarrow=False,
            font=dict(color="white", size=16)
        )

        fig.add_annotation(
            x=2.0, y=0.8,
            text=f"RFI Only<br><b>{rfi_only_pct}%</b><br>({rfi_only})",
            showarrow=False,
            font=dict(color="white", size=16)
        )

        fig.update_layout(
            height=320,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False, range=[-0.1, 2.7]),
            yaxis=dict(visible=False, range=[0, 1.6]),
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # RIGHT PANEL
    # -------------------------
    with right:

        st.markdown("#### Summary")

        st.markdown(f"""
🔵 TQ Not Responded  
**{round((tq_not/total)*100,1) if total else 0}% ({tq_not})**

🟢 RFI Not Responded  
**{round((rfi_not/total)*100,1) if total else 0}% ({rfi_not})**

🟣 Both Not Responded  
**{round((both_not/total)*100,1) if total else 0}% ({both_not})**
        """)

        st.markdown("---")

        st.markdown(f"""
### Total Outstanding > 7 Days

<span style='color:red;font-size:24px;'><b>{overdue}</b></span>  
({round((overdue/total)*100,1) if total else 0}%)
        """, unsafe_allow_html=True)