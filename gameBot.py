import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

from flask import *
from datetime import datetime, timedelta
import mysql.connector.pooling
import requests 
import sys

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
SECRET_KEY =config('SECRET_KEY')
app.secret_key=SECRET_KEY
app.permanent_session_lifetime = timedelta(hours=1)

DB_HOST=config('DB_HOST')
DB_PASSWORD=config('DB_PASSWORD')
dbconfig = {
    "database": "PLG",
    "user": "root",
    "host": DB_HOST,
    "password": DB_PASSWORD,
    "port":"3306"
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="myPLG",**dbconfig)
con = connection_pool.get_connection()
def callMessage(master,guest,tmonth,tday,week,time,locat):
    print("Time to send notification!")
    #userId = sys.argv[1]
    channel_access_token='+FQbYuiytVnAZ8OCDlak5nPWfSwi/8nzn04dmi6CoDACiqLGkb2xMS0rnoAeBO26FXKzjc5yc7g/ngrgFPTc0V+dfgU5VzTOdz8i4rkfCUfSsHdFQleWJDqH0QgSx/xfOdOHt81phIt8ldiPv7HGkwdB04t89/1O/w1cDnyilFU='
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {channel_access_token}"}

    data = {
        "to": "U9ea762678a659743a8517538a38db556",
        "messages": [
             {
                "type": "text",
                "text": "賽事即將到來囉，"+ str(tmonth)+"/"+str(tday)+"，"+str(time)+"，"+str(week)+"，"+str(master) + "v.s" +str(guest) +str(locat)+"，趕快關注！"
             },
         ]
        }
   
    print(data)
    response = requests.post(url, json=data, headers=headers)

    print(response.status_code)
    print(response.json())

def schedule_notification(theLastGame):
    year, month, day = map(int, (theLastGame[3], theLastGame[4], theLastGame[5]))
    master=theLastGame[2]
    guest=theLastGame[1]
    tmonth=theLastGame[4]
    tday=theLastGame[5]
    time=theLastGame[6]
    week=theLastGame[7]
    locat=theLastGame[8]
    game_date = datetime(year, month, day, hour=14, minute=0)
    o_date = datetime(year, month, day-3 )
    print("game_date" + str(game_date))
    print(o_date)

    current_time = datetime.now()
    time_difference = game_date - current_time
    print("time_difference" + str(time_difference))

    if time_difference.total_seconds() < 38400:
        print("time_difference"+str(time_difference.total_seconds()))
        callMessage(master,guest,tmonth,tday,week,time,locat)
    else:
        print("not yet")
        

def getDate():
    cur = con.cursor()
    time = datetime.now().strftime("%Y-%m-%d")
    d0 = time.split("-")[0]
    d1 = time.split("-")[1]
    d2 = time.split("-")[2]
    print(d0,d1,d2)
    cur.execute("SELECT * FROM regular_season24 WHERE year >= %s AND month >= %s AND day>=%s limit 1",
        (d0, d1, d2))
    result = cur.fetchall()
    theLastGame = result[0]
    schedule_notification(theLastGame)
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=18, minute=40)
print(trigger)
scheduler.add_job(getDate, trigger=trigger)

scheduler.start()

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
   
    scheduler.shutdown()
