let isLogging = false;

    let signupContainer = document.querySelector(".signupContainer");
    let signinContainer = document.querySelector(".signinContainer");

    $('.signBtn').on('click', function(e) {
        let client_id = '2001585939';
        let redirect_uri = 'http://127.0.0.1:5000/get/signin';
        let link = 'https://access.line.me/oauth2/v2.1/authorize?';
        link += 'response_type=code';
        link += '&client_id=' + client_id;
        link += '&redirect_uri=' + redirect_uri;
        link += '&state=login';
        link += '&scope=openid%20profile';
        URL += '&scope=openid%20profile%20email';
        window.location.href = link;

        
    });

    document.addEventListener("DOMContentLoaded", function () {    
        
        let userId=localStorage.getItem("userId")
        let nickname = localStorage.getItem('nickname');
        let welcomePic=document.querySelector("#welcomePic")
        let welcomeName=document.querySelector("#welcomeNickname")
        
        if(userId===null||userId==="undefined"){
        welcomePic.src=""
        let a=document.createElement("a")
        a.href="/signin"
        let linkText = document.createTextNode("Sign in");
        a.appendChild(linkText);
        welcomeName.appendChild(a)
        }else{
            welcomeName.textContent=nickname
        }
        fetch("/aa/signin", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => { 
            if (data) {
                
                isLogging = true;
                localStorage.setItem("userId", data.userId);
                localStorage.setItem("nickname", data.nickname);
                
                localStorage.setItem("teamresult",data.team)
                
                let uu=localStorage.getItem("userId")
                console.log(uu)
                if (uu==="undefined"){
                    uu=null
                    console.log(uu)
                    if (uu != null&& data.nickname != null) {
                        window.location.href = "/member";
                    } else if (uu != null&& data.nickname == null) {
                        //console.log(userId)
                        //console.log(data.nickname)
                        signinContainer.style.display = "none";
                        signupContainer.style.display = "flex";
                    } else if (uu == null && data.nickname == null) {
                        // 未登录
                        signinContainer.style.display = "flex";
                        signupContainer.style.display = "none";
                    }
                }else{
                    if (uu != null&& data.nickname != null) {
                        window.location.href = "/member";
                    } else if (uu != null&& data.nickname == null) {
                        //console.log(userId)
                        //console.log(data.nickname)
                        signinContainer.style.display = "none";
                        signupContainer.style.display = "flex";
                    } else if (uu == null && data.nickname == null) {
                        // 未登录
                        signinContainer.style.display = "flex";
                        signupContainer.style.display = "none";
                    }
                }
                
                
            }
        })
        .catch(error => {
            console.error("API请求错误", error);
        });
    
        let signupBtn = document.querySelector(".signupBtn");
        signupBtn.addEventListener("click", (e) => {
            e.preventDefault();
            let signUpNameInput = document.querySelector("#signUpName");
            let signUpTeamInput = document.querySelector("#signUpTeam");
            let userId=localStorage.getItem("userId")
            let signUpName = document.querySelector("#signUpName").value;
            let signUpTeam = document.querySelector("#signUpTeam").value;
            console.log(signUpTeam)
            fetch("/api/signInfo", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "userId": userId
                },
                body: JSON.stringify({
                    "signUpName": signUpName,
                    "signUpTeam": signUpTeam,
                }),
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                signUpNameInput.value = "";
                signUpTeamInput.value = "";
                signUpTeamInput.value = "全部隊伍"; 
                console.log("insertinfo ok")
                location.reload();
            });
        });
    
        const lineOutBtn = document.querySelector("#lineOutBtn");
        lineOutBtn.addEventListener("click", () => {
            let userId = localStorage.getItem("userId");
            fetch("/api/signout", {
                method: "POST",
                headers: {
                    "userId": userId,
                },
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (data) {
                    isLogging = false;
                    localStorage.removeItem("userId");
                }
            });
        });

        let signupLink=document.getElementById("signupLink")
        signupLink.addEventListener("click",()=>{
            signupContainer.style.display="flex"
            signinContainer.style.display="none"
        });
        let toSignin=document.querySelector(".toSignin")
        toSignin.addEventListener("click",function(){
            signupContainer.style.display="none"
            signinContainer.style.display="flex"
        })
    });
    