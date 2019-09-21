
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
            "title": "Do choi van dong",
            "subtitle": "Xem danh sach do choi van dong",
            "image_url": "https://imgur.com/kzo7OF5.png",          
            "buttons": [
              {
                "title": "Xem danh sach",
                "type": "web_url",
                "url": "https://www.mykingdom.com.vn/danh-muc/do-choi-van-dong.html",
                "messenger_extensions": False,
                "webview_height_ratio": "tall",
                         
              }
            ]
          },
         
          {
            "title": "Phuong tien giao thong",
            "image_url": "https://imgur.com/RN6BXcP.png",
            "subtitle": "Xem danh sach phuong tien giao thong",
            "default_action": {
              "type": "web_url",
              "url": "https://www.mykingdom.com.vn/danh-muc/phuong-tien-giao-thong.html",
              "messenger_extensions": False,
              "webview_height_ratio": "tall",
              
            },
            "buttons": [
              {
                "title": "Xem danh sach",
                "type": "web_url",
                "url": "https://www.mykingdom.com.vn/danh-muc/phuong-tien-giao-thong.html",
                "messenger_extensions": False,
                "webview_height_ratio": "tall",
                  
              }
            ]        
          }
        ],
         "buttons": [
          {
            "title": "Danh muc san pham",
            "type": "postback",
            "payload": "{\"type\":\"legacy_reply_to_message_action\",\"message\":\"Danh muc san pham\"}"            
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

