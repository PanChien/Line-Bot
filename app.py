from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('G3p0eikHKImALtnleI4Nv+v8SGBnznt1aRnnIOxs6MpIDKRWN1eOGvtLNl9A/g8MOlQpb+GwWL1PaW5fphmeE7cSgCC3hyKyauhBbGF45X6bomraU9kIMHw64xROOB253afqEmsLvHsc8zjbFnvBaAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('471c1dc192ed3cfbd4b7732878990194')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，您說什麼!!'

    if msg in ['hi', 'Hi', 'HI']:
        r = msg
    elif msg == '你吃飯了嗎?':
        r = '我是機器人，不用吃飯哦!'
    elif '訂位' in msg:
        r = '你想訂位嗎? 我們訂位服務還沒起用哦。'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":    #當main function被執行時，再向下執行
    app.run()