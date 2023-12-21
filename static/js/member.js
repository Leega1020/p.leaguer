      
            const lineOutBtn=document.querySelector("#lineOutBtn")
            lineOutBtn.addEventListener("click", () => {
                    let userId=localStorage.getItem("userId")
                    fetch("/api/signout", {
                    method: "POST",
                    headers: {
                    "userId": userId,
                    },

                    })
                    .then(response => {
                    return response.json()
                    })
                    .then(data=>{
                        if(data){
                            isLogging=false
                            localStorage.removeItem("userId")
                            localStorage.removeItem("currentCount")
                            localStorage.removeItem("nickname")
                            localStorage.removeItem("teamresult")
                            localStorage.removeItem("btnswitch")
                            localStorage.removeItem("hasReloaded")
                            
                            location.reload()
                        }
                    })
                
                    });

    document.addEventListener("DOMContentLoaded", function () {
        let hasReloaded = localStorage.getItem("hasReloaded");

        if (!hasReloaded) {
            // 设置标志位，表示已经执行过重新加载
            localStorage.setItem("hasReloaded", "true");

            // 一秒后执行重新加载
            setTimeout(function () {
                location.reload();
            }, 3000);
        }
            console.log("ffff!")

            getCheckSign();
            handleTeamType()
        let userId=localStorage.getItem("userId")
        let nicknames=localStorage.getItem("nickname")
        if(nicknames===null||nicknames==="undefined"){
            window.location.href="/"
        }
        
            let isClickEnabled
            handleWelcomePic()
            console.log(isClickEnabled)
            let lastSignTime;
            let currentDayIndex;
            let nickname = localStorage.getItem('nickname');

        
            let username=document.querySelector("#username")
            
            username.textContent=nickname

        function getCheckSign() {
            let userId = localStorage.getItem("userId");
            
            fetch("/api/signday", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "userId": userId
                },
                })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    if (data) {
                        console.log(data)
                        let currentCount = data.count;
                        localStorage.setItem("currentCount",currentCount)
                        const picul = document.querySelector(".picul");
                        const perdaypics = picul.querySelectorAll("li");
                        let lastTime=data.lastTime
                        
                        if(lastTime==="timenotok"){
                        localStorage.setItem("btnswitch","off")
                        }else{
                            localStorage.setItem("btnswitch","on")
                        }
                        
                        //console.log(currentCount)
                        
                        console.log()
                        for (let i = 0; i < currentCount; i++) {
                            perdaypics[i].style.opacity = 1;
                        if(currentCount>6){
                            perdaypics[6].style.opacity = 1;
                        }
                        }
                        headpic(currentCount)
                    }
                });
            }



        let btnswitch = localStorage.getItem("btnswitch");
        let perdaypics = document.querySelectorAll(".picul li");
        let currentOpenIndex = 0;
        let currentCount=parseInt(localStorage.getItem("currentCount"))
        console.log(btnswitch);
        console.log(currentCount);
        if (btnswitch === "on") {
            let isClickEnabled = true;
            
            perdaypics.forEach((element, index) => {
                element.style.opacity = "0.3";
                if (index === currentCount) {
                    console.log(currentCount);
                element.addEventListener("click", () => {
                    currentCount++
                    console.log(currentOpenIndex)
                    let currentday = "day" + (index + 1);
                    let currentDate = new Date();
                    let userId = localStorage.getItem("userId");

                        fetch("/api/signday", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "userId": userId,
                            },
                            body: JSON.stringify({
                                "check": currentday,
                                "lastTime": currentDate,
                            }),
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);

                            if (data) {
                                isClickEnabled = false;
                                let first = data.first;

                                if (first === "yes1") {
                                    localStorage.setItem("btnswitch", "on");
                                }

                                getCheckSign();
                                disableOtherButtons();
                            }
                        })
                        .catch(error => {
                            console.error("Error during sign-in:", error);
                      
                        });

                    
                    
                })}
            });

            function disableOtherButtons() {
                perdaypics.forEach((perdaypic, i) => {
                    if (i !== currentOpenIndex) {
                        perdaypic.style.pointerEvents = "none"; 
                        perdaypic.style.opacity = 0.3; 
                    }
                });
            }
        }
        function headpic(currentCount) {
            let perdayContainers = document.querySelectorAll(".perdaypic");

            perdayContainers.forEach((perdayContainer, index) => {
                perdayContainer.style.opacity = "0.3";
                perdayContainer.style.pointerEvents = "none";
                perdayContainer.removeEventListener("click", null);

                if (currentCount >=1 && currentCount < 4) {
                    perdayContainers[0].style.opacity = "1";
                    perdayContainers[0].style.pointerEvents = "auto"; 
                    perdayContainers[0].addEventListener("click", (e) => {
                        let perdaypics = e.currentTarget.querySelector("img");
                        let headpicimg = document.querySelector("#headpicimg");
                        headpicimg.src = perdaypics.src;
                    });
                } else if (currentCount >= 4 && currentCount < 7) {
                    perdayContainers[0].style.opacity = "1";
                    perdayContainers[1].style.opacity = "1";
                    perdayContainer.style.pointerEvents = "auto";
                    perdayContainer.addEventListener("click", (e) => {
                        let perdaypics = e.currentTarget.querySelector("img");
                        let headpicimg = document.querySelector("#headpicimg");
                        headpicimg.src = perdaypics.src;
                    });
                } else if (currentCount >= 7) {
                    perdayContainers[0].style.opacity = "1";
                    perdayContainers[1].style.opacity = "1";
                    perdayContainers[2].style.opacity = "1";
                    perdayContainer.style.pointerEvents = "auto"; 
                    perdayContainer.addEventListener("click", (e) => {
                        let perdaypics = e.currentTarget.querySelector("img");
                        let headpicimg = document.querySelector("#headpicimg");
                        headpicimg.src = perdaypics.src;
                    });
                }disableOtherButtons2()
                
            });
            function disableOtherButtons2() {
                perdayContainers.forEach((a) => {
                    if (a.style.opacity === "0.3") {
                        a.style.pointerEvents = "none"; 
                    }
                });}
        }
            
            function handleTeamType(){
                let teamresult=localStorage.getItem("teamresult")
                let headpicimg=document.querySelector("#headpicimg")
                let dt1=document.querySelector("#dt1")
                let dt2=document.querySelector("#dt2")
                let dt3=document.querySelector("#dt3")
                if(teamresult==="臺北富邦勇士"){
                    headpicimg.src="/static/images/taipei.png"
                    dt1.src="/static/images/badges/f1.png"
                    dt2.src="/static/images/badges/f2.png"
                    dt3.src="/static/images/badges/f3.png"
                }else if(teamresult==="新北國王"){
                    headpicimg.src="/static/images/king.png"
                    dt1.src="/static/images/badges/i1.png"
                    dt2.src="/static/images/badges/i2.png"
                    dt3.src="/static/images/badges/i3.png"
                }else if(teamresult==="新竹街口攻城獅"){
                    headpicimg.src="/static/images/lion.png"
                    dt1.src="/static/images/badges/l1.png"
                    dt2.src="/static/images/badges/l2.png"
                    dt3.src="/static/images/badges/l4.png"
                }else if(teamresult==="福爾摩沙台新夢想家"){
                    headpicimg.src="/static/images/taihsin.png"
                    dt1.src="/static/images/badges/d1.png"
                    dt2.src="/static/images/badges/d2.png"
                    dt3.src="/static/images/badges/d3.png"
                }else if(teamresult==="桃園領航猿"){
                    headpicimg.src="/static/images/taoyuan_logo.png"
                    dt1.src="/static/images/badges/p1.png"
                    dt2.src="/static/images/badges/p2.png"
                    dt3.src="/static/images/badges/p3.png"
                }else if(teamresult==="高雄17直播鋼鐵人"){
                    headpicimg.src="/static/images/kauo.png"
                    dt1.src="/static/images/badges/k1.png"
                    dt2.src="/static/images/badges/k2.png"
                    dt3.src="/static/images/badges/k3.png"
                }
            }

            let ts=document.querySelector("#ts")
            ts.addEventListener("change",()=>{
                let tsValue=ts.value
                console.log(tsValue)
                let userId=localStorage.getItem("userId")
                fetch("/api/updateTeam", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "userId": userId
                    },
                    body: JSON.stringify({
                        "changeTeam": tsValue,
                    
                    }),
                })
                .then(response => {
                    return response.json();
                }).then(data => {
                let changeTeam=data.changeTeam
                localStorage.setItem("teamresult",changeTeam)
                handleTeamType()
                ts.value="CHANGE TEAM"
                handleWelcomePic()
            })})

            let helpbtn=this.documentElement.querySelector("#helpbtn")
            let dialogue=document.querySelector(".dialogue")
            helpbtn.addEventListener("click",()=>{
                dialogue.style.display="block"
                if(dialogue.style.display="block"){
                    setTimeout(() => {
                        dialogue.style.display="none"
                    }, 5000);
                }
            })

        


})