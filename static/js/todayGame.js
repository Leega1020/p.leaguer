document.addEventListener("DOMContentLoaded", function () {

   

        let userId=localStorage.getItem("userId")
        
        let welcomePic=document.querySelector("#welcomePic")
       
        let nickname = localStorage.getItem('nickname');
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
    let data;  // 提升 data 的声明

   
    

    
    function updateUI(data) {
        console.log(data);
        let date = document.querySelector("#date");
        date.textContent = data.year + "-" + data.month + "-" + data.day + " " + data.time;

        let gpic=document.querySelector("#gpic")
        gpic.src=data.masterTeamLogo
        let mfinal=document.querySelector("#mfinal")
        mfinal.textContent=data.mQFinal
        let mteam=document.querySelector("#mteam")
        mteam.textContent=data.masterTeam
        let mQ1=document.querySelector("#mQ1")
        mQ1.textContent=data.mQ1
        let mQ2=document.querySelector("#mQ2")
        mQ2.textContent=data.mQ2
        let mQ3=document.querySelector("#mQ3")
        mQ3.textContent=data.mQ3
        let mQ4=document.querySelector("#mQ4")
        mQ4.textContent=data.mQ4
        let mQ5=document.querySelector("#mQ5")
        mQ5.textContent=data.mQFinal

        let gfinal=document.querySelector("#gfinal")
        gfinal.textContent=data.gQFinal
        let gteam=document.querySelector("#gteam")
        gteam.textContent=data.guestTeam
        let mpic=document.querySelector("#mpic")
        mpic.src=data.guestTeamLogo
        let gQ1=document.querySelector("#gQ1")
        gQ1.textContent=data.gQ1
        let gQ2=document.querySelector("#gQ2")
        gQ2.textContent=data.gQ2
        let gQ3=document.querySelector("#gQ3")
        gQ3.textContent=data.gQ3
        let gQ4=document.querySelector("#gQ4")
        gQ4.textContent=data.gQ4
        let gQ5=document.querySelector("#gQ5")
        gQ5.textContent=data.gQFinal

        let T1name=document.querySelector("#T1name")
        T1name.textContent=data.masterTeam
        let T2name=document.querySelector("#T2name")
        T2name.textContent=data.guestTeam


        let playerContainer = document.querySelector("#pcontainer");
        playerContainer.innerHTML = "";  // 清空原有内容

        data.today_master_List.forEach(function (player) {
            createPlayerContainer(player, playerContainer);
        });
    }

    function createPlayerContainer(player, container) {
        // Create team container
        let teamContainer = document.createElement("div");
        teamContainer.classList.add("c-team");

        // Create player info container
        let playerInfoContainer = document.createElement("div");
        playerInfoContainer.classList.add("playerInfo");

        // Create backNumber and playerName elements
        let backNumberDiv = document.createElement("div");
        backNumberDiv.classList.add("backNumber");
        backNumberDiv.innerHTML = "<p>" + player[2] + "</p>";

        let playerNameDiv = document.createElement("div");
        playerNameDiv.classList.add("playerName");
        playerNameDiv.innerHTML = "<p>" + player[3] + "</p>";

        // Append backNumber and playerName elements to playerInfo container
        playerInfoContainer.appendChild(backNumberDiv);
        playerInfoContainer.appendChild(playerNameDiv);

        // Create gameInfo container
        let gameInfoContainer = document.createElement("div");
        gameInfoContainer.classList.add("gameInfo");

        // Create minutes, backboard, assist, and Score elements
        let minutesP = document.createElement("div");
        minutesP.classList.add("minutes");
        minutesP.innerHTML = "<p>" + player[4] + "</p>";

        let backboardP = document.createElement("div");
        backboardP.classList.add("backboard");
        backboardP.innerHTML = "<p>" + player[5] + "</p>";

        let assistP = document.createElement("div");
        assistP.classList.add("assist");
        assistP.innerHTML = "<p>" + player[6] + "</p>";

        let scoreP = document.createElement("div");
        scoreP.classList.add("Score");
        scoreP.innerHTML = "<p>" + player[7] + "</p>";

        // Append minutes, backboard, assist, and Score elements to gameInfo container
        gameInfoContainer.appendChild(minutesP);
        gameInfoContainer.appendChild(backboardP);
        gameInfoContainer.appendChild(assistP);
        gameInfoContainer.appendChild(scoreP);

        // Append playerInfo and gameInfo containers to teamContainer
        teamContainer.appendChild(playerInfoContainer);
        teamContainer.appendChild(gameInfoContainer);

        // Append teamContainer to container
        container.appendChild(teamContainer);
    }

    fetch("/api/getTodayGame", {
        method: "GET",
    })
    .then(response => {
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error("Failed to fetch data");
        }
    })
    .then(fetchedData => {
        data = fetchedData;  // 将 data 赋值为 fetchedData
        updateUI(data);
    })  
    .catch(error => {
        console.error("Error:", error.message);
    });

    let T1 = document.querySelector("#T1");
    T1.addEventListener("click", () => {
        let playerContainer = document.querySelector("#pcontainer");
        playerContainer.innerHTML = "";  // 清空原有内容

        data.today_master_List.forEach(function (player) {
            createPlayerContainer(player, playerContainer);
        });
    });

    let T2 = document.querySelector("#T2");
    T2.addEventListener("click", () => {
        let playerContainer = document.querySelector("#pcontainer");
        playerContainer.innerHTML = "";  // 清空原有内容

        data.today_guest_List.forEach(function (player) {
            createPlayerContainer(player, playerContainer);
        });
    });
});
