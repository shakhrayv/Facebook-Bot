import requests
from flask import Flask, request
from bot import Bot
import time

app = Flask(__name__)
bot = Bot()

ACCESS_TOKEN = "EAAKt8AcCHZCgBAHbCLyynWUrmkzduHXUZCykMfNIjIFRwag8C2X6XWh7mculY8bFd3boT67gxHSAC2GU8LaLh8LeV79TL7o4EB11Cj4Ii8KRUOp35Q76X4Ad2OZALHOm7DsOJZBhm6xplsrTQFjRgqJaMb0tzmbhWlAAVlYYfAZDZD"


@app.route('/', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']


def reply(user_id, msges):
    for msg in msges:
        data = {
            "recipient": {"id": user_id},
            "message": {"text": msg}
        }
        resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
        print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    print(data)
    message_info = data['entry'][0]['messaging'][0]
    sender = message_info['sender']['id']

    if 'sticker_id' in message_info['message'] and message_info['message']['sticker_id'] == 369239263222822:
        reply(sender, ["^_^"])
        return 'ok'

    command = message_info['message']['text']
    response = bot.execute(command, sender)

    if type(response) == str:
        response = [response]
    if type(response) == tuple and response[1] == True:
        reply(sender, response[0])

    reply(sender, response)
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
