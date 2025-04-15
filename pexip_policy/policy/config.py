# config.py

# Registration config
ALLOWED_REGISTRATION_DOMAINS = ["@example.com", "@trusted.net"]

# Service config
ROOM_CONFIG = {
    "sip:engineering@example.com": {
        "service_tag": "engineering-room",
        "name": "Engineering Room"
    },
    "sip:sales@example.com": {
        "service_tag": "sales-room",
        "name": "Sales Room"
    }
}