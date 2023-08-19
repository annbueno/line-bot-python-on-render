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
    MessageEvent, TextMessage, TextSendMessage
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

output = output_excel_data('20230804')
output_str = '北:'+output['Kiki']+'桃竹苗:'+output['Alex']+'中:'+output['陳沱']

UPLOAD_FOLDER = '1Fyu6HFGWcqILdwpiqxSUxF_odXUFflMC'
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'google_auth.json'  # 金鑰檔案


@myapp.route("/callback", methods=['POST'])
def callback():
    # line_bot_api.push_message('C913bcb87db489f8af1dc7b392a303e73', TextSendMessage(text=output_str))
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    type = TextMessage(text=event.message.type)
    line_bot_api.reply_message(event.reply_token, type)
    if event.message.text == 'ID?' or event.message.text == 'id?':
        user_id = TextMessage(text=event.source.user_id)
        line_bot_api.reply_message(event.reply_token, user_id)
    elif event.message.text == 'GroupID?':
        group_id = TextMessage(text=event.source.group_id)
        line_bot_api.reply_message(event.reply_token, group_id)
    else:
        None


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    image_content = line_bot_api.get_message_content(event.message.id)
    # 取得當前時間
    current_time = datetime.datetime.now()
    # 將時間轉換成字串格式，例如：2023-06-18_12-34-56
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    # 生成唯一的檔案名稱
    unique_filename = formatted_time + '_' + str(uuid.uuid4().hex[:6])
    filename = unique_filename + '.jpg'  # 上傳檔的名字
    # 把圖片存在本地
    with open(filename, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)
    # 建立憑證物件
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    # 把本地圖片上傳到雲端
    media = MediaFileUpload(filename)
    file = {'name': filename, 'parents': [UPLOAD_FOLDER]}
    service.files().create(body=file, media_body=media).execute()

if __name__ == '__main__':
    myapp.run(port=10000)
