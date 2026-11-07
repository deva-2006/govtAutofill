import os
import cv2
import hashlib
import torch
import numpy as np
from pathlib import Path
from typing import Union, List, Tuple
import easyocr
import easyocr.config

# Multi-threading for fast CPU inference
try:
    torch.set_num_threads(4)
except Exception:
    pass

from app.core.logging import logger
from app.ocr.pdf_utils import pdf_to_images, extract_pdf_embedded_text

# Patch EasyOCR Tamil character set if truncated in pip release
MISSING_TAMIL_CHARS = 'வஷஸஹாிீுூெேைொோௌ்'
if 'tamil_g1' in easyocr.config.recognition_models.get('gen1', {}):
    curr_chars = easyocr.config.recognition_models['gen1']['tamil_g1'].get('characters', '')
    for ch in MISSING_TAMIL_CHARS:
        if ch not in curr_chars:
            easyocr.config.recognition_models['gen1']['tamil_g1']['characters'] += ch

class OCREngine:
    _instance = None
    _reader = None
    _cache: dict[str, List[Tuple[str, float]]] = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        logger.info("Initializing EasyOCR Engine with languages ['ta', 'en']...")
        self._reader = easyocr.Reader(['ta', 'en'], gpu=False, verbose=False)
        logger.info("EasyOCR Engine initialized successfully.")

    def preprocess_image(self, img: np.ndarray, max_dim: int = 1100) -> np.ndarray:
        """Resizes image if too large while maintaining aspect ratio and enhances contrast."""
        h, w = img.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / float(max(h, w))
            new_w = int(w * scale)
            new_h = int(h * scale)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Contrast enhancement (CLAHE on L-channel)
        if len(img.shape) == 3:
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            return enhanced
        return img

    def _get_cache_key(self, file_path_or_bytes: Union[str, Path, bytes]) -> str:
        if isinstance(file_path_or_bytes, (str, Path)):
            p = Path(file_path_or_bytes).resolve()
            if p.exists():
                return f"{p}:{p.stat().st_mtime}"
            return str(p)
        return hashlib.md5(file_path_or_bytes).hexdigest()

    def extract_text_from_file(self, file_path_or_bytes: Union[str, Path, bytes], is_pdf: bool = False, max_pages: int = 2) -> List[Tuple[str, float]]:
        """
        Processes image or PDF file and returns list of (detected_text, confidence).
        Caches results for high performance.
        """
        cache_key = self._get_cache_key(file_path_or_bytes)
        if cache_key in self._cache:
            return self._cache[cache_key]

        images = []
        is_pdf_file = is_pdf
        target_path = None
        if isinstance(file_path_or_bytes, (str, Path)):
            target_path = Path(file_path_or_bytes).resolve()
            if str(target_path).lower().endswith('.pdf'):
                is_pdf_file = True

        if is_pdf_file:
            target_src = target_path if target_path else file_path_or_bytes
            embedded_text = extract_pdf_embedded_text(target_src)
            if embedded_text and len(embedded_text.strip()) > 50:
                logger.info(f"Using high-fidelity digital text ({len(embedded_text)} chars) for PDF document.")
                results = [(line.strip(), 1.0) for line in embedded_text.splitlines() if line.strip()]
                self._cache[cache_key] = results
                return results
            images = pdf_to_images(target_src, dpi=110, max_pages=max_pages)
        elif target_path:
            # Use np.fromfile to avoid Windows path / Unicode encoding issues
            if target_path.exists():
                data = np.fromfile(str(target_path), dtype=np.uint8)
                img = cv2.imdecode(data, cv2.IMREAD_COLOR)
                if img is not None:
                    images.append(img)
            else:
                logger.warning(f"File not found: {target_path}")
        else:
            nparr = np.frombuffer(file_path_or_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                images.append(img)

        results = []
        for idx, img in enumerate(images):
            prep = self.preprocess_image(img, max_dim=1100)
            raw_ocr = self._reader.readtext(prep, detail=1, batch_size=4)
            for item in raw_ocr:
                text = item[1].strip()
                conf = float(item[2])
                if text:
                    results.append((text, conf))

        self._cache[cache_key] = results
        return results

    def extract_full_text(self, file_path_or_bytes: Union[str, Path, bytes], is_pdf: bool = False) -> str:
        """Returns all recognized text joined with newlines."""
        items = self.extract_text_from_file(file_path_or_bytes, is_pdf=is_pdf)
        return "\n".join([t for t, _ in items])

ocr_engine = OCREngine.get_instance()
