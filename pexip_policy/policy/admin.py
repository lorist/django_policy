from django.contrib import admin
from .models import RoomConfig, AllowedDomain

@admin.register(RoomConfig)
class RoomConfigAdmin(admin.ModelAdmin):
    list_display = ("alias", "name", "service_tag")
    search_fields = ("alias",)

@admin.register(AllowedDomain)
class AllowedDomainAdmin(admin.ModelAdmin):
    list_display = ("domain",)
    search_fields = ("domain",)