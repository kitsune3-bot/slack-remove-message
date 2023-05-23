Slack書き込み自動削除
===

Slackの書き込みを自動削除するPythonスクリプトです。  
無料版でポスト上限枠を超えないように不要なチャンネルの書き込みを削除することを目的としています。

## 環境設定

環境設定は下記手順を実行する必要があります。

- Python環境構築
- Slack API Token発行

### Python環境構築

- Pythonインストール
- パッケージインストール
  ```
  pip install slack-bolt
  ```
### Slack API Token発行

**概要**

SlackAPIでAppを新規作成し、アクセストークンを発行します。  
自分のアカウントの読み書き権限を付与して該当の書き込みを削除します。

**実行手順**

- [SlackAPI](https://api.slack.com/apps)へアクセスし、Create New Appをクリック
  - アプリ名と対称ワークスペースを入力してCreate Appをクリック
- アプリのSettings -> Basic Informationの画面でPermissionを選択
- User Token Scopesで下記を指定
  - `channels:history`
  - `channels.read`
  - `chat.write`
- OAuth Tokens for Your WorkspaceのInstall to Workspaceをクリックし、ワークスペースにアプリをインストールし、トークンを発行する
  - 発行した`User OAuth Token` (xoxpから始まるトークン)をスクリプトで使用します




## 使い方