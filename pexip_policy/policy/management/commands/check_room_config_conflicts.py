from django.core.management.base import BaseCommand
from policy.models import RoomConfig
from policy.config import ROOM_CONFIG

class Command(BaseCommand):
    help = "Detects conflicts between ROOM_CONFIG (config.py) and DB RoomConfig"

    def handle(self, *args, **kwargs):
        db_entries = {
            rc.alias: {"name": rc.name, "service_tag": rc.service_tag}
            for rc in RoomConfig.objects.all()
        }

        config_entries = ROOM_CONFIG

        missing_in_db = []
        missing_in_config = []
        mismatches = []

        for alias, config_data in config_entries.items():
            if alias not in db_entries:
                missing_in_db.append(alias)
            elif db_entries[alias] != config_data:
                mismatches.append((alias, config_data, db_entries[alias]))

        for alias in db_entries:
            if alias not in config_entries:
                missing_in_config.append(alias)

        if missing_in_db:
            self.stdout.write(self.style.WARNING("⚠️ Missing in DB:"))
            for alias in missing_in_db:
                self.stdout.write(f"  - {alias}")

        if missing_in_config:
            self.stdout.write(self.style.WARNING("⚠️ Missing in config.py:"))
            for alias in missing_in_config:
                self.stdout.write(f"  - {alias}")

        if mismatches:
            self.stdout.write(self.style.WARNING("⚠️ Mismatched entries:"))
            for alias, config_val, db_val in mismatches:
                self.stdout.write(f"  - {alias}")
                self.stdout.write(f"    config.py: {config_val}")
                self.stdout.write(f"    DB       : {db_val}")

        if not (missing_in_db or missing_in_config or mismatches):
            self.stdout.write(self.style.SUCCESS("✅ No conflicts detected!"))
