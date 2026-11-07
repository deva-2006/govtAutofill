// Community Certificate Application Verification System - Frontend Orchestrator

let isSampleMode = false;

// Preload official sample data for testing and staff demo
async function loadSampleData() {
  try {
    const res = await fetch("/api/verify/sample-info");
    if (!res.ok) throw new Error("Could not fetch sample info");
    const data = await res.json();
    
    const app = data.sample_applicant;
    document.getElementById("child_name").value = app.child_name || "";
    document.getElementById("child_gender").value = app.child_gender || "Male";
    document.getElementById("child_dob").value = app.child_dob || "";
    document.getElementById("child_community").value = app.child_community || "MBC";
    document.getElementById("child_sub_caste").value = app.child_sub_caste || "";
    document.getElementById("father_name").value = app.father_name || "";
    document.getElementById("father_community").value = app.father_community || "MBC";
    document.getElementById("mother_name").value = app.mother_name || "";
    document.getElementById("mother_community").value = app.mother_community || "MBC";
    
    const radioParent = document.querySelector(`input[name="parent_certificate_submitted"][value="${app.parent_certificate_submitted}"]`);
    if (radioParent) radioParent.checked = true;

    document.getElementById("door_no").value = app.door_no || "";
    document.getElementById("street").value = app.street || "";
    document.getElementById("village_town").value = app.village_town || "";
    document.getElementById("taluk").value = app.taluk || "";
    document.getElementById("district").value = app.district || "";
    document.getElementById("pincode").value = app.pincode || "";

    // Highlight sample files loaded
    setPreviewText("preview_parent_community", "box_parent_community", "mother_community.jpeg (Sample MBC Certificate)");
    setPreviewText("preview_birth", "box_birth", "child_birth.jpeg (Sample Municipal Record)");
    setPreviewText("preview_aadhaar", "box_aadhaar", "child_aadhar.pdf (Sample Official e-Aadhaar)");
    setPreviewText("preview_family", "box_family", "ration_card.pdf (Sample Tamil Family Card)");

    isSampleMode = true;
    document.getElementById("validationWarning").innerText = "Official sample documents & particulars loaded. Ready to execute pipeline.";
    document.getElementById("validationWarning").style.color = "var(--success)";
  } catch (err) {
    console.error("Error loading sample data:", err);
    alert("Could not load sample data from server. Ensure backend is running.");
  }
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
  const file = input.files[0];
  if (file) {
    const sizeKB = (file.size / 1024).toFixed(1);
    setPreviewText(previewId, boxId, `${file.name} (${sizeKB} KB)`);
    document.getElementById("validationWarning").innerText = "";
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
  if (flagsList && flags.length > 0) {
    flagsList.innerHTML = flags.map(f => {
      const isWarn = status === "MANUAL_REVIEW";
      return `<li class="flag-item ${isWarn ? 'flag-warning' : 'flag-danger'}"><span>${isWarn ? '⚠️' : '❌'}</span><span>${f}</span></li>`;
    }).join("");
  }
}

function toggleStageDetails(stageId) {
  const detail = document.getElementById(`detail_${stageId}`);
  if (detail) {
    detail.style.display = detail.style.display === "none" ? "block" : "none";
  }
}

async function handleFormSubmit(event) {
  event.preventDefault();
  const warningEl = document.getElementById("validationWarning");
  warningEl.innerText = "";

  // Check mandatory file upload if not in sample demo mode
  if (!isSampleMode) {
    const parentCert = document.getElementById("parent_community_certificate").files[0];
    const birthCert = document.getElementById("birth_certificate").files[0];
    const aadhaar = document.getElementById("aadhaar_card").files[0];
    const family = document.getElementById("family_card").files[0];

    if (!parentCert || !birthCert || !aadhaar || !family) {
      warningEl.innerText = "All 4 supporting documents are mandatory. Please upload all files or click 'Demo: Load Official Sample Data'.";
      return;
    }
  }

  // Setup UI for processing
  const btnSubmit = document.getElementById("btnSubmitVerify");
  btnSubmit.disabled = true;
  btnSubmit.innerHTML = `<span class="spinner"></span> Processing 8-Stage Pipeline...`;

  const pipelineSection = document.getElementById("pipelineSection");
  pipelineSection.style.display = "block";
  pipelineSection.scrollIntoView({ behavior: "smooth" });

  initPipelineUI();
  document.getElementById("matrixContainer").style.display = "none";
  document.getElementById("outcomeContainer").style.display = "none";
  document.getElementById("pipelineStatusBanner").innerHTML = `
    <span class="spinner spinner-primary"></span> Executing bilingual OCR extraction and multi-stage verification... Please wait (15-30s on CPU).
  `;

  // Simulate active stage transitions for user visual feedback while request completes
  let simulatedStage = 1;
  updateStageUI("stage_1", "PROCESSING", "Validating applicant details and statutory rules...");
  const simInterval = setInterval(() => {
    simulatedStage++;
    if (simulatedStage <= 5) {
      updateStageUI(`stage_${simulatedStage - 1}`, "VERIFIED", "Stage completed.");
      updateStageUI(`stage_${simulatedStage}`, "PROCESSING", `Extracting and analyzing document ${simulatedStage}...`);
    }
  }, 4000);

  try {
    let response;
    if (isSampleMode) {
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
      <span style="color: var(--danger);">❌ Verification Pipeline Error: ${error.message}</span>
    `;
    alert(`Verification Pipeline Error: ${error.message}`);
  } finally {
    btnSubmit.disabled = false;
    btnSubmit.innerHTML = `<span>🚀 Execute 8-Stage Verification Pipeline</span>`;
  }
}

function renderPipelineResults(report) {
  // Update stage statuses with official backend report
  report.stages.forEach(st => {
    updateStageUI(st.stage_id, st.status, st.message, st.flags || []);
    // Auto-open detail if there are flags
    if (st.flags && st.flags.length > 0) {
      const detail = document.getElementById(`detail_${st.stage_id}`);
      if (detail) detail.style.display = "block";
    }
  });

  // Update overall badge & banner
  const overallBadge = document.getElementById("pipelineOverallBadge");
  const banner = document.getElementById("pipelineStatusBanner");

  if (report.overall_status === "VERIFIED") {
    overallBadge.innerHTML = `<span class="badge badge-success">✓ Fully Verified</span>`;
    banner.innerHTML = `✅ <strong>Pre-Verification Successful:</strong> All supporting documents and statutory community inheritance rules verified. Official application ready for Tahsildar sign-off.`;
  } else if (report.overall_status === "MANUAL_REVIEW") {
    overallBadge.innerHTML = `<span class="badge badge-warning">⚠️ Manual Review Required</span>`;
    banner.innerHTML = `⚠️ <strong>Pre-Verification Complete with Notes:</strong> Application document prepared with designated inquiry remarks for Tahsildar field scrutiny.`;
  } else {
    overallBadge.innerHTML = `<span class="badge badge-danger">✗ Verification Failed</span>`;
    banner.innerHTML = `❌ <strong>Verification Rejected:</strong> Critical discrepancies detected in submitted supporting documents.`;
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
        <td><code>${m.application_value || "—"}</code></td>
        <td><code>${m.document_value || "—"}</code></td>
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