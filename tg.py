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
            "This TRAVBOT IS A SIMPLE TRAVEL BOT THAT WILL SUGGEST  "
            "YOU SOME TRAVEL CHOICES BASED ON YOUR MOOD. "
            "You can choose from these moods for now: " + ','.join(MOODS))
        self.send_message(
            "You can show how you are feeling by typing the"
            " mood after this \"/recommend\" sign ")

    def recommend(self, mood):
        self.send_message(
            "Will help you get started with your upcoming trip! "
            "I have found an amazing place for you to visit since you are feeling " + mood)
        r_index = int(random.random() * LIMIT)
        if mood == 'Anxious':
            r_index = 0 + r_index
        elif mood == 'Bored':
            r_index = 3 + r_index
        elif mood == 'Frustrated':
            r_index = 6 + r_index
        elif mood == 'Happy':
            r_index = 9 + r_index
        elif mood == 'Sad':
            r_index = 13 + r_index
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
        elif self.text.startswith('Thank you'):
            self.send_message("Thank you for using TravBot:) Hope you enjoy your vacation!")
        elif self.text.startswith('Hello'):
            self.send_message("Hey, I am TravBot type /start to start me.")
        elif self.text.startswith('Okay'):
            self.send_message("Okay, Thank you for using TravBot:)")
