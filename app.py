# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser,WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
line_bot_api = LineBotApi('0FfdZaCtwUuVjXvlYpoH8xqKSNdd0rjynNlEFa4C5zBye1U7nASeCBTQFTGVUij1xJ/vnzg07mSsz2b1YpyWkPyAWOTOoLQ/o43uDNOwBrKvcyUJsbTLLC1dGN1+ANKrU+oSeMUoeCWZsWcHyu+PdgdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('defb53f3549ef8ea2a9d91455e9a120e')
handler = WebhookHandler('defb53f3549ef8ea2a9d91455e9a120e')

@app.route("/yeah")
def hello():
    return "Hello World!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    return 'OK'


################################################################
from note import note
def tanggapanNote(event):
    text = event.message.text
    data = text.split(' ')
    user_id = event.source.user_id
    ins=note(user_id,'tmp')
    if data[1]=='add':
        ins.inputData(data[2])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Note berhasil dimasukkan\n"))
    elif data[1]=='show':
        if ins.isDataExist():
            data = ins.readData()
            textnya = ""
            counter=1
            for dat in data:
                textnya = textnya+ str(counter)+". "+ dat +"\n"
                counter=counter+1
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=textnya))            
        else:
            line_bot_api.push_message(event.source.user_id,TextSendMessage(text='Empty'))    
    elif data[1]=='delall':
        ins.deleteAllData()
        line_bot_api.push_message(event.source.user_id,TextSendMessage(text='Terhapus semua'))
##################################################################
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user
    data = text.split(' ')
    if data[0]=='!note':
        tanggapanNote(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)) #reply the same message from user
    line_bot_api.push_message(event.source.user_id,TextSendMessage(text='Hello World!'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    """arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)"""
