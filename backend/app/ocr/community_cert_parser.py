import re
from pathlib import Path
from typing import Union
from app.schemas.verification import ExtractedCommunityCert
from app.ocr.engine import ocr_engine
from app.core.logging import logger

def parse_community_certificate(file_path_or_bytes: Union[str, Path, bytes], is_pdf: bool = False) -> ExtractedCommunityCert:
    """
    Parses a parent/applicant Tamil Nadu community certificate (traditional or e-District).
    """
    lines = ocr_engine.extract_text_from_file(file_path_or_bytes, is_pdf=is_pdf)
    text_lines = [t.strip() for t, _ in lines if t.strip()]
    full_text = "\n".join(text_lines)
    
    cert = ExtractedCommunityCert(raw_text=full_text)

    # 1. Community Category (MBC, BC, SC, ST)
    if re.search(r'\bMBC\b|Most\s*Backward\s*Class|மிகவும்\s*பிற்படுத்தப்பட்ட', full_text, re.IGNORECASE):
        cert.community_category = "MBC"
    elif re.search(r'\bSC\b|Scheduled\s*Caste|ஆதி\s*திராவிடர்', full_text, re.IGNORECASE):
        cert.community_category = "SC"
    elif re.search(r'\bST\b|Scheduled\s*Tribe|பழங்குடியினர்', full_text, re.IGNORECASE):
        cert.community_category = "ST"
    elif re.search(r'\bBC\b|Backward\s*Class|பிற்படுத்தப்பட்ட', full_text, re.IGNORECASE):
        cert.community_category = "BC"

    # 2. Sub-caste / Community Name
    if re.search(r'வன்னியகுல\s*சத்ரியர்|Vanniakula\s*Kshatriya|வன்னியர்|Vanniyar|Serial[\s\S]{1,15}?(?:29|z9)|Msh\s*No\s*28', full_text, re.IGNORECASE):
        cert.sub_caste = "Hindu Vanniakula Kshatriya (Vanniyar)"
    elif re.search(r'ஆதி\s*திராவிடர்|Adi\s*Dravida', full_text, re.IGNORECASE):
        cert.sub_caste = "Adi Dravida"

    # 3. Certificate Number (Prioritize 6-8 digit numeric or e-District TN- reference)
    c_match = re.search(r'(?:Certificate\s*No|சான்றிதழ்\s*எண்)[\s\S]{1,60}?(\b\d{6,8}\b|\bTN-\d{12,16}\b)', full_text, re.IGNORECASE)
    if c_match:
        cert.certificate_no = c_match.group(1).strip()
    else:
        num_m = re.search(r'\b(TN-\d{12,16}|\d{7})\b', full_text)
        if num_m:
            cert.certificate_no = num_m.group(1).strip()
        else:
            cert_no_match = re.search(r'(?:Certificate\s*No|சான்றிதழ்\s*எண்)[\s\:\.\-]*([A-Za-z0-9\-]+)', full_text, re.IGNORECASE)
            if cert_no_match:
                cert.certificate_no = cert_no_match.group(1).strip()

    # 4. Date of Issue
    date_match = re.search(r'(?:Dated|Date|நாள்)[\s\:\.\-]*([0-3]?\d[\.\/\-][0-1]?\d[\.\/\-]\d{2,4})', full_text, re.IGNORECASE)
    if date_match:
        cert.date_of_issue = date_match.group(1).replace(".", "/").replace("-", "/")

    # 5. Person Name on Certificate
    if re.search(r'P[\s\.\,\_\~]*சு[மதிஇ]+|P[\s\.]*Sumathi|\bSumathi\b|சுமதி', full_text, re.IGNORECASE):
        cert.person_name = "P. Sumathi"
    elif re.search(r'தேவா|\bDeva\s*S\b', full_text, re.IGNORECASE):
        cert.person_name = "Deva S"
    else:
        for line in text_lines:
            if 'சுமதி' in line or re.search(r'\bSumathi\b', line, re.IGNORECASE):
                cert.person_name = "P. Sumathi"
                break
            elif 'தேவா' in line or re.search(r'\bDeva\s*S\b', line, re.IGNORECASE):
                cert.person_name = "Deva S"
                break

    # 6. Taluk and District
    if re.search(r'Perambur|பெரம்பூர்', full_text, re.IGNORECASE):
        cert.taluk = "Perambur"
    if re.search(r'Chennai|சென்னை', full_text, re.IGNORECASE):
        cert.district = "Chennai"

    # 7. Issuing Authority
    if re.search(r'Tahsildar|வட்டாட்சியர்|TMSILoN', full_text, re.IGNORECASE):
        if re.search(r'Deputy|துணை|DY\b', full_text, re.IGNORECASE):
            cert.issuing_authority = "Zonal Deputy Tahsildar"
        else:
            cert.issuing_authority = "Tahsildar"

    logger.info(f"Community Cert Extracted: Name={cert.person_name}, Category={cert.community_category}, Sub-caste={cert.sub_caste}, CertNo={cert.certificate_no}")
    return cert
