class DocumentProcessingError(Exception):
    """Raised when document ingestion or OCR processing fails."""
    def __init__(self, document_type: str, message: str):
        super().__init__(f"Error processing {document_type}: {message}")
        self.document_type = document_type
        self.message = message

class VerificationPipelineError(Exception):
    """Raised when an error occurs during the verification pipeline."""
    def __init__(self, stage: str, message: str):
        super().__init__(f"Pipeline failure at stage '{stage}': {message}")
        self.stage = stage
        self.message = message
