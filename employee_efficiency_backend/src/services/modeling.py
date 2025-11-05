import os
import base64
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from joblib import dump, load
from tempfile import NamedTemporaryFile

from src.core.models import Dataset, ModelResult


def _load_df(dataset: Dataset) -> pd.DataFrame:
    if not os.path.exists(dataset.stored_path):
        raise ValueError("Dataset file not found")
    return pd.read_csv(dataset.stored_path)


def _prepare_xy(df: pd.DataFrame, target: str):
    if target not in df.columns:
        raise RuntimeError("Target column not found")
    df_clean = df.dropna()
    y = df_clean[target]
    X = df_clean.drop(columns=[target])
    # keep only numeric features
    X = X.select_dtypes(include="number")
    if X.empty:
        raise RuntimeError("No numeric features available for training")
    return X, y


def _serialize_model(model) -> str:
    with NamedTemporaryFile(suffix=".joblib", delete=False) as tmp:
        dump(model, tmp.name)
        tmp.seek(0)
        with open(tmp.name, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
    os.remove(tmp.name)
    return encoded


def _deserialize_model(b64: str):
    raw = base64.b64decode(b64.encode("utf-8"))
    with NamedTemporaryFile(suffix=".joblib", delete=False) as tmp:
        tmp.write(raw)
        tmp.flush()
        model = load(tmp.name)
    os.remove(tmp.name)
    return model


# PUBLIC_INTERFACE
def train_model(dataset_id: int, target: str, algorithm: str, db: Session) -> dict:
    """Train a model and store metrics and serialized model in DB."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")

    df = _load_df(dataset)
    X, y = _prepare_xy(df, target)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if algorithm.lower() == "linear_regression":
        model = LinearRegression()
    elif algorithm.lower() == "random_forest":
        model = RandomForestRegressor(n_estimators=200, random_state=42)
    else:
        raise RuntimeError("Unsupported algorithm. Use 'linear_regression' or 'random_forest'.")

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    metrics = {
        "r2": float(r2_score(y_test, preds)),
        "rmse": float(mean_squared_error(y_test, preds, squared=False)),
        "features": list(X.columns),
        "target": target,
    }

    blob = _serialize_model(model)

    existing = db.query(ModelResult).filter(ModelResult.dataset_id == dataset.id).first()
    if existing:
        existing.algo = algorithm
        existing.metrics_json = metrics
        existing.model_blob = blob
    else:
        db.add(ModelResult(dataset_id=dataset.id, algo=algorithm, metrics_json=metrics, model_blob=blob))
    db.commit()

    return {"metrics": metrics}


# PUBLIC_INTERFACE
def predict_with_model(model_dataset_id: int, rows: list, db: Session):
    """Predict using the stored model for dataset."""
    dataset = db.query(Dataset).filter(Dataset.id == model_dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")
    stored = db.query(ModelResult).filter(ModelResult.dataset_id == dataset.id).first()
    if not stored:
        raise RuntimeError("No trained model found for this dataset")

    model = _deserialize_model(stored.model_blob)
    # Ensure incoming rows have numeric features in the same order
    features = stored.metrics_json.get("features", [])
    import pandas as pd
    df = pd.DataFrame(rows, columns=features)
    df = df[features]
    preds = model.predict(df)
    return [float(p) for p in preds]
