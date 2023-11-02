from django.urls import path
from .views import TravelAPI, TownAPI, DestinationAPI, UserCreateAPI

urlpatterns = [
    path('', TravelAPI.as_view()),
    path('destination/', DestinationAPI.as_view()),
    path('where/', TownAPI.as_view()),
    path('users/', UserCreateAPI.as_view()),
]
