from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAKt8AcCHZCgBAHbCLyynWUrmkzduHXUZCykMfNIjIFRwag8C2X6XWh7mculY8bFd3boT67gxHSAC2GU8LaLh8LeV79TL7o4EB11Cj4Ii8KRUOp35Q76X4Ad2OZALHOm7DsOJZBhm6xplsrTQFjRgqJaMb0tzmbhWlAAVlYYfAZDZD"

@app.route('/', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']


def reply(user_id, msg):
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
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']

    reply(sender, "твоя мама " + adjs[randint(0,2)] + " шлюха")

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
