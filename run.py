import datetime
import os
import uuid

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
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import  MediaFileUpload

myapp = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

UPLOAD_FOLDER = '1Fyu6HFGWcqILdwpiqxSUxF_odXUFflMC'
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'google_auth.json'  # 金鑰檔案


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
    print('image')
    image_content = line_bot_api.get_message_content(event.message.id)
    filename = event.message.id + '.jpg'
    print('filename='+filename)
    # 把圖片存在本地
    with open(filename, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)
    # linebot回傳訊息
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='收到您上傳的照片囉!'))
    '''
    # 建立憑證物件
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    # 把本地圖片上傳到雲端
    media = MediaFileUpload(filename)
    file = {'name': filename, 'parents': [UPLOAD_FOLDER]}
    service.files().create(body=file, media_body=media).execute()
    '''

if __name__ == '__main__':
    myapp.run(port=10000)
