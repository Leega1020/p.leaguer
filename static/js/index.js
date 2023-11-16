document.addEventListener("DOMContentLoaded", function () {
        

    fetch("/api/lastGame", {
        method: "GET"
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        const dateElements = document.querySelectorAll("#dates");
        const weekElements = document.querySelectorAll("#week");
        const team1Elements = document.querySelectorAll("#team1P");
        const team2Elements = document.querySelectorAll("#team2P");
        const locationElements = document.querySelectorAll("#location");
        const team1pics=document.querySelectorAll("#team1")
        const team2pics=document.querySelectorAll("#team2")
        data.forEach(function (gameData, index) {
            const dateElement = dateElements[index];
            const weekElement = weekElements[index];
            const team1Element = team1Elements[index];
            const team2Element = team2Elements[index];
            const locationElement = locationElements[index];
            const team1pic = team1pics[index];
            const team2pic = team2pics[index];
            dateElement.textContent = dateElement.textContent.replace("", gameData.month+"/"+gameData.day+" "+gameData.week);
            weekElement.textContent = weekElement.textContent.replace("", gameData.week);
            team1Element.textContent = team1Element.textContent.replace("", gameData.team1P);
            team2Element.textContent = team2Element.textContent.replace("", gameData.team2P);
            locationElement.textContent = locationElement.textContent.replace("", gameData.location);
            team1pic.src=gameData.team1_pic
            team2pic.src=gameData.team2_pic
        });
        });


        let nickname = localStorage.getItem('nickname');
        let welcomeName=document.querySelector("#welcomeNickname")
        let userId=localStorage.getItem("userId")
        let welcomePic=document.querySelector("#welcomePic")
        let c=document.querySelector("#c")
        
        if(userId===null||userId==="undefined"){
        welcomePic.src=""
        c.textContent=""
        let a=document.createElement("a")
        a.href="/signin"
        let linkText = document.createTextNode("Sign in");
        a.appendChild(linkText);
        welcomeName.appendChild(a)
        }else{
            welcomeName.textContent="hi"+nickname
            c.textContent=nickname
        }
        
        let teamresult=localStorage.getItem("teamresult")
        let fanspic=document.querySelector("#fanspic")
        let welcomeText=document.querySelector("#welcomeText")
        
        if(teamresult==="臺北富邦勇士"){
            fanspic.src="/static/images/c_fubon.png"
            welcomeText.textContent="FOUR THE WIN，歡迎邦迷"
        }else if(teamresult==="新北國王"){
            fanspic.src="/static/images/c_king.png"
            welcomeText.textContent="Crown the City，歡迎王迷"
        }else if(teamresult==="新竹街口攻城獅"){
            fanspic.src="/static/images/c_lion.png"
            welcomeText.textContent="2024，返擊，歡迎獅迷"
        }else if(teamresult==="福爾摩沙台新夢想家"){
            fanspic.src="/static/images/c_dream.png"
            welcomeText.textContent="我無所懼，歡迎夢迷"
         }else if(teamresult==="桃園領航猿"){
            fanspic.src="/static/images/c_monkey.png"
            welcomeText.textContent="Dare to Fly-永不低頭，歡迎猿迷"
        }else if(teamresult==="高雄17直播鋼鐵人"){
            fanspic.src="/static/images/c_ironman.png"
            welcomeText.textContent="GO雄TEAM，歡迎鋼鐵之心"
        }else{
            fanspic.src=""
            welcomeText.textContent="#唯有籃球"
        }
    });

