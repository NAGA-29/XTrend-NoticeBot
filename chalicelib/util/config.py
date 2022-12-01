# from chalicelib import Hololive, Noripro
# from chalicelib import HololiveProfile
# from chalicelib import NoriproProfile
        
# def select_model(obj:str):
#     """文字列からどのモデルを参照するか判定

#     Args:
#         obj (str): 所属グループ名
#                     hololive or noripro
#     """
#     if obj == 'hololive':
#         return HololiveProfile
#     elif obj == 'noripro':
#         return NoriproProfile

# def select_tw_ids(obj:str):
#     if obj == 'hololive':
#         return Hololive.get_twitter_ids()
#     elif obj == 'noripro':
#         return Noripro.get_twitter_ids()

# def select_tube_ids(obj:str):
#     """文字列からどのidリストを参照するか判定

#     Args:
#         obj (str): _description_

#     Returns:
#         _type_: _description_
#     """
#     if obj == 'hololive':
#         return Hololive.get_video_ids()
#     elif obj == 'noripro':
#         return Noripro.get_video_ids()