import datetime
import os
import uuid
import psycopg2
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)
from getexceldata import output_excel_data

myapp = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@myapp.route("/callback", methods=['POST'])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'ID?':
        line_bot_api.reply_message(event.reply_token, TextMessage(text=event.source.user_id))
    elif event.message.text == 'GroupID?':
        line_bot_api.reply_message(event.reply_token, TextMessage(text=event.source.group_id))
    else:
        None


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    image_content = line_bot_api.get_message_content(event.message.id)
    filename = event.message.id + '.jpg'
    content = image_content.content
    # 連接到 PostgreSQL 數據庫
    conn = psycopg2.connect(
        host='dpg-cjgeufb6fquc73dh444g-a.singapore-postgres.render.com',
        port='5432',
        database='test_7dh8',
        user='ann',
        password='ChUXVe8a8D29IU2WwvJFGyetV206S5I9',
        sslmode='allow'
    )
    # 建立一個游標
    cursor = conn.cursor()
    # 插入新資料的 SQL 語句
    sql = 'INSERT INTO files (filename, content) VALUES (%s, %s)'
    # 執行插入操作
    cursor.execute(sql, (filename, content))
    # 提交變更並關閉游標和連接
    conn.commit()
    cursor.close()
    conn.close()
    line_bot_api.reply_message(event.reply_token, TextMessage(text='上傳完畢'))
    

if __name__ == '__main__':
    myapp.run(port=10000)
