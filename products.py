
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
        "template_type": "list",
        "top_element_style": "compact",
        "elements": [
          {
            "title": "Classic T-Shirt Collection",
            "subtitle": "See all our colors",
            "image_url": "https://peterssendreceiveapp.ngrok.io/img/collection.png",          
            "buttons": [
              {
                "title": "View",
                "type": "web_url",
                "url": "https://peterssendreceiveapp.ngrok.io/collection",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://peterssendreceiveapp.ngrok.io/"            
              }
            ]
          },
          {
            "title": "Classic White T-Shirt",
            "subtitle": "See all our colors",
            "default_action": {
              "type": "web_url",
              "url": "https://peterssendreceiveapp.ngrok.io/view?item=100",
              "messenger_extensions": False,
              "webview_height_ratio": "tall"
            }
          },
          {
            "title": "Classic Blue T-Shirt",
            "image_url": "https://peterssendreceiveapp.ngrok.io/img/blue-t-shirt.png",
            "subtitle": "100% Cotton, 200% Comfortable",
            "default_action": {
              "type": "web_url",
              "url": "https://peterssendreceiveapp.ngrok.io/view?item=101",
              "messenger_extensions": True,
              "webview_height_ratio": "tall",
              "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
            },
            "buttons": [
              {
                "title": "Shop Now",
                "type": "web_url",
                "url": "https://peterssendreceiveapp.ngrok.io/shop?item=101",
                "messenger_extensions": True,
                "webview_height_ratio": "tall",
                "fallback_url": "https://peterssendreceiveapp.ngrok.io/"            
              }
            ]        
          }
        ],
         "buttons": [
          {
            "title": "View More",
            "type": "postback",
            "payload": "payload"            
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


def list_DCVD(recipient_id):
    log("sending list template to {recipient}: {text}".format(recipient=recipient_id, text=""))
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
        "attachments":[
              { "type": "image",
                "payload": {"image_url": "https://www.mykingdom.com.vn/media/catalog/product/cache/73a368d029059537f29915590ba445d6/magento/BATTAT/VE3001_VE1005Z/VE3001_VE1005Z_1.jpg",
                            "title:": "Xe may xuc",
                            "subtitle": "399,000 VND",
                            "is_reusable":True}
              },
              { "type": "image",
                "payload": {"image_url": "https://www.mykingdom.com.vn/media/catalog/product/cache/73a368d029059537f29915590ba445d6/magento/BATTAT/VE3000_VE1002Z/VE3000_VE1002Z_1.jpg",
                            "title:": "Xe can cau",
                            "subtitle": "399,000 VND",
                            "is_reusable":True}
              },
              { "type": "image",
                "payload": {"image_url": "https://www.mykingdom.com.vn/media/catalog/product/cache/73a368d029059537f29915590ba445d6/magento/BATTAT/VE3000_VE1000Z/VE3000_VE1000Z_1.jpg",
                            "title:": "Xe ben",
                            "subtitle": "399,000 VND",
                            "is_reusable":True}
              }
            ]

    }
    })
    r = requests.post("https://graph.facebook.com/v4.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

