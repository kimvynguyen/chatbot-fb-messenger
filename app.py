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

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]
                    if messaging_event['postback']['payload'] == "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Get Started\"}":
                        send_message(sender_id,'Chung toi quan niem: "Dung ep doanh nghiep linh hoat theo giai phap ma phai dem den giai phap linh hoat voi doanh nghiep"')
                        send_attachment(sender_id,"vmarketing")
                       
                   
                    
    return "ok", 200

#ham gui tin nhan
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
    r = requests.post("https://graph.facebook.com/v4.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

#ham gui hinh anh va nut
def send_attachment(recipient_id,message_text):
    log("sending attachment to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

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
            "attachment":{
        "type":"template",
        "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Vmarketing",
            "image_url":"https://drive.google.com/open?id=1idJiBzo9Nt8pyajD8plqs5KZi8zqGgv6.png",
            "buttons":[
                {
                    "type": "postback",
                    "title":"Chatbot Marketing - Tiep can de dang ",
                    "payload": "chatbot"
                },
                {
                    "type": "postback",
                    "title": "Mobile Marketing - Nhan dien nhanh chong ",
                    "payload": "mobile"
                },
                {
                    "type": "postback",
                    "title":" Online to Offline - Quan tam xuyen suot ",
                    "payload": "online"
                }
                ]   
          }
        ]
      }
    }
        }
    })
    r = requests.post("https://graph.facebook.com/v4.0/me/messages", params=params, headers=headers, data=data)
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
