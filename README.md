# NVSP Form 6 Auto-Fill Engine

An AI-powered web application that extracts information from uploaded Indian Government documents (Aadhaar PDF, PAN Card, Driving License) and automatically populates the ECI NVSP Form 6 voter application.

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
Ensure Ollama is running in the background on port `11434`:
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
Open another terminal or directly launch the frontend:

- **Option A (Direct File)**: Open `frontend/index.html` directly in any web browser.
- **Option B (Local HTTP Server)**:
  ```bash
  cd frontend
  python -m http.server 3000
  ```
  Then open `http://localhost:3000` in your browser.

---

## Usage

1. Click **Upload Document Images / PDFs** and attach your Aadhaar PDF or ID scan document.
2. Click **Process Documents & Auto-Fill**.
3. The AI engine will extract:
   - Full Applicant Name, DOB, Gender, Mobile Number
   - Verified 12-digit Aadhaar / Reference Number
   - Applicant Face Portrait Photo
   - Relative Details & Type of Relation
   - Full Address Breakdown (House No, Street, City, Pincode, District, State)
