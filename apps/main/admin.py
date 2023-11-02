from django.contrib import admin
from .models import Travel, Town, Advertising, TelegramUser


@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id']


@admin.register(Town)
class WhereToWhereAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ['client', 'where', 'to_where', 'created_at', 'completed']


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

    @staticmethod
    def name(obj):
        return obj.text[:50]
