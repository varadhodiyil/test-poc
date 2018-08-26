from channels.generic.websocket import WebsocketConsumer
import json


class CartConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        username = self.scope["user"]
        if(username.is_authenticated):
            self.send(text_data=json.dumps({
                'message': text_data
            }))

class PromotionsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        username = self.scope["user"]
        if(username.is_authenticated):
            self.send(text_data=json.dumps({
                'message': "A new Product is added to our Inventory, click here to view"
            }))