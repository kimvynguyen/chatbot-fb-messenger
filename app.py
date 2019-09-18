import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    params = {
        "access_token": "EAAFvTbGl9ccBAEZBlWiBuLk6wdjWl6VvlLdNG3FTrzOozWKv1GXPRqU8Xv7QzUTlbSUsA5vOwApzUZCF4C0iRXjodzZA7imDw3OvDeJkBzn1ZBA14zeL5yfsoYQk7yqzG9pRd67psnxvCiRPcEneuAxYpawhx0sKvJLp56tiLaMFxcZClzqIeQucpCjxqoqUZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data =json.dumps({"get_started":{
            "payload":"GET_STARTED_PAYLOAD"},
            "greeting":[
            {
                "locale":"default",
                "text":"Xin chao {{user_full_name}}, cam on ban da quan tam den chung toi! Hay nhan Bat dau de tuong tac cung chung toi nhe!"
            }],
            "persistent_menu":[
            {
            "locale":"default",
            "composer_input_disabled": True,
            "call_to_actions":[
                {
                    "type": "web_url",
                    "title": "Power by IChat",
                    "url": "https://ichat.vmarketing.vn/",
                    "webview_height_ratio": "full"
                },
                {
                    "type":"postback",
                    "title":"Chat voi nhan vien",
                    "payload": "CARE_HELP"
                }
            ]
            }
        ],
        "whitelisted_domains":["https://www.mykingdom.com.vn"],
        })

    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",params=params, headers=headers, data=data)
    send_message("","Cam on ban da lua chon Ichat lam nen tang")
    send_attachment(sender_id)
    send_button(sender_id)
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print (u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
