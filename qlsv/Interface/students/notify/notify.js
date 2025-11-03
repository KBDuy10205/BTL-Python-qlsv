async function loadThongBao() {
  const token = localStorage.getItem("token");
  const tbody = document.getElementById("tbody");
  tbody.innerHTML = "<tr><td colspan='4'>Đang tải...</td></tr>";

  try {
    const res = await fetch("http://127.0.0.1:8000/api/thongbao/", {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    if (!res.ok) {
      tbody.innerHTML = "<tr><td colspan='4'>Không thể tải dữ liệu.</td></tr>";
      return;
    }

    const data = await res.json();
    tbody.innerHTML = "";

    if (data.length === 0) {
      tbody.innerHTML = "<tr><td colspan='4'>Không có thông báo nào.</td></tr>";
      return;
    }

    data.forEach((tb, index) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${index + 1}</td>
        <td>${tb.tieu_de}</td>
        <td>${new Date(tb.ngay_gui).toLocaleString("vi-VN")}</td>
        <td><span class="icon" onclick="xemChiTiet(${tb.id})">💬</span></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    tbody.innerHTML = "<tr><td colspan='4'>Lỗi kết nối đến server.</td></tr>";
  }
}

function xemChiTiet(id) {
  // Chuyển hướng đến trang chi tiết hoặc hiển thị popup
  window.location.href = `thongbao_chitiet.html?id=${id}`;
}

loadThongBao();
