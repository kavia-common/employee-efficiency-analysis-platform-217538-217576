from io import BytesIO
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa
from sqlalchemy.orm import Session

from src.core.models import Dataset, EDAResult, ANOVAResult, ModelResult, ClusterResult
from src.services.recommendations import get_recommendations

TEMPLATES_DIR = "employee-efficiency-analysis-platform-217538-217576/employee_efficiency_backend/reports/templates"


def _html_to_pdf_bytes(html: str) -> bytes:
    result = BytesIO()
    pisa.CreatePDF(src=html, dest=result)
    return result.getvalue()


# PUBLIC_INTERFACE
def build_pdf_report(dataset_id: int, db: Session):
    """Render the executive report HTML and convert to PDF bytes."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise ValueError("Dataset not found")

    eda = db.query(EDAResult).filter(EDAResult.dataset_id == dataset.id).first()
    anova = db.query(ANOVAResult).filter(ANOVAResult.dataset_id == dataset.id).first()
    model = db.query(ModelResult).filter(ModelResult.dataset_id == dataset.id).first()
    cluster = db.query(ClusterResult).filter(ClusterResult.dataset_id == dataset.id).first()

    items = get_recommendations(dataset_id, db)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape()
    )
    template = env.get_template("executive_report.html")

    context = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "dataset": dataset,
        "eda": eda.summary_json if eda else {},
        "anova": anova.result_json if anova else {},
        "model": model.metrics_json if model else {},
        "cluster": {
            "n_clusters": cluster.n_clusters if cluster else 0,
            "labels": (cluster.labels_json or {}).get("labels", []) if cluster else [],
            "centers": (cluster.centers_json or {}).get("centers", []) if cluster else [],
        },
        "recommendations": items,
    }

    html = template.render(**context)
    pdf_bytes = _html_to_pdf_bytes(html)
    filename = f"executive_report_{dataset_id}.pdf"
    return filename, pdf_bytes
