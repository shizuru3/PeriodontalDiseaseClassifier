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

line_bot_api = LineBotApi('DztDCGomcU99mq6goPFYjKOHBZPvAstmWZGPtoma0abJMGvhNuitL3YhmMXIwNHs4RQPFfWR2UZa31e9JOYP7Bl+R/Ih5IW8ioOWdDYpsMPpPBq6rl3pZYTfT9++LB1i1SAwmWGexUod66JFGS6NvAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bc9a4adcbffe53fc2f07287badb2a7e6')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()