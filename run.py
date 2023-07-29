import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage
)

myapp = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
parser = WebhookParser(channel_secret)


@myapp.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'ID?' or event.message.text == 'id?':
        user_id = TextMessage(text=event.source.user_id)
        line_bot_api.reply_message(event.reply_token, user_id)
    elif event.message.text == 'GroupID?':
        group_id = TextMessage(text=event.source.group_id)
        line_bot_api.reply_message(event.reply_token, group_id)
    else:
        None


if __name__ == '__main__':
    myapp.run(port=10000)
