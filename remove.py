import logging
from time import sleep

from slack_bolt import App
from slack_sdk.errors import SlackApiError

app = App(
    token="",
)

logging.basicConfig(level=logging.INFO)

channel_id = ""
user_id = ""

target_thread_ts_list = []
cursor = None
latest = None

# NOTE: 先に対象IDの書き込みを全取得する
while True:
    response = app.client.conversations_history(
        channel=channel_id, cursor=cursor, latest=latest, limit=1000
    )

    # NOTE: スレッド内の書き込みの探索が必要なので、親スレッドの書き込みは全探索が必要
    # NOTE: response.data.messages[].reply_usersの中に自分のIDがあればスレッド内探索

    # TODO: messagesキー存在有無
    for thread_msg in response.data["messages"]:
        # スレッドが対象ユーザーの書き込み
        if "user" not in thread_msg.keys():
            continue

        if thread_msg["user"] == user_id:
            target_thread_ts_list.append(thread_msg["ts"])
            continue
        try:
            # スレッド内に対象ユーザーの書き込みがある場合
            if user_id in thread_msg["reply_users"]:
                target_thread_ts_list.append(thread_msg["ts"])
        except KeyError:
            pass

    # 続きを探索するためのカーソルを更新
    if response.data["has_more"] == False:
        break

    cursor = response.data["response_metadata"]["next_cursor"]
    latest = None
    sleep(10)


delete_ts_list = []

for target_thread_ts in target_thread_ts_list:
    cursor = None

    while True:
        sleep(10)
        response = app.client.conversations_replies(
            channel=channel_id, ts=target_thread_ts, cursor=cursor
        )

        for next_thread_msg in response.data["messages"]:
            if next_thread_msg["user"] == user_id:
                delete_ts_list.append(next_thread_msg["ts"])

        if response.data["has_more"] == False:
            break

        cursor = response.data["response_metadata"]["next_cursor"]

for next_delete_ts in delete_ts_list:
    try:
        app.client.chat_delete(channel=channel_id, ts=next_delete_ts)
    except SlackApiError as e:
        logging.info(e)

    sleep(10)
