from datetime import datetime
from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.core.db import Base


class Dataset(Base):
    __tablename__ = "datasets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    stored_path: Mapped[str] = mapped_column(String(512))
    rows: Mapped[int] = mapped_column(Integer, default=0)
    cols: Mapped[int] = mapped_column(Integer, default=0)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    eda_result = relationship("EDAResult", back_populates="dataset", uselist=False)
    anova_result = relationship("ANOVAResult", back_populates="dataset", uselist=False)
    model_result = relationship("ModelResult", back_populates="dataset", uselist=False)
    cluster_result = relationship("ClusterResult", back_populates="dataset", uselist=False)
    recommendations = relationship("Recommendation", back_populates="dataset")


class EDAResult(Base):
    __tablename__ = "eda_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"), unique=True)
    summary_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="eda_result")


class ANOVAResult(Base):
    __tablename__ = "anova_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"), unique=True)
    result_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="anova_result")


class ModelResult(Base):
    __tablename__ = "model_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"), unique=True)
    algo: Mapped[str] = mapped_column(String(100))
    metrics_json: Mapped[dict] = mapped_column(JSON)
    model_blob: Mapped[str] = mapped_column(Text)  # store as base64 string for simplicity
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="model_result")


class ClusterResult(Base):
    __tablename__ = "cluster_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"), unique=True)
    n_clusters: Mapped[int] = mapped_column(Integer)
    labels_json: Mapped[dict] = mapped_column(JSON)  # {"labels": [...]}
    centers_json: Mapped[dict] = mapped_column(JSON)  # {"centers": [[...], ...]}
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="cluster_result")


class Recommendation(Base):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"))
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="recommendations")
