(() => {
  const trainingAccessToken = localStorage.getItem("access_token");
  const trainingUserRole = localStorage.getItem("user_role");

  if (!trainingAccessToken) {
    alert("Vui lòng đăng nhập trước!");
    window.location.href = "../../index.html";
  } else if (trainingUserRole !== "Student") {
    alert("Bạn không có quyền truy cập trang này!");
    window.location.href = "../../index.html";
  }

  const tableBody = document.getElementById("subjectTableBody");

  async function fetchSubjects() {
    try {
      const res = await fetch("http://localhost:8000/api/courses/", {
        headers: {
          "Authorization": `Bearer ${trainingAccessToken}`,
          "Content-Type": "application/json"
        }
      });

      if (!res.ok) throw new Error("Không thể tải danh sách môn học!");
      const data = await res.json();
      renderSubjects(data);
    } catch (error) {
      console.error(error);
      alert("Lỗi khi tải danh sách môn học!");
    }
  }

  function renderSubjects(subjects) {
    tableBody.innerHTML = "";

    if (subjects.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="5">Không có môn học nào</td></tr>`;
      return;
    }

    subjects.forEach((s, i) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${i + 1}</td>
        <td>${s.CourseID}</td>
        <td>${s.CourseName}</td>
        <td>${s.Credit}</td>
      `;
      tableBody.appendChild(tr);
    });
  }

  fetchSubjects();
})();
