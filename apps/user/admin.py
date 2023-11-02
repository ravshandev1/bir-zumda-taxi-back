from django.contrib import admin
from .models import Client, TaxiDriver
from main.models import Destination


class DesInline(admin.StackedInline):
    model = Destination
    extra = 0


@admin.register(TaxiDriver)
class TaxiDriverAdmin(admin.ModelAdmin):
    inlines = [DesInline]
    list_display = ['name', 'phone', 'created_at']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'travels_count', 'created_at']
