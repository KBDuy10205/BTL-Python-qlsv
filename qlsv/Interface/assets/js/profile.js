//Cố định nội dung bên phải
    function loadPage(page) {
      console.log("Đang load:", page);
      fetch(page)
        .then(res => {
          if (!res.ok) throw new Error("Không tìm thấy " + page);
          return res.text();
        })
        .then(html => {
          document.getElementById("main-content").innerHTML = html;
        })
        .catch(err => {
          console.error(err);
          document.getElementById("main-content").innerHTML =
            "<p style='color:red'>Lỗi khi tải nội dung: " + err.message + "</p>";
        });
    }

    function Homepage(){
      window.location.href = "profile.html";
    }

    function tb(){
      window.location.href = "tb.html";
    }

    function grade(){
      window.location.href = "grades.html";
    }

    function schedule(){
      window.location.href = "schedule.html";
    }

    async function loadProfile() {
      const token = localStorage.getItem("token");
      //Chưa đăng nhập
      if(!token){
        //alert("Chưa đăng nhập đâu, đăng nhập đi!");
        //window.location.href = "../index.html";
        return;
      }

      try{
        const res = await fetch("http://localhost:8000/api/students/{id}/",{
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        if(!res.ok) throw new Error("Không lấy được dữ liệu");
        const data = await res.json();

        //Hiển thị dữ liệu
        document.getElementById("studentID").innerText = data.StudentID;
        document.getElementById("name").innerText = data.FullName;
        document.getElementById("birthday").innerText = data.BirthDate;
        document.getElementById("gender").innerText = data.Gender;
        document.getElementById("email").innerText = data.Email;
        document.getElementById("province").innerText = data.Address;

        //...        
      }
      catch(err){
        console.error(err);
        alert("Phiên đăng nhập hết hạn, vui lòng đăng nhập lại!");
        window.location.href = "../index.html";
      }
    }

    function logout(){
      localStorage.removeItem("token");
      window.location.href = "../index.html";
    }

    //Khi vào trang thì load profile luôn
    window.onload = loadProfile;