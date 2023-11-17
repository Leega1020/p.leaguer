import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
from bs4 import BeautifulSoup
from flask import *
from decouple import config
import jwt
from datetime import datetime, timedelta
import mysql.connector.pooling
import requests 
import boto3
import pymysql
import uuid

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key="akksso"

SECRET_KEY = config('SECRET_KEY')
APP_ID = config('APP_ID')
APP_KEY = config('APP_KEY')
PARTNER_KEY = config('PARTNER_KEY')

AWS_ACCESS_KEY=config('AWS_ACCESS_KEY')
AWS_SECRET_KEY=config('AWS_SECRET_KEY')
S3_BUCKET=config('S3_BUCKET')
RDS_HOST=config('RDS_HOST')
RDS_USER=config('RDS_USER')
RDS_PASSWORD=config('RDS_PASSWORD')
RDS_DB=config('RDS_DB')

dbconfig = {
    "database": RDS_DB,
    "user": RDS_USER,
    "host": RDS_HOST,
    "password": RDS_PASSWORD,
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="myPLG",**dbconfig)
con = connection_pool.get_connection()



##################  未來賽事 ################


@app.route("/api/lastGame",methods=["GET"])
def get_lastGame():
    try:
        cur=con.cursor()
        time = datetime.now().strftime("%Y-%m-%d")
        d0=time.split("-")[0]
        d1=time.split("-")[1]
        d2=time.split("-")[2]
        #print(time,d0,d1,d2)
        
        cur.execute("SELECT * FROM regular_season24 WHERE year >= %s AND month >= %s AND day >= %s limit 10", (d0, d1, d2))
        result=cur.fetchall()
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
        
        #print(team_pic)
        json_data = json.dumps(response_data_list, ensure_ascii=False).encode("utf-8")
        response = Response(json_data, content_type="application/json")
        #print(response_data_list)
        return response
        
    
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
    
    #print(typeName)
    cur = con.cursor()  # 在这里初始化 cur

   
        

    if choosed_team == "全部隊伍" and typeName !="":
        cur.execute("SELECT * FROM player WHERE playerName LIKE %s", ("%" + typeName + "%",))
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
            }
            response_data.append(player_data)

        json_data = json.dumps(response_data, ensure_ascii=False).encode("utf-8")
        response = Response(json_data, content_type="application/json")
        
        return response
    elif(choosed_team != "全部隊伍"):
        cur.execute("SELECT * FROM player WHERE p_team=%s", (choosed_team,))
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
            }
            response_data.append(player_data)

        json_data = json.dumps(response_data, ensure_ascii=False).encode("utf-8")
        response = Response(json_data, content_type="application/json")
        return response
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
            }
            response_data.append(player_data)

        json_data = json.dumps(response_data, ensure_ascii=False).encode("utf-8")
        response = Response(json_data, content_type="application/json")
        return response

CHANNEL_ID = ''
CHANNEL_SECRET = ''
REDIRECT_URI = ''

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
        get_user_profile_url = "https://api.line.me/v2/profile"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        profile_response = requests.get(get_user_profile_url, headers=headers)
        
        if profile_response.status_code == 200:
            user_profile = profile_response.json()
            userId=user_profile.get("userId")
            session["userId"]=userId
            cur=con.cursor()
            cur.execute("SELECT*FROM userInfo WHERE userId=%s",(userId,))
            result=cur.fetchone()
            if result:
                print("founded")
                return jsonify({"data":"already signuped"})
            else:
                cur.execute("INSERT INTO userInfo (userId) VALUES (%s)", (userId,))
                con.commit()
                print(userId)
                print("insert DB")
                return userId
@app.route("/aa/signin")
def getSignin():
    access_token = session.get("access_token")
    userId = session.get("userId")

    response_data = {"token": access_token, "userId": userId}
    return jsonify(response_data)

@app.route("/api/signout", methods=["POST"])
def logout_line_user():
    token = request.headers.get('Authorization').split(' ')[1]
    if token:
        access_token = session.get("access_token")
        refresh_token = session.get("refresh_token")

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
            print("User logged out successfully.")
            return jsonify({"data": "ok"})
        else:
            print(f"Failed to log out. Status code: {response.status_code}")
            print(response.text)
            return jsonify({"data": "notnotok"})

@app.route("/api/likePlayer", methods=["POST"])
def saveLikePlayer():
    
    token=request.headers.get("Authorization").split(" ")[1]
    cplayerName=request.json.get("name")
    userId=session.get("userId")
    if token:
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
            return jsonify({"data":"ok"})

@app.route("/api/getLikePlayer", methods=["GET"])
def getLikePlayer():
    
    token = request.headers.get('Authorization').split(' ')[1]
    userId=request.headers.get('userId')
    print(userId)
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
    cur = con.cursor()
    cur.execute("SELECT * FROM today_game")
    result = cur.fetchone()
    gameId = result[1]
    
    # 賽程（主客隊、日期）
    cur.execute("SELECT * FROM regular_season24 WHERE gameId=%s", (gameId,))
    gameInfo = cur.fetchall()
   
    masterTeam = gameInfo[0][2]
    guestTeam = gameInfo[0][1]
    
    # 隊伍（圖片）LIKE %s", ("%" + typeName + "%",)
    cur.execute("SELECT logo FROM plg_team WHERE team LIKE %s", ("%" + masterTeam + "%",))
    masterTeamLogo = cur.fetchall()[0]
    print(masterTeamLogo)
    cur.execute("SELECT logo FROM plg_team WHERE team LIKE %s", ("%" + guestTeam + "%",))
    guestTeamLogo = cur.fetchall()[0]
   
    # 分數（內容：數據、球員數據）
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
        "today_guest_List":today_guest_List,
        "today_master_List":today_master_List
    }
    print(response_data)
    return jsonify(response_data)

    
    

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/player")
def player():
	return render_template("player.html")
@app.route("/signin")
def signin():
	return render_template("line.html") 
@app.route("/game")
def todayGame():
	return render_template("games.html") 
app.run()
