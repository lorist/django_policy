# export stuff from the db to a config that can be used in another deployment
import json
from django.core.management.base import BaseCommand
from policy.models import RoomConfig
from pathlib import Path

class Command(BaseCommand):
    help = "Exports RoomConfig DB entries to ROOM_CONFIG-style Python dictionary"

    def handle(self, *args, **kwargs):
        configs = RoomConfig.objects.all()
        exported = {
            rc.alias: {
                "name": rc.name,
                "service_tag": rc.service_tag
            }
            for rc in configs
        }

        # Output as valid Python dictionary
        config_string = "ROOM_CONFIG = " + json.dumps(exported, indent=4)

        # Save to file
        output_file = Path("room_config_export.py")
        output_file.write_text(config_string)

        # Display
        self.stdout.write(self.style.SUCCESS("Exported ROOM_CONFIG to file:"))
        self.stdout.write(self.style.SUCCESS(str(output_file.resolve())))
        self.stdout.write(config_string)
