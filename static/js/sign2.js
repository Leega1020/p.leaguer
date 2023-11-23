let isLogging=false

$('#lineLoginBtn').on('click', function(e) {
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
            console.log(data);  // 确保数据被正确获取
            if (data) {
                console.log(data.token);
                isLogging = true;
                localStorage.setItem("token", data.token);
                localStorage.setItem("userId", data.userId);
            }
        })
        .catch(error => {
            console.error("API请求错误", error);
        });
    
    
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