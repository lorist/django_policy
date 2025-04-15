from django.core.management.base import BaseCommand
from policy.models import AllowedDomain
from policy.config import ALLOWED_REGISTRATION_DOMAINS

class Command(BaseCommand):
    help = "Sync static ALLOWED_REGISTRATION_DOMAINS into the database"

    def handle(self, *args, **kwargs):
        for domain in ALLOWED_REGISTRATION_DOMAINS:
            AllowedDomain.objects.get_or_create(domain=domain)
        self.stdout.write(self.style.SUCCESS("Synced allowed domains from config.py"))
