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
    });

