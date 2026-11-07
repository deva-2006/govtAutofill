from typing import Optional
from pydantic import BaseModel, Field

class ApplicantDetails(BaseModel):
    # Child Information
    child_name: str = Field(..., description="Full name of the child/applicant")
    child_gender: str = Field(..., description="Gender (Male / Female / Other)")
    child_dob: str = Field(..., description="Date of birth (DD/MM/YYYY)")
    child_community: str = Field(..., description="Claimed Community (e.g., MBC, BC, SC, ST)")
    child_sub_caste: Optional[str] = Field(None, description="Claimed Sub-caste / Caste Name (e.g., Hindu Vanniakula Kshatriya / Vanniyar)")
    
    # Parent Information
    father_name: str = Field(..., description="Father's full name")
    father_community: Optional[str] = Field(None, description="Father's community")
    mother_name: str = Field(..., description="Mother's full name")
    mother_community: Optional[str] = Field(None, description="Mother's community")
    
    # Community Inheritance Choice
    parent_certificate_submitted: str = Field(
        default="mother",
        description="'father' or 'mother' certificate used as primary community proof"
    )

    # Residential Address
    door_no: Optional[str] = Field(None, description="Door / House No.")
    street: Optional[str] = Field(None, description="Street / Locality")
    village_town: Optional[str] = Field(None, description="Village / Town / Area")
    taluk: Optional[str] = Field(None, description="Taluk")
    district: Optional[str] = Field(None, description="District")
    pincode: Optional[str] = Field(None, description="PIN Code")
    phone: Optional[str] = Field(None, description="Contact phone number")
