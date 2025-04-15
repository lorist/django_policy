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
    
from django.db import models

class PolicyLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    policy_type = models.CharField(max_length=50)  # e.g., 'service', 'participant', 'registration'
    alias = models.CharField(max_length=255)
    action = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'continue', 'reject'
    details = models.JSONField()  # Store full request parameters or response data

    def __str__(self):
        return f"[{self.timestamp}] {self.policy_type.upper()} — {self.alias} → {self.action or 'N/A'}"
