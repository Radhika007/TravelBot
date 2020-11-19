import os
import requests
import random
import json
import csv


API_TOKEN = os.environ['TG_API_TOKEN']
MOODS = [
    'Frustrated', 'Anxious', 'Bored', 'Sad', 'Happy'
]
LIMIT = 3

Data = []
with open('moods.csv') as file:
    cr = csv.DictReader(file)
    for line in cr:
        Data.append(line)


class Task:
    chat_id = None
    text = None

    def __init__(self, chat_id, text):
        self.chat_id = chat_id
        self.text = text

    def send_message(self, message):
        req = requests.post(
            'https://api.telegram.org/bot{token}/sendMessage'.format(
                token=API_TOKEN),
            json={"chat_id": self.chat_id, "text": message}
        )
        return req.text

    def send_duration(self, nights):
        nights = 'Number of nights will be: ' + str(nights)
        return self.send_message(nights)

    def send_estcost(self, estcost):
        estcost = 'The estimated cost of travel is: ' + str(estcost)
        return self.send_message(estcost)

    def send_location(self, lat, lng, rid):
        req = requests.post(
            'https://api.telegram.org/bot{token}/sendLocation'.format(
                token=API_TOKEN),
            json={"chat_id": self.chat_id, "latitude": lat,
                  "longitude": lng, "reply_to_message_id": rid}
        )
        return req.text

    def start(self):
        self.send_message(
            "This TravBot is a simple travel bot that will suggest"
            "you some travelchoices based on your mood. "
            "You can choose from these moods for now: " + ','.join(MOODS))
        self.send_message(
            "You can show how you are feeling by typing the"
            " mood after this \"/\" sign ")

    def recommend(self, mood):
        self.send_message(
            "Will help you get started with your upcoming trip! "
            "You are feeling: " + mood)
        r_index = int(random.random() * LIMIT)
        r_index += MOODS.index(mood) 
        name = Data[r_index]['DESTINATION']
        nights = Data[r_index]['Number of Nights']
        estcost = Data[r_index]['PRICE']
        longitude = Data[r_index]['longitude']
        latitude = Data[r_index]['latitude']
        website = Data[r_index]['WEBSITE']

        msg1 = json.loads(self.send_message(name))
        msg1_id = msg1['result']['message_id']

        self.send_duration(nights)
        self.send_estcost(estcost)
        self.send_message(website)

        self.send_location(latitude, longitude, msg1_id)

    def do(self):
        if self.text.startswith('/start'):
            self.start()
        elif self.text.startswith('/recommend anxious'):
            self.recommend("Anxious")
        elif self.text.startswith('/recommend frustrated'):
            self.recommend("Frustrated")
        elif self.text.startswith('/recommend bored'):
            self.recommend("Bored")
        elif self.text.startswith('/recommend happy'):
            self.recommend("Happy")
        elif self.text.startswith('/recommend sad'):
            self.recommend("Sad")
