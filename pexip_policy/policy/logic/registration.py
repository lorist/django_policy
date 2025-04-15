# registration.py
import logging
# from policy.config import ALLOWED_REGISTRATION_DOMAINS
from policy.models import AllowedDomain



logger = logging.getLogger("pexip_policy.registration")

from urllib.parse import unquote
def get_registration_policy(alias_encoded: str):
    # decoded_alias = unquote(alias_encoded).lower()
    decoded_alias = unquote(alias_encoded).lower().strip()
    logger.debug("Registration request for alias: %s", decoded_alias)

    allowed_domains = [d.domain for d in AllowedDomain.objects.all()]
    action = "reject"
    if any(decoded_alias.endswith(domain) for domain in allowed_domains):
        action = "continue"

    logger.debug("Action determined: %s", action)

    return {
        "status": "success",
        "action": action,
        "result": {}
    }