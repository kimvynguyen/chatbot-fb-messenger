import os
import sys
import json
from datetime import datetime

import requests
from flask import Flask, request
import products
import view

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
    log(data)  # you may not want tolog every incoming message in production, but it's good for testing
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"] # the message's text
                    
                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    if messaging_event['postback']['payload'] == "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Get Started\"}":
                        send_message(sender_id, "Cam on ban da chon Ichat la noi tin tuong lam nen tang.")
                        send_attachment(sender_id,"ichat")
                    elif messaging_event['postback']['payload'] == "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Mua hang online\"}":
                        webview(sender_id,"Mua hang online")
                    elif messaging_event['postback']['payload'] == "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Chia se\"}":
                        share(sender_id,"Chia se")
                    elif messaging_event['postback']['payload'] == "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Danh muc san pham\"}":
                        list_template(sender_id,"Danh muc san pham")
                    elif messaging_event['postback']['payload'] == "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Do choi van dong\"}":
                        list_DCVD(sender_id,"Do choi van dong")
                #send_message(sender_id, "Nhan vien cua chung toi se tuong tac voi ban!")

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
        "message": {"text": message_text}
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
            "title":"Ichat!",
            "image_url":"https://i.imgur.com/nt9zvJk.png",
            "subtitle":"Platform giup khach hang tuong tac truc quan voi doanh nghiep",
            "default_action": {
              "type": "web_url",
              "url": "https://www.mykingdom.com.vn",
              "messenger_extensions": True,
              "webview_height_ratio": "tall",
            },
            "buttons":[
                {
                    "type": "postback",
                    "title": "Mua hang online",
                    "payload": "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Mua hang online\"}"
                },
                {
                    "type": "postback",
                    "title": "Chia se",
                    "payload": "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Chia se\"}"
                },
                {
                    "type": "postback",
                    "title":"Thong tin san pham",
                    "payload": "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Danh muc san pham\"}"
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

#ham gui nut tra loi nhanh
def send_quick_reply(recipient_id, message_text):
    log("sending quick reply to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data= json.dumps({
    "recipient": {
        "id": recipient_id
    },
    "messaging_type": "RESPONSE",
    "message":{
        "text": message_text,
        "quick_replies":[
        {
            "content_type":"text",
            "title":"Red",
            "payload":"send quick reply",
            "image_url":"http://example.com/img/red.png"
        },
        {
            "content_type":"text",
            "title":"Green",
            "payload":"send quick reply",
            "image_url":"http://example.com/img/green.png"
        }
        ]
    }
    })
    r = requests.post("https://graph.facebook.com/v4.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
#ham nut chia se
def share(recipient_id,message_text):
    log("sending share to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data= json.dumps({
    "recipient": {
        "id": recipient_id
    },
    "message": { 
    "type": "element_share",
    "share_contents": { 
    "attachment": {
        "type": "template",
        "payload": {
        "template_type": "generic",
        "elements": [
           {
            "title":"Chia se",
            "subtitle": "Chia se uu dai ngay",
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS6O9Mb30_y44TLcGH7qbdMyhhzOxsOn-HqWz640VL2HeXdX_J3",
            "default_action": {
              "type": "web_url",
              "url": "https://www.mykingdom.com.vn"
            },
            "buttons": [
            {
                "type": "web_url",
                "url": "https://m.me/105274930862928?ref=story.chiasenhanuudai", 
                "title": "Chia se"
            } ]
         } 
    ]
      }
    }
  }
    }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        
def list_template(recipient_id, message_text):
    log("sending list template to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data= json.dumps({
    "recipient": {
            "id": recipient_id
        },
    "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "generic",
        "elements":[
           {
            "title":"Do choi van dong",
            "image_url":"https://imgur.com/15NSVJ2.png",
            "subtitle":"Xem danh sach",
            "buttons":[
                {
                    "title": "Xem danh sach",
                    "type": "postback",
                    "payload":"{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Do choi van dong\"}"
                    
                }]
           },
           {
            "title":"Do choi tri tue",
            "image_url":"https://imgur.com/lFBpXic.png",
            "subtitle":"Da dang, phong phu cac loai do choi tri tue",
            "buttons":[
                {
                    "title": "Xem danh sach",
                    "type": "postback",
                    "payload":"{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Do choi tri tue\"}"

                }]
           },
           {
            "title":"Phuong tien giao thong",
            "image_url":"https://imgur.com/RN6BXcP.png",
            "subtitle":"Da dang, phong phu cac loai phuong tien giao thong",
            "buttons":[
            {
                "title": "Xem danh sach",
                "type": "postback",
                "payload":"{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Phuong tien giao thong\"}"

            }]
           }
        ]
      } 
    } 
    }       
        })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        
def list_DCVD(recipient_id,message_text):
    log("sending list template to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data= json.dumps({
    "recipient": {
            "id": recipient_id
        },
    "message":{
        "attachments":{
            "type": "template",
            "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": "Xe may xuc",
                    "subtitle": "399,000 VND",
                    "image_url": "https://imgur.com/TJuA5Zj.png",          
                    "buttons": [
                        {
                            "title": "Mua ngay",
                            "type": "postback",
                            "payload": "Mua ngay"
                        }
                    ],
                },
                {
                    "title": "Xe can cau",
                    "subtitle": "399,000 VND",
                    "image_url": "https://imgur.com/5ibsmK0.png",          
                    "buttons": [
                        {
                            "title": "Mua ngay",
                            "type": "postback",
                            "payload": "Mua ngay"
                        }
                    ],
                },
                {
                    "title": "Xe ben",
                    "subtitle": "399,000 VND",
                    "image_url": "https://imgur.com/Bnci9NZ.png",          
                    "buttons": [
                        {
                            "title": "Mua ngay",
                            "type": "postback",
                            "payload": "Mua ngay"
                        }
                    ],
                }
            ]
             
            }
        }

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
