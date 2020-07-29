import os
import requests
import random
import json

import csv
Data = []
with open('moods') as file:
    cr = csv.DictReader(file)
    for line in cr:
        Data.append(line)

API_TOKEN = "1259023928:AAGdw1z_tbsILyJdFja_HKzucX_eOrxe5Po"
MOODS = [
    'Frustrated','Anxious','Bored','Sad','Happy'
]

LIMIT = 7

class Task: 
    chat_id = None
    text = None

    def __init__(self,chat_id,text):
        self.chat_id = chat_id
        self.text = text
    
    def send_message(self,message):
        req = requests.post(
            'https://api.telegram.org/bot{token}/sendMessage'.format(token = API_TOKEN),
            json={"chat_id": self.chat_id,"text": message}
        )
        return req.text

    def send_duration(self,nights):
         req = requests.post(
            'https://api.telegram.org/bot{token}/sendDuration'.format(token = API_TOKEN), 
            json={"chat_id": self.chat_id, "nights": Number of Nights}
        )
        return req.text

    def send_estcost(self,estcost):
        req = requests.post(
            'https://api.telegram.org/bot{token}/sendEstimatedCost'.format(token = API_TOKEN),
            json={"chat_id": self.chat_id,"price": PRICE}
        )
        return req.text

    def send_image(chat_id,image_path, image_caption=" "):
        data1 = {"chat_id": self.chat_id, "caption": image_caption}
        url1 = "https://api.telegram.org/bot{token}/sendPhoto".format(token = API_token) 
        with open(image_path,"rb") as image_file:
            ret = requests.post(url, data=data, files={"photo": image_file})
        return ret.json()


    def start(self):
        self.send_message("This TravBot is a simple travel bot that will suggest you some travel choices based on your mood. You can choose from these moods for now: " + ','.join(MOODS))

    def recommend(self,mood):
        self.send_message('Will help you get started with your upcoming trip! You are feeling: ' + mood)
        r_index = int(random.random() * LIMIT)
        if mood == 'Anxious':
            r_index = 1 + r_index
        elif mood == 'Bored':
            r_index = 4 + r_index
        elif mood == 'Frustrated':
            r_index = 7 + r_index
        elif mood == 'Happy':
            r_index = 10 + r_index
        elif mood == 'Sad':
            r_index = 14 + r_index
        name = Data[r_index]['Destination']
        nights = Data[r_index]['Number of Nights']
        estcost = Data[r_index]['PRICE']

        msg1 = json.loads(self.send_message(name))
        msg1_id = msg1['result']['message_id']

        self.send_duration(nights,msg1_id)
        self.send_estcost(estcost,msg1_id)

    def do(self):
        if self.text.startswith('/start'):
            self.start()
        elif self.text.startswith('/anxious'):
            self.recommend("Anxious")
        elif self.text.startswith('/frustrated'):
            self.recommend("Frustrated")
        elif self.text.startswith('/bored'):
            self.recommend("Bored")
        elif self.text.startswith('/happy'):
            self.recommend("Happy")
        elif self.text.startswith('/sad'):
            self.recommend("Sad")
