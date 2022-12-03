from chalice import Chalice, Cron, Rate
import boto3

import datetime
import os
from pprint import pprint
import sys
import tweepy

'''origin'''
from chalicelib import app
from chalicelib import TwitterWrapper
from chalicelib import Hololive
from chalicelib import TrendWatcher
from chalicelib import PKL_BY_BOT3

import pymysql

# 本番アカウント
CONSUMER_KEY = app.CONSUMER_KEY
CONSUMER_SECRET = app.CONSUMER_SECRET
ACCESS_TOKEN = app.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = app.ACCESS_TOKEN_SECRET

ENDPOINT = app.RDS_HOST
PORT = app.RDS_PORT
USER = app.RDS_USER
PASS = app.RDS_PASS
REGION = app.REGION
DBNAME = app.RDS_DB

BUCKET_NAME = app.BUCKET_NAME
TREND_SAVE_FILE = app.TREND_SAVE_FILE

app = Chalice(app_name='HoloTrend-NoticeBot')

@app.schedule(Rate(15, unit=Rate.MINUTES))
def Main(event):
    tw = TwitterWrapper(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET)
    
    pkl_by_bot3 = PKL_BY_BOT3(BUCKET_NAME)
    trend_file = pkl_by_bot3.read_pkl(TREND_SAVE_FILE)
    print(trend_file)
    # trend = TrendWatcher(twitter_api=tw)
    # trend.main(trend=trend_file)
    
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=PASS,
                                db=DBNAME, charset='utf8mb4', port=int(PORT),
                                connect_timeout=5)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        pprint(e)
        sys.exit()

    print("SUCCESS: Connection to RDS MySQL instance succeeded")
    with conn.cursor() as cursors:
        cursors.execute('show databases')
        pprint(cursors.fetchall())
    conn.close()
    conn = None
    print('END!')
