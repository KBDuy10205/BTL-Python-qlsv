async function changePassword() {
  const old_password = document.getElementById("old_password").value;
  const new_password = document.getElementById("new_password").value;
  const confirm_password = document.getElementById("confirm_password").value;
  const msg = document.getElementById("msg");

  const token = localStorage.getItem("token");
  if (!token) {
    alert("Bạn chưa đăng nhập!");
    window.location.href = "../index.html";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/account/change-password/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ old_password, new_password, confirm_password })
    });

    const data = await res.json();

    if (res.ok) {
      msg.innerText = data.message;
      msg.className = "message";
      // Có thể tự động đăng xuất sau khi đổi mật khẩu
      setTimeout(() => {
        localStorage.removeItem("token");
        window.location.href = "../index.html";
      }, 2000);
    } else {
      msg.innerText = data.error || "Có lỗi xảy ra";
      msg.className = "error";
    }
  } catch (error) {
    msg.innerText = "Không thể kết nối đến server";
    msg.className = "error";
  }
}
