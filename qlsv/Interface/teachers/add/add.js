const API_URL = "http://localhost:8000/api/students/";

    document.getElementById("formAdd").addEventListener("submit", async (e) => {
      e.preventDefault();

      // Lấy dữ liệu form
      const formData = new FormData(e.target);
      const data = Object.fromEntries(formData.entries());

      try {
        const res = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });

        if (res.ok) {
          alert("✅ Thêm sinh viên thành công!");
          window.location.href = "index.html";
        } else {
          const err = await res.json();
          alert("❌ Lỗi khi thêm sinh viên: " + JSON.stringify(err));
        }
      } catch (error) {
        alert("⚠️ Không thể kết nối đến server!");
        console.error(error);
      }
    });