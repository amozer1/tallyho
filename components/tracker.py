def render_tracker(df):

    if df is None or df.empty:
        st.warning("No data available.")
        return

    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = ["doc type", "date sent", "reply date"]

    for c in required:
        if c not in df.columns:
            st.error(f"Missing column: {c}")
            return

    # =========================
    # CLEAN + SAFE DATA PROCESSING
    # =========================

    df["doc type"] = df["doc type"].astype(str).str.lower().str.strip()

    df["date sent"] = pd.to_datetime(df["date sent"], errors="coerce")
    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())

    df["age"] = (today - df["date sent"]).dt.days

    # optional safety: remove invalid rows affecting age logic
    df = df[df["age"].notna()]

    total = len(df)

    # =========================
    # SPLIT TYPES
    # =========================
    tq = df[df["doc type"] == "tq"]
    rfi = df[df["doc type"] == "rfi"]

    tq_total = len(tq)
    rfi_total = len(rfi)

    tq_pct = round((tq_total / total) * 100, 1) if total else 0
    rfi_pct = round((rfi_total / total) * 100, 1) if total else 0

    # =========================
    # NOT RESPONDED
    # =========================
    tq_not = len(tq[tq["reply date"].isna()])
    rfi_not = len(rfi[rfi["reply date"].isna()])
    total_not = len(df[df["reply date"].isna()])

    tq_not_pct = round((tq_not / tq_total) * 100, 1) if tq_total else 0
    rfi_not_pct = round((rfi_not / rfi_total) * 100, 1) if rfi_total else 0
    total_not_pct = round((total_not / total) * 100, 1) if total else 0

    # =========================
    # OVERDUE (>7 DAYS)
    # =========================
    overdue = len(df[(df["reply date"].isna()) & (df["age"] > 7)])

    # =========================
    # CARD WRAPPER START
    # =========================
    render_card(
        "TQ & RFI Intelligence Hub",
        "Project Controls • Response Analytics • Document Tracking"
    )

    # =========================
    # LAYOUT
    # =========================
    left, right = st.columns([1, 1])

    with left:
        fig = go.Figure()

        # =================================================
        # YOUR EXISTING FIGURE CODE (UNCHANGED)
        # =================================================
        # (keep all shapes, annotations, layout exactly as-is)

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # OPTIONAL RIGHT PANEL (IF YOU USE IT LATER)
    # =========================
    with right:
        st.markdown("")

    # =========================
    # CLOSE CARD
    # =========================
    end_card()