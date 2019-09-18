def webview(recipient_id):
    log("sending web view to {recipient}: {text}".format(recipient=recipient_id, text=""))
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
            "title": "Xe cun cung di tap",
            "subtitle": "1,469,000 VND",
            "image_url": "https://www.mykingdom.com.vn/media/catalog/product/cache/73a368d029059537f29915590ba445d6/magento/FISHER_PRICE_19/FHY96/FHY96_1.jpg",          
            "buttons": [
              {
                "title": "Mua",
                "type": "web_url",
                "url": "",
                "messenger_extensions": True,
                "webview_height_ratio": "full",
                "fallback_url": ""            
              }
            ]
          },
          {
            "title": "Luc Lac Thu Cung",
            "subtitle": "119,000 VND",
            "image_url": "https://www.mykingdom.com.vn/media/catalog/product/cache/73a368d029059537f29915590ba445d6/magento/FISHER_PRICE_19/FGJ54/FGJ54_1.jpg",          
            "buttons": [
              {
                "title": "Mua",
                "type": "web_url",
                "url": "",
                "messenger_extensions": True,
                "webview_height_ratio": "full",
                "fallback_url": ""            
              }
            ]
          },
            {
            "title": "Sach tap dem thu cung",
            "subtitle": "244,000 VND",
            "image_url": "https://www.mykingdom.com.vn/media/catalog/product/cache/73a368d029059537f29915590ba445d6/magento/FISHER_PRICE_19/FYK57/FYK57_1.jpg",          
            "buttons": [
              {
                "title": "Mua",
                "type": "web_url",
                "url": "",
                "messenger_extensions": True,
                "webview_height_ratio": "full",
                "fallback_url": ""            
              }
            ]
          }
            ]        
          } }
    }   
    })

