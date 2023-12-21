import time
import ssl
import requests
from bs4 import BeautifulSoup
from flask import Flask
from decouple import config
from threading import Thread
import mysql.connector.pooling
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

SECRET_KEY = config('SECRET_KEY')
APP_ID = config('APP_ID')
APP_KEY = config('APP_KEY')
PARTNER_KEY = config('PARTNER_KEY')
DB_HOST=config('DB_HOST')
DB_PASSWORD=config('DB_PASSWORD')
dbconfig = {
    "database": "PLG",
    "user": "root",
    "host": DB_HOST,
    "password": DB_PASSWORD,
    "port":"3306"
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="myPLG", **dbconfig)
con = connection_pool.get_connection()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

scheduler = BackgroundScheduler()
scheduler.daemonic = True 

def get_match_id(driver):
    url = "https://pleagueofficial.com/schedule-regular-season/2023-24"
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "is-passed-tab")))

    passed_tab = driver.find_element(By.ID, "is-passed-tab")
    passed_tab.click()

    time.sleep(1)

    pass_count_element = driver.find_element(By.CLASS_NAME, "pass-count")
    pass_count_text = pass_count_element.text
    print(pass_count_text)

    match_id_elements = driver.find_elements(By.CSS_SELECTOR, ".fs14.mb-2")
    if len(match_id_elements) >= 2:
        second_element_text = match_id_elements[int(pass_count_text) - 1].text
        print(second_element_text)

    return second_element_text

def execute_game():
    try:
        with webdriver.Chrome(options=options) as driver:
            driver.set_window_size(1920, 1080)
            match_id = get_match_id(driver)

            cur = con.cursor()
            cur.execute("SELECT gameNumber FROM regular_season24 WHERE gameId=%s", (match_id,))
            result = cur.fetchone()[0]
            print(match_id)

            cur.execute("SELECT gameId FROM today_game WHERE gameId=%s", (match_id,))
            founded_game = cur.fetchone()

            if founded_game is None:
                next_link = "https://pleagueofficial.com/game/" + str(result)
                print(next_link)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                }

                response = requests.get(next_link, headers=headers)

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

                    #game_state = root.find('span', class_="badge badge-secondary").string
                    #print(guestQ1,guestQ2,guestQ3,guestQ4,masterQ1,masterQ2,masterQ3,masterQ4)
                    driver=webdriver.Chrome(options=options)

                    driver.get(next_link) 

                    import time
                    time.sleep(1) 

                    tfoot_table_m=[]
                    tfoot_table_g=[]
                    tfoot_master = driver.find_elements(By.CSS_SELECTOR, "table#home_table tfoot tr td")
                    for td_element in tfoot_master:
                        text_content = td_element.get_attribute("textContent")
                        tfoot_table_m.append(text_content)
                    #print(tfoot_table_m)
                    foulshot_m=tfoot_table_m[8].split("-")[1]
                    foul_m=tfoot_table_m[18]
                    print(foulshot_m,foul_m)

                    tfoot_guest = driver.find_elements(By.CSS_SELECTOR, "table#away_table tfoot tr td")
                    for td_element in tfoot_guest:
                        text_content = td_element.get_attribute("textContent")
                        tfoot_table_g.append(text_content)
                    #print(tfoot_table_m)
                    foulshot_g=tfoot_table_g[8].split("-")[1]
                    foul_g=tfoot_table_g[18]
                    print(foulshot_g,foul_g)

                    g_all_data = []
                    m_all_data = []
                    table_rows = driver.find_elements(By.CSS_SELECTOR, "table#away_table tbody tr")

                    for row in table_rows:
                        data = row.text
                        fields = data.split()
                        if len(fields) >= 15:
                            player_data = {}
                            player_data["backnumber"] = fields[0] if fields[0] else "N/A"
                            if "〇" in data:
                                player_data["player"] = fields[2] if fields[2] else "N/A"
                                player_data["onTime"] = fields[3] if fields[3] else "N/A"
                                player_data["backboard"] = fields[11] if fields[11] else "N/A"
                                player_data["assist"] = fields[14] if fields[14] else "N/A"
                                player_data["score"] = fields[10] if fields[10] else "N/A"
                                player_data["foul"] = fields[8]
                                player_data["foulShot"] = fields[18] if fields[18] else "N/A"
                            else:
                                player_data["player"] = fields[1] if fields[1] else "N/A"
                                player_data["onTime"] = fields[2] if fields[2] else "N/A"
                                player_data["backboard"] = fields[10] if fields[10] else "N/A"
                                player_data["assist"] = fields[13] if fields[13] else "N/A"
                                player_data["score"] = fields[9] if fields[9] else "N/A"
                                player_data["foul"] = fields[7]
                                player_data["foulShot"] = fields[17] if fields[17] else "N/A"

                            g_all_data.append(player_data)

                    # 处理 home_table
                    table_master = driver.find_elements(By.CSS_SELECTOR, "table#home_table tbody tr")

                    for row2 in table_master:
                        data2 = row2.text
                        fields2 = data2.split()
                        if len(fields2) >= 15:
                            player_data = {}
                            player_data["backnumber"] = fields2[0] if fields2[0] else "N/A"
                            if '〇' in data2:
                                player_data["player"] = fields2[2] if fields2[2] else "N/A"
                                player_data["onTime"] = fields2[3] if fields2[3] else "N/A"
                                player_data["backboard"] = fields2[11] if fields2[11] else "N/A"
                                player_data["assist"] = fields2[14] if fields2[14] else "N/A"
                                player_data["score"] = fields2[10] if fields2[10] else "N/A"
                                player_data["foul"] = fields2[8]
                                player_data["foulShot"] = fields2[18] if fields2[18] else "N/A"
                            else:
                                player_data["player"] = fields2[1] if fields2[1] else "N/A"
                                player_data["onTime"] = fields2[2] if fields2[2] else "N/A"
                                player_data["backboard"] = fields2[10] if fields2[10] else "N/A"
                                player_data["assist"] = fields2[13] if fields2[13] else "N/A"
                                player_data["score"] = fields2[9] if fields2[9] else "N/A"
                                player_data["foul"] = fields2[7]
                                player_data["foulShot"] = fields2[17] if fields2[17] else "N/A"

                            m_all_data.append(player_data)
                    #print(m_all_data[0]["backnumber"])
                    
                    cur.execute("INSERT INTO today_game(gameId,guestQ1,guestQ2,guestQ3,guestQ4,guestFinal,masterQ1,masterQ2,masterQ3,masterQ4,masterFinal,masterfoulshot,masterfoul,guestfoulshot,guestfoul) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (match_id,guestQ1,guestQ2,guestQ3,guestQ4,guestFinal,masterQ1,masterQ2,masterQ3,masterQ4,masterFinal,foulshot_m,foul_m,foulshot_g,foul_g))

                    con.commit()
                    for i in g_all_data:
                        cur.execute("INSERT INTO today_guest_player(gameId,backnumber,name,ontime,backboard,assist,score,foul,foulshot) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (match_id,i["backnumber"],i["player"],i["onTime"],i["backboard"],i["assist"],i["score"],i["foul"],i["foulShot"]))
                        con.commit()
                    for i in m_all_data:
                        cur.execute("INSERT INTO today_master_player(gameId,backnumber,name,ontime,backboard,assist,score,foul,foulshot) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (match_id,i["backnumber"],i["player"],i["onTime"],i["backboard"],i["assist"],i["score"],i["foul"],i["foulShot"]))
                        con.commit()
                    driver.quit()

                else:
                    print("Failed to retrieve game data")

            else:
                print("Game already inserted")

    except Exception as e:
        print(e)

    finally:
        if 'con' in locals():
            con.close()
            print("Database connection closed.")
        if 'connection_pool' in locals():
            connection_pool.close()
            print("Database connection pool closed.")

trigger = IntervalTrigger(seconds=10)
scheduler.add_job(execute_game, trigger)

scheduler.start()

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    if 'connection_pool' in locals():
        connection_pool.close()
        print("Database connection pool closed.")