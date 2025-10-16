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

// ========== 2. Khai báo phần tử ==========
const tableBody = document.querySelector("#studentTable tbody");
const searchInput = document.getElementById("searchInput");
const btnSearch = document.getElementById("btnSearch");
const btnAdd = document.getElementById("btnAdd");
const filterClass = document.getElementById("filterClass");

let allStudents = []; // dữ liệu sinh viên từ backend

// ========== 3. Gọi API lấy danh sách sinh viên ==========
async function fetchStudents() {
  try {
    const res = await fetch("http://localhost:8000/api/students/", {
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    });

    if (!res.ok) {
      throw new Error("Không thể tải danh sách sinh viên!");
    }

    const data = await res.json();
    allStudents = data;
    renderTable(data);
    renderClassOptions(data);
  } catch (error) {
    console.error(error);
    alert("Lỗi khi tải dữ liệu sinh viên!");
  }
}

// ========== 4. Hiển thị danh sách sinh viên ==========
function renderTable(data) {
  tableBody.innerHTML = "";

  if (data.length === 0) {
    tableBody.innerHTML = `<tr><td colspan="6">Không có sinh viên nào</td></tr>`;
    return;
  }

  data.forEach((sv) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${sv.student_id || "-"}</td>
      <td>${sv.full_name}</td>
      <td>${sv.gender || "-"}</td>
      <td>${sv.phone || "-"}</td>
      <td>${sv.address || "-"}</td>
      <td>
        <button class="btnEdit" data-id="${sv.student_id}">Sửa</button>
        <button class="btnDelete" data-id="${sv.student_id}">Xóa</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
  // Gán lại sự kiện sau khi render
  attachActionEvents();
}

function attachActionEvents() {
  // Sửa sinh viên
  document.querySelectorAll(".btnEdit").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-id");
      editStudent(id);
    });
  });

  // Xóa sinh viên
  document.querySelectorAll(".btnDelete").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-id");
      deleteStudent(id);
    });
  });
}

//Hàm sửa sinh viên
function editStudent(id) {
  localStorage.setItem("edit_student_id", id);
  window.location.href = "../edit/edit.html";
}


//Hàm xóa sinh viên
async function deleteStudent(id) {
  if (!confirm("Bạn có chắc chắn muốn xóa sinh viên này?")) return;

  try {
    const res = await fetch(`http://localhost:8000/api/students/${id}/`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${accessToken}`,
      },
    });

    if (res.ok) {
      alert("Đã xóa sinh viên thành công!");
      fetchStudents(); // load lại danh sách
    } else {
      alert("Không thể xóa sinh viên!");
    }
  } catch (error) {
    console.error(error);
    alert("Lỗi khi xóa sinh viên!");
  }
}

// ========== 5. Tạo danh sách lớp để lọc ==========
function renderClassOptions(data) {
  const classes = [...new Set(data.map((sv) => sv.class_name || sv.lop).filter(Boolean))];
  filterClass.innerHTML = '<option value="">-- Tất cả --</option>';
  classes.forEach((lop) => {
    const opt = document.createElement("option");
    opt.value = lop;
    opt.textContent = lop;
    filterClass.appendChild(opt);
  });
}

// ========== 6. Xử lý tìm kiếm theo mã sinh viên ==========
btnSearch.addEventListener("click", () => {
  const keyword = searchInput.value.trim().toLowerCase();
  const filtered = allStudents.filter((sv) =>
    (sv.student_id || "").toLowerCase().includes(keyword)
  );
  renderTable(filtered);
});

// ========== 7. Lọc theo lớp ==========
filterClass.addEventListener("change", () => {
  const selectedClass = filterClass.value;
  if (!selectedClass) {
    renderTable(allStudents);
  } else {
    const filtered = allStudents.filter((sv) => (sv.class_name || sv.lop) === selectedClass);
    renderTable(filtered);
  }
});

// ========== 8. Chuyển sang trang thêm sinh viên ==========
btnAdd.addEventListener("click", () => {
  window.location.href = "../add/add.html";
});

//Chuyển sang trang môn học
btnManageSubjects.addEventListener("click", () => {
  window.location.href = "../subjects/subjects.html";
});
// ========== 9. Khởi chạy ==========
fetchStudents();
học