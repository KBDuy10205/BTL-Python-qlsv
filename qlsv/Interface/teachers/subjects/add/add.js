document.getElementById("addCourseForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const message = document.getElementById("message");
      message.textContent = "";

      const data = {
        CourseID: document.getElementById("course_code").value.trim(),
        CourseName: document.getElementById("course_name").value.trim(),
        Credit: document.getElementById("credits").value,
        //semester: document.getElementById("semester").value,
        //department: document.getElementById("department").value.trim(),
      };

      try {
        const res = await fetch("http://localhost:8000/api/courses/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access_token"), // nếu bạn dùng JWT
          },
          body: JSON.stringify(data),
        });

        if (res.ok) {
          message.textContent = "✅ Thêm môn học thành công!";
          message.className = "success";
          e.target.reset();
        } else {
          const err = await res.json();
          message.textContent = "❌ Lỗi: " + (err.detail || JSON.stringify(err));
          message.className = "error";
        }
      } catch (error) {
        message.textContent = "❌ Không thể kết nối tới server!";
        message.className = "error";
      }
    });

function goBack() {
  window.location.href = "../subjects.html";
}