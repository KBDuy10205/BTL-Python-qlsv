// ========== 1. Kiểm tra đăng nhập ==========
const accessToken = localStorage.getItem("access_token");
if (!accessToken) {
  alert("Vui lòng đăng nhập trước!");
  window.location.href = "../../index.html";
}

// ========== 2. Lấy ID sinh viên cần sửa ==========
const studentIdToEdit = localStorage.getItem("edit_student_id");
if (!studentIdToEdit) {
  alert("Không tìm thấy sinh viên cần sửa!");
  window.location.href = "../home/home.html";
}

// ========== 3. Khai báo phần tử ==========
const studentIdInput = document.getElementById("studentId");
const fullNameInput = document.getElementById("fullName");
const genderInput = document.getElementById("gender");
const form = document.getElementById("editForm");
const btnCancel = document.getElementById("btnCancel");

// ========== 4. Gọi API lấy thông tin sinh viên ==========
async function fetchStudentDetail() {
  try {
    const res = await fetch(`http://localhost:8000/api/students/${studentIdToEdit}/`, {
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    });

    if (!res.ok) throw new Error("Không thể tải thông tin sinh viên!");

    const data = await res.json();

    // Gán dữ liệu lên form
    studentIdInput.value = data.student_id || "";
    fullNameInput.value = data.full_name || "";
    genderInput.value = data.gender || "Nam";
    
  } catch (error) {
    console.error(error);
    alert("Lỗi khi tải dữ liệu sinh viên!");
  }
}

// ========== 5. Lưu thay đổi ==========
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const updatedData = {
    full_name: fullNameInput.value.trim(),
    gender: genderInput.value,
    
  };

  try {
    const res = await fetch(`http://localhost:8000/api/students/${studentIdToEdit}/`, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedData),
    });

    if (!res.ok) throw new Error("Cập nhật thất bại!");

    alert("Cập nhật thành công!");
    localStorage.removeItem("edit_student_id");
    window.location.href = "../home/home.html";
  } catch (error) {
    console.error(error);
    alert("Lỗi khi cập nhật sinh viên!");
  }
});

// ========== 6. Hủy ==========
btnCancel.addEventListener("click", () => {
  window.location.href = "../home/home.html";
});

// ========== 7. Khởi chạy ==========
fetchStudentDetail();
