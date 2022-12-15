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
from chalicelib import session
from chalicelib import KeepWatch
from chalicelib import NowLiveKeepWatch
from .pickle_handler import PickleHandler

TWITTER_SCREEN_NAME = app.TWITTER_SCREEN_NAME
WOEID_DICT = app.WOEID_DICT
DEFAULT_CHECK_LIST = app.DEFAULT_CHECK_LIST
CHECK_LIST = app.CHECK_LIST
NOTIFICATION_SEC = app.NOTIFICATION_SEC
BUCKET_NAME = app.BUCKET_NAME
TREND_SAVE_FILE = app.TREND_SAVE_FILE


class TrendWatcher:
    def __init__(
                self, twitter_api: TwitterWrapper,
                logger=None,
                trend_save_file: str = None
                ) -> None:
        self.TWITTER_API = twitter_api.API
        self.SCREEN_NAME = TWITTER_SCREEN_NAME  # @usernameの自分のusername
        self.WOEID_DICT = WOEID_DICT
        self.DEFAULT_CHECK_LIST = DEFAULT_CHECK_LIST
        self.CHECK_LIST = CHECK_LIST
        self.NOTIFICATION_SEC = NOTIFICATION_SEC   # 通知基準 60分
        self.TREND_SAVE_FILE = TREND_SAVE_FILE
        
        if trend_save_file is not None:
            self.TREND_SAVE_FILE = trend_save_file
        self.logger = logger

    def hashtag_extract(self, texts: object):
        """テキスト(タイトル)からハッシュタグを抽出する

        Args:
            table (str): テーブル名
            text (str): テキスト(タイトル)

        Returns:
            hashtags(list[str]): 検索候補のハッシュタグ
        """
        tags = ''
        hashtags = []
        regex = r"([#＃][^#\s]*?)[\/\／\【\】\(\)\[\]　 \「\」]"

        for data in texts:
            tags = re.findall(regex, data.title)
            for tag in tags:
                hashtags.append(re.sub('＃', '#', tag))
        return hashtags

    def check_notice_time(self, last_notice_time: str, sec: int):
        return (datetime.now() - last_notice_time).seconds >= sec

    def main(self, trend, tables=[], default=False):
        """

        Args:
            default (bool, optional): _description_. Defaults to False.
        """
        Read_Trend_log = trend
        Write_Trend_log = {}
        New_Trend = {}
        
        now_live_keep_watch_db = session.query(NowLiveKeepWatch)\
            .filter(NowLiveKeepWatch.belongs == 'hololive')\
            .all()
        target_trend = self.hashtag_extract(now_live_keep_watch_db)
        
        if not target_trend and not default:
            return

        if default:
            target_trend = target_trend + self.DEFAULT_CHECK_LIST
        print(target_trend)

        try:
            pickle_handler = PickleHandler(BUCKET_NAME)
            # with open(self.TREND_SAVE_FILE, 'rb') as f:
            #     Read_Trend_log = pickle.load(f)
            Read_Trend_log = pickle_handler.read_pkl(TREND_SAVE_FILE)
            pprint(Read_Trend_log)
        except EOFError as err:
            print(f'EOFError on load pickle file: {err}')
            self.logger.error(f'EOFError on load pickle file: {err}')
            
        for place, woeid in self.WOEID_DICT.items():
            pprint(self.TWITTER_API)
            trends = self.TWITTER_API.trends_place(woeid)

        rank = 0
        Reset_flag = True
        for tr in trends[0]['trends']:
            rank += 1
            # トレンドにキーワ-ドが出現した場合
            if tr['name'] in target_trend:
                tr['rank'] = rank
                tr['place'] = place
                name = tr['name']
                New_Trend[name] = tr  # トレンドを追加
                print(f'{name}がトレンドにランクインしました')
                Reset_flag = False

        if Reset_flag:
            # キーワ-ドが出現しなかったらリセット
            Read_Trend_log = []

        try:
            if Read_Trend_log:  # 前回のトレンドがある場合
                for key, value in Read_Trend_log.items():
                    message = 'Hololive Trend (β ver)\n\n'
                    message += f'{key}\n\n'

                    # 順位が1位になったか判定
                    if value['rank'] == 1:
                        Write_Trend_log[key] = New_Trend[key]
                        message += 'twitterトレンドランキング1位獲得!\n'
                        if self.check_notice_time(tr['last_notice_time'], self.NOTIFICATION_SEC):
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
                        message += 'ランキング上昇!\n'
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
                        message += 'ランキング急上昇中!\n'
                        Write_Trend_log[key] = New_Trend[key]
                        self.tweet(self.TWITTER_API, message)
                        print(f'{key}がランキング上昇中!')

            else:  # 前回のトレンドがない場合
                for key, value in New_Trend.items():
                    message = "Hololive Trend (β ver)\n\n"
                    message += f'{key}\n\n'

                    # 順位が1位
                    if value['rank'] == 1:
                        Write_Trend_log[key] = New_Trend[key]
                        message += '新着トレンド入りです!\n'
                        message += 'twitterトレンドランキング1位獲得!\n'
                        # FIXME:
                        tr['last_notice_time'] = datetime.now()
                        self.tweet(self.TWITTER_API, message)
                        continue

                    # 新規
                    Write_Trend_log[key] = New_Trend[key]
                    message += '新着トレンド入りです!\n'
                    message += f'ランキング{value["rank"]}位獲得!\n'
                    self.tweet(self.TWITTER_API, message)

            # pklファイルに保存
            pprint('pklファイルに保存')
            # with open(self.TREND_SAVE_FILE, 'wb') as f:
            #     pickle.dump(Write_Trend_log, f)
            pickle_handler.write_pkl(Write_Trend_log, TREND_SAVE_FILE)
        except Exception as err:
            print(f'ERROR on save pickle file: {err}')
            # self.logger.error(f'ERROR on save pickle file: {err}')