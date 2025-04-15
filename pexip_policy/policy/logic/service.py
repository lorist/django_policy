from urllib.parse import unquote
import logging
from policy.models import RoomConfig, PolicyLog

logger = logging.getLogger("pexip_policy.service")

DEFAULT_DOMAIN = "example.com"

def normalize_alias(raw_alias: str) -> str:
    decoded = unquote(raw_alias).lower().strip()
    if "@" not in decoded:
        decoded = f"sip:{decoded}@{DEFAULT_DOMAIN}"
    return decoded

def extract_alias_user(local_alias: str) -> str:
    return local_alias.split("@")[0].replace("sip:", "").lower()

def get_service_configuration(local_alias_encoded: str, params: dict):
    local_alias = normalize_alias(local_alias_encoded)
    logger.debug("Service request for alias: %s", local_alias)

    try:
        db_config = RoomConfig.objects.get(alias=local_alias)
        name = db_config.name + " | " + extract_alias_user(local_alias)
        service_tag = db_config.service_tag
        logger.debug("Using DB config for alias: %s", local_alias)
    except RoomConfig.DoesNotExist:
        if local_alias.endswith(f"@{DEFAULT_DOMAIN}"):
            name = extract_alias_user(local_alias)
            service_tag = "default"
        else:
            name = "Default Room | " + local_alias
            service_tag = "default"
        logger.debug("Alias not found in DB. Using fallback for alias: %s", local_alias)

    # Log policy event
    remote_address = params.get("remote_address", "")
    protocol = params.get("protocol", "")
    location = params.get("location", "")

    PolicyLog.objects.create(
        policy_type="service",
        alias=local_alias,
        action=None,
        details={
            "remote_address": remote_address,
            "protocol": protocol,
            "location": location,
            "service_tag": service_tag,
        }
    )

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
