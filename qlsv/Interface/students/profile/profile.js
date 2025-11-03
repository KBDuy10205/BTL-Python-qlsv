//Cố định nội dung bên phải
    function loadPage(page) {
      console.log("Đang load:", page);
      fetch(page)
        .then(res => {
          if (!res.ok) throw new Error("Không tìm thấy " + page);
          return res.text();
        })
        .then(html => {
          const main=document.getElementById("main-content");
          main.innerHTML = html;

          // >>> Thêm đoạn này <<<
          // Kích hoạt lại tất cả <script> trong trang vừa load
          const scripts = main.querySelectorAll("script");
          scripts.forEach(oldScript => {
            const newScript = document.createElement("script");
            if (oldScript.src) {
              newScript.src = oldScript.src;
            } else {
              newScript.textContent = oldScript.textContent;
            }
            document.body.appendChild(newScript);
          });
          // <<< Hết đoạn thêm >>>
        })
        .catch(err => {
          console.error(err);
          document.getElementById("main-content").innerHTML =
            "<p style='color:red'>Lỗi khi tải nội dung: " + err.message + "</p>";
        });
    }


    async function loadProfile() {
      const token = localStorage.getItem("access_token");
      //Chưa đăng nhập
      if(!token){
        alert("Chưa đăng nhập đâu, đăng nhập đi!");
        window.location.href = "../../index.html";
        return;
      }

      try{
        const student_id = localStorage.getItem("student_id");
        const res = await fetch(`http://localhost:8000/api/students/${student_id}`,{
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        if(!res.ok) throw new Error("Không lấy được dữ liệu");
        const data = await res.json();

        //Hiển thị dữ liệu
        document.getElementById("studentID").innerText = data.student_id;
        document.getElementById("name").innerText = data.full_name;
        document.getElementById("birthday").innerText = data.birth_date;
        document.getElementById("gender").innerText = data.gender;
        document.getElementById("email").innerText = data.email;
        document.getElementById("province").innerText = data.address;

        document.getElementById("tk").innerText = data.email;
        document.getElementById("name1").innerText = data.full_name;

        //...        
      }
      catch(err){
        console.error(err);
        alert("Lỗi kết nối hoặc không lấy được dữ liệu!");
        //window.location.href = "../index.html";
      }
    }

    function logout(){
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user_role");
      localStorage.removeItem("student_id");
      window.location.href = "../../index.html";
    }

    
    //Khi vào trang thì load profile luôn
    window.onload = loadProfile;