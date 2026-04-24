import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def prepare_data(df):

    df = df.copy()

    df["AgeDays"] = df["AgeDays"].fillna(0)

    df["IsTQ"] = (df["Doc Type"] == "TQ").astype(int)
    df["IsRFI"] = (df["Doc Type"] == "RFI").astype(int)

    sender_load = df["Sender"].value_counts().to_dict()
    df["SenderLoad"] = df["Sender"].map(sender_load)

    recipient_load = df["Recipient"].value_counts().to_dict()
    df["RecipientLoad"] = df["Recipient"].map(recipient_load)

    df["Target"] = (df["AgeDays"] > 7).astype(int)

    X = df[[
        "AgeDays",
        "IsTQ",
        "IsRFI",
        "SenderLoad",
        "RecipientLoad"
    ]].fillna(0)

    y = df["Target"]

    return X, y, df


def train_model(df):

    X, y, df = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    return model, accuracy, df


def predict(model, df):

    X, _, df = prepare_data(df)

    df["Risk %"] = model.predict_proba(X)[:, 1] * 100

    df["Risk Level"] = pd.cut(
        df["Risk %"],
        bins=[0,40,70,100],
        labels=["Low","Medium","High"]
    )

    return df