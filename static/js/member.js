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
document.addEventListener("DOMContentLoaded", function () {
    let lastSignTime;
    let currentDayIndex;

    perdaypics = document.querySelectorAll(".picul li");

    getCheckSign();

    perdaypics.forEach((element, index) => {
        element.addEventListener("click", () => {
            let currentday = "day" + (index + 1);

            // 檢查是否已簽到
            if (element.style.opacity === "1") {
                console.log("Already signed today!");
                return;
            }

            // 檢查是否過了24小時
            if (!is24HoursPassed(index)) {
                console.log("Cannot sign in. Please wait for 24 hours.");
                return;
            }

            // 發送簽到請求
            signDay(currentday, index);
        });
    });

    function signDay(currentday, index) {
        let userId = localStorage.getItem("userId");
        fetch("/api/signday", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "userId": userId,
            },
            body: JSON.stringify({
                "check": currentday,
            }),
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data);
                if (data.data === "Sign-in successful!") {
                    // 更新上次簽到的時間
                    lastSignTime = new Date();
                    // 更新當前點擊的按鈕索引
                    currentDayIndex = index;
                    // 簽到成功，禁用其他簽到按鈕
                    disableOtherButtons();
                }
            });
    }

    function is24HoursPassed(index) {
        // 如果上次簽到的時間為空，或者距離現在超過24小時，返回 true
        return !lastSignTime || (new Date() - lastSignTime) >= 24 * 60 * 60 * 1000;
    }

    function disableOtherButtons() {
        // 在這裡實現禁用其他簽到按鈕的邏輯
        // 例如，遍歷 perdaypics，禁用除了當前天數以外的其他天數的簽到按鈕
        perdaypics.forEach((perdaypic, i) => {
            if (i !== currentDayIndex) {
                perdaypic.style.pointerEvents = "none"; // 禁用點擊事件
                perdaypic.style.opacity = 0.3; // 設置透明度為 30%
            }
        });
    }



    function getCheckSign(){
        let userId=localStorage.getItem("userId")
        fetch("/api/signday", {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            "userId":userId
            }, })
            .then(response => {
            return response.json()
            })
            .then(data=>{
                if (data) {
                    let currentCount=data.currentCount
                    const picul = document.querySelector(".picul");
                    const perdaypics = picul.querySelectorAll("li");
        
                    for (let i = 0; i < currentCount; i++) {
                        perdaypics[i].style.opacity = 100;
                    }
                }
            })
    }

    function changeBadge(returnedNumber){
        const perdaypics = document.querySelectorAll(".perdaypic");
        const headpicimg = document.getElementById("headpicimg");
    
        perdaypics.forEach((perdaypic, index) => {
            perdaypic.addEventListener("click", () => {
                // 取得點選 perdaypic 的圖片路徑
                const clickedImagePath = perdaypic.querySelector("img").src;
    
                // 更換 headpicimg 的圖片
                headpicimg.src = clickedImagePath;
    
                // 取得回傳的數字
               // const returnedNumber = /* 這裡填入從後端回傳的數字 */;
    
                // 根據回傳的數字設置透明度
                setOpacity(returnedNumber);
            });
        });
    
        // 根據回傳的數字設置透明度
        function setOpacity(returnedNumber) {
            perdaypics.forEach((perdaypic, index) => {
                // 根據回傳的數字進行條件處理
                if (returnedNumber === 1 && index === 0) {
                    perdaypic.style.opacity = 1; // 這裡是 100%
                } else if (returnedNumber === 4 && index === 1) {
                    perdaypic.style.opacity = 1;
                } else if (returnedNumber === 7 && index === 2) {
                    perdaypic.style.opacity = 1;
                } else {
                    perdaypic.style.opacity = 0.3; // 這裡是 30%
                }
            });
        }
        }
})