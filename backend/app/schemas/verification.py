from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field

class StageStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    VERIFIED = "VERIFIED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    FAILED = "FAILED"

class ExtractedBirthCert(BaseModel):
    child_name: Optional[str] = None
    child_name_ta: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    registration_no: Optional[str] = None
    place_of_birth: Optional[str] = None
    issuing_authority: Optional[str] = None
    raw_text: Optional[str] = None

class ExtractedAadhaar(BaseModel):
    name: Optional[str] = None
    father_or_guardian: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    aadhaar_masked: Optional[str] = None
    raw_text: Optional[str] = None

class ExtractedCommunityCert(BaseModel):
    person_name: Optional[str] = None
    community_category: Optional[str] = None  # e.g., MBC, BC, SC, ST
    sub_caste: Optional[str] = None           # e.g., Hindu Vanniakula Kshatriya
    certificate_no: Optional[str] = None
    issuing_authority: Optional[str] = None
    taluk: Optional[str] = None
    district: Optional[str] = None
    date_of_issue: Optional[str] = None
    raw_text: Optional[str] = None

class ExtractedFamilyCard(BaseModel):
    head_name: Optional[str] = None
    father_or_spouse: Optional[str] = None
    members: list[str] = Field(default_factory=list)
    total_members_count: Optional[int] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    raw_text: Optional[str] = None

class FieldMatchResult(BaseModel):
    field_name: str
    doc1_label: str
    doc1_value: Optional[str] = None
    doc2_label: str
    doc2_value: Optional[str] = None
    match_score: float = 0.0
    status: StageStatus = StageStatus.PENDING
    remarks: str = ""

class StageReport(BaseModel):
    stage_id: str
    stage_name: str
    status: StageStatus
    message: str
    extracted_data: Optional[dict[str, Any]] = None
    flags: list[str] = Field(default_factory=list)

class VerificationPipelineReport(BaseModel):
    application_ref: str
    submission_time: str
    overall_status: StageStatus
    can_generate_pdf: bool
    stages: list[StageReport]
    cross_matches: list[FieldMatchResult]
    audit_notes: list[str] = Field(default_factory=list)
    pdf_filename: Optional[str] = None
