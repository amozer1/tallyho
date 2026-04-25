import joblib
import pandas as pd

MODEL_PATH = "models/risk_model.pkl"

def train_model(df):
    from sklearn.ensemble import RandomForestClassifier

    df = df.copy()
    df["Target"] = (df["AgeDays"] > 7).astype(int)

    X = df[["AgeDays"]]
    y = df["Target"]

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    return model


def load_model():
    return joblib.load(MODEL_PATH)


def predict_risk(model, df):
    df = df.copy()
    df["RiskScore"] = model.predict_proba(df[["AgeDays"]])[:, 1]
    return df