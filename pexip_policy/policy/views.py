from django.http import JsonResponse
from django.views.decorators.http import require_GET
from urllib.parse import unquote
import logging
from .logic.registration import get_registration_policy
from .logic.participant import get_participant_properties
from .logic.service import get_service_configuration

# logger = logging.getLogger(__name__)
logger = logging.getLogger("pexip_policy")



@require_GET
def registration_policy(request, alias):
    response_data = get_registration_policy(alias)
    logger.debug("Registration response: %s", response_data)
    return JsonResponse(response_data)

@require_GET
def participant_properties(request):
    response_data = get_participant_properties(request.GET.dict())
    logger.debug("Participant response: %s", response_data)
    return JsonResponse(response_data)

@require_GET
def service_configuration(request):
    local_alias = request.GET.get("local_alias", "")
    response_data = get_service_configuration(local_alias)
    logger.debug("Service response: %s", response_data)
    return JsonResponse(response_data)