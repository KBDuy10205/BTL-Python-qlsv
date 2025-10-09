// Hàm render bảng điểm
function renderScores(data) {
    const tbody = document.querySelector("#scoreTable tbody");
    tbody.innerHTML = ""; // reset
    data.forEach((item, idx) => {
      let tr = `
        <tr>
          <td>${idx + 1}</td>
          <td>${item.maMH}</td>
          <td>${item.tenMH}</td>
          <td>${item.soTinChi}</td>
          <td>${item.diemThi ?? '-'}</td>
          <td>${item.ketQua ?? '-'}</td>
        </tr>`;
      tbody.innerHTML += tr;
    });
}

    // Giả sử token được lưu trong localStorage sau khi login
    const token = localStorage.getItem("token");

    if (!token) {
      //alert("Bạn chưa đăng nhập!");
      //window.location.href = "../index.html"; // chuyển hướng về login
    } else {
      document.getElementById("username").textContent = localStorage.getItem("username");

      // Gọi API backend để lấy dữ liệu điểm
      fetch("http://localhost:3000/api/diem", {
        headers: { "Authorization": "Bearer " + token }
      })
      .then(res => res.json())
      .then(data => renderScores(data))
      .catch(err => console.error("Lỗi:", err));
    }

    function logout() {
      localStorage.clear();
      window.location.href = "../index.html";
    }