#!/usr/bin/python
#coding:utf-8
from flask import Flask, request, abort
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, LocationSendMessage
)


app = Flask(__name__)

line_bot_api = LineBotApi('1CUPhhi293CP/Mg79zmAwgOGmRHCbSjE/9H0+iehP6cpdEjxjPPpOJjhQefOTCfoJJj504I8oM7dqC0iU5fMBhPx9Zpc7mGJd8HRkTxoc8rime7WAon92AalaEKW5OmHI2fIEn1G+cbTRFav+J8NJgdB04t89/1O/w1cDnyilFU=')   #I put my TOKEN
handler = WebhookHandler('8c59beaf31178f4e0a8cafcaf06cc53a')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value  	X-Line-Signature:ID generated for each request
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

# 傳送文字訊息時會觸發
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.type:", event.message.type)
    content = u'這是文字訊息'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
    return 0

# 傳送位置資訊時會觸發
@handler.add(MessageEvent, message=LocationMessage)
def handel_location(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.type:", event.message.type)
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )
    return 0

if __name__ == "__main__":
    app.run()