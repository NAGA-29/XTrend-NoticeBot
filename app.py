from chalice import Chalice, Cron, Rate
import datetime
import os
from pprint import pprint
import tweepy
import boto3
import sys
'''origin'''
from chalicelib import Hololive
from chalicelib import TwitterWrapper
import trend_watcher

from pprint import pprint 

import pymysql

### initialize
# # 本番アカウント
# # ###############################################################################
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

app = Chalice(app_name='HoloTrend-NoticeBot')

# host = os.environ['RDS_HOST']
# user = os.environ['RDS_USER']
# password = os.environ['RDS_PASS']
# db = os.environ['RDS_DB']

# connection = pymysql.connect(host=host, user=user, password=password, database=db, charset='utf8mb4', port=3306,)

ENDPOINT = os.environ['RDS_HOST']
PORT = "3306"
USER = os.environ['RDS_USER']
PASS = os.environ['RDS_PASS']
REGION = "ap-northeast-1"
DBNAME = os.environ['RDS_DB']

@app.schedule(Rate(10, unit=Rate.MINUTES))
def Main(event):
    tw = TwitterWrapper(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # news = news.NewsAPIResearch_Every(fromDay, toDay)
    # for key, val in news.items():
    #     title = val[0]
    #     short_URL = bit.get_shortenURL(key)
    # message = f'Hololive News!!💖\n\n{title}\n{short_URL}\n#hololive'
    # tw.tweet(message)
    # trend_watcher()
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=PASS, db=DBNAME, charset='utf8mb4', port=3306, connect_timeout=5)
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

    # item_count = 0
    # with conn.cursor() as cur:
    #     cur.execute("create table Employee ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")
    #     cur.execute('insert into Employee (EmpID, Name) values(1, "Joe")')
    #     cur.execute('insert into Employee (EmpID, Name) values(2, "Bob")')
    #     cur.execute('insert into Employee (EmpID, Name) values(3, "Mary")')
    #     conn.commit()
    #     cur.execute("select * from Employee")
    #     for row in cur:
    #         item_count += 1
    #         # logger.info(row)
    #         print(row)
    # conn.commit()

    # return "Added %d items from RDS MySQL table" %(item_count)
