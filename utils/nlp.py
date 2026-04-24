import pandas as pd

def keyword_risk(df):

    keywords = ["delay", "urgent", "critical", "risk", "blocked"]

    def score(text):
        if pd.isna(text):
            return 0
        text = str(text).lower()
        return sum(k in text for k in keywords)

    df["KeywordRisk"] = df["Subject"].apply(score)

    return df