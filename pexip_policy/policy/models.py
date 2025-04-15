from django.db import models

class RoomConfig(models.Model):
    alias = models.CharField(max_length=255, unique=True)  # e.g. 'sip:sales@example.com'
    name = models.CharField(max_length=255)                # e.g. 'Sales Room'
    service_tag = models.CharField(max_length=255)         # e.g. 'sales-room'

    def __str__(self):
        return f"{self.alias} → {self.name}"

class AllowedDomain(models.Model):
    domain = models.CharField(max_length=255, unique=True)  # e.g. '@example.com'

    def __str__(self):
        return self.domain