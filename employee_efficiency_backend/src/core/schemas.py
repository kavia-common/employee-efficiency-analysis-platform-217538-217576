from typing import List
from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class UploadResponse(BaseModel):
    """Response for dataset upload."""
    dataset_id: int = Field(..., description="Identifier of the uploaded dataset")
    filename: str = Field(..., description="Original filename")
    rows: int = Field(..., description="Row count")
    cols: int = Field(..., description="Column count")


# PUBLIC_INTERFACE
class CleanResponse(BaseModel):
    """Response for cleaning endpoint."""
    dataset_id: int
    removed_rows: int
    removed_cols: int
    message: str


# PUBLIC_INTERFACE
class EDAResponse(BaseModel):
    """EDA response."""
    dataset_id: int
    summary: dict


# PUBLIC_INTERFACE
class ANOVAResponse(BaseModel):
    """ANOVA response."""
    dataset_id: int
    results: dict


# PUBLIC_INTERFACE
class TrainRequest(BaseModel):
    """Model training request."""
    dataset_id: int
    target: str
    algorithm: str = Field(..., description="linear_regression | random_forest")


# PUBLIC_INTERFACE
class TrainResponse(BaseModel):
    """Model training response containing metrics."""
    dataset_id: int
    algorithm: str
    metrics: dict


# PUBLIC_INTERFACE
class PredictRequest(BaseModel):
    """Prediction request with feature rows."""
    model_dataset_id: int
    rows: list


# PUBLIC_INTERFACE
class PredictResponse(BaseModel):
    """Prediction response with predicted values."""
    predictions: list


# PUBLIC_INTERFACE
class ClusterRequest(BaseModel):
    """Cluster run request."""
    dataset_id: int
    n_clusters: int = 3


# PUBLIC_INTERFACE
class ClusterResponse(BaseModel):
    """Cluster response with labels and centers."""
    dataset_id: int
    n_clusters: int
    labels: List[int]
    centers: list


# PUBLIC_INTERFACE
class RecommendationsResponse(BaseModel):
    """Recommendations list response."""
    dataset_id: int
    items: List[str]


# PUBLIC_INTERFACE
class ReportPDFResponse(BaseModel):
    """Metadata response for report generation."""
    dataset_id: int
    filename: str
