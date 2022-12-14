from retry import retry
import tweepy
from tweepy import TweepError
from pprint import pprint


class TwitterWrapper:
    '''
    Initial Setting
    '''
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, 
                 ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API=None):

        # CONSUMER_KEY = os.environ.get('CONSUMER_KEY') if CONSUMER_KEY is None else CONSUMER_KEY
        # CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') if CONSUMER_SECRET is None else CONSUMER_SECRET
        # ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') if ACCESS_TOKEN is None else ACCESS_TOKEN
        # ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET') if ACCESS_TOKEN_SECRET is None else ACCESS_TOKEN_SECRET
        
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        if API is None:
            self.API = tweepy.API(self.auth)
        else:
            self.API = API
        
    @property
    def img_path(self):
        return self.__img_path

    @img_path.setter
    def imp_path(self, img_path):
        self.__img_path = img_path

    def tweet(self, message: str):
        """ツイート
        Args:
            message (str): ツイートするメッセージ

        Returns:
            bool: 成功(True) or 失敗(False)
        """
        # ツイート内容
        TWEET_TEXT = message
        try :
            tweet_status = self.API.update_status(TWEET_TEXT)
            if tweet_status == 200 : # 成功
                # pprint(tweet_status)
                return True
            else:
                pprint(tweet_status)
                return False
        except tweepy.TweepError as err:
            return False
        except Exception as err:
            return False

    def tweetWithImg(self, message, img_path=None):
        """
        ツイート 画像付き 
        """
        FILE_NAME = img_path
        try :
            # ↓添付したい画像のファイル名
            status = self.API.update_with_media(filename=FILE_NAME, status=message)
            if status == 200: # 成功
                pprint("Succeed!")
                return True
            else:
                return False

        except tweepy.TweepError as err:
            pprint(err)
            return False
        except Exception as err:
            pprint(err)
            return False
        
    @retry(exceptions=TweepError, tries=3, delay=2)
    def tweetWithImg(self, message:str, img:str):
        """画像つきツイート

        Args:
            message (str): ツイートするメッセージ
            img (str): 画像のパス

        Returns:
            tweepy : ツイート結果を返す
        """
        FILE_NAME = img
        # try :
        # ↓添付したい画像のファイル名
        return self.API.update_with_media(filename=FILE_NAME, status=message)
        #     if status == 200: #成功
        #         pprint("Succeed!")
        #         return True
        #     else:
        #         return False

        # except TweepError as err:
        #     pprint(err)
        #     return False
        # except Exception as err:
        #     pprint(err)
        #     return False
            
    def get_user(self, twitter_name: str):
        return self.API.get_user()