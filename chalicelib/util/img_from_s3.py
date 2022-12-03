"""
s3のpklファイルを扱うためのクラス
"""
import base64
import boto3
import pickle


class IMG_FROM_S3:
    def __init__(self, bucket_name):
        self.BUCKET_NAME = bucket_name
        # self.OBJECT_KEY_NAME = object_key_name

    def __get_s3object(self, object_key_name):
        s3 = boto3.resource('s3')
        return s3.Object(self.BUCKET_NAME, object_key_name)
    
    def __get_bucket(self):
        """bucketを取得する

        Returns:
            
        """
        s3 = boto3.resource('s3')
        return s3.Bucket(self.BUCKET_NAME)

    def get_img_from_s3(self, filename: str, file_path: str):
        """s3から画像を取得する

        Args:
            filename (str): バケット内の画像のファイル名
            file_path (str): 保存先のパス
        """
        bucket = self.__get_bucket()
        bucket.download_file(filename, file_path)

    def read_pkl(self, object_key_name: str):
        """pklを読み込む

        Args:
            object_key_name (str): バケット内のpklファイルの名前

        Returns:
            dict: pklファイルの中身
        """
        s3_object = self.__get_s3object(object_key_name).get()
        return pickle.loads(s3_object['Body'].read())

    def write_pkl(self, data, object_key_name: str):
        """pklファイルに書き込む

        Args:
            data : 書き込むデータ
            object_key_name (str): バケット内のpklファイルの名前
        """
        pickle_byte_obj = pickle.dumps(data)
        s3_object = self.__get_s3object(object_key_name)
        s3_object.put(Body=pickle_byte_obj)

# def read_noticed_space_id(NOTICED_SPACE_FILE):
#     try:
#         with open(NOTICED_SPACE_FILE, 'rb') as f:
#             noticed_space_id_list = pickle.load(f)
#             return noticed_space_id_list
#     except EOFError as err:
#             print(f'EOFError on load pickle file: {err}')
