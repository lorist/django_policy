# service.py

from urllib.parse import unquote
import logging
logger = logging.getLogger("pexip_policy.service")

def get_service_configuration(local_alias_encoded: str):
    local_alias = unquote(local_alias_encoded).lower()

    room_config = {
        "sip:engineering@example.com": {
            "service_tag": "engineering-room",
            "name": "Engineering Room"
        },
        "sip:sales@example.com": {
            "service_tag": "sales-room",
            "name": "Sales Room"
        }
    }

    config = room_config.get(local_alias, {
        "service_tag": "default",
        "name": "Default Room"
    })

    logger.debug("Service request for alias: %s", local_alias)
    logger.debug("Resolved config: %s", config)

    result_data = {
        "service_type": "conference",
        "name": config["name"],
        "description": "Pexip Test Conference Room",
        "aliases": [local_alias],
        "pin": "",
        "guest_pin": "",
        "allow_guests": False,  # boolean
        "media_encryption": "best_effort",
        "enable_chat": "default",  # string, Pexip-specific
        "enable_overlay_text": True,
        "enable_active_speaker_indication": "true",
        "max_callrate_in": 8192000,
        "max_callrate_out": 8192000,
        "participant_limit": 50,
        "service_theme": None,
        "ivr_theme": None,
        "host_view": "one_main_seven_pips",
        "guests_can_present": True,
        "service_tag": config["service_tag"],
    }

    return {
        "status": "success",
        "result": result_data
    }
