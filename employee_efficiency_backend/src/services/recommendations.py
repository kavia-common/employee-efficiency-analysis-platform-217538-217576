from sqlalchemy.orm import Session

from src.core.models import Dataset, EDAResult, ANOVAResult, ClusterResult


# PUBLIC_INTERFACE
def get_recommendations(dataset_id: int, db: Session):
    """Generate simple rule-based recommendations from EDA, ANOVA, and Clustering."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")

    eda = db.query(EDAResult).filter(EDAResult.dataset_id == dataset.id).first()
    anova = db.query(ANOVAResult).filter(ANOVAResult.dataset_id == dataset.id).first()
    cluster = db.query(ClusterResult).filter(ClusterResult.dataset_id == dataset.id).first()

    recs = []

    if eda and eda.summary_json:
        shape = eda.summary_json.get("shape", {})
        recs.append(f"Dataset has {shape.get('rows', 0)} rows and {shape.get('cols', 0)} columns.")
        if "numeric_summary" in eda.summary_json:
            recs.append("Standardize numeric features before modeling to improve stability.")

    if anova and anova.result_json:
        pval = anova.result_json.get("p_value", 1.0)
        if pval < 0.05:
            recs.append(f"ANOVA indicates significant differences across {anova.result_json.get('group_by')} (p={pval:.3f}). Consider tailored policies.")
        else:
            recs.append("No significant group differences detected by ANOVA.")

    if cluster and cluster.labels_json:
        k = cluster.n_clusters
        recs.append(f"Clustering found {k} segments. Personalize recommendations per cluster.")

    if not recs:
        recs.append("Upload data and run EDA/ANOVA/Clustering to receive recommendations.")

    return recs
