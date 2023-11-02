from rest_framework import serializers
from .models import Travel, Town, TelegramUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id']


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ['name']


class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        fields = ['id', 'client', 'where', 'to_where', 'lat', 'lon', 'count_person', 'note', 'completed']
