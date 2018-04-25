from pprint import pprint
import requests

bot_token="545110014:AAFL9tBt7h93I2fywdCnFU-U7FYeLi77aQY"
test_url="https://f4f9d755.ngrok.io/{}".format(bot_token)

def get_url(method):
    return "https://api.telegram.org/bot{}/{}".format(bot_token, method)

r = requests.post(get_url("setWebhook"), data={"url": test_url})
r = requests.post(get_url("getWebhookInfo"))

pprint(r.status_code)
pprint(r.json())
