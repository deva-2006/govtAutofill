# NVSP Form 6 Auto-Fill Engine

AI-powered app that extracts info from Indian Government documents (Aadhaar, PAN, DL, Passport) and auto-fills the ECI NVSP Form 6 voter application.

## Setup

### Prerequisites

- Python 3.10+
- Ollama (for Llama 3.2 AI model)

### Install Ollama

**Mac:**
```bash
brew install ollama
```

**Windows:** Download from https://ollama.com/download

Then pull the model:
```bash
ollama pull llama3.2
```

### Run the App

Open **3 terminals** and run these:

**Terminal 1 — Start Ollama:**
```bash
ollama serve
```

**Terminal 2 — Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Terminal 3 — Frontend:**
```bash
cd frontend
python3 -m http.server 3000
```

Open http://localhost:3000 in your browser.

## Usage

1. Upload document images/PDFs (Aadhaar, PAN, Passport, etc.)
2. Click **Process Documents & Auto-Fill**
3. AI extracts name, DOB, gender, Aadhaar number, address, and crops a passport photo automatically.
