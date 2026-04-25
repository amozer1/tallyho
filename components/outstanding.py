import streamlit as st


def render_outstanding_line(df, total):

    if df is None or len(df) == 0:
        st.warning("No data available")
        return

    df = df.copy()

    # =========================
    # CLEAN DATA PROPERLY (CRITICAL FIX)
    # =========================
    df["doc type"] = (
        df["doc type"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["reply date"] = pd.to_datetime(df["reply date"], errors="coerce")

    # =========================
    # OVERDUE FILTER (>7 DAYS + NOT REPLIED)
    # =========================
    overdue_df = df[(df["reply date"].isna()) & (df["age"] > 7)]

    overdue = len(overdue_df)
    overdue_pct = round((overdue / total) * 100, 1) if total else 0

    # =========================
    # SPLIT BY TYPE (NOW RELIABLE)
    # =========================
    tq_df = df[df["doc type"] == "TQ"]
    rfi_df = df[df["doc type"] == "RFI"]

    overdue_tq = len(overdue_df[overdue_df["doc type"] == "TQ"])
    overdue_rfi = len(overdue_df[overdue_df["doc type"] == "RFI"])

    tq_pct = round((overdue_tq / len(tq_df)) * 100, 1) if len(tq_df) else 0
    rfi_pct = round((overdue_rfi / len(rfi_df)) * 100, 1) if len(rfi_df) else 0

    # =========================
    # DEBUG (TEMP - REMOVE LATER)
    # =========================
    st.write("DEBUG - Total rows:", len(df))
    st.write("DEBUG - Overdue rows:", len(overdue_df))

    # =========================
    # OUTPUT
    # =========================
    st.markdown(f"""
### ⚠ Overdue (> 7 Days)

🔴 **Overdue = {overdue} ({overdue_pct}%)**

➡ TQ overdue: **{overdue_tq} ({tq_pct}%)**  
➡ RFI overdue: **{overdue_rfi} ({rfi_pct}%)**
""")