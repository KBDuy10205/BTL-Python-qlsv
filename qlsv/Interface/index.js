async function login() {
  const email = document.getElementById("email_address").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorMsg = document.getElementById("errorMsg");

  errorMsg.style.display = "none";

  if (!email || !password) {
    errorMsg.textContent = "Vui lòng nhập đầy đủ thông tin!";
    errorMsg.style.display = "block";
    return;
  }

  try {
    console.log("📤 Gửi request...");
    const response = await fetch("http://localhost:8000/account/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    console.log("📩 Nhận phản hồi:", response);

    let data;
    try {
      data = await response.json();
      console.log("✅ JSON:", data);
    } catch (jsonError) {
      console.error("❌ JSON parse lỗi:", jsonError);
      errorMsg.textContent = "Phản hồi không phải JSON hợp lệ!";
      errorMsg.style.display = "block";
      return;
    }

    if (!response.ok) {
      console.warn("❌ Server trả mã lỗi:", response.status);
      errorMsg.textContent = data?.error || "Sai tài khoản hoặc mật khẩu!";
      errorMsg.style.display = "block";
      return;
    }

    // ✅ Lưu token
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("user_role", data.user.role);
    localStorage.setItem("student_id",data.student_id);


    console.log("🎯 Đăng nhập thành công:", data.user.role);

    if (data.user.role === "Student") {
      window.location.href = "students/profile/profile.html";
    } else if (data.user.role === "Admin") {
      window.location.href = "teachers/home/home.html";
    } else {
      alert("Không xác định vai trò người dùng!");
    }

  } catch (error) {
    console.error("💥 Lỗi khi fetch:", error);
    errorMsg.textContent = "Không thể kết nối tới server!";
    errorMsg.style.display = "block";
  }
}
