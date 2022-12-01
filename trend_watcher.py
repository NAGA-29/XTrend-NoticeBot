from datetime import datetime
from datetime import datetime
from dotenv import load_dotenv
import os
from os.path import join, dirname
import pickle
from pprint import pprint
import re
import sys
import tweepy

from chalicelib import TwitterWrapper

'''
original
'''
from chalicelib import app
# sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from chalicelib import session
from chalicelib import KeepWatch
from chalicelib import NowLiveKeepWatch

TWITTER_SCREEN_NAME = os.environ.get('TWITTER_SCREEN_NAME')
WOEID_DICT = os.environ.get('WOEID_DICT')
DEFAULT_CHECK_LIST = os.environ.get('DEFAULT_CHECK_LIST')
CHECK_LIST = os.environ.get('CHECK_LIST')
NOTIFICATION_SEC = os.environ.get('NOTIFICATION_SEC')
class TrendWatcher:
    def __init__(self, twitter_api:TwitterWrapper, lineAPI=None, logger=None, trend_save_file:str=None):
        self.TWITTER_API        = twitter_api
        self.SCREEN_NAME        = TWITTER_SCREEN_NAME # @usernameの自分のusername
        self.WOEID_DICT         = WOEID_DICT
        self.DEFAULT_CHECK_LIST = DEFAULT_CHECK_LIST
        self.CHECK_LIST         = CHECK_LIST
        self._NOTIFICATION_SEC  = NOTIFICATION_SEC   # 通知基準 60分
        self.TREND_SAVE_FILE    = '/Users/nagaki/Documents/naga-sample-code/python/MyHololiveProject_stg/My_Hololive_Project/config/trend_log_JP.pkl'
        
        if trend_save_file != None:
            self.TREND_SAVE_FILE = trend_save_file
        self.logger = logger

    def hashtag_extract(self, table:str, text:str):
        """テキスト(タイトル)からハッシュタグを抽出する

        Args:
            text (str): テキスト(タイトル)

        Returns:
            hashtags(list[str]): 検索候補のハッシュタグ
        """
        tags = ''
        hashtags = []
        # keep_watch_db = session.query(KeepWatch).all()
        now_live_keep_watch_db = session.query(NowLiveKeepWatch).filter(NowLiveKeepWatch.belongs == 'hololive').all()
        for data in now_live_keep_watch_db:
            # tags = re.findall(r"([#＃][^#\s]*?)[\/\／\【\】\(\)\[\]　 \「\」]", data.title)
            tags = re.findall(r"([#＃][^#\s]*?)[\/\／\【\】\(\)\[\]　 \「\」]", data.title)
            for tag in tags:
                hashtags.append(re.sub('＃', '#', tag))
        return hashtags

    def check_notice_time(self, last_notice_time:str, sec:int):
        return (datetime.now() - last_notice_time).seconds >= sec

    def main(self, tables=[], default=False):
        """

        Args:
            default (bool, optional): _description_. Defaults to False.
        """
        Read_Trend_log = {}
        Write_Trend_log = {}
        New_Trend = {}
        target_trend = self.hashtag_extract()
        
        if not target_trend and not default:
            return

        if default:
            target_trend = target_trend + self.DEFAULT_CHECK_LIST
        print(target_trend)

        try:
            with open(self.TREND_SAVE_FILE, 'rb') as f:
                Read_Trend_log = pickle.load(f)
                pprint(Read_Trend_log)
        except EOFError as err:
            # print(f'EOFError on load pickle file: {err}')
            self.logger.error(f'EOFError on load pickle file: {err}')
            
        for place, woeid in self.WOEID_DICT.items():
            trends = self.TWITTER_API.trends_place(woeid)

        rank = 0
        Reset_flag = True
        for tr in trends[0]['trends']:
            # pprint(tr)
            rank += 1
            # トレンドにキーワ-ドが出現した場合
            if tr['name'] in target_trend:
                tr['rank'] = rank
                tr['place'] = place
                name = tr['name']
                New_Trend[name] = tr #トレンドを追加
                print(f'{name}がトレンドにランクインしました')
                Reset_flag = False

        if Reset_flag:
            # キーワ-ドが出現しなかったらリセット
            Read_Trend_log = []

        try:
            if Read_Trend_log: #前回のトレンドがある場合
                for key, value in Read_Trend_log.items():
                    message = f'Hololive Trend (β ver)\n\n'
                    message += f'{key}\n\n'

                    # 順位が1位になったか判定
                    if value['rank'] == 1:
                        Write_Trend_log[key] = New_Trend[key]
                        message += f'twitterトレンドランキング1位獲得!\n'
                        if self.check_notice_time(tr['last_notice_time'], self._NOTIFICATION_SEC):
                            # FIXME:
                            Write_Trend_log[key]['last_notice_time'] = datetime.now()
                            self.tweet(self.TWITTER_API, message)
                        continue

                    # 新規
                    if key not in New_Trend:
                        message += '新着トレンド入りです!\n'
                        Write_Trend_log[key] = New_Trend[key]
                        self.tweet(self.TWITTER_API, message)
                        print(f'{key}が新着トレンド入り')
                        continue

                    # 前回より順位上昇しているか判定
                    if value['rank'] > New_Trend[key]['rank']:
                        message += f'ランキング上昇!\n'
                        if self.check_notice_time(tr['last_notice_time'], 0):
                            # FIXME:
                            Write_Trend_log[key]['last_notice_time'] = datetime.now()
                            Write_Trend_log[key] = New_Trend[key]
                            self.tweet(self.TWITTER_API, message)
                            print(f'{key}がランキング上昇中!')
                        continue

                    # 前回より順位が急上昇しているか判定
                    if value['rank'] > New_Trend[key]['rank'] \
                            and value['rank'] - New_Trend[key]['rank'] >= 9:
                        message += f'ランキング急上昇中!\n'
                        Write_Trend_log[key] = New_Trend[key]
                        self.tweet(self.TWITTER_API, message)
                        print(f'{key}がランキング上昇中!')

            else: #前回のトレンドがない場合
                for key, value in New_Trend.items():
                    message = f'Hololive Trend (β ver)\n\n'
                    message += f'{key}\n\n'

                    # 順位が1位
                    if value['rank'] == 1:
                        Write_Trend_log[key] = New_Trend[key]
                        message += '新着トレンド入りです!\n'
                        message += f'twitterトレンドランキング1位獲得!\n'
                        # FIXME:
                        tr['last_notice_time'] = datetime.now()
                        self.tweet(self.TWITTER_API, message)
                        continue

                    # 新規
                    Write_Trend_log[key] = New_Trend[key]
                    message += '新着トレンド入りです!\n'
                    message += f'ランキング{value["rank"]}位獲得!\n'
                    self.tweet(self.TWITTER_API, message)

        # try:
            # pklファイルに保存
            pprint('pklファイルに保存')
            with open(self.TREND_SAVE_FILE, 'wb') as f:
                pickle.dump(Write_Trend_log, f)
        except Exception as err:
            print(f'ERROR on save pickle file: {err}')
            # self.logger.error(f'ERROR on save pickle file: {err}')