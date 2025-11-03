document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("changePasswordForm");
  if (!form) {
    console.error("Không tìm thấy form có id='changePasswordForm'");
    return;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const old_password = document.getElementById("old_password").value;
    const new_password = document.getElementById("new_password").value;
    const confirm_password = document.getElementById("confirm_password").value;
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
      alert("Vui lòng đăng nhập lại!");
      window.location.href = "../../index.html";
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/account/change-password/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          old_password,
          new_password,
          confirm_password
        })
      });

      const data = await res.json();

      if (res.ok) {
        alert("Đổi mật khẩu thành công!");
        window.location.href = "../../index.html";
      } else {
        alert(data.detail || "Đổi mật khẩu thất bại!");
      }
    } catch (error) {
      console.error("Lỗi:", error);
      alert("Đã xảy ra lỗi. Vui lòng thử lại!");
    }
  });
});
