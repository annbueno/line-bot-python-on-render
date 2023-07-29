import os
import sys
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

myapp = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@myapp.route("/callback", methods=['POST'])
def callback():
    try:
        # 網址被執行時，等同使用 GET 方法發送 request，觸發 LINE Message API 的 push_message 方法
        line_bot_api.push_message('U0bcbd8d8784be8615a919ddceb0d0b28', TextSendMessage(text='...0960'))
    except InvalidSignatureError:
        abort(400)
    return 'OK'


if __name__ == '__main__':
    myapp.run(port=10000)
