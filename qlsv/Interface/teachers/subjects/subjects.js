async function loadSubjects() {
  const res = await fetch("/api/subjects/");
  const subjects = await res.json();
  renderSubjectsBySemester(subjects);
}

function renderSubjectsBySemester(subjects) {
  const container = document.getElementById("subjectContainer");
  container.innerHTML = ""; // reset nội dung cũ

  // Gom nhóm môn học theo học kỳ
  const grouped = {};
  subjects.forEach((s) => {
    if (!grouped[s.semester]) grouped[s.semester] = [];
    grouped[s.semester].push(s);
  });

  // Duyệt qua 8 học kỳ (hoặc tùy bạn quy định)
  for (let sem = 1; sem <= 8; sem++) {
    const semSubjects = grouped[sem] || [];
    const section = document.createElement("section");
    section.classList.add("semester-section");

    section.innerHTML = `
      <h2>Học kỳ ${sem}</h2>
      <table class="subject-table">
        <thead>
          <tr>
            <th>Mã môn</th>
            <th>Tên môn học</th>
            <th>Số tín chỉ</th>
            <th>Thao tác</th>
          </tr>
        </thead>
        <tbody>
          ${
            semSubjects.length > 0
              ? semSubjects
                  .map(
                    (s) => `
            <tr>
              <td>${s.code}</td>
              <td>${s.name}</td>
              <td>${s.credits}</td>
              <td>
                <button class="btnEdit" data-id="${s.id}">Sửa</button>
                <button class="btnDelete" data-id="${s.id}">Xóa</button>
              </td>
            </tr>
          `
                  )
                  .join("")
              : `<tr><td colspan="4" style="text-align:center;">(Chưa có môn học)</td></tr>`
          }
        </tbody>
      </table>
    `;

    container.appendChild(section);
  }

  // Thêm sự kiện cho các nút xóa/sửa (nếu cần)
  document.querySelectorAll(".btnDelete").forEach((btn) =>
    btn.addEventListener("click", () => deleteSubject(btn.dataset.id))
  );
}

async function addSubject() {
  const name = prompt("Tên môn học:");
  const code = prompt("Mã môn học:");
  const credits = prompt("Số tín chỉ:");
  const semester = prompt("Học kỳ (1-8):");

  if (!name || !code || !semester) {
    alert("Vui lòng nhập đủ thông tin!");
    return;
  }

  await fetch("/api/subjects/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      code,
      credits: Number(credits),
      semester: Number(semester),
    }),
  });

  loadSubjects();
}

async function deleteSubject(id) {
  if (!confirm("Xóa môn học này?")) return;

  await fetch(`/api/subjects/${id}/`, {
    method: "DELETE",
  });

  loadSubjects();
}

btnAddSubject.addEventListener("click", () => {
  window.location.href = "add/add.html";
});
loadSubjects();
