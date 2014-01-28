import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_view_exempt, csrf_response_exempt
from django.views.decorators.http import require_http_methods
from datawinners.main.database import get_db_manager
from datawinners.project.helper import NOT_AVAILABLE_DS
from datawinners.submission.organization_finder import OrganizationFinder
from datawinners.project.data_sender_helper import data_sender_by_mobile
from datawinners.submission.views import sms, _get_from_and_to_numbers

logger = logging.getLogger("django")


def get_organization_setting_by_mobile(mobile):
    return OrganizationFinder().find_organization_setting_includes_trial_account(mobile)


def is_data_sender(data_sender_number, org_settings):
    dbm = get_db_manager(org_settings.document_store)
    data_sender = data_sender_by_mobile(dbm, data_sender_number)
    return data_sender[0] != NOT_AVAILABLE_DS


@csrf_view_exempt
@csrf_response_exempt
@require_http_methods(['POST'])
def process_sms(request):
    _from, _to = _get_from_and_to_numbers(request)
    org_settings = get_organization_setting_by_mobile(_from)
    if org_settings is not None and is_data_sender(_to, org_settings):
        logger.info('got a sms to data sender, stopped.')
        return HttpResponse(status=400)
    else:
        return sms(request)
