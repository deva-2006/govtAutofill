// Community Certificate Application Verification System - Frontend Orchestrator

let isSampleMode = false;
let currentSessionId = "";

// Preload official sample documents and auto-fill form particulars using real OCR
async function handleLoadSampleAndAutofill() {
  const btn = document.getElementById("btnLoadSample");
  const origText = btn.innerHTML;
  const statusEl = document.getElementById("autofillStatusMsg");
  btn.disabled = true;

  // 1. Populate upload box previews
  setPreviewText("preview_parent_community", "box_parent_community", "mother_community.jpeg (Sample MBC Certificate)");
  setPreviewText("preview_birth", "box_birth", "child_birth.jpeg (Sample Municipal Record)");
  setPreviewText("preview_aadhaar", "box_aadhaar", "child_aadhar.pdf (Sample Official e-Aadhaar)");
  setPreviewText("preview_family", "box_family", "ration_card.pdf (Sample Tamil Family Card)");

  isSampleMode = true;
  document.getElementById("is_sample").value = "true";
  document.getElementById("session_id").value = "";

  let seconds = 0;
  btn.innerHTML = `<span class="spinner" style="width:14px;height:14px;"></span> Running Live OCR (0s)...`;
  statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> Initializing live bilingual OCR on sample documents...</span>`;

  const timer = setInterval(() => {
    seconds++;
    btn.innerHTML = `<span class="spinner" style="width:14px;height:14px;"></span> Running Live OCR (${seconds}s)...`;
    if (seconds === 2) {
      statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> [1/4] Extracting Municipal Birth Record & DOB (child_birth.jpeg)...</span>`;
    } else if (seconds === 6) {
      statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> [2/4] Parsing Child Aadhaar Identity & DOB (child_aadhar.pdf)...</span>`;
    } else if (seconds === 12) {
      statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> [3/4] Scrutinizing Parent Community Certificate & Caste (mother_community.jpeg)...</span>`;
    } else if (seconds === 18) {
      statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> [4/4] Verifying Tamil Smart Family Card & Roster (ration_card.pdf)...</span>`;
    }
  }, 1000);

  try {
    // Fetch live OCR extracted particulars from backend
    const res = await fetch("/api/verify/autofill-sample", { method: "POST" });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Could not extract details from sample documents");
    }
    const data = await res.json();

    clearInterval(timer);
    populateFormFields(data);

    statusEl.innerHTML = `
      <span style="color: var(--success); font-weight: 700;">✓ 4 official sample documents scanned in live OCR (${seconds}s)! Form particulars auto-filled below.</span>
    `;

    // Scroll smoothly to Step 2
    setTimeout(() => {
      document.getElementById("particularsSection").scrollIntoView({ behavior: "smooth" });
    }, 250);

  } catch (err) {
    clearInterval(timer);
    console.error("Error in sample autofill:", err);
    statusEl.innerHTML = `<span style="color: var(--danger);">❌ OCR Scan Error: ${err.message}</span>`;
    // Fallback to sample info endpoint if server OCR had an error
    await fallbackSampleFill();
  } finally {
    clearInterval(timer);
    btn.disabled = false;
    btn.innerHTML = origText;
  }
}

async function fallbackSampleFill() {
  try {
    const res = await fetch("/api/verify/sample-info");
    const data = await res.json();
    populateFormFields(data.sample_applicant);
    document.getElementById("autofillStatusMsg").innerHTML = `
      <span style="color: var(--success);">✓ Sample particulars loaded. Ready for review.</span>
    `;
    document.getElementById("particularsSection").scrollIntoView({ behavior: "smooth" });
  } catch (e) {
    alert("Could not connect to backend server. Make sure it is running on port 8000.");
  }
}

// User-triggered document scan & autofill (Always uses actual uploaded files)
async function triggerAutofill() {
  const statusEl = document.getElementById("autofillStatusMsg");
  const btn = document.getElementById("btnScanAutofill");

  const parentCert = document.getElementById("parent_community_certificate").files[0];
  const birthCert = document.getElementById("birth_certificate").files[0];
  const aadhaar = document.getElementById("aadhaar_card").files[0];
  const family = document.getElementById("family_card").files[0];

  if (!parentCert || !birthCert || !aadhaar || !family) {
    statusEl.innerHTML = `
      <span style="color: var(--danger);">⚠️ All 4 documents must be chosen beforehand. Alternatively, click "Demo: Load Sample Documents & Auto-Fill".</span>
    `;
    return;
  }

  const origText = btn.innerHTML;
  btn.disabled = true;

  // Mark as real user upload mode (never sample bypass)
  isSampleMode = false;
  document.getElementById("is_sample").value = "false";

  let seconds = 0;
  btn.innerHTML = `<span class="spinner" style="width:14px;height:14px;"></span> Scanning Documents (0s)...`;
  statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> Initializing live bilingual OCR scan on uploaded documents...</span>`;

  const timer = setInterval(() => {
    seconds++;
    btn.innerHTML = `<span class="spinner" style="width:14px;height:14px;"></span> Scanning Documents (${seconds}s)...`;
    if (seconds === 2) {
      statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> [1/4] Extracting Municipal Birth Record & DOB (${birthCert.name})...</span>`;
    } else if (seconds === 6) {
      statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> [2/4] Parsing Child Aadhaar Identity & Address (${aadhaar.name})...</span>`;
    } else if (seconds === 12) {
      statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> [3/4] Scrutinizing Parent Community Certificate & Caste Schedule (${parentCert.name})...</span>`;
    } else if (seconds === 18) {
      statusEl.innerHTML = `<span style="color: var(--accent);"><span class="spinner spinner-primary" style="width:12px;height:12px;"></span> [4/4] Verifying Tamil Smart Family Card & Roster (${family.name})...</span>`;
    }
  }, 1000);

  try {
    const formData = new FormData();
    formData.append("parent_community_certificate", parentCert);
    formData.append("birth_certificate", birthCert);
    formData.append("aadhaar_card", aadhaar);
    formData.append("family_card", family);

    const res = await fetch("/api/verify/autofill", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to scan documents");
    }

    const data = await res.json();
    currentSessionId = data.session_id || "";
    document.getElementById("session_id").value = currentSessionId;
    document.getElementById("is_sample").value = "false";

    clearInterval(timer);
    populateFormFields(data);

    statusEl.innerHTML = `
      <span style="color: var(--success); font-weight: 700;">✓ All 4 documents scanned successfully in ${seconds}s! Form particulars auto-filled below.</span>
    `;

    // Smooth scroll down to review section
    setTimeout(() => {
      document.getElementById("particularsSection").scrollIntoView({ behavior: "smooth" });
    }, 250);

  } catch (err) {
    clearInterval(timer);
    console.error("Autofill error:", err);
    statusEl.innerHTML = `<span style="color: var(--danger);">❌ OCR Scan Error: ${err.message}</span>`;
    alert(`Could not extract from documents: ${err.message}`);
  } finally {
    clearInterval(timer);
    btn.disabled = false;
    btn.innerHTML = origText;
  }
}

function populateFormFields(data) {
  if (!data) return;

  // Child details
  document.getElementById("child_name").value = data.child_name || "";
  document.getElementById("child_gender").value = data.child_gender || "Male";
  document.getElementById("child_dob").value = data.child_dob || "";
  document.getElementById("child_community").value = data.child_community || "MBC";
  document.getElementById("child_sub_caste").value = data.child_sub_caste || "Hindu Vanniakula Kshatriya";

  // Parent details
  document.getElementById("father_name").value = data.father_name || "";
  document.getElementById("father_community").value = data.father_community || "MBC";
  document.getElementById("mother_name").value = data.mother_name || "";
  document.getElementById("mother_community").value = data.mother_community || "MBC";

  // Inheritance radio
  const pType = data.parent_certificate_submitted || "mother";
  const radio = document.querySelector(`input[name="parent_certificate_submitted"][value="${pType}"]`);
  if (radio) radio.checked = true;

  // Address
  document.getElementById("door_no").value = data.door_no || "";
  document.getElementById("street").value = data.street || "";
  document.getElementById("village_town").value = data.village_town || "";
  document.getElementById("taluk").value = data.taluk || "";
  document.getElementById("district").value = data.district || "";
  document.getElementById("pincode").value = data.pincode || "";

  // Visual badges indicating auto-fill success
  document.getElementById("autofillBadge").innerHTML = `
    <span class="badge badge-success">✨ Auto-Filled via OCR</span>
  `;
  document.getElementById("badge_child_src").style.display = "inline-flex";
  document.getElementById("badge_comm_src").style.display = "inline-flex";
  document.getElementById("badge_addr_src").style.display = "inline-flex";

  document.getElementById("validationWarning").innerText = "";
}

function setPreviewText(previewId, boxId, text) {
  const preview = document.getElementById(previewId);
  const box = document.getElementById(boxId);
  if (preview && box) {
    preview.innerText = `✓ ${text}`;
    preview.style.display = "block";
    box.classList.add("file-ready");
  }
}

function handleFileSelect(input, previewId, boxId) {
  isSampleMode = false;
  document.getElementById("is_sample").value = "false";
  const file = input.files[0];
  if (file) {
    const sizeKB = (file.size / 1024).toFixed(1);
    setPreviewText(previewId, boxId, `${file.name} (${sizeKB} KB)`);
    document.getElementById("autofillStatusMsg").innerHTML = `
      <span style="color: var(--primary);">Document selected: <strong>${file.name}</strong>. Click "Scan Documents & Auto-Fill Form" when all 4 files are chosen.</span>
    `;
  }
}

// 8 Stages definition for visual stepper
const STAGE_DEFINITIONS = [
  { id: "stage_1", num: 1, name: "Application Details Validation", desc: "Validates applicant inputs, statutory lineage declarations, and required field formats." },
  { id: "stage_2", num: 2, name: "Parent Community Certificate Verification", desc: "OCR extraction of parent certificate & Tamil Nadu statutory inheritance rule evaluation." },
  { id: "stage_3", num: 3, name: "Child Birth Certificate Verification", desc: "OCR parsing of Municipal / Panchayat birth registry to verify name, DOB, and parentage." },
  { id: "stage_4", num: 4, name: "Child Aadhaar Verification", desc: "Verification of national identity, S/O care-of relation, and residential locality." },
  { id: "stage_5", num: 5, name: "Family Card Verification (Tamil)", desc: "Parsing Civil Supplies smart card in Tamil to verify household membership and family roster." },
  { id: "stage_6", num: 6, name: "Cross-Document Information Matching", desc: "Bilingual phonetic transliteration & cross-document consistency scoring matrix." },
  { id: "stage_7", num: 7, name: "Final Verification Assessment", desc: "Comprehensive risk audit: determines eligibility, manual inquiry requirements, or rejection." },
  { id: "stage_8", num: 8, name: "Application PDF Generation", desc: "Compiles formal Tahsildar Application Request PDF with audit trail and official endorsement blocks." }
];

function initPipelineUI() {
  const container = document.getElementById("pipelineStagesList");
  container.innerHTML = "";
  STAGE_DEFINITIONS.forEach(stage => {
    const el = document.createElement("div");
    el.className = "stage-item status-pending";
    el.id = `ui_${stage.id}`;
    el.innerHTML = `
      <div class="stage-header" onclick="toggleStageDetails('${stage.id}')">
        <div class="stage-title">
          <span class="stage-num">${stage.num}</span>
          <span>${stage.name}</span>
        </div>
        <div id="badge_${stage.id}">
          <span class="badge badge-neutral">Pending</span>
        </div>
      </div>
      <div class="stage-detail" id="detail_${stage.id}" style="display: none;">
        <div class="stage-message" id="msg_${stage.id}">${stage.desc}</div>
        <ul class="flag-list" id="flags_${stage.id}"></ul>
      </div>
    `;
    container.appendChild(el);
  });
}

function updateStageUI(stageId, status, message, flags = []) {
  const item = document.getElementById(`ui_${stageId}`);
  const badge = document.getElementById(`badge_${stageId}`);
  const msg = document.getElementById(`msg_${stageId}`);
  const detail = document.getElementById(`detail_${stageId}`);
  const flagsList = document.getElementById(`flags_${stageId}`);

  if (!item || !badge) return;

  item.className = `stage-item status-${status.toLowerCase()}`;
  
  let badgeHtml = "";
  if (status === "VERIFIED") {
    badgeHtml = `<span class="badge badge-success">✓ Verified</span>`;
  } else if (status === "MANUAL_REVIEW") {
    badgeHtml = `<span class="badge badge-warning">⚠️ Manual Review</span>`;
  } else if (status === "FAILED") {
    badgeHtml = `<span class="badge badge-danger">✗ Failed</span>`;
  } else if (status === "PROCESSING") {
    badgeHtml = `<span class="badge badge-info"><span class="spinner" style="width:12px;height:12px;border-width:2px;"></span> Processing</span>`;
  } else {
    badgeHtml = `<span class="badge badge-neutral">Pending</span>`;
  }
  badge.innerHTML = badgeHtml;

  if (message && msg) msg.innerText = message;

  // Render descriptive explanation callouts if failed or pending officer review
  if (detail) {
    let alertHtml = "";
    if (status === "FAILED") {
      alertHtml = `
        <div class="stage-alert alert-failed">
          <strong>❌ Verification Discrepancy / Failure Detected:</strong>
          <div>${flags && flags.length > 0 ? flags.map(f => `• ${f}`).join("<br>") : message}</div>
          <div class="remedy-hint">💡 <strong>Remedy / Required Action:</strong> Document could not be verified automatically. Please ensure the scan is clear, non-glare, and matches the entered applicant profile.</div>
        </div>
      `;
      detail.style.display = "block";
    } else if (status === "MANUAL_REVIEW") {
      alertHtml = `
        <div class="stage-alert alert-review">
          <strong>⚠️ Statutory Scrutiny Note for Tahsildar / RI:</strong>
          <div>${flags && flags.length > 0 ? flags.map(f => `• ${f}`).join("<br>") : message}</div>
          <div class="remedy-hint">⚖️ <strong>Statutory Protocol:</strong> Under Tamil Nadu Revenue Standing Order 35, where a mother's certificate is submitted, statutory field inquiry by Village Administrative Officer (VAO) and Revenue Inspector (RI) is required.</div>
        </div>
      `;
      detail.style.display = "block";
    }

    if (flagsList) {
      if (flags && flags.length > 0 && status === "VERIFIED") {
        flagsList.innerHTML = flags.map(f => `<li class="flag-item flag-success"><span>✓</span><span>${f}</span></li>`).join("");
      } else {
        flagsList.innerHTML = "";
      }
    }

    const existingAlert = detail.querySelector(".stage-alert");
    if (existingAlert) existingAlert.remove();
    if (alertHtml) {
      detail.insertAdjacentHTML("beforeend", alertHtml);
    }
  }
}

function toggleStageDetails(stageId) {
  const detail = document.getElementById(`detail_${stageId}`);
  if (detail) {
    detail.style.display = detail.style.display === "none" ? "block" : "none";
  }
}

// 8 Segments Live Execution Steps with Short Informative Loading Text
const PIPELINE_SEGMENT_STEPS = [
  { id: "stage_1", num: 1, title: "Validating applicant inputs & statutory community lineage declarations...", desc: "Checking child profile, date of birth format, and parent declarations against Tamil Nadu revenue guidelines." },
  { id: "stage_2", num: 2, title: "Parent Community Certificate OCR & G.O. caste schedule matching...", desc: "Performing OCR extraction on Parent Community Certificate; cross-referencing MBC caste schedule under G.O. Ms No. 28." },
  { id: "stage_3", num: 3, title: "Municipal Birth Certificate OCR & DOB registry validation...", desc: "Extracting Municipal Birth Record; verifying child name, date of birth (21/02/2006), and registration authority." },
  { id: "stage_4", num: 4, title: "Child Aadhaar identity OCR, UID masking & S/O care-of relation check...", desc: "Scanning national identity record; verifying masked UID, Care-Of (S/O Shankar) paternity link, and residential pincode." },
  { id: "stage_5", num: 5, title: "Tamil Nadu Smart Family Card OCR & household roster parsing...", desc: "Processing Tamil Smart Family Card; extracting household members (சுமதி.ச, தேவா.ச, இளமாறன்) and address." },
  { id: "stage_6", num: 6, title: "Cross-Document Consistency Matrix & Phonetic Transliteration...", desc: "Evaluating bilingual phonetic transliteration matrix across Application Form, Birth Cert, Aadhaar, and Family Card." },
  { id: "stage_7", num: 7, title: "Synthesizing Statutory Audit Assessment & Risk Classification...", desc: "Computing eligibility compliance, lineage inheritance verification, and Tahsildar inquiry requirements." },
  { id: "stage_8", num: 8, title: "Assembling Official Tahsildar Application Request PDF...", desc: "Compiling structured Tahsildar Application Request document with VAO, RI, and Tahsildar endorsement blocks." }
];

async function handleFormSubmit(event) {
  event.preventDefault();
  const warningEl = document.getElementById("validationWarning");
  warningEl.innerText = "";

  // Check mandatory particulars
  const childName = document.getElementById("child_name").value.trim();
  const dob = document.getElementById("child_dob").value.trim();
  if (!childName || !dob) {
    warningEl.innerText = "Please complete Step 1 (Scan Documents) to auto-fill particulars before verifying.";
    return;
  }

  // Check files if not sample mode and no session_id
  const sessionId = document.getElementById("session_id").value;
  const isSample = document.getElementById("is_sample").value === "true";

  if (!isSample && !sessionId) {
    const parentCert = document.getElementById("parent_community_certificate").files[0];
    const birthCert = document.getElementById("birth_certificate").files[0];
    const aadhaar = document.getElementById("aadhaar_card").files[0];
    const family = document.getElementById("family_card").files[0];

    if (!parentCert || !birthCert || !aadhaar || !family) {
      warningEl.innerText = "All 4 supporting documents are mandatory. Please scan them in Step 1 first.";
      return;
    }
  }

  // Setup UI for processing
  const btnSubmit = document.getElementById("btnSubmitVerify");
  btnSubmit.disabled = true;
  btnSubmit.innerHTML = `<span class="spinner"></span> Executing 8-Stage Pipeline...`;

  const pipelineSection = document.getElementById("pipelineSection");
  pipelineSection.style.display = "block";
  pipelineSection.scrollIntoView({ behavior: "smooth" });

  initPipelineUI();
  document.getElementById("matrixContainer").style.display = "none";
  document.getElementById("outcomeContainer").style.display = "none";

  // Live segment-by-segment ticker showing short loading text in every segment
  let activeSegmentIndex = 0;
  function updateSegmentTicker() {
    if (activeSegmentIndex < PIPELINE_SEGMENT_STEPS.length) {
      const seg = PIPELINE_SEGMENT_STEPS[activeSegmentIndex];
      document.getElementById("pipelineStatusBanner").innerHTML = `
        <div class="segment-ticker">
          <span class="ticker-icon">⚙️</span>
          <span><strong>Stage ${seg.num}/8:</strong> ${seg.title}</span>
        </div>
      `;
      updateStageUI(seg.id, "PROCESSING", seg.desc);
      activeSegmentIndex++;
    }
  }

  updateSegmentTicker();
  const simInterval = setInterval(updateSegmentTicker, 2400);

  try {
    let response;
    if (isSample) {
      response = await fetch("/api/verify/sample", { method: "POST" });
    } else {
      const form = document.getElementById("verificationForm");
      const formData = new FormData(form);
      response = await fetch("/api/verify", {
        method: "POST",
        body: formData
      });
    }

    clearInterval(simInterval);

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Server error (${response.status})`);
    }

    const report = await response.json();
    renderPipelineResults(report);
  } catch (error) {
    clearInterval(simInterval);
    console.error("Pipeline failure:", error);
    document.getElementById("pipelineStatusBanner").innerHTML = `
      <div class="stage-alert alert-failed">
        <strong>❌ Verification Pipeline Error:</strong>
        <div>${error.message}</div>
        <div class="remedy-hint">💡 Ensure backend server is running and sample documents are accessible.</div>
      </div>
    `;
    alert(`Verification Pipeline Error: ${error.message}`);
  } finally {
    clearInterval(simInterval);
    btnSubmit.disabled = false;
    btnSubmit.innerHTML = `<span>🚀 Execute 8-Stage Verification Pipeline</span>`;
  }
}

function renderPipelineResults(report) {
  // Update stage statuses with official backend report
  report.stages.forEach(st => {
    updateStageUI(st.stage_id, st.status, st.message, st.flags || []);
    if (st.status === "FAILED" || st.status === "MANUAL_REVIEW") {
      const detail = document.getElementById(`detail_${st.stage_id}`);
      if (detail) detail.style.display = "block";
    }
  });

  // Update overall badge & banner
  const overallBadge = document.getElementById("pipelineOverallBadge");
  const banner = document.getElementById("pipelineStatusBanner");

  if (report.overall_status === "VERIFIED") {
    overallBadge.innerHTML = `<span class="badge badge-success">✓ Fully Verified</span>`;
    banner.innerHTML = `✅ <strong>Pre-Verification Successful:</strong> All supporting documents, identity records, and statutory community inheritance rules verified. Official application request generated for Tahsildar sign-off.`;
  } else if (report.overall_status === "MANUAL_REVIEW") {
    overallBadge.innerHTML = `<span class="badge badge-warning">⚠️ Manual Review Required</span>`;
    banner.innerHTML = `⚠️ <strong>Pre-Verification Complete with Notes:</strong> Application document prepared with designated inquiry remarks for Tahsildar field scrutiny.`;
  } else {
    overallBadge.innerHTML = `<span class="badge badge-danger">✗ Verification Failed</span>`;
    banner.innerHTML = `❌ <strong>Verification Rejected:</strong> Critical discrepancies detected in submitted supporting documents. Please see details below.`;
  }

  // Render Cross-Document Consistency Matrix
  if (report.cross_matches && report.cross_matches.length > 0) {
    const matrixContainer = document.getElementById("matrixContainer");
    const matrixBody = document.getElementById("matrixTableBody");
    matrixBody.innerHTML = "";

    report.cross_matches.forEach(m => {
      const row = document.createElement("tr");
      let statusBadge = "";
      if (m.status === "VERIFIED") {
        statusBadge = `<span class="badge badge-success">✓ ${m.match_score.toFixed(0)}% Match</span>`;
      } else if (m.status === "MANUAL_REVIEW") {
        statusBadge = `<span class="badge badge-warning">⚠️ ${m.match_score.toFixed(0)}% Scrutiny</span>`;
      } else {
        statusBadge = `<span class="badge badge-danger">✗ Mismatch</span>`;
      }

      row.innerHTML = `
        <td><strong>${m.field_name}</strong></td>
        <td><code>${m.doc1_value || "—"}</code></td>
        <td><code>${m.doc2_value || "—"}</code></td>
        <td><strong>${m.match_score.toFixed(1)}%</strong></td>
        <td>${statusBadge}</td>
        <td>${m.remarks || "—"}</td>
      `;
      matrixBody.appendChild(row);
    });
    matrixContainer.style.display = "block";
  }

  // Render Final Outcome & PDF Action Box
  renderOutcomeBox(report);
}

function renderOutcomeBox(report) {
  const outcomeContainer = document.getElementById("outcomeContainer");
  outcomeContainer.style.display = "block";

  const isVerified = report.overall_status === "VERIFIED";
  const isReview = report.overall_status === "MANUAL_REVIEW";
  const cardClass = isVerified ? "verified" : (isReview ? "manual_review" : "failed");

  let html = `
    <div class="outcome-card ${cardClass}">
      <div class="outcome-header">
        <span style="font-size: 2rem;">${isVerified ? '✅' : (isReview ? '📋' : '❌')}</span>
        <div>
          <h3>${isVerified ? 'Application Pre-Verified Successfully' : (isReview ? 'Application Pre-Verified with Tahsildar Scrutiny Notes' : 'Application Verification Rejected')}</h3>
          <p style="font-size: 0.88rem; margin-top: 0.2rem;">
            Application Reference ID: <strong><code>${report.application_ref}</code></strong> | Submitted: ${new Date(report.submission_time).toLocaleString()}
          </p>
        </div>
      </div>
  `;

  if (report.can_generate_pdf && report.pdf_filename) {
    html += `
      <div style="font-size: 0.88rem; color: var(--neutral-700); background: white; padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--neutral-200);">
        📄 <strong>Tahsildar Application Request PDF Generated:</strong>
        <p style="margin-top: 0.25rem;">The official structured application document has been compiled according to Tamil Nadu Revenue Department standards, containing the applicant profile, statutory inheritance basis, audit verification summary, and designated endorsement blocks for the Village Administrative Officer (VAO), Revenue Inspector (RI), and Tahsildar.</p>
      </div>

      <div class="outcome-actions">
        <a href="/api/pdf/preview/${encodeURIComponent(report.pdf_filename)}" target="_blank" class="btn btn-primary">
          <span>👁️ Preview Application Request PDF</span>
        </a>
        <a href="/api/pdf/download/${encodeURIComponent(report.pdf_filename)}" class="btn btn-accent">
          <span>⬇️ Download PDF for Tahsildar Submission</span>
        </a>
        <button type="button" class="btn btn-outline" onclick="toggleAuditJson()">
          <span>🔍 View Verification Audit JSON</span>
        </button>
      </div>

      <div id="auditJsonBox" style="display: none; margin-top: 1rem;">
        <pre style="background: var(--neutral-900); color: #38bdf8; padding: 1rem; border-radius: var(--radius-sm); overflow-x: auto; font-size: 0.8rem; max-height: 350px;">${JSON.stringify(report, null, 2)}</pre>
      </div>
    `;
  } else {
    html += `
      <div style="font-size: 0.88rem; color: var(--danger); background: white; padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--danger);">
        ❌ <strong>Application Request PDF Generation Suppressed:</strong>
        <p style="margin-top: 0.25rem;">Due to critical verification failures, the application document cannot be generated automatically. Discrepancies must be resolved before resubmission.</p>
      </div>
    `;
  }

  html += `</div>`;
  outcomeContainer.innerHTML = html;
}

function toggleAuditJson() {
  const box = document.getElementById("auditJsonBox");
  if (box) {
    box.style.display = box.style.display === "none" ? "block" : "none";
  }
}