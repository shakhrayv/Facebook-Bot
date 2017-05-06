# Useful imports
import requests
from flask import Flask, request
import json
from bot import Bot
import logging
logging.basicConfig(filename='info.log', filemode='w', level=logging.DEBUG)


# Facebook Configurations
ACCESS_TOKEN = "EAAKt8AcCHZCgBAHbCLyynWUrmkzduHXUZCykMfNIjIFRwag8C2X6XWh7mculY8bFd3boT67gxHSAC2GU8LaLh8LeV79TL7o4EB11Cj4Ii8KRUOp35Q76X4Ad2OZALHOm7DsOJZBhm6xplsrTQFjRgqJaMb0tzmbhWlAAVlYYfAZDZD"
VER_SCT = "YKIZr)*FCZSO@[mTS/eW"

app = Flask(__name__)   # Creating Flask application
bot = Bot()             # Creating a bot instance


# Handling verification
@app.route('/', methods=['GET'])
def handle_verification():
    logging.info("Handling Verification...")

    if request.args.get('hub.verify_token', '') == VER_SCT:
        logging.info("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        logging.critical("Verification failed!")
        return 'Error, wrong validation token.'


# Getting user info
def get_user_info(token, user_id):
    r = requests.get("https://graph.facebook.com/v2.6/" + user_id,
                     params={"fields": "first_name,last_name", "access_token": token })
    if r.status_code != requests.codes.ok:
        logging.error(r.text)
    return json.loads(r.content)


# Sending a message with 'text' to the recipient
def send_message(recipient, text):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": ACCESS_TOKEN},
        data=json.dumps({
            "recipient": {"id": recipient},
            "message": {"text": text}
            }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        logging.error(r.text)


# This method will be called every time the message is received
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    # Getting the request data
    payload = request.get_data()
    logging.info("Incoming messages...")

    for sender, message in messaging_events(payload):

        # In some cases, the message can be empty
        # In other cases, the 'sender' field may be absent
        if sender is None:
            logging.warning("Empty sender.")
            continue
        elif message is None:
            logging.info("Sticker!")
            send_message(sender, '^_^')
            continue

        # Trying to answer by calling 'bot.execute'
        try:
            for bot_message in bot.execute(message, sender):
                if bot_message is not None:
                    logging.info(bot_message)
                    send_message(sender, bot_message[:640])
        except Exception as e:
            logging.error("Unexpected error.")
            send_message(sender, "Internal error occurred.")
    return "ok"


# Parse incoming payload
def messaging_events(payload):
    data = json.loads(payload)

    if 'entry' not in data or 'messaging' not in data['entry'][0]:
        return

    # Loading messages events
    messages = data["entry"][0]["messaging"]

    for event in messages:
        # Checking if all the field are present
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]
        elif 'sender' in event:
            yield event['sender']['id'], None


# Main function
# Launching Flask application
if __name__ == '__main__':
    logging.info("App started.")
    app.run(debug=True)
