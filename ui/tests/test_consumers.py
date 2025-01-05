# filepath: ui/test_consumers.py
'''Test the consumers'''
import pytest
from channels.testing import WebsocketCommunicator
#from channels.layers import get_channel_layer
#from django.conf import settings
from django.test import TestCase
from scorekeywords.asgi import application

@pytest.mark.asyncio
class ConsumerTests(TestCase):
    '''Test the consumers'''
    async def test_keyword_consumer(self):
        '''Test the keyword consumer'''
        communicator = WebsocketCommunicator(application, "/ws/keywords/")
        connected, subprotocol = await communicator.connect()
        print(subprotocol)
        assert connected

        await communicator.send_json_to({"message": "add_keyword"})
        response = await communicator.receive_json_from()
        assert response["message"] == "Keyword added"

        await communicator.disconnect()

    async def test_corpus_consumer(self):
        '''Test the corpus consumer'''
        communicator = WebsocketCommunicator(application, "/ws/corpus/")
        connected, subprotocol = await communicator.connect()
        print(subprotocol)

        assert connected

        await communicator.send_json_to({"message": "set_corpus_location"})
        response = await communicator.receive_json_from()
        assert response["message"] == "Corpus location set"

        await communicator.disconnect()

    async def test_user_consumer(self):
        '''Test the user consumer'''
        communicator = WebsocketCommunicator(application, "/ws/users/")
        connected, subprotocol = await communicator.connect()
        print(subprotocol)
        assert connected

        await communicator.send_json_to({"message": "add_user"})
        response = await communicator.receive_json_from()
        assert response["message"] == "User added/removed"

        await communicator.disconnect()

    async def test_visual_consumer(self):
        '''Test the visual consumer'''
        communicator = WebsocketCommunicator(application, "/ws/visuals/")
        connected, subprotocol = await communicator.connect()
        print(subprotocol)
        assert connected

        await communicator.send_json_to({"message": "publish_visual"})
        response = await communicator.receive_json_from()
        assert response["message"] == "Visual published"

        await communicator.disconnect()
