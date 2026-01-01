# HoloTrend-NoticeBot

## 概要

**HoloTrend-NoticeBot** は、VTuber（特にホロライブ）に関連するTwitterのトレンドを監視するためのサーバーレスアプリケーションです。AWS Chaliceフレームワークを利用して構築されており、定期的にTwitterのトレンドを取得し、特定のキーワードが含まれている場合に何らかのアクションを実行することを目的としています。

## 主な機能

- 15分間隔での定期実行
- Twitterのトレンドリストの取得と監視
- 特定のキーワード（例: `#hololive`）に関連するトレンドの検出
- AWS S3を利用したトレンドデータの永続化

## 使用技術

- **言語:** Python 3.9
- **フレームワーク:** [AWS Chalice](https://aws.github.io/chalice/)
- **主要ライブラリ:**
  - `tweepy`: Twitter APIラッパー
  - `boto3`: AWS SDK for Python
  - `python-dotenv`: 環境変数管理
- **インフラストラクチャ:**
  - AWS Lambda
  - Amazon S3

## セキュリティ

このリポジトリはセキュリティ監査済みです。

ソースコード全体を対象に、AWSやTwitterなどの機密情報（APIキー、シークレットキーなど）がハードコードされていないことを確認しています。すべての認証情報は`.env`ファイルを通じて環境変数として読み込まれる設計になっており、安全に管理されています。

## 前提条件

- Python 3.9
- AWSアカウントと、設定済みのAWS CLI認証情報
- Twitter開発者アカウントと、発行済みのAPIキー/トークン

## インストールと設定

1.  **リポジトリをクローンします:**
    ```bash
    git clone https://github.com/your-username/HoloTrend-NoticeBot.git
    cd HoloTrend-NoticeBot
    ```

2.  **Pythonの仮想環境を作成し、有効化します:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **必要なライブラリをインストールします:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **環境変数を設定します:**
    プロジェクトのルートディレクトリに`.env`ファイルを作成し、必要なAPIキーや設定値を記述します。`chalicelib/config/app.py`に必要な変数がリストされています。

    ```.env
    # .env ファイルの例
    CONSUMER_KEY="<YOUR_CONSUMER_KEY>"
    CONSUMER_SECRET="<YOUR_CONSUMER_SECRET>"
    ACCESS_TOKEN="<YOUR_ACCESS_TOKEN>"
    ACCESS_TOKEN_SECRET="<YOUR_ACCESS_TOKEN_SECRET>"
    BUCKET_NAME="<YOUR_S3_BUCKET_NAME>"
    TREND_SAVE_FILE="trend_log.pkl"
    # ... その他必要な変数
    ```

## デプロイ

このアプリケーションはAWS Chaliceを使って簡単にデプロイできます。

```bash
chalice deploy
```

上記コマンドを実行すると、ChaliceがAWS上に必要なリソース（Lambda関数、IAMロールなど）を自動的にプロビジョニングし、アプリケーションをデプロイします。
