async function login() {
  const email = document.getElementById("email_address").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorMsg = document.getElementById("errorMsg");

  // Ẩn thông báo lỗi ban đầu
  errorMsg.style.display = "none";

  if (!email || !password) {
    errorMsg.textContent = "Vui lòng nhập đầy đủ thông tin!";
    errorMsg.style.display = "block";
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/account/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email,
        password: password
      }),
    });

    const data = await response.json();
    console.log(data);

    if (!response.ok) {
      errorMsg.textContent = data.error || "Sai tài khoản hoặc mật khẩu!";
      errorMsg.style.display = "block";
      return;
    }

    // ✅ Lưu token + role để sử dụng sau
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("user_role", data.user.role);

    // ✅ Chuyển hướng theo vai trò
    if (data.user.role === "Student") {
      window.location.href = "students/profile.html";
    } else if (data.user.role === "Admin") {
      window.location.href = "teachers/home/home.html";
    } else {
      alert("Không xác định vai trò người dùng!");
    }

  } catch (error) {
    console.error("Lỗi:", error);
    errorMsg.textContent = "Không thể kết nối tới server!";
    errorMsg.style.display = "block";
  }
  console.log("Sending request:", { email, password });
console.log("Response status:", response.status);
console.log("Response body:", data);

}
