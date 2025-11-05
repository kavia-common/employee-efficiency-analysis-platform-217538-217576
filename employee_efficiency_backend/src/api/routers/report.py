from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO

from src.core.db import get_db
from src.core.schemas import ReportPDFResponse
from src.services.report import build_pdf_report

router = APIRouter(tags=["Report"])


# PUBLIC_INTERFACE
@router.get("/pdf", summary="Generate executive report PDF", response_model=ReportPDFResponse)
def generate_pdf(dataset_id: int, db: Session = Depends(get_db)):
    """Generate the executive report PDF and return metadata; the PDF stream is available at /report/pdf/download."""
    # Produce and cache PDF in memory to be downloaded by a follow-up endpoint if needed
    try:
        filename, _ = build_pdf_report(dataset_id, db)
        return ReportPDFResponse(dataset_id=dataset_id, filename=filename)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# PUBLIC_INTERFACE
@router.get("/pdf/download", summary="Download report PDF")
def download_pdf(dataset_id: int, db: Session = Depends(get_db)):
    """Return the PDF as application/pdf."""
    try:
        filename, pdf_bytes = build_pdf_report(dataset_id, db)
        return StreamingResponse(BytesIO(pdf_bytes), media_type="application/pdf", headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        })
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
