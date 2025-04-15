# registration.py
import logging
# from policy.config import ALLOWED_REGISTRATION_DOMAINS
from policy.models import AllowedDomain, PolicyLog



logger = logging.getLogger("pexip_policy.registration")

from urllib.parse import unquote
# def get_registration_policy(alias_encoded: str):
def get_registration_policy(alias_encoded: str, params: dict):
    # decoded_alias = unquote(alias_encoded).lower()
    decoded_alias = unquote(alias_encoded).lower().strip()
    remote_address = params.get("remote_address", "")
    protocol = params.get("protocol", "")
    location = params.get("location", "")
    logger.debug("Registration request for alias: %s", decoded_alias)

    allowed_domains = [d.domain for d in AllowedDomain.objects.all()]
    action = "reject"
    if any(decoded_alias.endswith(domain) for domain in allowed_domains):
        action = "continue"

    logger.debug("Action determined: %s", action)
    
    PolicyLog.objects.create(
        policy_type="registration",
        alias=decoded_alias,
        action=action,
        details={
            "remote_address": remote_address,
            "protocol": protocol,
            "location": location
        }
    )

    return {
        "status": "success",
        "action": action,
        "result": {}
    }
