import json
from channels.generic.websocket import WebsocketConsumer

class userAddedConsumer(WebsocketConsumer):
    def connect(self):
        print("connect")
        self.accept()

    def disconnect(self, cljose_code):
        print("disconnect")

    def receive(self, text_data):
        print("recieving ...")
        print(text_data)
        self.send("test back")

    # def send(self, text_data):
    #     print("sending ...")
    #     print(text_data)
