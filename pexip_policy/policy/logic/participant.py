
# participant.py

from urllib.parse import unquote
import logging
logger = logging.getLogger("pexip_policy.participant")

def get_participant_properties(params: dict):

    raw_alias = params.get("remote_alias", "")
    remote_alias = unquote(raw_alias).lower()
    service_tag = params.get("service_tag", "").lower()
    display_name = params.get("remote_display_name", "")
    participant_type = params.get("participant_type", "")
    
    logger.debug("Participant request: alias=%s, type=%s, tag=%s, display_name=%s", remote_alias, participant_type, service_tag, display_name)
    # Default continue
    action = "continue"

    if not remote_alias:
        logger.warning("Missing remote_alias in participant policy request.")
        action = "reject"

    result_data = {}

    # if remote_alias.endswith("@vp.pexip.com"):
    #     action = "reject"

    # result_data["service_tag"] = service_tag or "default"

    return {
        "status": "success",
        "action": action,
        "result": result_data
    }