from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import os
# import sqlite3

RDS_HOST = os.environ.get('RDS_HOST')
RDS_DB = os.environ.get('RDS_DB')
RDS_USER = os.environ.get('RDS_USER')
RDS_PASS = os.environ.get('RDS_PASS')

# mysqlのDBの設定
DATABASE = f'mysql://{RDS_USER}:{RDS_PASS}@{RDS_HOST}/{RDS_DB}?charset=utf8mb4'

ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=True, # Trueだと実行のたびにSQLが出力される
    pool_pre_ping=True # 接続の悲観的なテスト
)

# Sessionの作成
session = scoped_session(
# ORM実行時の設定。自動コミットするか、自動反映するなど。
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()