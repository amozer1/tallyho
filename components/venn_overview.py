import streamlit as st


def render_venn_overview(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()

    # =========================
    # NORMALISE COLUMN NAMES
    # =========================
    df.columns = [c.strip().lower() for c in df.columns]

    # Map your real columns
    TYPE = "doc type"
    PROJECT = "project id"
    ORIGINATOR = "originator"
    RECIPIENT = "recipient"
    SUBJECT = "subject"

    required = [TYPE, PROJECT, ORIGINATOR, RECIPIENT]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    # CLEAN DATA
    # =========================
    for col in df.columns:
        df[col] = df[col].astype(str).str.lower()

    # =========================
    # SPLIT TQ / RFI
    # =========================
    tq = df[df[TYPE] == "tq"]
    rfi = df[df[TYPE] == "rfi"]

    # =========================
    # BUILD RELATIONSHIP KEY
    # =========================
    def build_key(x):
        return f"{x[PROJECT]}|{x[ORIGINATOR]}|{x[RECIPIENT]}|{x[SUBJECT][:20]}"

    tq["key"] = tq.apply(build_key, axis=1)
    rfi["key"] = rfi.apply(build_key, axis=1)

    # =========================
    # OVERLAP = COMMON KEYS
    # =========================
    overlap_keys = set(tq["key"]).intersection(set(rfi["key"]))

    overlap = df[df.apply(build_key, axis=1).isin(overlap_keys)]

    # =========================
    # CLEAN GROUPS
    # =========================
    tq_only = tq[~tq["key"].isin(overlap_keys)]
    rfi_only = rfi[~rfi["key"].isin(overlap_keys)]

    # =========================
    # TITLE
    # =========================
    st.markdown("## TQ / RFI Relationship Overview")

    # =========================
    # VISUAL OUTPUT
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="
            background: rgba(0,123,255,0.15);
            padding: 22px;
            border-radius: 16px;
            text-align:center;
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
                Project + Originator + Recipient + Subject Match
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
        ">
            <h3 style="color:white;">RFIs ONLY</h3>
            <h1 style="color:#ffb347;">{len(rfi_only)}</h1>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # INSIGHT SUMMARY
    # =========================
    st.markdown("---")

    st.markdown(f"""
    ### Insight Summary

    - Total TQs: **{len(tq)}**
    - Total RFIs: **{len(rfi)}**
    - Overlap items: **{len(overlap)}**

    > Overlap is detected using Project ID + Originator + Recipient + Subject similarity.
    """)