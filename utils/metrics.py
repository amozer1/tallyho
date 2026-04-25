def get_metrics(df):
    if df.empty:
        return {
            "total_tq": 0,
            "total_rfi": 0,
            "closed": 0,
            "open": 0,
            "overdue7": 0,
            "avg_response": 0,
            "sla": 0
        }

    total_tq = len(df[df["Type"] == "TQ"])
    total_rfi = len(df[df["Type"] == "RFI"])
    closed = len(df[df["Status"].astype(str).str.lower() == "closed"])
    open_items = len(df[df["Status"].astype(str).str.lower() != "closed"])
    overdue7 = len(df[df["AgeDays"] > 7])
    avg_response = round(df["ResponseDays"].fillna(0).mean(), 1)

    within_sla = len(df[df["ResponseDays"] <= 7])
    sla = round((within_sla / len(df)) * 100, 1)

    return {
        "total_tq": total_tq,
        "total_rfi": total_rfi,
        "closed": closed,
        "open": open_items,
        "overdue7": overdue7,
        "avg_response": avg_response,
        "sla": sla
    }