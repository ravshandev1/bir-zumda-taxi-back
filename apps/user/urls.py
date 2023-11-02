from django.urls import path
from .views import ClientAPI, UserAPI, TaxiAPI

urlpatterns = [
    path('<int:pk>/', UserAPI.as_view()),
    path('client/', ClientAPI.as_view()),
    path('taxi/', TaxiAPI.as_view()),
]
