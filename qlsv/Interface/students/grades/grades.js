(() => {
  // ========== 1. Kiểm tra đăng nhập ==========

  
  const gradeAccessToken = localStorage.getItem("access_token");
  const gradeUserRole = localStorage.getItem("user_role");
  if (!gradeAccessToken) {
    alert("Vui lòng đăng nhập trước!");
    window.location.href = "../../index.html";
  } else if (gradeUserRole !== "Student") {
    alert("Bạn không có quyền truy cập trang này!");
    window.location.href = "../../index.html";
  }

  // ========== 2. Lấy mã sinh viên từ localStorage ==========
  const studentCode = localStorage.getItem("student_id");
  const subjectTableBody = document.getElementById("subjectTableBody");

  // ========== 3. Lấy dữ liệu sinh viên, môn học, và điểm ==========
  async function loadData() {
    try {
      // --- Lấy danh sách môn học ---
      const resCourses = await fetch("http://localhost:8000/api/courses/", {
        headers: { Authorization: `Bearer ${gradeAccessToken}` },
      });
      const courses = await resCourses.json();

      // --- Lấy danh sách điểm của sinh viên ---
      const resScores = await fetch(
        `http://localhost:8000/api/scores/?StudentCode=${studentCode}`,
        { headers: { Authorization: `Bearer ${gradeAccessToken}` } }
      );
      const scores = await resScores.json();

      // --- Hiển thị kết hợp ---
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
      const score = scores.find(s => s.CourseId === course.CourseID);

      const att = score?.Attendance ?? "";
      const mid = score?.Midterm ?? "";
      const fin = score?.Final ?? "";
      const total = score?.Total ?? "";
      const result = score
        ? total >= 5
          ? "✅ Đạt"
          : "❌ Rớt"
        : "-";

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${index + 1}</td>
        <td>${course.CourseID}</td>
        <td>${course.CourseName}</td>
        <td>${course.Credit}</td>
        <td>${att}</td>
        <td>${mid}</td>
        <td>${fin}</td>
        <td>${total}</td>
        <td style="color:${result.includes("Đạt") ? "green" : "red"};">${result}</td>
      `;
      subjectTableBody.appendChild(row);
    });
  }

  // ========== 7. Khởi chạy ==========
  loadData();

})();