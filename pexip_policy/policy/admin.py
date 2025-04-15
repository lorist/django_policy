from django.contrib import admin
from .models import RoomConfig

@admin.register(RoomConfig)
class RoomConfigAdmin(admin.ModelAdmin):
    list_display = ("alias", "name", "service_tag")
    search_fields = ("alias",)
