// ====================== 1. Kiểm tra đăng nhập ======================
const accessToken = localStorage.getItem("access_token");
const userRole = localStorage.getItem("user_role");

if (!accessToken) {
  alert("Vui lòng đăng nhập trước!");
  window.location.href = "../../index.html";
} else if (userRole !== "Admin") {
  alert("Bạn không có quyền truy cập trang này!");
  window.location.href = "../../index.html";
}

// ====================== 2. Khai báo phần tử ======================
const tableBody = document.getElementById("subjectTableBody");
const btnBack = document.getElementById("btnBack");
const btnSave = document.getElementById("btnSaveSubject");
const form = document.getElementById("subjectForm");

const inputCode = document.getElementById("subjectCode");
const inputName = document.getElementById("subjectName");
const inputCredit = document.getElementById("subjectCredit");

let editingId = null; // lưu id khi đang sửa

// ====================== 3. Hàm tải danh sách môn học ======================
async function fetchSubjects() {
  try {
    const res = await fetch("http://localhost:8000/api/courses/", {
      headers: {
        "Authorization": `Bearer ${accessToken}`,
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

// ====================== 4. Hiển thị danh sách ======================
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
      <td>
        <button class="btn-edit" data-id="${s.CourseID}">Sửa</button>
        <button class="btn-delete" data-id="${s.CourseID}">Xóa</button>
      </td>
    `;
    tableBody.appendChild(tr);
  });

  // Gán sự kiện
  document.querySelectorAll(".btn-edit").forEach(btn =>
    btn.addEventListener("click", () => editSubject(btn.dataset.id))
  );

  document.querySelectorAll(".btn-delete").forEach(btn =>
    btn.addEventListener("click", () => deleteSubject(btn.dataset.id))
  );
}

// ====================== 5. Thêm hoặc cập nhật môn học ======================
async function saveSubject() {
  const subjectData = {
    CourseID: inputCode.value.trim(),
    CourseName: inputName.value.trim(),
    Credit: parseInt(inputCredit.value)
  };

  if (!subjectData.CourseID || !subjectData.CourseName || !subjectData.Credit) {
    alert("Vui lòng nhập đầy đủ thông tin!");
    return;
  }

  try {
    let url = "http://localhost:8000/api/courses/";
    let method = "POST";

    if (editingId) {
      url = `http://localhost:8000/api/courses/${editingId}/`;
      method = "PUT";
    }

    const res = await fetch(url, {
      method: method,
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(subjectData)
    });

    if (!res.ok) throw new Error("Không thể lưu môn học!");

    alert(editingId ? "Cập nhật thành công!" : "Thêm môn học thành công!");
    form.reset();
    editingId = null;
    btnSave.textContent = "+ Thêm môn học";
    await fetchSubjects();

  } catch (error) {
    console.error(error);
    alert("Lỗi khi lưu môn học!");
  }
}

// ====================== 6. Chỉnh sửa môn học ======================
async function editSubject(id) {
  try {
    const res = await fetch(`http://localhost:8000/api/courses/${id}/`, {
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json"
      }
    });

    if (!res.ok) throw new Error("Không thể lấy thông tin môn học!");

    const data = await res.json();
    inputCode.value = data.CourseID;
    inputName.value = data.CourseName;
    inputCredit.value = data.Credit;

    editingId = id;
    btnSave.textContent = "💾 Lưu thay đổi";
  } catch (error) {
    console.error(error);
    alert("Lỗi khi tải dữ liệu môn học!");
  }
}

// ====================== 7. Xóa môn học ======================
async function deleteSubject(id) {
  if (!confirm("Bạn có chắc chắn muốn xóa môn học này?")) return;

  try {
    const res = await fetch(`http://localhost:8000/api/courses/${id}/`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${accessToken}`
      }
    });

    if (!res.ok) throw new Error("Không thể xóa môn học!");
    alert("Đã xóa môn học thành công!");
    await fetchSubjects();
  } catch (error) {
    console.error(error);
    alert("Lỗi khi xóa môn học!");
  }
}

// ====================== 8. Sự kiện ======================
btnSave.addEventListener("click", saveSubject);
btnBack.addEventListener("click", () => {
  window.location.href = "../home/home.html";
});

// ====================== 9. Khởi chạy ======================
fetchSubjects();
