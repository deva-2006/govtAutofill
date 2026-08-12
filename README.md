# NVSP Form 6 Auto-Fill Engine

An AI-powered web application that extracts information from uploaded Indian Government documents (Aadhaar PDF, PAN Card, Driving License, Passport) and automatically populates the ECI NVSP Form 6 voter application.

Powered by **Llama 3.2** (via local Ollama), **EasyOCR**, and **OpenCV YuNet Deep Learning** for face identification.

---

## Key Features

- 📄 **Multi-Document Accumulative Upload**: Upload multiple document images or PDFs (e.g. Aadhaar Front + Aadhaar Back + PAN Card) at once or one-by-one.
- 👤 **Deep Learning Face Identification**: Built-in OpenCV YuNet neural network detects facial features with $\ge 92\%$ confidence and crops 1:1 passport photos.
- 🤖 **Llama 3.2 AI Extraction**: Parses OCR text into structured JSON fields.
- ⚡ **Regex & Rules Fallbacks**: Guarantees accurate 12-digit Aadhaar/Reference numbers, 10-digit mobile numbers, DOB formatting (`YYYY-MM-DD`), relative details (`Father`/`Husband`), and clean address components (`House No`, `Street`).

---

## Prerequisites

1. **Python 3.10+** installed.
2. **Ollama** running locally with `llama3.2` model installed:
   ```bash
   ollama pull llama3.2
   ```

---

## How to Run

### Step 1: Start Ollama Engine
Ensure Ollama is running locally on port `11434`:
```bash
ollama serve
```

### Step 2: Install Backend Dependencies & Start Server
Open a terminal in the project directory:

```bash
# Navigate to backend directory
cd backend

# Install Python requirements
pip install -r requirements.txt

# Start FastAPI backend server (runs on port 8000)
uvicorn main:app --reload --port 8000
```

### Step 3: Open Frontend Interface
Open `frontend/index.html` directly in any web browser, or serve via local HTTP:

```bash
cd frontend
python -m http.server 3000
```
Then open `http://localhost:3000` in your browser.

---

## Usage

1. Click **Upload Document Images / PDFs** or drag & drop single/multiple ID files (Aadhaar Front, Aadhaar Back, PAN Card, etc.).
2. Click **⚡ Process Documents & Auto-Fill**.
3. The AI engine extracts name, DOB, gender, 12-digit reference ID, relative info, clean address breakdown, and crops the applicant's passport photo automatically.
