from flask import Flask, request, abort
from flask.ext.api import status
import os

webhook_app = Flask(__name__)

#ACCESS_TOKEN = os.environ["PAGE_ACCESS_TOKEN"]
#VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]

ACCESS_TOKEN = "EAACU3AopqPkBAO2HHeh47JxxrJz4ZCqRdEMkPdpOlsVAze3wSYOZAMV6AFsHo54viMJseoPXVJL1WWELZBllWv2oM6QjMEyunHaWUHlGpR41Mx5ilZAFNLx7cNsHYDxkLUEXwLytZBcNCZBtXAh0H9bZATOhCyENaRiMKpOMPdc9VPRdEjdM81C"
VERIFY_TOKEN = "my_verify_token_is_a_secret"
@webhook_app.route('/', methods=['GET'])
def verify_webhook_token():
    if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.verify")==VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed"



@webhook_app.route('/', methods=['POST'])
def process_event():
    if request.is_json:
        json_data = request.get_json()
        if json_data["object"]=="page":
            entries = json_data["entry"]
            for entry in entries:
                messaging_array = entry["messaging"]
                for messaging_element in messaging_array:
                    if messaging_element.get("message"):
                        sender_id = messaging_element["sender"]["id"]
                        recipient_id = messaging_element["recipient"]["id"]
                        content = messaging_element["message"]["text"]
                        acknowledge_text_message("Message received!",sender_id)

                    if messaging_element.get("delivery"):
                        pass

                    if messaging_element.get("optins"):
                        pass

                    if messaging_element.get("postback"):
                        pass

    return status.HTTP_200_OK

def acknowledge_text_message(message_text, recipient_id):
    params = {
        "access_token": ACCESS_TOKEN
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





if __name__ == '__main__':
    webhook_app.run()