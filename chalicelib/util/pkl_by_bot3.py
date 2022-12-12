'''
s3のpklファイルを扱うためのクラス
'''
import boto3
import pickle


class PickleHandler:
    def __init__(self, bucket_name):
        self.BUCKET_NAME = bucket_name

    def __get_s3object(self, object_key_name):
        s3 = boto3.resource('s3', region_name='ap-northeast-1')
        s3_object = s3.Object(self.BUCKET_NAME, object_key_name)
        return s3_object

    def read_pkl(self, object_key_name: str):
        """pklを読み込む

        Args:
            object_key_name (str): バケット内のpklファイルの名前

        Returns:
            pklファイルの中身
        """
        s3_object = self.__get_object(object_key_name).get()
        return pickle.loads(s3_object['Body'].read())

    def write_pkl(self, data, object_key_name: str):
        """pklファイルに書き込む

        Args:
            data (_type_): pklファイルに書き込むデータ
            object_key_name (str):  バケット内のpickleファイルの名前
        """
        pickle_byte_obj = pickle.dumps(data)
        s3_object = self.__get_object(object_key_name)
        s3_object.put(Body=pickle_byte_obj)

    def noticed_space_id_check(self, space_id, object_key_name):
        """pickleファイル内のnoticed_space_idリストに指定したIDが含まれるか確認する

        Args:
            space_id (int): 確認するID
            object_key_name (str): バケット内のpickleファイルの名前

        Returns:
            含まれる場合はTrue、含まれない場合はFalse
        """
        noticed_space_id_list = None
        try:
            noticed_space_id_list = self.read_pkl(object_key_name)
        except EOFError as err:
            print(f'EOFError on load pickle file: {err}')
                
        if space_id in noticed_space_id_list:
            return True
        else:
            return False
        
    def append_to_pickle(self, data, object_key_name, noticed_space_id: list):
        """pickleファイルにデータを追加する

        Args:
            data (_type_): pickleファイルに追加するデータ
            object_key_name (str): バケット内のpickleファイルの名前
            noticed_space_id (list): pickleファイル内に追加するデータのリスト

        Returns:
            None
        """
        noticed_space_id.append(data)
        pickle_byte_obj = pickle.dumps(noticed_space_id)
        s3_object = self.__get_object(object_key_name)
        s3_object.put(Body=pickle_byte_obj)







# def read_noticed_space_id(NOTICED_SPACE_FILE):
#     try:
#         with open(NOTICED_SPACE_FILE, 'rb') as f:
#             noticed_space_id_list = pickle.load(f)
#             return noticed_space_id_list
#     except EOFError as err:
#             print(f'EOFError on load pickle file: {err}')
