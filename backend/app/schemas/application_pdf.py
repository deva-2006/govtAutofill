from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.applicant import ApplicantDetails
from app.schemas.verification import VerificationPipelineReport

class ApplicationPDFContent(BaseModel):
    application_ref: str
    application_date: str
    district: str
    taluk: str
    applicant: ApplicantDetails
    verification_report: VerificationPipelineReport
    documents_enclosed: list[str] = Field(default_factory=list)
    declaration_accepted: bool = True
