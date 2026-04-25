def compute_metrics(df):
    total = len(df)
    tq = len(df[df["Doc Type"]=="TQ"])
    rfi = len(df[df["Doc Type"]=="RFI"])
    closed = df["Closed"].sum()
    open_ = df["Open"].sum()
    overdue = df["Overdue"].sum()
    avg_response = round(df["ResponseDays"].mean(),1)
    sla = round(((total-overdue)/total)*100,1)

    return {
        "total": total,
        "tq": tq,
        "rfi": rfi,
        "closed": closed,
        "open": open_,
        "overdue": overdue,
        "avg_response": avg_response,
        "sla": sla
    }