async function loadCTDT() {
  const response = await fetch('http://127.0.0.1:8000/api/ctdt/');
  const data = await response.json();

  const tbody = document.getElementById("tableBody");
  tbody.innerHTML = "";

  data.forEach((row, index) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${row.ma_mh}</td>
      <td>${row.ten_mh}</td>
      <td>${row.chuyen_nganh || ""}</td>
      <td>${row.so_tin_chi}</td>
      <td>${row.mon_bat_buoc ? "x" : ""}</td>
      <td>${row.da_hoc ? "x" : ""}</td>
      <td>${row.tong_tiet}</td>
      <td>${row.ly_thuyet}</td>
      <td>${row.thuc_hanh}</td>
      <td>${row.tiet_thanh_phan}</td>
    `;
    tbody.appendChild(tr);
  });
}

document.addEventListener("DOMContentLoaded", loadCTDT);
