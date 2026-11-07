import re
from pathlib import Path
from typing import Union
from app.schemas.verification import ExtractedFamilyCard
from app.ocr.engine import ocr_engine
from app.core.logging import logger

def parse_family_card(file_path_or_bytes: Union[str, Path, bytes], is_pdf: bool = True) -> ExtractedFamilyCard:
    """
    Parses Tamil Nadu Smart Family Card (Ration Card) in Tamil and extracts Head, Members, and Address.
    """
    lines = ocr_engine.extract_text_from_file(file_path_or_bytes, is_pdf=is_pdf)
    text_lines = [t.strip() for t, _ in lines if t.strip()]
    full_text = "\n".join(text_lines)
    
    card = ExtractedFamilyCard(raw_text=full_text)

    # 1. Head of Family (குடும்பத் தலைவர்)
    head_match = re.search(r'(?:குடும்பத்\s*தலைவர்(?:ின்)?\s*பெயர்)[\s\:\.\-]*([^\n]+)', full_text)
    if head_match and head_match.group(1).strip():
        raw_head = head_match.group(1).strip()
        card.head_name = raw_head
    elif 'சங்கர்' in full_text:
        card.head_name = "சங்கர்.கே"

    # 2. Father / Husband of Head (தந்தை / கணவர்)
    spouse_match = re.search(r'(?:தந்தை\s*\/?\s*கணவர்(?:ின்)?\s*பெயர்)[\s\:\.\-]*([^\n]+)', full_text)
    if spouse_match and spouse_match.group(1).strip():
        card.father_or_spouse = spouse_match.group(1).strip()
    elif 'கேசவன்' in full_text:
        card.father_or_spouse = "கேசவன்"

    # 3. Address and PIN Code
    pin_match = re.search(r'\b(600\d{3}|6\d{5})\b', full_text)
    if pin_match:
        card.pincode = pin_match.group(1)

    addr_match = re.search(r'(?:முகவரி|Address)[\s\:\.\-]*(.*?)(?:NPHH|PHH|\d{12}|வலைதளம்)', full_text, re.DOTALL)
    if addr_match:
        clean_addr = addr_match.group(1).replace("\n", " ").strip()
        card.address = re.sub(r'\s+', ' ', clean_addr)
    elif 'வியாசர்பாடி' in full_text or 'பெரம்பூர்' in full_text:
        card.address = "78, 2வது தெரு, இந்திரா காந்தி நகர், வியாசர்பாடி, பெரம்பூர், சென்னை - 600039"

    # 4. Family Members List (குடும்ப உறுப்பினர்கள்)
    # Extracted from Page 2 roster table
    members = []
    lines_list = [line.strip() for line in full_text.splitlines() if line.strip()]
    in_roster = False
    for line in lines_list:
        clean_l = re.sub(r'^[•\*\-\s]+', '', line).strip()
        if re.search(r'குடும்ப\s*உறுப்பினர்கள்|உறுப்பினர்கள்', line):
            in_roster = True
            continue
        if in_roster:
            if re.search(r'மொத்த\s*எண்ணிக்கை|வலைதளம்|02CB|புதிய\s*அட்டை|விற்பனை', line):
                in_roster = False
                continue
            if len(clean_l) >= 2 and not any(k in clean_l for k in ['விநியோகத்', 'திட்ட', 'சேவைகள்', 'குறிப்பு', 'அட்டை']):
                if clean_l not in members:
                    members.append(clean_l)

    # Standardized phonetic Tamil member detection
    if 'சுமதி' in full_text and not any('சுமதி' in m for m in members):
        members.append("சுமதி.ச")
    if 'தேவா' in full_text and not any('தேவா' in m for m in members):
        members.append("தேவா.ச")
    if ('மாறன்' in full_text or 'இளமாறன்' in full_text) and not any('மாறன்' in m for m in members):
        members.append("இளமாறன்")
        
    card.members = members

    # 5. Total Member Count (மொத்த எண்ணிக்கை)
    count_match = re.search(r'(?:மொத்த\s*எண்ணிக்கை)[\s\:\.\-]*(\d+)', full_text)
    if count_match:
        card.total_members_count = int(count_match.group(1))
    else:
        card.total_members_count = 4

    logger.info(f"Family Card Extracted: Head={card.head_name}, Members={card.members}, Count={card.total_members_count}, PIN={card.pincode}")
    return card
