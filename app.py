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


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
options=Options()
def OnGame():
    driver=webdriver.Chrome(options=options)

    driver.get("https://pleagueofficial.com/game/197")  # 替换为实际的页面 URL

    import time
    time.sleep(1) 

    table_rows = driver.find_elements(By.CSS_SELECTOR, "table#away_table tbody tr")

    g_backnumbers=[]
    g_players=[]
    g_onTimes=[]
    g_backboards=[]
    g_assists=[]
    g_scores=[]

    g_fouls=[]
    g_foulShots=[]
    for row in table_rows:
        data = row.text
        fields = data.split()
        if len(fields) >= 15:
            backnumber = fields[0] if fields[0] else "N/A"
            g_backnumbers.append(backnumber)
            if "〇" in data:
                g_player = fields[2] if fields[2] else "N/A"
                g_players.append(g_player)
                g_onTime = fields[3] if fields[3] else "N/A"
                g_onTimes.append(g_onTime)
                g_backboard = fields[11] if fields[11] else "N/A"  # 如果字段为空，使用 "N/A" 作为占位符
                g_backboards.append(g_backboard)
                g_assist = fields[14] if fields[14] else "N/A"
                g_assists.append(g_assist)
                g_score = fields[10] if fields[10] else "N/A"
                g_scores.append(g_score)

                g_foul = fields[8].split("-")[1] 
                g_fouls.append(g_foul)
                g_foulShot= fields[18] if fields[18] else "N/A"
                g_foulShots.append(g_foulShot)
            else:
                g_player = fields[1] if fields[1] else "N/A"
                g_players.append(g_player)
                g_onTime = fields[2] if fields[2] else "N/A"
                g_onTimes.append(g_onTime)
                g_backboard = fields[10] if fields[10] else "N/A"  # 如果字段为空，使用 "N/A" 作为占位符
                g_backboards.append(g_backboard)
                g_assist = fields[13] if fields[13] else "N/A"
                g_assists.append(g_assist)
                g_score = fields[9] if fields[9] else "N/A"
                g_scores.append(g_score)

                g_foul = fields[7].split("-")[1] 
                g_fouls.append(g_foul)
                g_foulShot= fields[17] if fields[17] else "N/A"
                g_foulShots.append(g_foulShot)

    table_master = driver.find_elements(By.CSS_SELECTOR, "table#home_table tbody tr")

    m_backnumbers=[]
    m_players=[]
    m_onTimes=[]
    m_backboards=[]
    m_assists=[]
    m_scores=[]

    m_fouls=[]
    m_foulShots=[]
    for row2 in table_master:
        data2 = row2.text
        fields2 = data2.split()
        if len(fields2) >= 15:
            backnumber = fields2[0] if fields2[0] else "N/A"
            m_backnumbers.append(backnumber)
            if '〇' in data2:
                m_player = fields2[2] if fields2[2] else "N/A"
                m_players.append(m_player)
                m_onTime = fields2[3] if fields2[3] else "N/A"
                m_onTimes.append(m_onTime)
                m_backboard = fields2[11] if fields2[11] else "N/A"  # 如果字段为空，使用 "N/A" 作为占位符
                m_backboards.append(m_backboard)
                m_assist = fields2[14] if fields2[14] else "N/A"
                m_assists.append(m_assist)
                m_score = fields2[10] if fields2[10] else "N/A"
                m_scores.append(m_score)

                m_foul = fields2[8].split("-")[1] 
                m_fouls.append(m_foul)
                m_foulShot= fields2[18] if fields2[18] else "N/A"
                m_foulShots.append(m_foulShot)
            else:
                m_player = fields2[1] if fields2[1] else "N/A"
                m_players.append(m_player)
                m_onTime = fields2[2] if fields2[2] else "N/A"
                m_onTimes.append(m_onTime)
                m_backboard = fields2[10] if fields2[10] else "N/A"  # 如果字段为空，使用 "N/A" 作为占位符
                m_backboards.append(m_backboard)
                m_assist = fields2[13] if fields2[13] else "N/A"
                m_assists.append(m_assist)
                m_score = fields2[9] if fields2[9] else "N/A"
                m_scores.append(m_score)

                m_foul = fields2[7].split("-")[1] 
                m_fouls.append(m_foul)
                m_foulShot= fields2[17] if fields2[17] else "N/A"
                m_foulShots.append(m_foulShot)
        #print(data)
    print(m_fouls)
    driver.quit()

def lastGame():
    url = "https://pleagueofficial.com/schedule-regular-season/2022-23"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.text
        root = BeautifulSoup(data, "html.parser")

    ##################  近期完賽賽事 ################

    main_teams = root.select('span.PC_only.fs14')


    guest_team = []
    master_team = []


    for i in range(len(main_teams)):
        team = main_teams[i].get_text()
        
        if i % 2 == 0:
            guest_team.append(team)
        else:
            master_team.append(team)


    date_elements = root.find_all('div', class_='match_row_datetime')
    dates = []
    days = []
    times = []

    for element in date_elements:
        
        date_element = element.find('h5', class_='fs16')
        date = date_element.get_text() if date_element else ""

        day_element = element.find('h5', class_='fs12')
        day = day_element.get_text() if day_element else ""

        time_element = element.find('h6', class_='fs12')
        time = time_element.get_text() if time_element else ""

        dates.append(date)
        days.append(day)
        times.append(time)


    location_elements = root.find_all('h5', class_='fs12 mb-0')
    locations=[]
    for location in location_elements:
        locations.append(location.string)

    gameId_elements = root.find_all('h5', class_='fs14 mb-2')
    gameIds=[]
    for gameId in gameId_elements:
        gameIds.append(gameId.string)
    print(gameIds)
#OnGame()
##################  近期完賽賽事-數據 ################

def lastGameContent():
    url = "https://pleagueofficial.com/game/197"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.text
        root = BeautifulSoup(data, "html.parser")

    guestQ1 = root.find('td', id="q1_away").string
    guestQ2 = root.find('td', id="q2_away").string
    guestQ3 = root.find('td', id="q3_away").string
    guestQ4 = root.find('td', id="q4_away").string
    guestFinal = root.find('td', class_="score_away").string

    masterQ1 = root.find('td', id="q1_home").string
    masterQ2 = root.find('td', id="q2_home").string
    masterQ3 = root.find('td', id="q3_home").string
    masterQ4 = root.find('td', id="q4_home").string
    masterFinal = root.find('td', class_="score_home").string

    ################ 球員 #########################
 
def getPlayer():
    cur=con.cursor()  
    cur.execute("SELECT*FROM player")
    result=cur.fetchall()
    response_data_list = []
    for i in result:
        response_data = {
        "backNumber": i[0],
        "platerNAme": i[1],
        "p_team":i[2],
        "p_counts": i[3],
        "p_time": i[4],
        "point2": i[5],
        "point3":i[6],
        "p_foulShots": i[7],
        "p_scores": i[8],
        "p_backboards": i[9],
        "p_assists": i[10],
        "p_intercept": i[11],
        "p_miss": i[12],
        "p_foul": i[13],
        "nickNmae": i[14]
    }
        response_data_list.append(response_data)

    json_data = json.dumps(response_data_list, ensure_ascii=False).encode("utf-8")
    response = Response(json_data, content_type="application/json")
    print(response_data_list)
    return response


 ################ 喜愛球員 #########################
 
def getFavouritePlayer():
    userId=session.get("userId")
    cur=con.cursor()  
    cur.execute("SELECT*FROM likePlayer WHERE userId=%s",(userId,))
    result=cur.fetchall()
    response_data_list = []
    for i in result:
        response_data = {
        "backNumber": i[0],
        "platerNAme": i[1],
        "p_team":i[2],
        "p_counts": i[3],
        "p_time": i[4],
        "point2": i[5],
        "point3":i[6],
        "p_foulShots": i[7],
        "p_scores": i[8],
        "p_backboards": i[9],
        "p_assists": i[10],
        "p_intercept": i[11],
        "p_miss": i[12],
        "p_foul": i[13],
        "nickNmae": i[14]
    }
        response_data_list.append(response_data)

    json_data = json.dumps(response_data_list, ensure_ascii=False).encode("utf-8")
    response = Response(json_data, content_type="application/json")
    print(response_data_list)
    return response

################ 完賽 (只抓最上面一筆資料）#########################

def goOverGame():

    passed_tab = root.find("a", id="is-passed-tab")

    completed_matches_text = passed_tab.get_text()
    text_parts = completed_matches_text.split('(')
    if len(text_parts) >= 1:
        completed_matches_text = text_parts[0]
    print(completed_matches_text)

    url = "https://pleagueofficial.com/schedule-regular-season/2023-24"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.text
        root = BeautifulSoup(data, "html.parser")
    
    gameId=root.find("h5",class_="fs14 mb-2")
    gameIds=gameId.string

    cur=con.cursor()
    cur.execute("SELECT gameNumber FROM regular_season24 WHERE gameId=%s",(gameIds,))
    result=cur.fetchone()[0]
def goOverGameDetails():
    url = "https://pleagueofficial.com/schedule-regular-season/2023-24"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.text
        root = BeautifulSoup(data, "html.parser")
    
    gameId=root.find("h5",class_="fs14 mb-2")
    gameIds=gameId.string

    cur=con.cursor()
    cur.execute("SELECT gameNumber FROM regular_season24 WHERE gameId=%s",(gameIds,))
    result=cur.fetchone()[0]

    if result:
        nextLink="https://pleagueofficial.com/game/"+str(result)
        
        headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        response = requests.get(nextLink, headers=headers)
        
        if response.status_code == 200:
            data = response.text
            root = BeautifulSoup(data, "html.parser")
            guestQ1 = root.find('td', id="q1_away").string
            guestQ2 = root.find('td', id="q2_away").string
            guestQ3 = root.find('td', id="q3_away").string
            guestQ4 = root.find('td', id="q4_away").string
            guestFinal = root.find('td', class_="score_away").string

            masterQ1 = root.find('td', id="q1_home").string
            masterQ2 = root.find('td', id="q2_home").string
            masterQ3 = root.find('td', id="q3_home").string
            masterQ4 = root.find('td', id="q4_home").string
            masterFinal = root.find('td', class_="score_home").string

            game_state = root.find('span', class_="badge badge-secondary").string
            
            okStatus="已完賽"
            if game_state is okStatus:
                print("ok")
                #cur.execute("INSERT INTO over_game(gameId,guestQ1,guestQ2,guestQ3,guestQ4,guestFinal,masterQ1,masterQ2,masterQ3,masterQ4,masterFinal) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            #,(gameIds,gameId,guestQ1,guestQ2,guestQ3,guestQ4,guestFinal,masterQ1,masterQ2,masterQ3,masterQ4,masterFinal))
                driver=webdriver.Chrome(options=options)

                driver.get(nextLink)  # 替换为实际的页面 URL

                import time
                time.sleep(1) 

                table_rows = driver.find_elements(By.CSS_SELECTOR, "table#away_table tbody tr")

                g_backnumbers=[]
                g_players=[]
                g_onTimes=[]
                g_backboards=[]
                g_assists=[]
                g_scores=[]

                g_fouls=[]
                g_foulShots=[]
                for row in table_rows:
                    data = row.text
                    fields = data.split()
                    if len(fields) >= 15:
                        backnumber = fields[0] if fields[0] else "N/A"
                        g_backnumbers.append(backnumber)
                        if "〇" in data:
                            g_player = fields[2] if fields[2] else "N/A"
                            g_players.append(g_player)
                            g_onTime = fields[3] if fields[3] else "N/A"
                            g_onTimes.append(g_onTime)
                            g_backboard = fields[11] if fields[11] else "N/A"  # 如果字段为空，使用 "N/A" 作为占位符
                            g_backboards.append(g_backboard)
                            g_assist = fields[14] if fields[14] else "N/A"
                            g_assists.append(g_assist)
                            g_score = fields[10] if fields[10] else "N/A"
                            g_scores.append(g_score)

                            g_foul = fields[8].split("-")[1] 
                            g_fouls.append(g_foul)
                            g_foulShot= fields[18] if fields[18] else "N/A"
                            g_foulShots.append(g_foulShot)
                        else:
                            g_player = fields[1] if fields[1] else "N/A"
                            g_players.append(g_player)
                            g_onTime = fields[2] if fields[2] else "N/A"
                            g_onTimes.append(g_onTime)
                            g_backboard = fields[10] if fields[10] else "N/A"  # 如果字段为空，使用 "N/A" 作为占位符
                            g_backboards.append(g_backboard)
                            g_assist = fields[13] if fields[13] else "N/A"
                            g_assists.append(g_assist)
                            g_score = fields[9] if fields[9] else "N/A"
                            g_scores.append(g_score)

                            g_foul = fields[7].split("-")[1] 
                            g_fouls.append(g_foul)
                            g_foulShot= fields[17] if fields[17] else "N/A"
                            g_foulShots.append(g_foulShot)

                table_master = driver.find_elements(By.CSS_SELECTOR, "table#home_table tbody tr")

                m_backnumbers=[]
                m_players=[]
                m_onTimes=[]
                m_backboards=[]
                m_assists=[]
                m_scores=[]

                m_fouls=[]
                m_foulShots=[]
                for row2 in table_master:
                    data2 = row2.text
                    fields2 = data2.split()
                    if len(fields2) >= 15:
                        backnumber = fields2[0] if fields2[0] else "N/A"
                        m_backnumbers.append(backnumber)
                        if '〇' in data2:
                            m_player = fields2[2] if fields2[2] else "N/A"
                            m_players.append(m_player)
                            m_onTime = fields2[3] if fields2[3] else "N/A"
                            m_onTimes.append(m_onTime)
                            m_backboard = fields2[11] if fields2[11] else "N/A"  # 如果字段为空，使用 "N/A" 作为占位符
                            m_backboards.append(m_backboard)
                            m_assist = fields2[14] if fields2[14] else "N/A"
                            m_assists.append(m_assist)
                            m_score = fields2[10] if fields2[10] else "N/A"
                            m_scores.append(m_score)

                            m_foul = fields2[8].split("-")[1] 
                            m_fouls.append(m_foul)
                            m_foulShot= fields2[18] if fields2[18] else "N/A"
                            m_foulShots.append(m_foulShot)
                        else:
                            m_player = fields2[1] if fields2[1] else "N/A"
                            m_players.append(m_player)
                            m_onTime = fields2[2] if fields2[2] else "N/A"
                            m_onTimes.append(m_onTime)
                            m_backboard = fields2[10] if fields2[10] else "N/A"  # 如果字段为空，使用 "N/A" 作为占位符
                            m_backboards.append(m_backboard)
                            m_assist = fields2[13] if fields2[13] else "N/A"
                            m_assists.append(m_assist)
                            m_score = fields2[9] if fields2[9] else "N/A"
                            m_scores.append(m_score)

                            m_foul = fields2[7].split("-")[1] 
                            m_fouls.append(m_foul)
                            m_foulShot= fields2[17] if fields2[17] else "N/A"
                            m_foulShots.append(m_foulShot)
                    #print(data)
                print(m_fouls)
                driver.quit()
            else:print("Not Start")
                        #print(guestQ1)
def Gamed():
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    # 启动浏览器
    driver = webdriver.Chrome()  # 请根据您的浏览器选择合适的驱动程序

    # 打开网页
    url = "https://pleagueofficial.com/schedule-regular-season/2022-23"
    driver.get(url)

    # 找到"已完成賽事"标签并点击
    passed_tab = driver.find_element(By.ID, "is-passed-tab")
    passed_tab.click()

    import time
    time.sleep(1)

 
    match_id = driver.find_element(By.CSS_SELECTOR, ".fs14.mb-2").text
    #print("比赛ID:", match_id)

    # 关闭浏览器
    driver.quit()
    cur=con.cursor()
    cur.execute("SELECT gameNumber FROM regular_season24 WHERE gameId=%s",(match_id,))
    result=cur.fetchone()[0]
    print(match_id)
    if result:
        nextLink="https://pleagueofficial.com/game/"+str(result)
        
        headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        response = requests.get(nextLink, headers=headers)
        
        if response.status_code == 200:
            data = response.text
            root = BeautifulSoup(data, "html.parser")
            guestQ1 = root.find('td', id="q1_away").string
            guestQ2 = root.find('td', id="q2_away").string
            guestQ3 = root.find('td', id="q3_away").string
            guestQ4 = root.find('td', id="q4_away").string
            guestFinal = root.find('td', class_="score_away").string

            masterQ1 = root.find('td', id="q1_home").string
            masterQ2 = root.find('td', id="q2_home").string
            masterQ3 = root.find('td', id="q3_home").string
            masterQ4 = root.find('td', id="q4_home").string
            masterFinal = root.find('td', class_="score_home").string

            game_state = root.find('span', class_="badge badge-secondary").string
            print("ok")

Gamed()

  