import streamlit as st
import pandas as pd


def render_venn_overview(df):

    # =========================
    # SAFE COLUMN HANDLING
    # =========================
    def safe(col):
        return df[col] if col in df.columns else ""

    # Normalize text fields
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].astype(str).str.lower()

    # =========================
    # SPLIT DATA
    # =========================
    tq = df[df["type"] == "tq"] if "type" in df.columns else pd.DataFrame()
    rfi = df[df["type"] == "rfi"] if "type" in df.columns else pd.DataFrame()

    # =========================
    # OVERLAP LOGIC (COMBINATION RULE)
    # =========================
    overlap_mask = (
        df["project"].isin(df["project"]) |
        df["originator"].isin(df["originator"]) |
        df["recipient"].isin(df["recipient"]) |
        df["doc type"].isin(df["doc type"])
    ) if all(col in df.columns for col in ["project", "originator", "recipient", "doc type"]) else pd.Series([False]*len(df))

    overlap = df[overlap_mask]

    # Remove overlap from pure groups
    tq_only = tq.drop(overlap.index.intersection(tq.index), errors="ignore")
    rfi_only = rfi.drop(overlap.index.intersection(rfi.index), errors="ignore")

    # =========================
    # COUNTS
    # =========================
    tq_count = len(tq)
    rfi_count = len(rfi)
    overlap_count = len(overlap)

    # =========================
    # HEADER
    # =========================
    st.markdown("## TQ / RFI Relationship Overview")

    # =========================
    # VISUAL LAYOUT (3 CIRCLES STYLE)
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="
            background: rgba(0,123,255,0.15);
            padding: 20px;
            border-radius: 16px;
            text-align:center;
            border: 1px solid rgba(0,123,255,0.4);
        ">
            <h2 style="color:white;">TQs Only</h2>
            <h1 style="color:#4da3ff;">{tq_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background: rgba(138,43,226,0.18);
            padding: 25px;
            border-radius: 20px;
            text-align:center;
            border: 2px solid rgba(138,43,226,0.5);
        ">
            <h2 style="color:white;">OVERLAP</h2>
            <h1 style="color:#c084fc;">{overlap_count}</h1>
            <p style="color:#cbd5e1;font-size:12px;">
                Shared Project / Originator / Doc Type
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background: rgba(255,165,0,0.15);
            padding: 20px;
            border-radius: 16px;
            text-align:center;
            border: 1px solid rgba(255,165,0,0.4);
        ">
            <h2 style="color:white;">RFIs Only</h2>
            <h1 style="color:#ffb347;">{rfi_count}</h1>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # INSIGHT SUMMARY
    # =========================
    st.markdown("---")

    st.markdown(f"""
    ### Insight Summary
    - Total TQs: **{tq_count}**
    - Total RFIs: **{rfi_count}**
    - Overlapping Items: **{overlap_count}**

    > Overlap indicates shared project context, originator linkage, or document dependency between TQs and RFIs.
    """)