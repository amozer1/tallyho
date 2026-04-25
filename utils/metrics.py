def get_metrics(df):

    return {
        "total_tq": len(df[df["Doc Type"] == "TQ"]),
        "total_rfi": len(df[df["Doc Type"] == "RFI"]),
        "closed": len(df[df["IsClosed"] == True]),
        "open": len(df[df["IsClosed"] == False]),
        "overdue7": len(df[df["AgeDays"] > 7]),
        "sla": round((df["AgeDays"] <= 7).mean() * 100, 1)
    }