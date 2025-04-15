# registration.py
import logging
from policy.config import ALLOWED_REGISTRATION_DOMAINS


logger = logging.getLogger("pexip_policy.registration")

from urllib.parse import unquote
def get_registration_policy(alias_encoded: str):
    decoded_alias = unquote(alias_encoded).lower()

    logger.debug("Registration request for alias: %s", decoded_alias)

    # Default action is to continue
    action = "reject"

    # Allow aliases ending with domains that are listed in the config.py
    allowed_domains = ALLOWED_REGISTRATION_DOMAINS
    if any(decoded_alias.endswith(d) for d in allowed_domains):
        action = "continue"

    logger.debug("Action determined: %s", action)

    result_data = {}

    return {
        "status": "success",
        "action": action,
        "result": result_data
    }
