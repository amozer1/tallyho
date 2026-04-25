def get_metrics(df):
    if df is None or df.empty:
        return {
            "total_tq": 0,
            "total_rfi": 0,
            "closed": 0,
            "open": 0,
            "overdue7": 0,
            "avg_response": 0,
            "sla": 0
        }

    # Safe column access
    df = df.copy()

    df["Type"] = df.get("Type", "")
    df["Status"] = df.get("Status", "").astype(str)
    df["AgeDays"] = pd.to_numeric(df.get("AgeDays", 0), errors="coerce").fillna(0)

    response = pd.to_numeric(df.get("ResponseDays", 0), errors="coerce").fillna(0)

    total_tq = (df["Type"] == "TQ").sum()
    total_rfi = (df["Type"] == "RFI").sum()

    closed = df["Status"].str.lower().eq("closed").sum()
    open_items = len(df) - closed

    overdue7 = (df["AgeDays"] > 7).sum()

    avg_response = round(response.mean(), 1) if len(df) > 0 else 0

    within_sla = (response <= 7).sum()

    sla = round((within_sla / len(df)) * 100, 1) if len(df) > 0 else 0

    return {
        "total_tq": int(total_tq),
        "total_rfi": int(total_rfi),
        "closed": int(closed),
        "open": int(open_items),
        "overdue7": int(overdue7),
        "avg_response": float(avg_response),
        "sla": float(sla)
    }