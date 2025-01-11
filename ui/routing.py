'''This file contains the routing for the Django'''
#pylint: disable=C0114
# filepath: ui/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/keywords/', consumers.KeywordConsumer.as_asgi()),
    path('ws/corpus/', consumers.CorpusConsumer.as_asgi()),
    path('ws/users/', consumers.UserConsumer.as_asgi()),
    path('ws/visuals/', consumers.VisualConsumer.as_asgi()),
]
