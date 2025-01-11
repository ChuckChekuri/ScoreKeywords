#pylint: disable=C0114,W0612,C0115,C0116

# filepath: ui/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class KeywordConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        # Handle adding keywords
        self.send(text_data=json.dumps({
            'message': 'Keyword added'
        }))

class CorpusConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        # Handle setting corpus location
        self.send(text_data=json.dumps({
            'message': 'Corpus location set'
        }))

class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        # Handle adding/removing users
        self.send(text_data=json.dumps({
            'message': 'User added/removed'
        }))

class VisualConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        # Handle publishing visuals
        self.send(text_data=json.dumps({
            'message': 'Visual published'
        }))
