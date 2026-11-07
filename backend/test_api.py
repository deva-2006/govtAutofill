import sys
sys.stdout.reconfigure(encoding='utf-8')
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("=== 1. TESTING HEALTHCHECK ===")
r1 = client.get("/api/health")
print("Health:", r1.status_code, r1.json())

print("\n=== 2. TESTING SAMPLE INFO ===")
r2 = client.get("/api/verify/sample-info")
print("Sample info ready:", r2.status_code, r2.json().get("all_sample_docs_ready"))

print("\n=== 3. TESTING VERIFY SAMPLE PIPELINE ===")
r3 = client.post("/api/verify/sample")
print("Pipeline status:", r3.status_code)

if r3.status_code == 200:
    data = r3.json()
    print("Application Reference:", data.get("application_ref"))
    print("Overall Status:", data.get("overall_status"))
    print("Can Generate PDF:", data.get("can_generate_pdf"))
    print("Generated PDF:", data.get("pdf_filename"))
    
    print("\n--- STAGES SUMMARY ---")
    for s in data.get("stages", []):
        print(f"[{s['status']}] {s['stage_name']}: {s['message']}")
        
    print("\n--- CROSS MATCHES SUMMARY ---")
    for m in data.get("cross_matches", []):
        print(f"[{m['status']}] {m['field_name']}: {m['match_score']}% -> {m['remarks']}")
else:
    print("Error:", r3.text)
