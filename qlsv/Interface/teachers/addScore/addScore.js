// ========== 1. Kiểm tra đăng nhập ==========
const accessToken = localStorage.getItem("access_token");
const userRole = localStorage.getItem("user_role");

if (!accessToken) {
  alert("Vui lòng đăng nhập trước!");
  window.location.href = "../../index.html";
} else if (userRole !== "Admin") {
  alert("Bạn không có quyền truy cập trang này!");
  window.location.href = "../../index.html";
}

// ========== 2. Lấy mã sinh viên từ localStorage ==========
const studentCode = localStorage.getItem("addScoreID");
if (!studentCode) {
  alert("Không tìm thấy sinh viên cần nhập điểm!");
  window.location.href = "../home/home.html";
}

const studentInfoDiv = document.getElementById("studentInfo");
const subjectTableBody = document.getElementById("subjectTableBody");
const btnSave = document.getElementById("btnSave");
const btnBack = document.getElementById("btnBack");

// ========== 3. Lấy dữ liệu sinh viên, môn học, và điểm ==========
async function loadData() {
  try {
    // --- Lấy thông tin sinh viên ---
    const resStudent = await fetch(`http://localhost:8000/api/students/${studentCode}/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    const student = await resStudent.json();
    studentInfoDiv.textContent = `Mã SV: ${student.student_id} | Họ tên: ${student.full_name}`;

    // --- Lấy danh sách môn học ---
    const resCourses = await fetch("http://localhost:8000/api/courses/", {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    const courses = await resCourses.json();

    // --- Lấy danh sách điểm của sinh viên ---
    const resScores = await fetch(`http://localhost:8000/api/scores/?StudentCode=${studentCode}`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    const scores = await resScores.json();

    // Gộp dữ liệu môn học + điểm
    renderSubjectsWithScores(courses, scores);
  } catch (err) {
    console.error("Lỗi tải dữ liệu:", err);
    subjectTableBody.innerHTML = `<tr><td colspan="9">❌ Lỗi khi tải dữ liệu!</td></tr>`;
  }
}

// ========== 4. Gộp danh sách môn học và điểm ==========
function renderSubjectsWithScores(courses, scores) {
  subjectTableBody.innerHTML = "";

  if (!courses.length) {
    subjectTableBody.innerHTML = `<tr><td colspan="9">Không có môn học nào!</td></tr>`;
    return;
  }
 

  courses.forEach((course, index) => {
    // Tìm điểm tương ứng trong scores
    const score = scores.find(s => s.CourseId === course.CourseID);

    const mid = score?.Midterm ?? "";
    const fin = score?.Final ?? "";
    const att = score?.Attendance ?? "";
    const total = score?.Total ?? "-";
    const result = score ? (total >= 5 ? "✅ Đạt" : "❌ Rớt") : "-";

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${course.CourseID}</td>
      <td>${course.CourseName}</td>
      <td>${course.Credit}</td>
      <td><input type="number" class="score-input" data-course="${course.CourseID}" data-type="Attendance" min="0" max="10" step="0.1" value="${att}"></td>
      <td><input type="number" class="score-input" data-course="${course.CourseID}" data-type="Midterm" min="0" max="10" step="0.1" value="${mid}"></td>
      <td><input type="number" class="score-input" data-course="${course.CourseID}" data-type="Final" min="0" max="10" step="0.1" value="${fin}"></td>
      <td>${total}</td>
      <td style="color:${result.includes('Đạt') ? 'green' : 'red'};">${result}</td>
    `;
    subjectTableBody.appendChild(row);
  });
}

// ========== 5. Lưu điểm ==========
btnSave.addEventListener("click", async () => {
  const inputs = document.querySelectorAll(".score-input");
  const grouped = {};

  // Gom điểm theo CourseID
  inputs.forEach(input => {
    const courseId = input.dataset.course;
    const type = input.dataset.type;
    const value = parseFloat(input.value);

    if (!grouped[courseId]) grouped[courseId] = {};
    if (!isNaN(value)) grouped[courseId][type] = value;
  });

  const updates = Object.entries(grouped).map(([courseId, data]) => ({
    StudentCode: studentCode,
    CourseId: courseId,
    ...data,
  }));

  if (!updates.length) {
    alert("Không có điểm nào để lưu!");
    return;
  }

  try {
    for (const item of updates) {
      // Kiểm tra xem đã có record Score chưa
      const existingRes = await fetch(
        `http://localhost:8000/api/scores/?StudentCode=${item.StudentCode}&CourseId=${item.CourseId}`,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );
      const existing = await existingRes.json();

      if (existing.length > 0) {
        // Đã có -> PUT cập nhật
        await fetch(`http://localhost:8000/api/scores/${existing[0].id}/`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(item),
        });
      } else {
        // Chưa có -> POST tạo mới
        await fetch("http://localhost:8000/api/scores/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(item),
        });
      }
    }

    alert("💾 Lưu điểm thành công!");
    await loadData(); // Cập nhật lại bảng
  } catch (err) {
    console.error(err);
    alert("❌ Lỗi khi lưu điểm!");
  }
});

// ========== 6. Quay lại ==========
btnBack.addEventListener("click", () => {
  window.location.href = "../home/home.html";
});

// ========== 7. Khởi chạy ==========
loadData();
