from urllib.parse import unquote
import logging
from policy.config import ROOM_CONFIG

logger = logging.getLogger("pexip_policy.service")

DEFAULT_DOMAIN = "example.com"

def normalize_alias(raw_alias: str) -> str:
    decoded = unquote(raw_alias).lower().strip()
    if "@" not in decoded:
        decoded = f"sip:{decoded}@{DEFAULT_DOMAIN}"
    return decoded

def extract_alias_user(local_alias: str) -> str:
    return local_alias.split("@")[0].replace("sip:", "").lower()

def get_service_configuration(local_alias_encoded: str):
    local_alias = normalize_alias(local_alias_encoded)
    logger.debug("Service request for alias: %s", local_alias)

    from policy.models import RoomConfig

    # Step 1: Try database
    try:
        db_config = RoomConfig.objects.get(alias=local_alias)
        name = db_config.name + " | " + extract_alias_user(local_alias)
        service_tag = db_config.service_tag
    except RoomConfig.DoesNotExist:
        # Step 2: Try ROOM_CONFIG fallback
        config = ROOM_CONFIG.get(local_alias)
        if config:
            name = config["name"] + " | " + extract_alias_user(local_alias)
            service_tag = config["service_tag"]
        # Step 3: Final fallback
        elif local_alias.endswith(f"@{DEFAULT_DOMAIN}"):
            name = extract_alias_user(local_alias)
            service_tag = "default"
        else:
            name = "Default Room | " + local_alias
            service_tag = "default"

    logger.debug("Resolved name: %s, tag: %s", name, service_tag)

    result_data = {
        "service_type": "conference",
        "name": name,
        "description": "Pexip Test Conference Room",
        "aliases": [local_alias],
        "pin": "",
        "guest_pin": "",
        "allow_guests": False,
        "media_encryption": "best_effort",
        "enable_chat": "default",
        "enable_overlay_text": True,
        "enable_active_speaker_indication": "true",
        "max_callrate_in": 8192000,
        "max_callrate_out": 8192000,
        "participant_limit": 50,
        "service_theme": None,
        "ivr_theme": None,
        "host_view": "one_main_seven_pips",
        "guests_can_present": True,
        "service_tag": service_tag,
    }

    return {
        "status": "success",
        "result": result_data
    }
