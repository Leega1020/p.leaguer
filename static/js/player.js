let isClicked = false;
let choosed_team = "";
let typeName = "";
let data; // 添加一個變數用來保存從伺服器獲取的數據

document.addEventListener("DOMContentLoaded", function () {
    const selected = document.querySelector("#open");
    const typeNameInput = document.querySelector("#searchBox");
    const searchBtn = document.querySelector("#searchBtn");
    const selected2 = document.querySelector("#open2");

    selected.addEventListener("change", function () {
        choosed_team = selected.value;
        typeName = typeNameInput.value; // 設置 typeName 的值
        getTeam();
    });

    searchBtn.addEventListener("click", (e) => {
        e.preventDefault();
        choosed_team = "全部隊伍";
        typeName = typeNameInput.value; 
        
        getTeam();
        typeNameInput.value=""
        selected.value="全部隊伍"
    });

    // 初始化一次
    choosed_team = selected.value;
    typeName = typeNameInput.value;
    console.log(choosed_team);
    getTeam();

    function getTeam() {
        fetch("/api/player", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                team: choosed_team,
                typeName: typeName,
            }),
        })
            .then((response) => {
                console.log("ok");
                return response.json();
            })
            .then((responseData) => {
                data = responseData; // 保存從伺服器獲取的數據
                renderData(); // 渲染頁面
            });
    }

    selected2.addEventListener("change", function () {
        const choosed_player = selected2.value;
        const filteredData = data.filter((player) => player.playerName === choosed_player);

        if (filteredData.length > 0) {
            const player = filteredData[0];
            renderPlayer(player);
        }
    });

    function renderData() {
        const tbody = document.getElementById("mytbody");
        const selectElement = document.getElementById("open2");

        // 清空之前的選項
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
                    img.src = "/static/images/star (1).png";
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
                    if (isClicked) {
                        event.target.src = "/static/images/star (1).png";
                    } else {
                        event.target.src = "/static/images/star.png";
                    }
                    isClicked = !isClicked; // 切換圖片的狀態
                });
            });
        }
    }

    function renderPlayer(player) {
        const tbody = document.getElementById("mytbody");
        tbody.innerHTML = ""; // 清空之前的數據
    
        const list_tltle = document.createElement("tr");
        list_tltle.classList.add("list_tltle2");
    
        const imgth = document.createElement("th");
        const img = document.createElement("img");
        img.src = "/static/images/star (1).png";
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
            if (isClicked) {
                event.target.src = "/static/images/star (1).png";
            } else {
                event.target.src = "/static/images/star.png";
            }
            isClicked = !isClicked; // 切換圖片的狀態
        });
    }
    
});
