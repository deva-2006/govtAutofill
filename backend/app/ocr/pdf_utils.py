from pathlib import Path
from typing import Union
import pymupdf
import numpy as np
from PIL import Image

def pdf_to_images(pdf_path_or_bytes: Union[str, Path, bytes], dpi: int = 200) -> list[np.ndarray]:
    """
    Renders all pages of a PDF to OpenCV/numpy RGB images at specified DPI.
    """
    if isinstance(pdf_path_or_bytes, (str, Path)):
        doc = pymupdf.open(str(pdf_path_or_bytes))
    else:
        doc = pymupdf.open(stream=pdf_path_or_bytes, filetype="pdf")
        
    images = []
    zoom = dpi / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    
    for page in doc:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(np.array(img))
        
    doc.close()
    return images

def extract_pdf_embedded_text(pdf_path_or_bytes: Union[str, Path, bytes]) -> str:
    """
    Extracts selectable embedded text directly from the PDF if present.
    """
    if isinstance(pdf_path_or_bytes, (str, Path)):
        doc = pymupdf.open(str(pdf_path_or_bytes))
    else:
        doc = pymupdf.open(stream=pdf_path_or_bytes, filetype="pdf")
        
    text_chunks = []
    for page in doc:
        t = page.get_text()
        if t:
            text_chunks.append(t)
            
    doc.close()
    return "\n".join(text_chunks).strip()
