const API_URL = "http://localhost:8000/api/students/";

document.getElementById("formAdd").addEventListener("submit", async (e) => {
  e.preventDefault();

  const studentData = {
    student_id: document.getElementById("id").value.trim(),
    full_name: document.getElementById("name").value.trim(),
    birth_date: document.getElementById("b_date").value,
    gender: document.getElementById("gender").value,
    address: document.getElementById("adr").value.trim(),
    email: document.getElementById("email").value.trim(),
  };

  const token = localStorage.getItem("access_token"); // ✅ lấy token từ localStorage

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`, // ✅ gửi token cho server
      },
      body: JSON.stringify(studentData),
    });

    if (res.ok) {
      alert("✅ Thêm sinh viên thành công!");
      window.location.href = "../home/home.html";
    } else {
      const err = await res.json();
      alert("❌ Lỗi khi thêm sinh viên: " + JSON.stringify(err));
    }
  } catch (error) {
    console.error("Lỗi kết nối:", error);
    alert("⚠️ Không thể kết nối đến server!");
  }
});
