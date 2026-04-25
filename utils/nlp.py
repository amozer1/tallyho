import pandas as pd

def extract_keywords(df):

    text = df["Subject"].fillna("").str.lower()

    keywords = {
        "risk": text.str.contains("risk").sum(),
        "urgent": text.str.contains("urgent").sum(),
        "delay": text.str.contains("delay").sum(),
        "design": text.str.contains("design").sum()
    }

    return keywords