// Base URL of your FastAPI backend. Change this if your server runs elsewhere.
const API_BASE = "http://127.0.0.1:8000/api/opportunities";

let allOpportunities = [];
let currentFilter = "all";
let editingId = null; // null = create mode, otherwise = edit mode

// ---------- DOM references ----------
const listContainer = document.getElementById("listContainer");
const emptyState = document.getElementById("emptyState");
const loadingState = document.getElementById("loadingState");
const countLabel = document.getElementById("countLabel");

const detailOverlay = document.getElementById("detailOverlay");
const detailPanel = document.getElementById("detailPanel");
const detailContent = document.getElementById("detailContent");

const formOverlay = document.getElementById("formOverlay");
const oppForm = document.getElementById("oppForm");
const formTitle = document.getElementById("formTitle");
const formError = document.getElementById("formError");

const toast = document.getElementById("toast");

// ---------- Init ----------
document.getElementById("newOppBtn").addEventListener("click", () => openForm());
document.getElementById("closeFormBtn").addEventListener("click", closeForm);
document.getElementById("cancelFormBtn").addEventListener("click", closeForm);
formOverlay.addEventListener("click", (e) => { if (e.target === formOverlay) closeForm(); });
detailOverlay.addEventListener("click", closeDetail);
oppForm.addEventListener("submit", handleFormSubmit);

document.querySelectorAll(".filter-tab").forEach(btn => {
  btn.addEventListener("click", () => {
    currentFilter = btn.dataset.filter;
    document.querySelectorAll(".filter-tab").forEach(b => {
      b.classList.remove("text-ink", "border-ink", "font-medium");
      b.classList.add("text-inksoft", "border-transparent");
    });
    btn.classList.remove("text-inksoft", "border-transparent");
    btn.classList.add("text-ink", "border-ink", "font-medium");
    renderList();
  });
});

fetchAll();

// ---------- API calls ----------
async function fetchAll() {
  loadingState.classList.remove("hidden");
  emptyState.classList.add("hidden");
  try {
    const res = await fetch(API_BASE);
    if (!res.ok) throw new Error("Failed to load opportunities");
    allOpportunities = await res.json();
    renderList();
  } catch (err) {
    showToast("Could not reach the server. Is the backend running?", "error");
  } finally {
    loadingState.classList.add("hidden");
  }
}

async function fetchOne(id) {
  const res = await fetch(`${API_BASE}/${id}`);
  if (res.status === 404) throw new Error("Opportunity not found");
  if (!res.ok) throw new Error("Failed to load opportunity");
  return res.json();
}

async function createOpportunity(payload) {
  const res = await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(extractError(data));
  return data;
}

async function updateOpportunity(id, payload) {
  const res = await fetch(`${API_BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(extractError(data));
  return data;
}

async function deleteOpportunityApi(id) {
  const res = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
  const data = await res.json();
  if (!res.ok) throw new Error(extractError(data));
  return data;
}

function extractError(data) {
  if (!data || !data.detail) return "Something went wrong.";
  if (typeof data.detail === "string") return data.detail;
  // FastAPI validation errors come back as a list of objects
  if (Array.isArray(data.detail)) {
    return data.detail.map(d => d.msg || JSON.stringify(d)).join(", ");
  }
  return "Something went wrong.";
}

// ---------- Rendering ----------
function renderList() {
  const filtered = currentFilter === "all"
    ? allOpportunities
    : allOpportunities.filter(o => o.status === currentFilter);

  countLabel.textContent = `${filtered.length} listing${filtered.length !== 1 ? "s" : ""}`;

  if (filtered.length === 0) {
    listContainer.innerHTML = "";
    emptyState.classList.remove("hidden");
    return;
  }
  emptyState.classList.add("hidden");

  listContainer.innerHTML = filtered.map(o => `
    <button data-id="${o.id}" class="opp-row w-full text-left row-divider py-4 flex items-start justify-between gap-4 hover:bg-paper2 transition-colors px-2 -mx-2">
      <div class="min-w-0">
        <p class="font-serif text-lg font-semibold text-ink truncate">${escapeHtml(o.title)}</p>
        <p class="text-sm text-inksoft mt-0.5">${escapeHtml(o.research_area)} · ${escapeHtml(o.department)} · ${escapeHtml(o.faculty_name)}</p>
      </div>
      <div class="flex flex-col items-end gap-1 shrink-0">
        <span class="text-xs px-2 py-1 font-medium ${o.status === 'Open' ? 'bg-opensoft text-open' : 'bg-closedsoft text-closed'}">${o.status}</span>
        <span class="text-xs text-inksoft">${formatDate(o.application_deadline)}</span>
      </div>
    </button>
  `).join("");

  document.querySelectorAll(".opp-row").forEach(row => {
    row.addEventListener("click", () => openDetail(row.dataset.id));
  });
}

async function openDetail(id) {
  try {
    const o = await fetchOne(id);
    detailContent.innerHTML = `
      <div class="flex items-start justify-between mb-6">
        <span class="text-xs px-2 py-1 font-medium ${o.status === 'Open' ? 'bg-opensoft text-open' : 'bg-closedsoft text-closed'}">${o.status}</span>
        <button id="closeDetailBtn" class="text-inksoft hover:text-ink text-xl leading-none">&times;</button>
      </div>
      <h2 class="font-serif text-2xl font-semibold text-ink mb-1">${escapeHtml(o.title)}</h2>
      <p class="text-sm text-inksoft mb-6">${escapeHtml(o.research_area)} · ${escapeHtml(o.department)}</p>

      <p class="text-sm leading-relaxed mb-6">${escapeHtml(o.description)}</p>

      <dl class="space-y-3 text-sm border-t border-rule pt-4">
        <div class="flex justify-between"><dt class="text-inksoft">Faculty member</dt><dd>${escapeHtml(o.faculty_name)}</dd></div>
        <div class="flex justify-between"><dt class="text-inksoft">Required skills</dt><dd class="text-right">${escapeHtml(o.required_skills)}</dd></div>
        <div class="flex justify-between"><dt class="text-inksoft">Available positions</dt><dd>${o.available_positions}</dd></div>
        <div class="flex justify-between"><dt class="text-inksoft">Application deadline</dt><dd>${formatDate(o.application_deadline)}</dd></div>
      </dl>

      <div class="flex flex-wrap gap-3 mt-8 pt-6 border-t border-rule">
        <button id="editBtn" class="bg-ink text-paper px-4 py-2 text-sm font-medium hover:bg-[#2A3D52]">Edit</button>
        <button id="toggleStatusBtn" class="border border-rule px-4 py-2 text-sm font-medium hover:bg-paper2">
          Mark as ${o.status === 'Open' ? 'Closed' : 'Open'}
        </button>
        <button id="deleteBtn" class="text-closed text-sm font-medium px-4 py-2 hover:bg-closedsoft">Delete</button>
      </div>
    `;

    document.getElementById("closeDetailBtn").addEventListener("click", closeDetail);
    document.getElementById("editBtn").addEventListener("click", () => { closeDetail(); openForm(o); });
    document.getElementById("toggleStatusBtn").addEventListener("click", () => toggleStatus(o));
    document.getElementById("deleteBtn").addEventListener("click", () => confirmDelete(o));

    detailOverlay.classList.remove("hidden");
    detailPanel.classList.remove("translate-x-full");
  } catch (err) {
    showToast(err.message, "error");
  }
}

function closeDetail() {
  detailOverlay.classList.add("hidden");
  detailPanel.classList.add("translate-x-full");
}

// ---------- Create / Edit form ----------
function openForm(opp = null) {
  oppForm.reset();
  formError.classList.add("hidden");
  editingId = opp ? opp.id : null;
  formTitle.textContent = opp ? "Edit Opportunity" : "Post an Opportunity";

  if (opp) {
    document.getElementById("f_title").value = opp.title;
    document.getElementById("f_description").value = opp.description;
    document.getElementById("f_research_area").value = opp.research_area;
    document.getElementById("f_department").value = opp.department;
    document.getElementById("f_faculty_name").value = opp.faculty_name;
    document.getElementById("f_required_skills").value = opp.required_skills;
    document.getElementById("f_available_positions").value = opp.available_positions;
    document.getElementById("f_application_deadline").value = opp.application_deadline;
    document.getElementById("f_status").value = opp.status;
  }

  formOverlay.classList.remove("hidden");
  formOverlay.classList.add("flex");
}

function closeForm() {
  formOverlay.classList.add("hidden");
  formOverlay.classList.remove("flex");
  editingId = null;
}

async function handleFormSubmit(e) {
  e.preventDefault();
  formError.classList.add("hidden");

  const payload = {
    title: document.getElementById("f_title").value.trim(),
    description: document.getElementById("f_description").value.trim(),
    research_area: document.getElementById("f_research_area").value.trim(),
    department: document.getElementById("f_department").value.trim(),
    faculty_name: document.getElementById("f_faculty_name").value.trim(),
    required_skills: document.getElementById("f_required_skills").value.trim(),
    available_positions: parseInt(document.getElementById("f_available_positions").value, 10),
    application_deadline: document.getElementById("f_application_deadline").value,
    status: document.getElementById("f_status").value,
  };

  // Basic client-side validation (server still re-validates independently)
  const missing = Object.entries(payload).filter(([k, v]) => v === "" || v === null || Number.isNaN(v));
  if (missing.length > 0) {
    formError.textContent = "Please fill in every field before saving.";
    formError.classList.remove("hidden");
    return;
  }
  if (payload.available_positions <= 0) {
    formError.textContent = "Available positions must be at least 1.";
    formError.classList.remove("hidden");
    return;
  }

  try {
    if (editingId) {
      await updateOpportunity(editingId, payload);
      showToast("Opportunity updated.", "success");
    } else {
      await createOpportunity(payload);
      showToast("Opportunity posted.", "success");
    }
    closeForm();
    fetchAll();
  } catch (err) {
    formError.textContent = err.message;
    formError.classList.remove("hidden");
  }
}

// ---------- Status toggle / delete ----------
async function toggleStatus(opp) {
  const newStatus = opp.status === "Open" ? "Closed" : "Open";
  try {
    await updateOpportunity(opp.id, { status: newStatus });
    showToast(`Marked as ${newStatus}.`, "success");
    closeDetail();
    fetchAll();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function confirmDelete(opp) {
  if (!confirm(`Delete "${opp.title}"? This cannot be undone.`)) return;
  deleteOpportunityApi(opp.id)
    .then(() => {
      showToast("Opportunity deleted.", "success");
      closeDetail();
      fetchAll();
    })
    .catch(err => showToast(err.message, "error"));
}

// ---------- Helpers ----------
function showToast(message, type = "success") {
  toast.textContent = message;
  toast.className = `fixed bottom-6 right-6 z-50 px-4 py-3 text-sm font-medium shadow-lg ${
    type === "success" ? "bg-ink text-paper" : "bg-closed text-paper"
  }`;
  toast.classList.remove("hidden");
  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(() => toast.classList.add("hidden"), 3500);
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr);
  if (isNaN(d)) return dateStr;
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}
