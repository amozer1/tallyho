import streamlit as st


def render_venn_overview(df):

    # =========================
    # SAFETY CHECK
    # =========================
    if df is None or df.empty:
        st.warning("No data available for Venn analysis.")
        return

    df = df.copy()

    # =========================
    # NORMALISE COLUMNS
    # =========================
    for col in df.columns:
        df[col] = df[col].astype(str).str.lower()

    # =========================
    # REQUIRED FIELDS CHECK
    # =========================
    required = ["type", "project", "originator", "recipient", "doc type"]

    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing required columns: {missing}")
        return

    # =========================
    # SPLIT TQ / RFI
    # =========================
    tq = df[df["type"] == "tq"]
    rfi = df[df["type"] == "rfi"]

    # =========================
    # OVERLAP LOGIC (COMBINED INTELLIGENCE RULE)
    # =========================
    overlap_mask = (
        df["project"].isin(df["project"]) |
        df["originator"].isin(df["originator"]) |
        df["recipient"].isin(df["recipient"]) |
        df["doc type"].isin(df["doc type"])
    )

    overlap = df[overlap_mask]

    # Remove overlap duplicates from pure groups
    tq_only = tq.drop(overlap.index.intersection(tq.index), errors="ignore")
    rfi_only = rfi.drop(overlap.index.intersection(rfi.index), errors="ignore")

    # =========================
    # HEADER
    # =========================
    st.markdown("## TQ / RFI Relationship Overview")

    # =========================
    # VISUAL CIRCLES (STREAMLIT SAFE)
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="
            background: rgba(0,123,255,0.15);
            padding: 22px;
            border-radius: 16px;
            text-align:center;
            border: 1px solid rgba(0,123,255,0.4);
        ">
            <h3 style="color:white;">TQs ONLY</h3>
            <h1 style="color:#4da3ff;">{len(tq_only)}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background: rgba(138,43,226,0.20);
            padding: 26px;
            border-radius: 18px;
            text-align:center;
            border: 2px solid rgba(138,43,226,0.6);
        ">
            <h3 style="color:white;">OVERLAP</h3>
            <h1 style="color:#c084fc;">{len(overlap)}</h1>
            <p style="color:#cbd5e1;font-size:12px;">
                Shared Project • Originator • Doc Type • Recipient
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background: rgba(255,165,0,0.15);
            padding: 22px;
            border-radius: 16px;
            text-align:center;
            border: 1px solid rgba(255,165,0,0.4);
        ">
            <h3 style="color:white;">RFIs ONLY</h3>
            <h1 style="color:#ffb347;">{len(rfi_only)}</h1>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # INSIGHT BLOCK
    # =========================
    st.markdown("---")

    st.markdown(f"""
    ### Insight Summary

    - TQs (clean): **{len(tq_only)}**
    - RFIs (clean): **{len(rfi_only)}**
    - Overlap (linked items): **{len(overlap)}**

    > Overlap represents cross-linked communication items based on project, originator, recipient, and document type relationships.
    """)
