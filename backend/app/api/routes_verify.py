import os
import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.config import settings
from app.core.logging import logger
from app.schemas.applicant import ApplicantDetails
from app.schemas.verification import VerificationPipelineReport
from app.verification.pipeline import run_verification_pipeline

router = APIRouter(prefix="/verify", tags=["Verification"])

@router.get("/sample-info")
async def get_sample_info():
    """Returns sample applicant details and checks availability of sample documents for quick evaluation."""
    sample_files = {
        "birth_certificate": (settings.SAMPLE_DOCS_DIR / "child_birth.jpeg").exists(),
        "aadhaar_card": (settings.SAMPLE_DOCS_DIR / "child_aadhar.pdf").exists(),
        "parent_community_certificate": (settings.SAMPLE_DOCS_DIR / "mother_community.jpeg").exists(),
        "family_card": (settings.SAMPLE_DOCS_DIR / "ration_card.pdf").exists(),
    }
    sample_applicant = {
        "child_name": "Deva S",
        "child_gender": "Male",
        "child_dob": "21/02/2006",
        "child_community": "MBC",
        "child_sub_caste": "Hindu Vanniakula Kshatriya",
        "father_name": "Shankar",
        "father_community": "MBC",
        "mother_name": "Sumathi",
        "mother_community": "MBC",
        "parent_certificate_submitted": "mother",
        "door_no": "78",
        "street": "2nd Street, Indra Gandhi Nagar",
        "village_town": "Vyasarpadi",
        "taluk": "Perambur",
        "district": "Chennai",
        "pincode": "600039"
    }
    return {
        "sample_applicant": sample_applicant,
        "sample_docs_available": sample_files,
        "all_sample_docs_ready": all(sample_files.values())
    }

@router.post("/sample", response_model=VerificationPipelineReport)
async def verify_sample_pipeline():
    """
    Executes the full 8-stage verification pipeline using the preloaded official sample documents.
    Allows instant demonstration and review of the verification workflow.
    """
    birth_path = settings.SAMPLE_DOCS_DIR / "child_birth.jpeg"
    aadhaar_path = settings.SAMPLE_DOCS_DIR / "child_aadhar.pdf"
    comm_path = settings.SAMPLE_DOCS_DIR / "mother_community.jpeg"
    family_path = settings.SAMPLE_DOCS_DIR / "ration_card.pdf"

    for p in [birth_path, aadhaar_path, comm_path, family_path]:
        if not p.exists():
            raise HTTPException(status_code=404, detail=f"Sample document not found: {p.name}")

    applicant = ApplicantDetails(
        child_name="Deva S",
        child_gender="Male",
        child_dob="21/02/2006",
        child_community="MBC",
        child_sub_caste="Hindu Vanniakula Kshatriya",
        father_name="Shankar",
        father_community="MBC",
        mother_name="Sumathi",
        mother_community="MBC",
        parent_certificate_submitted="mother",
        door_no="78",
        street="2nd Street, Indra Gandhi Nagar",
        village_town="Vyasarpadi",
        taluk="Perambur",
        district="Chennai",
        pincode="600039"
    )

    report = run_verification_pipeline(
        applicant=applicant,
        birth_cert_path=birth_path,
        aadhaar_path=aadhaar_path,
        community_cert_path=comm_path,
        family_card_path=family_path
    )
    return report

@router.post("", response_model=VerificationPipelineReport)
async def verify_application(
    child_name: str = Form(...),
    child_gender: str = Form(...),
    child_dob: str = Form(...),
    child_community: str = Form(...),
    child_sub_caste: Optional[str] = Form(None),
    father_name: str = Form(...),
    father_community: Optional[str] = Form(None),
    mother_name: str = Form(...),
    mother_community: Optional[str] = Form(None),
    parent_certificate_submitted: str = Form("mother"),
    door_no: Optional[str] = Form(None),
    street: Optional[str] = Form(None),
    village_town: Optional[str] = Form(None),
    taluk: Optional[str] = Form(None),
    district: Optional[str] = Form(None),
    pincode: Optional[str] = Form(None),
    birth_certificate: UploadFile = File(...),
    aadhaar_card: UploadFile = File(...),
    parent_community_certificate: UploadFile = File(...),
    family_card: UploadFile = File(...)
):
    """
    Submits application details and 4 mandatory supporting documents to execute the 8-stage verification pipeline.
    """
    session_id = uuid.uuid4().hex[:8]
    session_upload_dir = settings.UPLOAD_DIR / session_id
    session_upload_dir.mkdir(parents=True, exist_ok=True)

    applicant = ApplicantDetails(
        child_name=child_name.strip(),
        child_gender=child_gender.strip(),
        child_dob=child_dob.strip(),
        child_community=child_community.strip(),
        child_sub_caste=child_sub_caste.strip() if child_sub_caste else None,
        father_name=father_name.strip(),
        father_community=father_community.strip() if father_community else None,
        mother_name=mother_name.strip(),
        mother_community=mother_community.strip() if mother_community else None,
        parent_certificate_submitted=parent_certificate_submitted.strip().lower(),
        door_no=door_no.strip() if door_no else None,
        street=street.strip() if street else None,
        village_town=village_town.strip() if village_town else None,
        taluk=taluk.strip() if taluk else None,
        district=district.strip() if district else None,
        pincode=pincode.strip() if pincode else None
    )

    # Save uploaded files safely
    def save_file(upload_file: UploadFile, filename: str) -> Path:
        dest_path = session_upload_dir / filename
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return dest_path

    birth_ext = Path(birth_certificate.filename or "birth.jpeg").suffix or ".jpeg"
    aadhaar_ext = Path(aadhaar_card.filename or "aadhaar.pdf").suffix or ".pdf"
    comm_ext = Path(parent_community_certificate.filename or "community.jpeg").suffix or ".jpeg"
    family_ext = Path(family_card.filename or "family.pdf").suffix or ".pdf"

    saved_birth = save_file(birth_certificate, f"birth_certificate{birth_ext}")
    saved_aadhaar = save_file(aadhaar_card, f"child_aadhaar{aadhaar_ext}")
    saved_comm = save_file(parent_community_certificate, f"parent_community{comm_ext}")
    saved_family = save_file(family_card, f"family_card{family_ext}")

    logger.info(f"Executing verification pipeline for applicant: {applicant.child_name}")
    try:
        report = run_verification_pipeline(
            applicant=applicant,
            birth_cert_path=saved_birth,
            aadhaar_path=saved_aadhaar,
            community_cert_path=saved_comm,
            family_card_path=saved_family
        )
        return report
    except Exception as e:
        logger.error(f"Pipeline execution error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Verification pipeline failed: {str(e)}")
