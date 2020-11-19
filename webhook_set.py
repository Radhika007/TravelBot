import requests
import os


api_url = (
    'https://api.telegram.org/bot' +
    os.environ['TG_API_TOKEN'] + '/setWebhook')
webhook_url = 'https://trabot-236007.el.r.appspot.com/updates'

print(requests.post(api_url, {
    'url': webhook_url
}).json())
