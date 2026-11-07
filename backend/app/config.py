from pathlib import Path
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "Community Certificate Application Verification System"
    VERSION: str = "2.0.0"
    API_PREFIX: str = "/api"
    
    # Storage paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    GENERATED_PDF_DIR: Path = BASE_DIR / "generated_pdfs"
    SAMPLE_DOCS_DIR: Path = BASE_DIR.parent / "sample_docs"
    
    # OCR settings
    OCR_LANGUAGES: list[str] = ["ta", "en"]
    OCR_USE_GPU: bool = False  # EasyOCR CPU mode default for universal compatibility
    
    # Verification Thresholds
    FUZZY_MATCH_HIGH: int = 80
    FUZZY_MATCH_LOW: int = 55
    
    def setup_directories(self):
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.GENERATED_PDF_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.setup_directories()
