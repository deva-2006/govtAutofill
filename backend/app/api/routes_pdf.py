from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.config import settings
from app.core.logging import logger

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """Download the generated Tahsildar Application Request PDF."""
    safe_name = Path(filename).name
    pdf_path = settings.GENERATED_PDF_DIR / safe_name
    
    if not pdf_path.is_file():
        logger.warning(f"Requested PDF not found: {safe_name}")
        raise HTTPException(status_code=404, detail="Requested PDF document not found.")
        
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=safe_name,
        headers={"Content-Disposition": f"attachment; filename=\"{safe_name}\""}
    )

@router.get("/preview/{filename}")
async def preview_pdf(filename: str):
    """Preview the generated Tahsildar Application Request PDF inline in the browser."""
    safe_name = Path(filename).name
    pdf_path = settings.GENERATED_PDF_DIR / safe_name
    
    if not pdf_path.is_file():
        logger.warning(f"Requested PDF not found for preview: {safe_name}")
        raise HTTPException(status_code=404, detail="Requested PDF document not found.")
        
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=\"{safe_name}\""}
    )
