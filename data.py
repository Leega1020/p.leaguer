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

# url = "https://pleagueofficial.com/schedule-regular-season"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     data = response.text
#     root = BeautifulSoup(data, "html.parser")

# ##################  未來賽事 ################

# main_teams = root.select('span.PC_only.fs14')

# teable24=[]
# guest_team = []
# master_team = []


# for i in range(len(main_teams)):
#     team = main_teams[i].get_text()
    
#     if i % 2 == 0:
#         guest_team.append(team)
#     else:
#         master_team.append(team)
# teable24.append(guest_team)
# teable24.append(master_team)

# date_elements = root.find_all('div', class_='match_row_datetime')
# dates = []
# days = []
# times = []
# years=[]
# months=[]
# weeks=[]
# for element in date_elements:
    
#     date_element = element.find('h5', class_='fs16')
#     date = date_element.get_text() if date_element else ""
#     newdate=date.split("/")[0]
#     if int(newdate)<10:
#         date="2024/"+date
#         dates.append(date)
#     else:date="2023/"+date
#     departdate=date.split("/")
#     year=departdate[0]
#     month=departdate[1]
#     day=departdate[2]

#     years.append(year)
#     months.append(month)
#     days.append(day)

#     day_element = element.find('h5', class_='fs12')
#     week = day_element.get_text() if day_element else ""

#     time_element = element.find('h6', class_='fs12')
#     time = time_element.get_text() if time_element else ""

    
#     weeks.append(week)
#     times.append(time)
    
# teable24.append(dates)
# teable24.append(days)
# teable24.append(times)


# location_elements = root.find_all('h5', class_='fs12 mb-0')
# locations=[]
# for location in location_elements:
#     locations.append(location.string)
# teable24.append(locations)

# gameId_elements = root.find_all('h5', class_='fs14 mb-2')
# gameIds=[]
# for gameId in gameId_elements:
#     gameIds.append(gameId.string)
# teable24.append(gameIds)

# start_value = 423
# num_values = 120
# gameNumber = [start_value + i for i in range(num_values)]
# teable24.append(gameNumber)
# cur=con.cursor()
# cur.execute("CREATE TABLE regular_season24(id INT PRIMARY KEY AUTO_INCREMENT, guest_team VARCHAR(255), master_team VARCHAR(255), year VARCHAR(255),month VARCHAR(255), day VARCHAR(255),week VARCHAR(255), time VARCHAR(255), locations VARCHAR(255), gameId VARCHAR(255), gameNumber INT)")
# #for i in range(len(guest_team)):
#     #cur.execute("INSERT INTO regular_season24 (guest_team, master_team, year,month,day, week, time, locations, gameId, gameNumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
#             #(guest_team[i], master_team[i], years[i], months[i],days[i],weeks[i], times[i], locations[i], gameIds[i], gameNumber[i]))
#     #con.commit()


# ################## 球員數據 ################
# url = "https://pleagueofficial.com/stat-player"
# headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     data = response.text
#     root = BeautifulSoup(data, "html.parser")
    
#     player_data = [] 

# player_rows = root.find_all("tr")

# # 遍歷每一個 <tr> 標籤，跳過第一個因為它包含表頭
# for player_row in player_rows[1:]:
#     player_info = []  
#     player_name = player_row.find("th").a.string  
#     player_info.append(player_name)  
#     player_stats = player_row.find_all("td")  # 找到球員的詳細數據
#     for stat in player_stats:
#         player_info.append(stat.string)
#     player_data.append(player_info) 


# #cur = con.cursor()
# #cur.execute("CREATE TABLE player (id INT PRIMARY KEY AUTO_INCREMENT, backNumber INT, playerName VARCHAR(255), p_team VARCHAR(255), p_counts INT, p_time VARCHAR(255), point2 VARCHAR(255), point3 VARCHAR(255), p_foulShots VARCHAR(255), p_scores FLOAT, p_backboards FLOAT, p_assists FLOAT, p_intercept FLOAT, p_miss FLOAT, p_foul FLOAT)")

# for player in player_data:
#     playerName = player[0] if len(player) > 0 else None
#     backNumber = player[1] if len(player) > 1 else None
#     p_team = player[2] if len(player) > 2 else None
#     p_counts = player[3] if len(player) > 3 else None
#     p_time = player[4] if len(player) > 4 else None
#     point2 = player[7] if len(player) > 7 else None
#     point3 = player[10] if len(player) > 10 else None
#     p_foulShots = player[13] if len(player) > 13 else None
#     p_scores = player[14] if len(player) > 14 else None
#     p_backboards = player[17] if len(player) > 17 else None
#     p_assists = player[18] if len(player) > 18 else None
#     p_intercept = player[19] if len(player) > 19 else None
#     p_miss = player[21] if len(player) > 21 else None
#     p_foul = player[22] if len(player) > 22 else None

#    # cur.execute("INSERT INTO player (backNumber, playerName, p_team, p_counts, p_time, point2, point3, p_foulShots, p_scores, p_backboards, p_assists, p_intercept, p_miss, p_foul) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
#               # (backNumber, playerName, p_team, p_counts, p_time, point2, point3, p_foulShots, p_scores, p_backboards, p_assists, p_intercept, p_miss, p_foul))

# #con.commit()

# #cur.close()
# #con.close()

################## 球隊數據＋圖片 ################

# url = "https://pleagueofficial.com/stat-team/2022-23/2#recordn"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     data = response.text
#     root = BeautifulSoup(data, "html.parser")

# teams_data=root.find("tbody")
# team_datas = []
# logos=[]

# pic_list = ["king", "taipei", "taoyuan_logo", "taihsin", "kauo", "lion"]
# base_url = "https://d3u20ovlrk4ryy.cloudfront.net/images/"
# logos = [base_url + pic + ".png" for pic in pic_list]

# for i, row in enumerate(teams_data.find_all('tr')):
#     names_data = row.find_all('a')
#     names = [name_data.get_text() for name_data in names_data]

#     columns = row.find_all('td')
#     team_stats = [column.get_text() for column in columns]

#     # 使用循环的索引 i 来访问对应的 logo URL
#     team_data_with_logo = names + team_stats + [logos[i]]

#     team_datas.append(team_data_with_logo)
# #print(team_datas)
# for i in team_datas:
#     team=i[0]
#     scores=i[12]
#     point2=i[5]
#     point3=i[8]
#     foulShot=i[11]
#     backboards=i[15]
#     assists=i[16]
#     block=i[18]
#     p_miss=i[19]
#     p_foul=i[20]
#     paint=i[22]
#     logo=i[23]
#     cur=con.cursor()
    #cur.execute("CREATE TABLE plg_team(id INT PRIMARY KEY AUTO_INCREMENT, team VARCHAR(255), scores VARCHAR(255), point2 VARCHAR(255), point3 VARCHAR(255), foulShot VARCHAR(255), backboards FLOAT, assists FLOAT, block FLOAT, p_miss FLOAT, p_foul FLOAT, paint FLOAT, logo VARCHAR(255))")

    # cur.execute("INSERT INTO plg_team(team,scores,point2,point3,foulShot,backboards,assists,block,p_miss,p_foul,paint,logo) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    #             (team,scores,point2,point3,foulShot,backboards,assists,block,p_miss,p_foul,paint,logo))
    # con.commit()
    
    # print(p_foul,paint,logo)

#cur.execute("CREATE TABLE userInfo(id INT PRIMARY KEY AUTO_INCREMENT, userId VARCHAR(255))")
# cur.execute("CREATE TABLE memberLike(id INT PRIMARY KEY AUTO_INCREMENT, userId VARCHAR(255), backNumber INT, playerName VARCHAR(255), p_team VARCHAR(255), p_counts INT, p_time VARCHAR(255), point2 VARCHAR(255), point3 VARCHAR(255), p_foulShots VARCHAR(255), p_scores FLOAT, p_backboards FLOAT, p_assists FLOAT, p_intercept FLOAT, p_miss FLOAT, p_foul FLOAT)")
# con.commit()

################## 近期賽程數據 ################
cur=con.cursor()
cur.execute("CREATE TABLE today_game (id INT PRIMARY KEY AUTO_INCREMENT,gameId VARCHAR(255),guestQ1 VARCHAR(255),guestQ2 VARCHAR(255),guestQ3 VARCHAR(255),guestQ4 VARCHAR(255),guestFinal VARCHAR(255),masterQ1 VARCHAR(255),masterQ2 VARCHAR(255),masterQ3 VARCHAR(255),masterQ4 VARCHAR(255),masterFinal VARCHAR(255))")
cur.execute("CREATE TABLE today_guest_player (id INT PRIMARY KEY AUTO_INCREMENT,gameId VARCHAR(255),backnumber VARCHAR(255),name VARCHAR(255),ontime VARCHAR(255),backboard VARCHAR(255),assist VARCHAR(255),score VARCHAR(255),foul VARCHAR(255),foulshot VARCHAR(255))")
cur.execute("CREATE TABLE today_master_player (id INT PRIMARY KEY AUTO_INCREMENT,gameId VARCHAR(255),backnumber VARCHAR(255),name VARCHAR(255),ontime VARCHAR(255),backboard VARCHAR(255),assist VARCHAR(255),score VARCHAR(255),foul VARCHAR(255),foulshot VARCHAR(255))")

con.commit()