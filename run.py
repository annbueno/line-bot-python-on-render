import os
from flask import Flask, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage

myapp = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


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
