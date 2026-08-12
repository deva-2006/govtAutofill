// Field Alias Dictionary to map backend JSON keys to HTML input IDs/Names
const FIELD_ALIASES = {
  full_name: ["applicant_fullname", "fullname", "fname", "name"],
  dob: ["date_of_birth", "dob", "birthdate"],
  gender: ["gender", "sex"],
  mobile: ["mobile_number", "mobile", "phone"],
  email: ["email_id", "email"],
  id_number: ["doc_identity_number", "id_num", "pan_no", "dl_no", "id_number"],
  
  // Relative details
  relation_type: ["relation_type", "relationship"],
  relative_name: ["relative_name", "father_name", "husband_name", "guardian_name"],
  
  // Address breakdown
  house_no: ["house_no", "door_no", "flat_no"],
  street: ["street_address", "street", "locality"],
  city: ["village_town", "city", "town"],
  post_office: ["post_office", "po"],
  pincode: ["pincode", "zip", "postal_code"],
  district: ["district"],
  state: ["state"],
  constituency: ["constituency", "assembly"],
  
  // Birth & Declaration
  birth_town: ["birth_town", "place_of_birth"],
  birth_state: ["birth_state"]
};

// Multi-document state accumulator
let attachedFiles = [];

// Helper to format bytes to KB/MB
function formatFileSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// Render multi-document chips UI
function renderFileListUI() {
  const container = document.getElementById('fileListContainer');
  const dropzoneContent = document.querySelector('.dropzone-content');

  if (!container || !dropzoneContent) return;

  container.innerHTML = '';

  if (attachedFiles.length === 0) {
    dropzoneContent.innerHTML = `
      <span class="upload-icon">📁</span>
      <p><strong>Upload Document Images / PDFs (Select one or multiple files)</strong></p>
      <p class="subtitle">Drag & drop or click to add Aadhaar Front, Back, PAN Card, Passport, etc.</p>
    `;
    return;
  }

  dropzoneContent.innerHTML = `
    <span class="upload-icon">✅</span>
    <p style="color: #16a34a;"><strong>${attachedFiles.length} Document(s) Attached</strong></p>
    <p class="subtitle" style="color: #2563eb; font-weight: 600;">Click or drop more files to add to list</p>
  `;

  attachedFiles.forEach((file, index) => {
    const chip = document.createElement('div');
    chip.className = 'file-chip';
    chip.innerHTML = `
      <span>📄 ${file.name} (${formatFileSize(file.size)})</span>
      <button type="button" class="remove-btn" title="Remove document" onclick="removeAttachedFile(${index})">✕</button>
    `;
    container.appendChild(chip);
  });
}

// Add new files to state (avoid duplicates)
function addFilesToAccumulator(newFiles) {
  Array.from(newFiles).forEach(file => {
    const isDuplicate = attachedFiles.some(f => f.name === file.name && f.size === file.size);
    if (!isDuplicate) {
      attachedFiles.push(file);
    }
  });
  renderFileListUI();
}

// Remove document from list
function removeAttachedFile(index) {
  attachedFiles.splice(index, 1);
  renderFileListUI();
}

// 1. Listen for file selection & drag-drop events
document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById('documentInput');
  const dropzone = document.querySelector('.upload-dropzone');

  if (fileInput) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files && fileInput.files.length > 0) {
        addFilesToAccumulator(fileInput.files);
        fileInput.value = ''; // Reset input to allow re-adding same file if needed
      }
    });
  }

  if (dropzone) {
    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('dragover');
      }, false);
    });

    dropzone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      if (dt && dt.files && dt.files.length > 0) {
        addFilesToAccumulator(dt.files);
      }
    });
  }
});

// 2. Triggers document upload to backend and invokes autofill
async function processDocument() {
  const status = document.getElementById('status');

  if (!attachedFiles || attachedFiles.length === 0) {
    alert("Please select or drop at least one document image or PDF first!");
    return;
  }

  status.innerText = `⏳ Processing ${attachedFiles.length} document file(s) with AI...`;
  status.style.color = "#2563eb";

  const formData = new FormData();
  for (let i = 0; i < attachedFiles.length; i++) {
    formData.append('files', attachedFiles[i]);
  }

  try {
    const response = await fetch('http://localhost:8000/extract', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Server returned status ${response.status}`);
    }

    const data = await response.json();
    console.log("Extracted Data Received from multiple documents:", data);
    
    autoFillForm(data);
    
    status.innerText = `✅ AI Extraction Complete! (${attachedFiles.length} document(s) processed)`;
    status.style.color = "#16a34a";
  } catch (err) {
    console.error("Extraction error:", err);
    status.innerText = "❌ Error processing document(s). Ensure FastAPI backend is running on port 8000.";
    status.style.color = "#dc2626";
  }
}

// 3. Iterates through extracted JSON and populates matching DOM inputs
function autoFillForm(data) {
  // Update face photo preview if present
  if (data.photo_base64) {
    const photoImg = document.getElementById('photo_preview');
    if (photoImg) {
      photoImg.src = data.photo_base64;
    }
  }

  // Iterate through key-value pairs
  Object.entries(data).forEach(([key, value]) => {
    if (!value || key === 'photo_base64') return;

    const aliases = FIELD_ALIASES[key] || [key];

    for (const alias of aliases) {
      const element = document.querySelector(
        `input[id="${alias}" i], select[id="${alias}" i], textarea[id="${alias}" i], input[name="${alias}" i]`
      );

      if (element) {
        if (element.tagName.toLowerCase() === 'select') {
          // Case-insensitive match for <select> options
          let matchedOption = Array.from(element.options).find(
            opt => opt.value.toLowerCase() === String(value).toLowerCase() ||
                   opt.text.toLowerCase().includes(String(value).toLowerCase())
          );
          if (matchedOption) {
            element.value = matchedOption.value;
          } else {
            element.value = value;
          }
        } else {
          element.value = value;
        }
        
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Brief blue highlight feedback
        element.style.transition = "background-color 0.5s";
        element.style.backgroundColor = "#e0f2fe";
        setTimeout(() => {
          element.style.backgroundColor = "";
        }, 1500);

        break;
      }
    }
  });

  // Default application date to today
  const declDate = document.getElementById('declaration_date');
  if (declDate && !declDate.value) {
    declDate.value = new Date().toISOString().split('T')[0];
  }
}