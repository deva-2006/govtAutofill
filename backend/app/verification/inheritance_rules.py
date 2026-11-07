from typing import Tuple
from app.schemas.applicant import ApplicantDetails
from app.schemas.verification import ExtractedCommunityCert, StageStatus
from app.core.logging import logger

# Official Tamil Nadu Reservation Categories
VALID_COMMUNITIES = ["MBC", "BC", "SC", "ST", "BCM", "DNC"]

# Mapping of known sub-castes to categories in Tamil Nadu
SUB_CASTE_TO_COMMUNITY = {
    "vanniyar": "MBC",
    "vanniakula kshatriya": "MBC",
    "hindu vanniakula kshatriya": "MBC",
    "adi dravida": "SC",
    "arunthathiyar": "SC",
    "kurumans": "ST"
}

def validate_community_inheritance(
    applicant: ApplicantDetails,
    parent_cert: ExtractedCommunityCert
) -> Tuple[StageStatus, str, list[str]]:
    """
    Validates community inheritance rules for Tamil Nadu:
    - Child inherits father's community (or mother's if alternative certificate provided)
    - Validates category and sub-caste alignment
    """
    flags = []
    
    if not parent_cert.community_category:
        return (
            StageStatus.FAILED,
            "Could not determine community category from submitted parent certificate.",
            ["Missing community category on certificate"]
        )

    claimed_cat = applicant.child_community.strip().upper()
    cert_cat = parent_cert.community_category.strip().upper()

    # Normalize category comparison (e.g. MBC vs MBC)
    if claimed_cat != cert_cat:
        flags.append(f"Claimed community '{claimed_cat}' differs from parent certificate category '{cert_cat}'.")
        return (
            StageStatus.MANUAL_REVIEW,
            f"Community category mismatch: Applicant claims {claimed_cat}, but parent certificate is {cert_cat}.",
            flags
        )

    # Sub-caste check if available
    if applicant.child_sub_caste and parent_cert.sub_caste:
        sub_claimed = applicant.child_sub_caste.lower()
        sub_cert = parent_cert.sub_caste.lower()
        
        # Check if key words match (e.g. Vanniyar or Vanniakula)
        key_matches = any(k in sub_claimed and k in sub_cert for k in ["vanniy", "dravida", "kshatriya", "sc", "mbc"])
        if not key_matches and sub_claimed not in sub_cert and sub_cert not in sub_claimed:
            flags.append(f"Sub-caste discrepancy: Claimed '{applicant.child_sub_caste}' vs Certificate '{parent_cert.sub_caste}'.")
            return (
                StageStatus.MANUAL_REVIEW,
                "Sub-caste requires Tahsildar manual verification.",
                flags
            )

    return (
        StageStatus.VERIFIED,
        f"Community inheritance rule satisfied. Child inherits {cert_cat} ({parent_cert.sub_caste or cert_cat}) as supported by {applicant.parent_certificate_submitted}'s certificate.",
        flags
    )
