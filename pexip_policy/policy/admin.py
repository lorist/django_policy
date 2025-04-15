from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import RoomConfig, AllowedDomain, PolicyLog


@admin.register(RoomConfig)
class RoomConfigAdmin(admin.ModelAdmin):
    list_display = ("alias", "name", "service_tag")
    search_fields = ("alias",)

@admin.register(AllowedDomain)
class AllowedDomainAdmin(admin.ModelAdmin):
    list_display = ("domain",)
    search_fields = ("domain",)

# todo: only show these filters for the participant logs
class ParticipantTypeFilter(SimpleListFilter):
    title = "Participant Type"
    parameter_name = "participant_type"

    def lookups(self, request, model_admin):
        return [
            ("standard", "Standard"),
            ("chair", "Chair"),
            ("guest", "Guest"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(details__participant_type=value)
        return queryset

class LocationFilter(SimpleListFilter):
    title = "Location"
    parameter_name = "location"

    def lookups(self, request, model_admin):
        return [("internal", "Internal"), ("external", "External")]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(details__location=value)
        return queryset
    
@admin.register(PolicyLog)
class PolicyLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "policy_type", "alias", "action", "short_details")
    list_filter = (
        "policy_type", 
        "action", 
        ParticipantTypeFilter,
        LocationFilter,
        )
    search_fields = ("alias", "details")
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"

    def short_details(self, obj):
        return str(obj.details)[:75] + "..." if obj.details else ""
    short_details.short_description = "Details"