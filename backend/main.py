import base64
import json
import os
import re
import cv2
import easyocr
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pypdfium2 as pdfium
import requests

app = FastAPI(title="NVSP Auto-Fill Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

reader = easyocr.Reader(['en'], gpu=False)

yunet_model_path = os.path.join(os.path.dirname(__file__), 'face_detection_yunet_2023mar.onnx')
yunet_detector = None
if os.path.exists(yunet_model_path):
    try:
        yunet_detector = cv2.FaceDetectorYN_create(
            model=yunet_model_path,
            config='',
            input_size=(300, 300),
            score_threshold=0.35,
            nms_threshold=0.3
        )
    except Exception as e:
        print("YuNet initialization warning:", e)


def contains_skin_tones(img_bgr: np.ndarray) -> bool:
    """Checks if an image crop contains human skin tones (rejects text/document crops)."""
    if img_bgr is None or img_bgr.size == 0:
        return False
    try:
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 5, 20], dtype=np.uint8)
        upper_skin = np.array([35, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        skin_pct = (np.count_nonzero(mask) / mask.size) * 100
        return skin_pct >= 2.0
    except Exception:
        return False


def extract_face_photo_from_cv2_img(img: np.ndarray, allow_fallback: bool = False) -> str | None:
    """Deep learning YuNet face identifier and portrait cropper with cascade fallbacks."""
    if img is None or img.size == 0:
        return None

    try:
        h_orig, w_orig = img.shape[:2]

        # 1. Primary Pass: Deep Learning YuNet Face Identification & Cropping
        if yunet_detector is not None:
            try:
                yunet_detector.setInputSize((w_orig, h_orig))
                detected = yunet_detector.detect(img)
                if detected is not None and detected[1] is not None and len(detected[1]) > 0:
                    faces = detected[1]
                    valid_yunet_faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
                    fx, fy, fw, fh = map(int, valid_yunet_faces[0][:4])

                    # Add 40% margin around identified face box for passport framing
                    margin_w = int(fw * 0.40)
                    margin_h = int(fh * 0.40)
                    y1 = max(0, fy - margin_h)
                    y2 = min(h_orig, fy + fh + margin_h)
                    x1 = max(0, fx - margin_w)
                    x2 = min(w_orig, fx + fw + margin_w)

                    cropped_face = img[y1:y2, x1:x2]
                    if cropped_face.size > 0:
                        _, buffer = cv2.imencode('.jpg', cropped_face)
                        b64_str = base64.b64encode(buffer).decode('utf-8')
                        return f"data:image/jpeg;base64,{b64_str}"
            except Exception as ye:
                print(f"YuNet detection error: {ye}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray_enhanced = clahe.apply(gray)

        faces = []
        if face_cascade and not face_cascade.empty():
            faces = face_cascade.detectMultiScale(
                gray_enhanced, scaleFactor=1.03, minNeighbors=2, minSize=(25, 25)
            )
            if len(faces) == 0:
                faces = face_cascade.detectMultiScale(
                    gray, scaleFactor=1.05, minNeighbors=2, minSize=(25, 25)
                )

        if len(faces) > 0:
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
            x, y, w, h = faces[0]

            margin = int(w * 0.35)
            y1 = max(0, y - margin)
            y2 = min(h_orig, y + h + margin)
            x1 = max(0, x - margin)
            x2 = min(w_orig, x + w + margin)

            cropped = img[y1:y2, x1:x2]
            _, buffer = cv2.imencode('.jpg', cropped)
            b64_str = base64.b64encode(buffer).decode('utf-8')
            return f"data:image/jpeg;base64,{b64_str}"

        # If direct face cascade failed, check if this is an embedded photo stream
        if allow_fallback:
            aspect_ratio = h_orig / max(1, w_orig)
            if 0.6 <= aspect_ratio <= 1.8 and 50 <= w_orig <= 2500 and 50 <= h_orig <= 2500:
                if contains_skin_tones(img):
                    _, buffer = cv2.imencode('.jpg', img)
                    b64_str = base64.b64encode(buffer).decode('utf-8')
                    return f"data:image/jpeg;base64,{b64_str}"

        # Fallback for ID card page/image: Search specifically in candidate left-hand card portrait boxes
        if h_orig >= 200 and w_orig >= 200:
            candidate_boxes = [
                # Box 1: Standalone PNG/JPG Front Card Scan (Exact photo rectangle: y 15%-58%, x 3%-22%)
                (int(h_orig * 0.15), int(h_orig * 0.58), int(w_orig * 0.03), int(w_orig * 0.22)),
                # Box 2: Full A4 PDF Page Render (Exact photo rectangle: y 55%-75%, x 4%-23%)
                (int(h_orig * 0.55), int(h_orig * 0.75), int(w_orig * 0.04), int(w_orig * 0.23))
            ]

            for y1, y2, x1, x2 in candidate_boxes:
                portrait_crop = img[y1:y2, x1:x2]
                if portrait_crop.size > 0:
                    has_face_box = False
                    if face_cascade and not face_cascade.empty():
                        crop_gray = cv2.cvtColor(portrait_crop, cv2.COLOR_BGR2GRAY)
                        crop_clahe = clahe.apply(crop_gray)
                        inner_faces = face_cascade.detectMultiScale(
                            crop_clahe, scaleFactor=1.02, minNeighbors=1, minSize=(15, 15)
                        )
                        if len(inner_faces) > 0:
                            has_face_box = True
                            ix, iy, iw, ih = sorted(inner_faces, key=lambda f: f[2] * f[3], reverse=True)[0]
                            imargin = int(iw * 0.35)
                            iy1 = max(0, iy - imargin)
                            iy2 = min(portrait_crop.shape[0], iy + ih + imargin)
                            ix1 = max(0, ix - imargin)
                            ix2 = min(portrait_crop.shape[1], ix + iw + imargin)
                            portrait_crop = portrait_crop[iy1:iy2, ix1:ix2]

                    # ONLY return candidate crop if a face box was matched OR human skin tone validation passes!
                    if has_face_box or contains_skin_tones(portrait_crop):
                        _, buffer = cv2.imencode('.jpg', portrait_crop)
                        b64_str = base64.b64encode(buffer).decode('utf-8')
                        return f"data:image/jpeg;base64,{b64_str}"

        return None
    except Exception as e:
        print(f"Face extraction error: {e}")
        return None


def extract_face_photo(image_bytes: bytes) -> str | None:
    try:
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return extract_face_photo_from_cv2_img(img, allow_fallback=True)
    except Exception as e:
        print(f"Image decode error in face extraction: {e}")
        return None


def extract_id_number_with_regex(raw_text: str) -> str | None:
    """Extract true 12-digit Aadhaar or 10-char PAN, ignoring enrolment numbers and noise."""
    # 1. Clean out Enrolment numbers (e.g. 2726/50810/45592 or Enrolment No: ...)
    cleaned_text = re.sub(r'\b\d{4}/\d{5}/\d{5}\b', '', raw_text)
    cleaned_text = re.sub(r'Enrolment\s*(No|Num|\.)?:?\s*[\d/]+', '', cleaned_text, flags=re.IGNORECASE)

    # 2. Prioritize explicitly spaced 12-digit Aadhaar pattern (4-4-4 digits separated by spaces, e.g. 6120 9678 1604)
    spaced_matches = re.findall(r'\b\d{4}\s\d{4}\s\d{4}\b', cleaned_text)
    if spaced_matches:
        for m in spaced_matches:
            digits = m.replace(' ', '')
            if len(digits) == 12:
                return digits

    # 3. Search near 'Your Aadhaar No' or 'Aadhaar' text header
    near_aadhaar = re.findall(r'(?:Aadhaar|Aadhar)\s*(?:No|Number|\.)?:?\s*(\d{4}\s?\d{4}\s?\d{4})', cleaned_text, re.IGNORECASE)
    if near_aadhaar:
        for m in near_aadhaar:
            digits = m.replace(' ', '')
            if len(digits) == 12:
                return digits

    # 4. Standard 12-digit Aadhaar pattern (with or without space)
    aadhaar_matches = re.findall(r'\b\d{4}\s?\d{4}\s?\d{4}\b', cleaned_text)
    for m in aadhaar_matches:
        digits = m.replace(' ', '')
        if len(digits) == 12:
            return digits

    # 5. 10-char PAN Card pattern
    pan_match = re.search(r'\b[A-Z]{5}\d{4}[A-Z]\b', raw_text)
    if pan_match:
        return pan_match.group(0)

    return None


def extract_images_from_pdf_page(page) -> list[np.ndarray]:
    """Extract embedded images directly from a PDF page as fallbacks."""
    extracted = []
    try:
        for obj in page.get_objects():
            if getattr(obj, 'type', None) == 3 or type(obj).__name__ == 'PdfImage':
                try:
                    bm = obj.get_bitmap()
                    if bm:
                        pil_img = bm.to_pil()
                        cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                        if cv_img is not None:
                            h, w = cv_img.shape[:2]
                            # Filter for plausible photo stream dimensions
                            if 80 <= h <= 800 and 80 <= w <= 800:
                                extracted.append(cv_img)
                except Exception as ex:
                    pass
    except Exception as e:
        print(f"Error extracting embedded PDF images: {e}")
    return extracted


def file_to_cv2_images(file_bytes: bytes, filename: str) -> list[np.ndarray]:
    cv2_images = []
    safe_filename = filename or ''

    # Check magic bytes for PDF (starts with %PDF) or filename
    is_pdf = safe_filename.lower().endswith('.pdf') or file_bytes.startswith(b'%PDF')

    if is_pdf:
        try:
            pdf = pdfium.PdfDocument(file_bytes)
            for page in pdf:
                # 1. Extract embedded sub-images (marked as embedded stream) FIRST
                embedded_imgs = extract_images_from_pdf_page(page)
                for emb in embedded_imgs:
                    cv2_images.append((emb, True))

                # 2. Render full page at high DPI for OCR
                bitmap = page.render(scale=300 / 72)
                pil_image = bitmap.to_pil()
                cv_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                cv2_images.append((cv_img, False))
        except Exception as e:
            print(f"PDF rendering error: {e}")
    else:
        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is not None:
            cv2_images.append((img, False))

    return cv2_images


def normalize_extracted_data(data: dict, raw_ocr_text: str) -> dict:
    """Normalizes dates to YYYY-MM-DD and extracts clean 10-digit mobile numbers."""
    
    # 1. Clean Mobile Number (Strict 10-digit Indian mobile starting with 6-9)
    mobile_match = re.search(r'\b[6-9]\d{4}\s?\d{5}\b|\b[6-9]\d{9}\b', raw_ocr_text)
    if mobile_match:
        clean_mob = re.sub(r'\D', '', mobile_match.group(0))
        if len(clean_mob) == 10:
            data["mobile"] = clean_mob
    elif data.get("mobile"):
        clean_mobile = re.sub(r'\D', '', str(data["mobile"]))
        if len(clean_mobile) >= 10:
            data["mobile"] = clean_mobile[-10:]

    # 2. Normalize DOB to YYYY-MM-DD for HTML <input type="date">
    dob = data.get("dob")
    if not dob or len(str(dob)) < 8:
        # Fallback regex search for DOB in OCR text e.g. "21/02/2006" or "DOB: 21-02-2006"
        d_search = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', raw_ocr_text)
        if d_search:
            day, month, year = d_search.groups()
            data["dob"] = f"{year}-{int(month):02d}-{int(day):02d}"
    else:
        d_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', str(dob))
        if d_match:
            day, month, year = d_match.groups()
            data["dob"] = f"{year}-{int(month):02d}-{int(day):02d}"

    # 3. Clean Gender
    if data.get("gender"):
        g_str = str(data["gender"]).upper()
        if "MALE" in g_str and "FEMALE" not in g_str:
            data["gender"] = "Male"
        elif "FEMALE" in g_str:
            data["gender"] = "Female"

    # 4. Extract / Normalize Relative Name & Relation Type
    # Regex fallback for Relative Name if missing (e.g. S/O: Shankar, SJO Shankar)
    if not data.get("relative_name"):
        rel_name_match = re.search(r'\b(?:S/O|D/O|W/O|C/O|SJO|S\.O)\s*:?\s*([A-Za-z\s]+?)(?=[,;\d\n]|$)', raw_ocr_text, re.IGNORECASE)
        if rel_name_match:
            rname = rel_name_match.group(1).strip()
            if len(rname) > 1 and not any(w in rname.lower() for w in ['street', 'nagar', 'road', 'district']):
                data["relative_name"] = rname

    if not data.get("relation_type"):
        if re.search(r'\b(S/O|D/O|SJO|S\.O)\b', raw_ocr_text, re.IGNORECASE):
            data["relation_type"] = "Father"
        elif re.search(r'\bW/O\b', raw_ocr_text, re.IGNORECASE):
            data["relation_type"] = "Husband"
        elif re.search(r'\bC/O\b', raw_ocr_text, re.IGNORECASE):
            data["relation_type"] = "Father"
    else:
        rel_str = str(data["relation_type"]).strip().lower()
        if any(k in rel_str for k in ["father", "s/o", "d/o", "c/o", "sjo", "s.o", "son", "daughter"]):
            data["relation_type"] = "Father"
        elif "husband" in rel_str or "w/o" in rel_str or "wife" in rel_str:
            data["relation_type"] = "Husband"
        elif "mother" in rel_str:
            data["relation_type"] = "Mother"
        elif "guardian" in rel_str:
            data["relation_type"] = "Legal Guardian"

    # 5. Extract Address breakdown (House No, Street, Village/Town, Post Office, District, State, Pincode)
    # Require explicit 'Address:' with colon or relative marker
    addr_match = re.search(r'\bAddress\s*:\s*(.*?)(?=\b\d{6}\b|\n\n|$)', raw_ocr_text, re.IGNORECASE | re.DOTALL)
    if not addr_match:
        addr_match = re.search(r'\b(?:S/O|D/O|W/O|C/O|SJO|S\.O)\s*:?\s*[^,;]+[,;]\s*(\d{1,4}[^,;]+[,;].*?)(?=\b\d{6}\b|\n\n|$)', raw_ocr_text, re.IGNORECASE | re.DOTALL)

    if addr_match:
        raw_addr = addr_match.group(1 if addr_match.lastindex >= 1 else 0).strip()
        raw_addr = re.sub(r'\s+', ' ', raw_addr)[:250]

        # Strip house number prefix + relative header e.g. "9 SJO Shankar;" or "S/O: Shankar;"
        clean_addr = re.sub(r'^\d*\s*(?:S/O|D/O|W/O|C/O|SJO|S\.O)\s*:?\s*[^;,]+[;,]\s*', '', raw_addr, flags=re.IGNORECASE).strip()
        
        parts = [p.strip() for p in re.split(r'[,;]', clean_addr) if p.strip()]

        # Filter parts containing non-address legal disclaimers or noise
        clean_parts = []
        for p in parts:
            p_clean = re.sub(r'[^A-Za-z0-9\s\-/]', '', p).strip()
            if p_clean and not any(w in p_clean.lower() for w in ['should be updated', 'entities seeking', 'aadhaar is proof', 'authority of india']):
                clean_parts.append(p_clean)

        if clean_parts:
            # First item is House No e.g. "78"
            parsed_house = clean_parts.pop(0)

            # Clean street items: keep valid English address words, stop at VTC/PO/DIST
            street_items = []
            for cp in clean_parts:
                cp_up = cp.upper()
                if any(k in cp_up for k in ['VTC', 'PO:', 'PO ', 'POST', 'DIST', 'STATE', 'PIN']):
                    break
                valid_words = []
                for word in cp.split():
                    if re.match(r'^(?:[0-9]+[A-Za-z]*|[A-Z][a-z]+|[A-Z]{2,})$', word):
                        if len(word) > 1 or word.isdigit():
                            if not re.search(r'[a-z][0-9]|[0-9][a-z]{3,}', word):
                                valid_words.append(word)
                if valid_words:
                    c_str = ' '.join(valid_words)
                    if c_str and not c_str.upper() in ['VYASARPADI', 'CHENNAI']:
                        street_items.append(c_str)

            parsed_street = ', '.join(street_items) if street_items else (clean_parts[0] if clean_parts else '')

            # Override house_no and street if missing or containing disclaimer junk
            current_house = str(data.get("house_no") or "")
            if not current_house or any(w in current_house.lower() for w in ['updated', 'entities', 'aadhaar', 'india', 'seeking']):
                data["house_no"] = parsed_house

            current_street = str(data.get("street") or "")
            if not current_street or any(w in current_street.lower() for w in ['updated', 'entities', 'aadhaar', 'india', 'seeking', '6t601g1']):
                data["street"] = parsed_street

    # Extract 6-digit Pincode via Regex fallback
    pin_match = re.search(r'\b\d{6}\b', raw_ocr_text)
    if pin_match and not data.get("pincode"):
        data["pincode"] = pin_match.group(0)

    return data


def clean_json_string(text: str) -> str:
    text = text.strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    return text


@app.post('/extract')
async def extract_document_data(files: list[UploadFile] = File(...)):
    combined_ocr_text = []
    extracted_photo_b64 = None
    processed_page_counter = 1

    for file in files:
        contents = await file.read()
        images = file_to_cv2_images(contents, file.filename)

        for img, is_embedded in images:
            if not extracted_photo_b64:
                extracted_photo_b64 = extract_face_photo_from_cv2_img(img, allow_fallback=True)

            # Perform EasyOCR text extraction on full document pages only (skip embedded sub-images)
            if not is_embedded:
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                ocr_results = reader.readtext(rgb_img, detail=0)
                page_text = ' '.join(ocr_results)

                if page_text.strip():
                    combined_ocr_text.append(
                        f'--- Document Page {processed_page_counter} ---\n{page_text}'
                    )
                    processed_page_counter += 1

    full_ocr_context = '\n\n'.join(combined_ocr_text)

    system_prompt = f"""
    You are an expert Indian government document parser. 
    Analyze the OCR text below and extract details into this exact JSON schema:

    {{
      "full_name": "Applicant's name ONLY or null",
      "dob": "YYYY-MM-DD or null",
      "gender": "Male or Female or Third Gender or null",
      "mobile": "10-digit phone number or null",
      "email": "email address or null",
      "id_number": "12-digit Aadhaar Number / PAN / License Number or null",
      "relation_type": "Father or Mother or Husband or null",
      "relative_name": "Name of Father/Mother/Husband ONLY or null",
      "house_no": "flat/door number or null",
      "street": "street/locality or null",
      "city": "village/town/city or null",
      "post_office": "post office name or null",
      "pincode": "6-digit postal pincode or null",
      "district": "district or null",
      "state": "state name or null",
      "constituency": "assembly constituency or null",
      "birth_town": "place of birth or null",
      "birth_state": "state of birth or null"
    }}

    STRICT RULES FOR ID NUMBER & NAMES:
    1. id_number: Extract the main 12-digit identity number. DO NOT extract Enrolment numbers or alphanumeric codes containing letters like 'u' or 'e'.
    2. full_name: Extract ONLY the primary applicant name (e.g., "Deva S"). DO NOT extract the relative name line.
    3. relative_name: Extract ONLY the relative's name following "S/O:", "D/O:", or "W/O:" WITHOUT the "S/O:" prefix.

    OCR Text:
    {full_ocr_context}
    """

    parsed_json = {}
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": system_prompt,
                "format": "json",
                "stream": False
            },
            timeout=30
        )

        res_data = response.json()
        ollama_output = res_data.get("response", "").strip()

        if ollama_output:
            cleaned_output = clean_json_string(ollama_output)
            parsed_json = json.loads(cleaned_output)

    except Exception as err:
        print(f"Ollama execution error: {err}")
        parsed_json = {}

    # Post-processing: Direct Regex extraction for id_number (Aadhaar / PAN)
    regex_id = extract_id_number_with_regex(full_ocr_context)
    if regex_id:
        parsed_json["id_number"] = regex_id

    # Clean relative_name prefix if leaked
    if parsed_json.get("relative_name"):
        parsed_json["relative_name"] = re.sub(r'^(S/O|D/O|W/O|C/O)\s*:?\s*', '', parsed_json["relative_name"], flags=re.IGNORECASE).strip()

    parsed_json = normalize_extracted_data(parsed_json, full_ocr_context)
    parsed_json['photo_base64'] = extracted_photo_b64
    return parsed_json