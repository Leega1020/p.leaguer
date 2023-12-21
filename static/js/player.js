document.addEventListener("DOMContentLoaded", function () {
    
    console.log(userId)
    const selected = document.querySelector("#open");
    const typeNameInput = document.querySelector("#searchBox");
    const searchBtn = document.querySelector("#searchBtn");
    const selected2 = document.querySelector("#open2");

    let all=document.getElementById("all")
    all.addEventListener("click",()=>{
       resetState()
    })

    selected.addEventListener("change", function () {
        choosed_team = selected.value;
        typeName = typeNameInput.value; 
    });

    searchBtn.addEventListener("click", (e) => {
        e.preventDefault();
        choosed_team = "全部隊伍";
        typeName = typeNameInput.value; 
        
        getTeam();
        typeNameInput.value=""
    });
    let teamresult=localStorage.getItem("teamresult")
    if(teamresult==="臺北富邦勇士"){
        choosed_team = "臺北富邦勇士";
    }else if(teamresult==="新北國王"){
        choosed_team = "新北國王";
    }else if(teamresult==="新竹街口攻城獅"){
        choosed_team = "新竹街口攻城獅";
    }else if(teamresult==="福爾摩沙台新夢想家"){
        choosed_team = "福爾摩沙台新夢想家";
     }else if(teamresult==="桃園領航猿"){
        choosed_team = "桃園領航猿";
    }else if(teamresult==="高雄17直播鋼鐵人"){
        choosed_team = "高雄17直播鋼鐵人";
    }else{
        choosed_team = selected.value;
    }
    
    typeName = typeNameInput.value;
    console.log(choosed_team);
    getTeam();

    function getTeam() {
        let userId=localStorage.getItem("userId")
        fetch("/api/player", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "userId":userId
            },
            body: JSON.stringify({
                "team": choosed_team,
                "typeName": typeName,
                
            }),
        })
            .then((response) => {
                console.log("ok");
                return response.json();
            })
            .then((responseData) => {
                data = responseData; 
                renderData(); 
            });
    }

    selected2.addEventListener("change", function () {
        const choosed_player = selected2.value;
        const filteredData = data.filter((player) => player.playerName === choosed_player);

        if (filteredData.length > 0) {
            const player = filteredData[0];
            console.log(player)
            renderPlayer(player);
        }
    });

    function renderData() {
        const tbody = document.getElementById("mytbody");
        const selectElement = document.getElementById("open2");
        selectElement.innerHTML = "";
        if (data) {
            tbody.innerHTML = "";
            const emptySelsct = document.createElement("option");
            emptySelsct.value = "";
            emptySelsct.textContent = "選擇球員";
            selectElement.appendChild(emptySelsct);

            data.forEach((element) => {
                const option = document.createElement("option");
                option.value = element.playerName;
                option.textContent = element.playerName;
                selectElement.appendChild(option);

                const list_tltle = document.createElement("tr");
                list_tltle.classList.add("list_tltle2");

                const imgth = document.createElement("th");
                    const img = document.createElement("img");
                    img.src = element.imagePath;
                    img.classList.add("myimg");
                    imgth.appendChild(img);
                    
                    const perth1 = document.createElement("th");
                    const perth2 = document.createElement("th");
                    const perth3 = document.createElement("th");
                    const perth4 = document.createElement("th");
                    const perth5 = document.createElement("th");
                    const perth6 = document.createElement("th");
                    const perth7 = document.createElement("th");
                    const perth8 = document.createElement("th");
                    const perth9 = document.createElement("th");
                    const perth10 = document.createElement("th");
                    const perth11 = document.createElement("th");
                    const perth12 = document.createElement("th");
                    const perth13 = document.createElement("th");
                    const perth14 = document.createElement("th");
    
                    perth1.textContent = element.backNumber;
                    perth2.textContent = element.playerName;
                    perth3.textContent = element.p_team;
                    perth4.textContent = element.p_counts;
                    perth5.textContent = element.p_time;
                    perth6.textContent = element.point2;
                    perth7.textContent = element.point3;
                    perth8.textContent = element.p_foulShots;
                    perth9.textContent = element.p_scores;
                    perth10.textContent = element.p_backboards;
                    perth11.textContent = element.p_assists;
                    perth12.textContent = element.p_intercept;
                    perth13.textContent = element.p_miss;
                    perth14.textContent = element.p_foul;
                    
                    perth1.style.fontFamily = "Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif";
    
                    if(perth3.textContent==="臺北富邦勇士"){
                        perth1.style.color="#005378"
                    }else if (perth3.textContent === "新北國王") {
                        perth1.style.color="#d3bd00"
                    }else if (perth3.textContent === "新竹街口攻城獅") {
                        perth1.style.color="#51308e"
                    }else if (perth3.textContent === "福爾摩沙台新夢想家"){
                        perth1.style.color="#52740e"
                    }else if (perth3.textContent === "桃園領航猿") {
                        perth1.style.color="#ea5504"
                    }else{perth1.style.color="#7d0004"}
    
                    list_tltle.appendChild(imgth);
                    list_tltle.appendChild(perth1);
                    list_tltle.appendChild(perth2);
                    list_tltle.appendChild(perth3);
                    list_tltle.appendChild(perth4);
                    list_tltle.appendChild(perth5);
                    list_tltle.appendChild(perth6);
                    list_tltle.appendChild(perth7);
                    list_tltle.appendChild(perth8);
                    list_tltle.appendChild(perth9);
                    list_tltle.appendChild(perth10);
                    list_tltle.appendChild(perth11);
                    list_tltle.appendChild(perth12);
                    list_tltle.appendChild(perth13);
                    list_tltle.appendChild(perth14);


                tbody.appendChild(list_tltle);
                
                imgth.addEventListener("click", (event) => {
                    if(userId===null|| userId === "undefined"){
                        alert("登入先")
                    }else{
                        event.target.src = "/static/images/star.png";
                    let playerData = getPlayerData(event.target.closest('tr'));
                    console.log(playerData);
                    addToFavorites(playerData);
                    isStarClicked = true;
                    }
                    
                });
                
            });
        }
    }

    function renderPlayer(player) {
        const tbody = document.getElementById("mytbody");
        tbody.innerHTML = ""; 
    
        const list_tltle = document.createElement("tr");
        list_tltle.classList.add("list_tltle2");
    
        const imgth = document.createElement("th");
        const img = document.createElement("img");
        img.src = player.imagePath;
        img.classList.add("myimg");
        imgth.appendChild(img);
    
        const perth1 = document.createElement("th");
        const perth2 = document.createElement("th");
        const perth3 = document.createElement("th");
        const perth4 = document.createElement("th");
        const perth5 = document.createElement("th");
        const perth6 = document.createElement("th");
        const perth7 = document.createElement("th");
        const perth8 = document.createElement("th");
        const perth9 = document.createElement("th");
        const perth10 = document.createElement("th");
        const perth11 = document.createElement("th");
        const perth12 = document.createElement("th");
        const perth13 = document.createElement("th");
        const perth14 = document.createElement("th");
    
        perth1.textContent = player.backNumber;
        perth2.textContent = player.playerName;
        perth3.textContent = player.p_team;
        perth4.textContent = player.p_counts;
        perth5.textContent = player.p_time;
        perth6.textContent = player.point2;
        perth7.textContent = player.point3;
        perth8.textContent = player.p_foulShots;
        perth9.textContent = player.p_scores;
        perth10.textContent = player.p_backboards;
        perth11.textContent = player.p_assists;
        perth12.textContent = player.p_intercept;
        perth13.textContent = player.p_miss;
        perth14.textContent = player.p_foul;
    
        perth1.style.fontFamily = "Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif";
    
        if (perth3.textContent === "臺北富邦勇士") {
            perth1.style.color = "#005378";
        } else if (perth3.textContent === "新北國王") {
            perth1.style.color = "#d3bd00";
        } else if (perth3.textContent === "新竹街口攻城獅") {
            perth1.style.color = "#51308e";
        } else if (perth3.textContent === "福爾摩沙台新夢想家") {
            perth1.style.color = "#52740e";
        } else if (perth3.textContent === "桃園領航猿") {
            perth1.style.color = "#ea5504";
        } else {
            perth1.style.color = "#7d0004";
        }
    
        list_tltle.appendChild(imgth);
        list_tltle.appendChild(perth1);
        list_tltle.appendChild(perth2);
        list_tltle.appendChild(perth3);
        list_tltle.appendChild(perth4);
        list_tltle.appendChild(perth5);
        list_tltle.appendChild(perth6);
        list_tltle.appendChild(perth7);
        list_tltle.appendChild(perth8);
        list_tltle.appendChild(perth9);
        list_tltle.appendChild(perth10);
        list_tltle.appendChild(perth11);
        list_tltle.appendChild(perth12);
        list_tltle.appendChild(perth13);
        list_tltle.appendChild(perth14);
    
        tbody.appendChild(list_tltle);
       
            imgth.addEventListener("click", (event) => {
            if(userId===null){
                alert("叫你登入")
            }else{
                event.target.src = "/static/images/star.png";
            let playerData = getPlayerData(event.target.closest('tr'));
            console.log(playerData);
            addToFavorites(playerData);
            isStarClicked = true;
            }
            
        }); 
    }
        function getPlayerData(row) {
                let playerData = {
                    name: row.querySelector('th:nth-child(3)').textContent,
                    
                };
                console.log(playerData)
                return playerData;
            }
        
        function addToFavorites(playerData) {
            let token=localStorage.getItem("token")
            let userId=localStorage.getItem("userId")
            console.log(token)
            fetch("/api/likePlayer",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "userId":userId
                },
                body:JSON.stringify(playerData),
                
            })
            .then(response=>{
                if (response.status === 200){
                    return response.json()
                } else{
                    throw new Error("")
                }
            })
            .then(data=>{
                console.log(data)
                if(data.userId===null){
                    alert("請先登入")
                }
                console.log("likePlayer_saved")
               
            })
            .catch(error => {
                console.error("API請求錯誤", error)
               
            });}
      
            const userLike = document.querySelector("#userLike");

            userLike.addEventListener("click", () => {
                let userId = localStorage.getItem("userId");
                if(userId===null||userId==="undefined"){
                    alert("請先登入")
                }else{like()}
                })
        function like(){
            let token = localStorage.getItem("token");
            let userId = localStorage.getItem("userId");

            fetch("/api/getLikePlayer", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "userId": userId
                }
            })
            .then(response => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    throw new Error("");
                }
            })
            .then(data => {
                let tbody = document.getElementById("mytbody");
                tbody.innerHTML = "";
                console.log(data);

                data.forEach(player => {
                    const list_tltle = document.createElement("tr");
                    list_tltle.classList.add("list_tltle2");

                    const imgth = document.createElement("th");
                    const img = document.createElement("img");
                    img.src = "/static/images/remove.png";
                    img.classList.add("myimg");
                    img.classList.add("deleteBtn");
                    imgth.appendChild(img);

                    const perth1 = document.createElement("th");
                    const perth2 = document.createElement("th");
                    const perth3 = document.createElement("th");
                    const perth4 = document.createElement("th");
                    const perth5 = document.createElement("th");
                    const perth6 = document.createElement("th");
                    const perth7 = document.createElement("th");
                    const perth8 = document.createElement("th");
                    const perth9 = document.createElement("th");
                    const perth10 = document.createElement("th");
                    const perth11 = document.createElement("th");
                    const perth12 = document.createElement("th");
                    const perth13 = document.createElement("th");
                    const perth14 = document.createElement("th");

                    perth1.textContent = player.backNumber;
                    perth2.textContent = player.playerName;
                    perth3.textContent = player.p_team;
                    perth4.textContent = player.p_counts;
                    perth5.textContent = player.p_time;
                    perth6.textContent = player.point2;
                    perth7.textContent = player.point3;
                    perth8.textContent = player.p_foulShots;
                    perth9.textContent = player.p_scores;
                    perth10.textContent = player.p_backboards;
                    perth11.textContent = player.p_assists;
                    perth12.textContent = player.p_intercept;
                    perth13.textContent = player.p_miss;
                    perth14.textContent = player.p_foul;

                    perth1.style.fontFamily = "Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif";

                    if (perth3.textContent === "臺北富邦勇士") {
                        perth1.style.color = "#005378";
                    } else if (perth3.textContent === "新北國王") {
                        perth1.style.color = "#d3bd00";
                    } else if (perth3.textContent === "新竹街口攻城獅") {
                        perth1.style.color = "#51308e";
                    } else if (perth3.textContent === "福爾摩沙台新夢想家") {
                        perth1.style.color = "#52740e";
                    } else if (perth3.textContent === "桃園領航猿") {
                        perth1.style.color = "#ea5504";
                    } else {
                        perth1.style.color = "#7d0004";
                    }

                    list_tltle.appendChild(imgth);
                    list_tltle.appendChild(perth1);
                    list_tltle.appendChild(perth2);
                    list_tltle.appendChild(perth3);
                    list_tltle.appendChild(perth4);
                    list_tltle.appendChild(perth5);
                    list_tltle.appendChild(perth6);
                    list_tltle.appendChild(perth7);
                    list_tltle.appendChild(perth8);
                    list_tltle.appendChild(perth9);
                    list_tltle.appendChild(perth10);
                    list_tltle.appendChild(perth11);
                    list_tltle.appendChild(perth12);
                    list_tltle.appendChild(perth13);
                    list_tltle.appendChild(perth14);

                    tbody.appendChild(list_tltle);

                    
                    });
                });}
            


            document.getElementById("mytbody").addEventListener("click", function (event) {
                const target = event.target;

                if (target.classList.contains("deleteBtn")) {
                    const row = target.closest("tr");
                    const playerName = row.querySelector("th:nth-child(3)").textContent;

                    console.log(playerName)
                    deleteLike(playerName);
                }
            });
                    
            function deleteLike(playerName){
                let userId = localStorage.getItem("userId");
                fetch("/api/deleteLike", {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "userId": userId,
                    },
                    body: JSON.stringify({
                        "deleteName": playerName
                    })
                })
                .then((response) => {
                    console.log("ok");
                    return response.json();
                })
                .then((data) => {
                if(data){
                    like()
                }
                })
                .catch(error => {
                    console.error("API請求錯誤", error);
                });
            };
            function resetState() {
                isClicked = false;
                choosed_team = "";
                typeName = "";
                data = null;
                isStarClicked = false;
                const selected = document.querySelector("#open");
                const typeNameInput = document.querySelector("#searchBox");
                const selectElement = document.getElementById("open2");
                const tbody = document.getElementById("mytbody");
            
                selected.value = "全部隊伍"; 
                selected2.value= "選擇球員";
                typeNameInput.value = "";  
            
                selectElement.innerHTML = "";
                const emptySelsct = document.createElement("option");
                emptySelsct.value = "";
                emptySelsct.textContent = "選擇球員";
                selectElement.appendChild(emptySelsct);
                tbody.innerHTML = "";
            
                choosed_team = "全部隊伍";  
                typeName = typeNameInput.value;
                getTeam();
                renderData();
            }
            
            let p_t_elements = document.querySelectorAll(".p_t");

        p_t_elements.forEach(function(element) {
            element.addEventListener("mouseover", function() {
                let p_t1 = element.querySelector(".p_t1");
                if (p_t1) {
                    p_t1.style.color = "#ffffff";
                }
                element.style.backgroundColor = "#000000";
            });

            element.addEventListener("mouseout", function() {
                let p_t1 = element.querySelector(".p_t1");
                if (p_t1) {
                    p_t1.style.color = "rgb(67, 66, 66)";
                }
                element.style.backgroundColor = "";
            });
        });

});

        
    
