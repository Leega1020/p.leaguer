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
def Gamed():
    driver = webdriver.Chrome()  # 请根据您的浏览器选择合适的驱动程序
    driver.get("https://pleagueofficial.com/game/316")

    # 找到"數據"链接并点击
    data_link = driver.find_element(By.LINK_TEXT, "數據")
    data_link.click()

    # 继续提取下一页的数据
    guestQ1 = driver.find_element(By.ID, "q1_away").text
    guestQ2 = driver.find_element(By.ID, "q2_away").text
    guestQ3 = driver.find_element(By.ID, "q3_away").text
    guestQ4 = driver.find_element(By.ID, "q4_away").text
    guestFinal = driver.find_element(By.CLASS_NAME, "score_away").text

    # 关闭浏览器
    driver.quit()

    print(guestQ1, guestQ2, guestQ3, guestQ4, guestFinal)

Gamed()