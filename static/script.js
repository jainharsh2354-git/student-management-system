const API = "/api/students";
const $ = (id) => document.getElementById(id);
const fields = ["name", "roll_no", "class_name", "marks", "contact"];
let timer;

function showMessage(text, ok = true) {
  const m = $("message");
  m.textContent = text;
  m.className = ok ? "ok" : "err";
}

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

async function loadStudents() {
  const q = $("search").value.trim();
  const res = await fetch(`${API}?q=${encodeURIComponent(q)}`);
  const data = await res.json();
  $("tbody").innerHTML = data.map((s) => `
    <tr>
      <td>${esc(s.name)}</td><td>${esc(s.roll_no)}</td><td>${esc(s.class_name)}</td>
      <td>${s.marks}</td><td>${esc(s.contact)}</td>
      <td>
        <button onclick='editStudent(${JSON.stringify(s)})'>Edit</button>
        <button class="danger" onclick="deleteStudent(${s.id})">Delete</button>
      </td>
    </tr>`).join("");
  $("empty").hidden = data.length > 0;
  $("count").textContent = `(${data.length})`;
}

function resetForm() {
  $("student-form").reset();
  $("student-id").value = "";
  $("form-title").textContent = "Add Student";
  $("submit-btn").textContent = "Add Student";
  $("cancel-btn").hidden = true;
}

window.editStudent = (s) => {
  $("student-id").value = s.id;
  fields.forEach((f) => ($(f).value = s[f]));
  $("form-title").textContent = "Edit Student";
  $("submit-btn").textContent = "Update Student";
  $("cancel-btn").hidden = false;
  window.scrollTo({ top: 0, behavior: "smooth" });
};

window.deleteStudent = async (id) => {
  if (!confirm("Delete this student?")) return;
  const res = await fetch(`${API}/${id}`, { method: "DELETE" });
  const data = await res.json();
  showMessage(data.message || data.errors.join(" "), res.ok);
  loadStudents();
};

$("student-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = {};
  fields.forEach((f) => (body[f] = $(f).value.trim()));

  // client-side validation
  if (!body.name || !body.roll_no || !body.class_name) return showMessage("Name, Roll No and Class are required.", false);
  if (isNaN(body.marks) || body.marks === "" || body.marks < 0 || body.marks > 100) return showMessage("Marks must be between 0 and 100.", false);
  if (!/^\d{10}$/.test(body.contact)) return showMessage("Contact must be a 10-digit number.", false);

  const id = $("student-id").value;
  const res = await fetch(id ? `${API}/${id}` : API, {
    method: id ? "PUT" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (res.ok) {
    showMessage(data.message);
    resetForm();
    loadStudents();
  } else {
    showMessage(data.errors.join(" "), false);
  }
});

$("cancel-btn").addEventListener("click", resetForm);
$("search").addEventListener("input", () => {
  clearTimeout(timer);
  timer = setTimeout(loadStudents, 250);
});

loadStudents();
