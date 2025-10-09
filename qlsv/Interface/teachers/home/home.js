// ========== 1. Kiểm tra đăng nhập ==========
const accessToken = localStorage.getItem("access_token");
const userRole = localStorage.getItem("user_role");

/*if (!accessToken) {
  alert("Vui lòng đăng nhập trước!");
  window.location.href = "../../index.html";
} else if (userRole !== "gv") {  // giả sử 'gv' là giáo viên / quản trị
  alert("Bạn không có quyền truy cập trang này!");
  window.location.href = "../../index.html";
}*/

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
      <td>${sv.class_name || sv.lop || "-"}</td>
      <td>${sv.khoa || "-"}</td>
      <td>
        <button class="btnEdit" data-id="${sv.id}">Sửa</button>
        <button class="btnDelete" data-id="${sv.id}">Xóa</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
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

// ========== 9. Khởi chạy ==========
fetchStudents();
