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
        group = line_bot_api.get_group_summary()
        line_bot_api.push_message(group.group_id, TextMessage(text='群組ID=' + group.group_id))
    except InvalidSignatureError:
        abort(400)
    return 'OK'


if __name__ == '__main__':
    myapp.run(port=10000)
