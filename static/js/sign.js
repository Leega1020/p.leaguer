let isLogging=false

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
    window.location.href = link;})

   
    


document.addEventListener("DOMContentLoaded", function () {    
    let userId = localStorage.getItem("userId");
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
            //console.log(data.nickname)
            if (data) {
                console.log(data.token);
                isLogging = true;
                localStorage.setItem("token", data.token);
                localStorage.setItem("userId", data.userId);
               
                toSignin.insertAdjacentElement("beforebegin",signupMessage)
                //window.location.href="/member"
                console.log(data.nickname)
                console.log(userId)
                if(userId!=null&&data.nickname!=null){
                    //window.location.href="/member"
                    
                    
                }else if(userId!=null&&data.nickname==null){
                    signinContainer.style.display="none"
                    signupContainer.style.display="flex"
                }else if(userId==null&&data.nickname==null){
                    signinContainer.style.display="flex"
                    signupContainer.style.display="none"
                }
            }
        })
        .catch(error => {
            console.error("API请求错误", error);
        });
    

  



        let signupForm=document.querySelector("#signupForm")
        let signupMessage=document.createElement("div")
        signupMessage.classList.add("signup-message")

        signupForm.addEventListener("submit",function(e){
            e.preventDefault()
            let signUpName=document.querySelector("#signUpName").value
            let signUpTeam=document.querySelector("#signUpTeam").value

            if (!signUpName || !signUpTeam) {
                signupMessage.textContent="欄位請完整填寫";
                signupMessage.style.color="red";
                toSignin.insertAdjacentElement("beforebegin",signupMessage);
                return
            }})


            let signinUpButton=document.getElementById("signin_up")
            let close_in=document.querySelector(".close_in")
            let close_up=document.querySelector(".close_up")
            let signupLink=document.getElementById("signupLink")
            signupLink.addEventListener("click",()=>{
                signupContainer.style.display="block"
                signinContainer.style.display="none"
            });
            let toSignin=document.querySelector(".toSignin")
            toSignin.addEventListener("click",function(){
                signupContainer.style.display="none"
                signinContainer.style.display="block"
            })

            let signupBtn=document.querySelector(".signupBtn")
            let signUpName=document.querySelector("#signUpName").value
            let signUpTeam=document.querySelector("#signUpTeam").value
            signupBtn.addEventListener("click",(e)=>{
                e.preventDefault()
                fetch("/api/signout", {
                    method: "POST",
                    headers: {
                    "Content-Type": "application/json",
                    "userId":userId
                    },
                    body: JSON.stringify({
                        "tesignUpNameam": signUpName,
                        "signUpTeam": signUpTeam,
                        
                    }),
            
                    })
                    .then(response => {
                    return response.json()
                    })
                    .then(data=>{
                        if(data){
                            isLogging=false
                            localStorage.removeItem("token")
                            localStorage.removeItem("userId")
                        }
                    })
                   
                    });

                    let token=localStorage.getItem("token")
const lineOutBtn=document.querySelector("#lineOutBtn")
lineOutBtn.addEventListener("click", () => {

        fetch("/api/signout", {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        "Authorization":`Bearer ${token}`
        },

        })
        .then(response => {
        return response.json()
        })
        .then(data=>{
            if(data){
                isLogging=false
                localStorage.removeItem("token")
                localStorage.removeItem("userId")
            }
        })
       
        });
                    
                    
            })

       