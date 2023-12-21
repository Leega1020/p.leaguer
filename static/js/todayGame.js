document.addEventListener("DOMContentLoaded", function () {
    function updateUI(data) {
        console.log(data);
        let btpic_m=document.querySelector("#btpic_m")
        btpic_m.src=data.masterTeamLogo
        let btpic_g=document.querySelector("#btpic_g")
        btpic_g.src=data.guestTeamLogo
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

        let bonpersent_m=document.querySelector("#bonpersent_m")
        bonpersent_m.textContent=data.gfoulshot/data.mfoul
        let bonpersent_g=document.querySelector("#bonpersent_g")
        bonpersent_g.textContent=data.mfoulshot/data.gfoul

        let playerContainer = document.querySelector("#pcontainer");
        playerContainer.innerHTML = ""; 

        data.today_master_List.forEach(function (player) {
            createPlayerContainer(player, playerContainer);
        });
    }

    function createPlayerContainer(player, container) {
        let teamContainer = document.createElement("div");
        teamContainer.classList.add("c-team");

        let playerInfoContainer = document.createElement("div");
        playerInfoContainer.classList.add("playerInfo");
        let backNumberDiv = document.createElement("div");
        backNumberDiv.classList.add("backNumber");
        backNumberDiv.innerHTML = "<p>" + player[2] + "</p>";

        let playerNameDiv = document.createElement("div");
        playerNameDiv.classList.add("playerName");
        playerNameDiv.innerHTML = "<p>" + player[3] + "</p>";

        playerInfoContainer.appendChild(backNumberDiv);
        playerInfoContainer.appendChild(playerNameDiv);

        let gameInfoContainer = document.createElement("div");
        gameInfoContainer.classList.add("gameInfo");

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

        gameInfoContainer.appendChild(minutesP);
        gameInfoContainer.appendChild(backboardP);
        gameInfoContainer.appendChild(assistP);
        gameInfoContainer.appendChild(scoreP);

        teamContainer.appendChild(playerInfoContainer);
        teamContainer.appendChild(gameInfoContainer);

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
        data = fetchedData;  
        updateUI(data);
    })  
    .catch(error => {
        console.error("Error:", error.message);
    });

    let T1 = document.querySelector("#T1");
    T1.addEventListener("click", () => {
        let playerContainer = document.querySelector("#pcontainer");
        playerContainer.innerHTML = "";  
        data.today_master_List.forEach(function (player) {
            createPlayerContainer(player, playerContainer);
        });
    });

    let T2 = document.querySelector("#T2");
    T2.addEventListener("click", () => {
        let playerContainer = document.querySelector("#pcontainer");
        playerContainer.innerHTML = ""; 
        data.today_guest_List.forEach(function (player) {
            createPlayerContainer(player, playerContainer);
        });
    });

    let bonContainer=document.querySelector(".bonContainer")
    let bonbtn=document.querySelector("#bonbonbtn")

    bonbtn.addEventListener("click",()=>{
        console.log("clicked")
        bonContainer.style.display="flex"
        description.style.display="none"
    })
    let desbtn=document.querySelector("#desbtn")
    let description=document.querySelector(".description")
    desbtn.addEventListener("click",()=>{
        bonContainer.style.display="none"
        description.style.display="block"
    })

    const teamElements = document.querySelectorAll('.teams');

    teamElements.forEach(team => {
        const teamName = team.querySelector('p');
    
        team.addEventListener('mouseleave', () => {
            teamName.style.color = 'white';
            team.style.backgroundColor = 'black';
        });
    
        team.addEventListener('mouseover', () => {
            teamName.style.color = 'black';
            team.style.backgroundColor = 'white';
            team.style.borderRadius = '5px 5px 0 0'; 
        });
    });
    
    
});
