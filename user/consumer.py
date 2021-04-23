import json
from channels.generic.websocket import WebsocketConsumer

class BotConsumer(WebsocketConsumer):
    def connect(self):
        print("connect")
        print(self.scope)
        self.accept()

    def disconnect(self, cljose_code):
        print("disconnect")

    def receive(self, text_data):
        print("recieving ...")
        print(text_data)

    def send(self, text_data):
        print("sending ...")
        print(text_data)
