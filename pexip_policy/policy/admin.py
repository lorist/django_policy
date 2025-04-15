from django.contrib import admin
from .models import RoomConfig, AllowedDomain, PolicyLog

@admin.register(RoomConfig)
class RoomConfigAdmin(admin.ModelAdmin):
    list_display = ("alias", "name", "service_tag")
    search_fields = ("alias",)

@admin.register(AllowedDomain)
class AllowedDomainAdmin(admin.ModelAdmin):
    list_display = ("domain",)
    search_fields = ("domain",)


@admin.register(PolicyLog)
class PolicyLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "policy_type", "alias", "action", "short_details")
    list_filter = ("policy_type", "action")
    search_fields = ("alias", "details")
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"
    
    def short_details(self, obj):
        return str(obj.details)[:75] + "..." if obj.details else ""
    short_details.short_description = "Details"