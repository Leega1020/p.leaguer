
    
  

    
    handleWelcomePic()

    

    function handleWelcomePic(){
        let teamresult=localStorage.getItem("teamresult")
        let welcomePic=document.querySelector("#welcomePic")

        if(teamresult==="臺北富邦勇士"){
            welcomePic.src="/static/images/taipei.png"
        }else if(teamresult==="新北國王"){
            welcomePic.src="/static/images/king.png"
        }else if(teamresult==="新竹街口攻城獅"){
            welcomePic.src="/static/images/lion.png"
        }else if(teamresult==="福爾摩沙台新夢想家"){
            welcomePic.src="/static/images/taihsin.png"
         }else if(teamresult==="桃園領航猿"){
            welcomePic.src="/static/images/taoyuan_logo.png"
        }else if(teamresult==="高雄17直播鋼鐵人"){
            welcomePic.src="/static/images/kauo.png"
        }
    }


