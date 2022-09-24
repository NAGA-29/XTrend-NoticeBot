from chalice import Chalice, Cron, Rate
import datetime
import os
from pprint import pprint
import tweepy

'''origin'''
from chalicelib import Hololive
from chalicelib import TwitterWrapper, NewsAPIWrapper, BitlyWrapper

### initialize
# # 本番アカウント
# # ###############################################################################
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
#bitly本番アカウント
BITLY_ACCESS_TOKEN = os.environ.get('BITLY_ACCESS_TOKEN')
# News API
NEWS_API_KEY = os.environ.get('NEWS_API')

app = Chalice(app_name='HoloNews-NoticeBot')

# @app.schedule(Rate(10, unit=Rate.MINUTES))
# @app.schedule('cron(10 22/7 * * ? *)')
@app.schedule('cron(0 22 * * ? *)')
def Main(event):
    # 日本時間 - 7日前
    base_toDay = datetime.date.today() - datetime.timedelta(days=1) 
    base_fromDay = base_toDay - datetime.timedelta(days=7)
    toDay =  base_toDay.strftime('%Y-%m-%d')
    fromDay =  base_fromDay.strftime('%Y-%m-%d')
    
    tw = TwitterWrapper(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    bit = BitlyWrapper(BITLY_ACCESS_TOKEN)
    news = NewsAPIWrapper(NEWS_API_KEY)

    news = news.NewsAPIResearch_Every(fromDay, toDay)
    for key, val in news.items():
        title = val[0]
        short_URL = bit.get_shortenURL(key)
    message = f'Hololive News!!💖\n\n{title}\n{short_URL}\n#hololive'
    tw.tweet(message)