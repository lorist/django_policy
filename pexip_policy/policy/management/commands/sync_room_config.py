"""
python manage.py sync_room_config
"""

from django.core.management.base import BaseCommand
from policy.models import RoomConfig
from policy.config import ROOM_CONFIG

class Command(BaseCommand):
    help = "Syncs static ROOM_CONFIG into the RoomConfig model"

    def handle(self, *args, **kwargs):
        created = 0
        updated = 0

        for alias, data in ROOM_CONFIG.items():
            obj, was_created = RoomConfig.objects.update_or_create(
                alias=alias,
                defaults={
                    "name": data["name"],
                    "service_tag": data["service_tag"],
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"ROOM_CONFIG sync complete: {created} created, {updated} updated."
        ))
