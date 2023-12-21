import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from flask import *
from decouple import config
from datetime import datetime, timedelta
import mysql.connector.pooling
import requests 
import redis
import threading
import subprocess
channel_accedd_token = config('channel_accedd_token')
url = "https://api.line.me/v2/bot/message/push"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {channel_accedd_token}"
}

SECRET_KEY = config('SECRET_KEY')
APP_ID = config('APP_ID')
APP_KEY = config('APP_KEY')
PARTNER_KEY = config('PARTNER_KEY')
CHANNEL_ID = config('CHANNEL_ID')
CHANNEL_SECRET = config('CHANNEL_SECRET')
REDIRECT_URI = config('REDIRECT_URI')
DB_HOST=config('DB_HOST')
DB_PASSWORD=config('DB_PASSWORD')
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key=SECRET_KEY
app.permanent_session_lifetime = timedelta(hours=1)

dbconfig = {
    "database": "PLG",
    "user": "root",
    "host": DB_HOST,
    "password": DB_PASSWORD,
    "port":"3306"
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="myPLG",**dbconfig,pool_reset_session=True, 
    connect_timeout=5,
    
   )
con = connection_pool.get_connection()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.route("/api/lastGame",methods=["GET"])
def get_lastGame():
    try:
        #r.delete("last_game_data")
        cached_data = r.get("last_game_data")

        if cached_data:
            print("lastGame ok")
            return Response(cached_data, content_type="application/json")
        cur=con.cursor()
        time = datetime.now().strftime("%Y-%m-%d")
        d0=time.split("-")[0]
        d1=time.split("-")[1]
        d2=time.split("-")[2]
        #print(time,d0,d1,d2)
        d2023=2023
        d2024=2024
        cur.execute("SELECT * FROM regular_season24 WHERE year >= %s AND month >= %s AND day>=%s limit 10",
            (d0,d1, d2))
        result=cur.fetchall()
        #print(result[0])
        #print(result)
        response_data_list = []
        for i in result:
            team1=i[2]
            team2=i[1]
            
            cur.execute("SELECT logo FROM plg_team WHERE team LIKE %s", ('%' + team1 + '%',))
            team1_pic=cur.fetchall()
            cur.execute("SELECT logo FROM plg_team WHERE team LIKE %s", ('%' + team2 + '%',))
            team2_pic=cur.fetchall()
            #print(team1_pic,team2_pic)
            response_data = {
            "month": i[4],
            "day": i[5],
            "week":i[6],
            "team1P": i[2],
            "team2P": i[1],
            "location": i[8],
            "team2_pic":team2_pic,
            "team1_pic":team1_pic
        }
            response_data_list.append(response_data)
        #print(response_data_list)
        # 
        #print(team_pic)
        
        response_data_list.append(response_data)
        json_data = json.dumps(response_data_list, ensure_ascii=False).encode("utf-8")
        r.setex("last_game_data", 3600, json_data)
        return Response(json_data, content_type="application/json")
        
    
    except Exception as e:
        error_message="伺服器內部錯誤"
        response_data={
            "error":True,
            "message":error_message
        }
        
        return jsonify({"data":response_data})


@app.route("/api/player", methods=["POST"])
def get_playerList():
    choosed_team = request.json.get("team")
    typeName = request.json.get("typeName")
    userId = request.headers.get("userId")
    #print(userId)
    cache_key = f"player_list:{userId}:{choosed_team}:{typeName}"
    cached_data = r.get(cache_key)
    if cached_data:
        print("cache_playerok")
        return Response(cached_data, content_type="application/json")
    cur = con.cursor()
    cur.execute("SELECT playerName FROM memberLike WHERE userId=%s", (userId,))
    liked_players = set(row[0] for row in cur.fetchall())

    if choosed_team == "全部隊伍" and typeName != "":
        cur.execute("SELECT * FROM player WHERE playerName LIKE %s", ("%" + typeName + "%",))
    elif choosed_team != "全部隊伍":
        cur.execute("SELECT * FROM player WHERE p_team=%s", (choosed_team,))
    else:
        cur.execute("SELECT * FROM player")

    result = cur.fetchall()
    response_data = []

    for i in result:
        player_data = {
            "backNumber": i[1],
            "playerName": i[2],
            "p_team": i[3],
            "p_counts": i[4],
            "p_time": i[5],
            "point2": i[6],
            "point3": i[7],
            "p_foulShots": i[8],
            "p_scores": i[9],
            "p_backboards": i[10],
            "p_assists": i[11],
            "p_intercept": i[12],
            "p_miss": i[13],
            "p_foul": i[14],
            "imagePath": "/static/images/star.png" if i[2] in liked_players else "/static/images/star (1).png",
        }
        response_data.append(player_data)
    #print(response_data)
    # json_data = json.dumps(response_data, ensure_ascii=False).encode("utf-8")
    # response = Response(json_data, content_type="application/json")
    json_data = json.dumps(response_data, ensure_ascii=False).encode("utf-8")
    r.setex(cache_key, 3600, json_data)
    return Response(json_data, content_type="application/json")

@app.route('/get/signin', methods=['GET'])
def line_signin():
    
    authorization_code = request.args.get('code')
    access_token_url = 'https://api.line.me/oauth2/v2.1/token'
    headers = {
     'Content-Type': 'application/x-www-form-urlencoded'
}
    payload = {
        'grant_type': 'authorization_code',
        'Content-Type':'application/x-www-form-urlencoded',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CHANNEL_ID,
        'client_secret': CHANNEL_SECRET
    }
    
    response = requests.post(access_token_url, headers=headers, data=payload)
    
    #print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        access_token = data.get('access_token')
        refresh_token=data.get("refresh_token")
        session["refresh_token"]=refresh_token
        #print(refresh_token)
        session["access_token"]=access_token
        session.permanent = True
        get_user_profile_url = "https://api.line.me/v2/profile"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        profile_response = requests.get(get_user_profile_url, headers=headers)
        
        if profile_response.status_code == 200:
            user_profile = profile_response.json()
            userId=user_profile.get("userId")
            session["userId"]=userId
            thread = threading.Thread(target=getId, args=(userId,))
            thread.start()
            getId(userId)
            getId(userId)
            r.set(f"userId:{userId}", userId)
            r.expire(f"userId:{userId}", 3600)


            cur=con.cursor()
            cur.execute("SELECT*FROM userInfo WHERE userId=%s",(userId,))
            result=cur.fetchone()
            if result:
                print("founded")
                return redirect("/signin")
            else:
                cur.execute("INSERT INTO userInfo (userId) VALUES (%s)", (userId,))
                con.commit()
                print(userId)
                print("insert DB")
                return redirect("/signin")

def getId(userId):
    print("HERE!")
    subprocess.run(["python3", "gameBot.py", userId])
    
@app.route("/aa/signin")
def getSignin():
    userId = session.get("userId")
    if userId is not None:

        cache_userId=r.get(f"userId:{userId}")
        if cache_userId is not None:
            userId=cache_userId
    
            cur = con.cursor()
            cur.execute("SELECT userId FROM userInfo WHERE userId=%s", (userId,))
            haveuserId = cur.fetchone()

            if haveuserId is not None:
                userId = haveuserId[0]
                cur.execute("SELECT nickname,team FROM userInfo WHERE userId=%s", (userId,))
                result = cur.fetchone()

                if result is not None:
                    nickname = result[0]
                    team=result[1]
                    response_data = {"userId": userId, "nickname": nickname,"team":team}
                    
                    return jsonify(response_data)
                        
                else:
                    # Handle the case where there is no nickname
                    print("No nickname found.")
                    return jsonify({"error": "No nickname found."})
            else:
                # Handle the case where haveuserId is None
                print("No userId found.")
                return jsonify({"error": "No userId found."})
    else:
        return jsonify({"data":"not signin"})


@app.route("/api/signInfo", methods=["POST"])
def getSignin2():
    userId = request.headers.get("userId")
    signUpName = request.json.get("signUpName")
    signUpTeam = request.json.get("signUpTeam")
    print(userId)
    print(signUpName)

    cur = con.cursor()
    cur.execute("SELECT nickname FROM userInfo WHERE userId=%s", (userId,))
    result = cur.fetchone()

    if result is not None:
        cur.execute("UPDATE userInfo SET nickname=%s, team=%s WHERE userId=%s", (signUpName, signUpTeam, userId))
        con.commit()
        
        print("ok")
        return jsonify({"data": "update ok"})
    else:
        print("NOY!")
        return jsonify({"data": "error"})

@app.route("/api/signout", methods=["POST"])
def logout_line_user():
    userId = request.headers.get('userId')
    if userId:
        access_token = session.get("access_token")
        if not access_token:
            print("No access token found.")
            return jsonify({"data": "notok"})

        revoke_url = "https://api.line.me/oauth2/v2.1/revoke"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            "access_token": access_token,
            "client_id": CHANNEL_ID,
            "client_secret": CHANNEL_SECRET  
        }

        response = requests.post(revoke_url, headers=headers, data=payload)

        print(response)

        if response.status_code == 200:
            session.clear()
            print("User logged out successfully.")
            return jsonify({"data": "ok"})
        else:
            print(f"Failed to log out. Status code: {response.status_code}")
            print(response.text)
            return jsonify({"data": "notnotok"})

@app.route("/api/likePlayer", methods=["POST"])
def saveLikePlayer():
    
    userId=request.headers.get("userId")
    cplayerName=request.json.get("name")
    
    if userId:
        cur=con.cursor()
        cur.execute("SELECT*FROM memberLike WHERE userId=%s AND playerName=%s",(userId,cplayerName))
        result1=cur.fetchall()
        print(result1)
        if  len(result1) > 0:
            return jsonify({"data":"already saved"})
          
        else:
            cur.execute("SELECT*FROM player WHERE playerName=%s",(cplayerName,))
            result=cur.fetchone()
            print(result)
            cur.execute("INSERT INTO memberLike(userId,backNumber, playerName, p_team, p_counts, p_time, point2, point3, p_foulShots, p_scores, p_backboards, p_assists, p_intercept, p_miss, p_foul) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (userId,result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[11], result[12], result[13], result[14]))
            con.commit()
            update_like_players_cache(userId)
            return jsonify({"data":"ok"})
    else:
        return jsonify({"data":"not signin in"})
        
def update_like_players_cache(userId):
    response_data = []
    cur = con.cursor()
    cur.execute("SELECT * FROM memberLike WHERE userId=%s", (userId,))
    result = cur.fetchall()

    for i in result:
        player_data = {
            "backNumber": i[2],
            "playerName": i[3],
            "p_team": i[4],
            "p_counts": i[5],
            "p_time": i[6],
            "point2": i[7],
            "point3": i[8],
            "p_foulShots": i[9],
            "p_scores": i[10],
            "p_backboards": i[11],
            "p_assists": i[12],
            "p_intercept": i[13],
            "p_miss": i[14],
            "p_foul": i[15],
        }
        response_data.append(player_data)

    json_data = json.dumps(response_data, ensure_ascii=False).encode("utf-8")
    r.set(f"like_players:{userId}", json_data, ex=3600)
    return Response(json_data, content_type="application/json")

@app.route("/api/getLikePlayer", methods=["GET"])
def getLikePlayer():
    
    token = request.headers.get('Authorization').split(' ')[1]
    userId=request.headers.get('userId')
    #print(userId)
    cached_data = r.get(f"like_players:{userId}")

    if cached_data:
        print("update pp ok")
        return Response(cached_data, content_type="application/json")
        return jsonify(cached_data)
    response_data = []  
    if userId is None:
        return jsonify({"data":None})
    else:
        cur=con.cursor()
        cur.execute("SELECT*FROM memberLike WHERE userId=%s",(userId,))
        result = cur.fetchall()
        for i in result:
            player_data = {
                "backNumber": i[2],
                "playerName": i[3],
                "p_team": i[4],
                "p_counts": i[5],
                "p_time": i[6],
                "point2": i[7],
                "point3": i[8],
                "p_foulShots": i[9],
                "p_scores": i[10],
                "p_backboards": i[11],
                "p_assists": i[12],
                "p_intercept": i[13],
                "p_miss": i[14],
                "p_foul": i[15],
            }
            response_data.append(player_data)

        
        return jsonify(response_data)

@app.route("/api/getTodayGame")
def getTodayGame():
    r.delete("today_game_data")
    cached_data = r.get("today_game_data")

    if cached_data:
        print("todayGame ok")
        return Response(cached_data, content_type="application/json")
    cur = con.cursor()
    cur.execute("SELECT * FROM today_game ORDER BY id DESC LIMIT 1")
    result = cur.fetchone()
    gameId = result[1]
    print(gameId)

    cur.execute("SELECT * FROM regular_season24 WHERE gameId=%s", (gameId,))
    gameInfo = cur.fetchall()
   
    masterTeam = gameInfo[0][2]
    guestTeam = gameInfo[0][1]
  
    cur.execute("SELECT logo FROM plg_team WHERE team LIKE %s", ("%" + masterTeam + "%",))
    masterTeamLogo = cur.fetchall()[0]
    print(masterTeamLogo)
    cur.execute("SELECT logo FROM plg_team WHERE team LIKE %s", ("%" + guestTeam + "%",))
    guestTeamLogo = cur.fetchall()[0]
   
    today_guest_List=[]
    today_master_List=[]
    cur.execute("SELECT * FROM today_game WHERE gameId = %s", (gameId,))
    todayGameData = cur.fetchall()[0]
    cur.execute("SELECT * FROM today_guest_player WHERE gameId = %s", (gameId,))
    today_guest_playerData = cur.fetchall()
    for i in today_guest_playerData:
        today_guest_List.append(i)
    cur.execute("SELECT * FROM today_master_player WHERE gameId = %s", (gameId,))
    today_master_playerData = cur.fetchall()
    for i in today_master_playerData:
        today_master_List.append(i)
    response_data = {
        "year": gameInfo[0][3],
        "month": gameInfo[0][4],
        "day": gameInfo[0][5],
        "time": gameInfo[0][7],
        "masterTeam": masterTeam,
        "guestTeam": guestTeam,
        "masterTeamLogo": masterTeamLogo[0],
        "guestTeamLogo": guestTeamLogo[0],
        "gQ1": todayGameData[2],
        "gQ2": todayGameData[3],
        "gQ3": todayGameData[4],
        "gQ4": todayGameData[5],
        "gQFinal": todayGameData[6],
        "mQ1": todayGameData[7],
        "mQ2": todayGameData[8],
        "mQ3": todayGameData[9],
        "mQ4": todayGameData[10],
        "mQFinal": todayGameData[11],
        "mfoulshot": todayGameData[12],
        "mfoul": todayGameData[13],
        "gfoulshot": todayGameData[14],
        "gfoul": todayGameData[15],
        "today_guest_List":today_guest_List,
        "today_master_List":today_master_List,
    }
    json_data = json.dumps(response_data, ensure_ascii=False).encode("utf-8")
    r.setex("today_game_data", 3600, json_data)
    return Response(json_data, content_type="application/json")

def check_deleteLike(deleteName,userId):
    if deleteName=="" or userId== "":
        return False
    else:
        return True
@app.route("/api/deleteLike", methods=["DELETE"])  
def deleteLike():
    deleteName=request.json.get("deleteName")
    userId=request.headers.get("userId")
    
    if check_deleteLike(deleteName,userId):
        cur=con.cursor()
        cur.execute("DELETE FROM memberLike WHERE userId=%s AND playerName=%s",(userId,deleteName))
        con.commit()
        update_like_players_cache(userId)
        return jsonify({"data":"ok"})
    else:
        return jsonify({"data":"invilid value"})


@app.route("/api/signday", methods=["POST"])
def handleSignday():
    userId = request.headers.get("userId")
    lastTime = request.json.get("lastTime")

    if userId is None:
        return jsonify({"data": "Not Signin"})
    else:
        checkDay = request.json.get("check")
        cur = con.cursor()
       
        cur.execute("SELECT day1 FROM userInfo WHERE userId=%s", (userId,))
        first = cur.fetchone()
        if first is not None:
            first = "not1"
        else:
            first = "yes1"
      
        cur.execute(f"SELECT {checkDay} FROM userInfo WHERE userId = %s", (userId,))
        result = cur.fetchone()

        if result is not None and result[0] == "checked":
            
            return jsonify({"first": first})
        else:
            checked = "checked"
            formatted_date = datetime.strptime(lastTime, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(f"UPDATE userInfo SET {checkDay} = %s, lasttime = %s WHERE userId = %s", (checked, formatted_date, userId))

            con.commit()
            print(formatted_date)
            return jsonify({"first": first})

    
@app.route("/api/signday", methods=["GET"])
def getSignDay():
    userId = request.headers.get("userId")
    if userId is None:
        return jsonify({"data": "Not Signin"})
    else:
        cur = con.cursor()
        cur.execute("SELECT day1, day2, day3, day4, day5, day6, day7 FROM userInfo WHERE userId=%s", (userId,))
        result = cur.fetchone()
        cur.execute("SELECT lasttime FROM userInfo WHERE userId=%s", (userId,))
        lasttimes = cur.fetchone()
        timeok = ""  # 給 timeok 初始值
        cur.execute("SELECT team FROM userInfo WHERE userId=%s", (userId,))
        teamresult=cur.fetchone()
        if teamresult is not None:
            teamresult = teamresult[0]
        if lasttimes is not None and len(lasttimes) > 0:
            lasttime = lasttimes[0]
            
            current_time = datetime.now()

            if lasttime is not None:
                time_difference = current_time - lasttime

                if time_difference > timedelta(seconds=5):
                    timeok = "timeok"
                else:
                    timeok = "timenotok"
            else:
                
                time_difference = timedelta(days=0)  # Set a default value
            print(current_time)
            print(time_difference)
            print(timedelta(days=1))
        if result is not None:
            has_none = any(value is None for value in result)
            print(timeok)
            if has_none:
                # If there are None values, return the count of unsigned days
                count = 7 - result.count(None)
                
                
                return jsonify({"count": count, "lastTime": timeok, "teamresult": teamresult})
            else:
                count = 7
                return jsonify({"count": count, "lastTime": timeok,"teamresult":teamresult})
        else:
            # Handle the case when result is None (no data found)
            print("No data found for user")
            
            return jsonify({"count": 0, "lastTime": timeok,"teamresult":teamresult})
@app.route("/api/updateTeam", methods=["POST"])
def updateTeam():
    userId=request.headers.get("userId")
    changeTeam=request.json.get("changeTeam")
    print(changeTeam)
    if userId is not None:
        cur=con.cursor()
        cur.execute("UPDATE userInfo SET team=%s WHERE userId=%s",(changeTeam,userId))
        con.commit()
        print("okchangeTeam")
        return jsonify({"changeTeam":changeTeam})


@app.route("/api/team",methods=["GET"])
def getTeam():
    r.delete("team_data")
    cached_data = r.get("team_data")

    if cached_data:
        print("team_data ok")
        return Response(cached_data, content_type="application/json")
    response_data_list=[]
    cur=con.cursor()
    cur.execute("SELECT*FROM plg_team")
    result=cur.fetchall()
    for i in result:
        response_data = {
            "id": i[0],
            "team":i[1],
            "scores": i[2],
            "point2":i[3],
            "point3": i[4],
            "foulShot": i[5],
            "backboards": i[6],
            "assists": i[7],
            "block": i[8],
            "p_miss":i[9],
            "p_foul": i[10],
            "paint": i[11],
            "tpic":i[12],
            "win":i[13],
            "lose":i[14],
            "pct":i[15]
        }
        response_data_list.append(response_data)  
    #print(response_data)
    json_data = json.dumps(response_data_list, ensure_ascii=False).encode("utf-8")
    #print(json_data)
    r.setex("team_data", 3600, json_data)
    return Response(json_data, content_type="application/json")


@app.route("/")
def index():
	return render_template("index.html")
@app.route("/player")
def player():
	return render_template("player.html")
@app.route("/signin")
def signin():
	return render_template("sign2.html") 
@app.route("/game")
def todayGame():
	return render_template("games.html") 
@app.route("/member")
def member():
	return render_template("member.html") 
@app.route("/linesign")
def linesign():
	return render_template("line.html") 
@app.route("/team")
def team():
	return render_template("team.html") 
app.run(host='0.0.0.0', port=5000, threaded=True)
