from rest_framework import serializers
from .models import TaxiDriver, Client


class TaxiDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxiDriver
        fields = ['telegram_id', 'username', 'name', 'phone']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'username', 'phone', 'telegram_id']
