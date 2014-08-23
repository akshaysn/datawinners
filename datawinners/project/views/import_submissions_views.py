from collections import OrderedDict
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_view_exempt, csrf_response_exempt
from django.views.generic.base import View
from datawinners.monitor.carbon_pusher import send_to_carbon
from datawinners.monitor.metric_path import create_path
from mangrove.form_model.form_model import get_form_model_by_code

from datawinners.accountmanagement.decorators import session_not_expired, is_not_expired
from datawinners.accountmanagement.models import Organization, NGOUserProfile
from datawinners.feeds.database import get_feeds_database
from datawinners.main.database import get_database_manager
from datawinners.project.models import Project
from datawinners.project.submission.submission_import import SubmissionImporter


class SubmissionQuotaService(object):
    def __init__(self, organization):
        self.organization = organization

    def increment_web_submission_count(self):
        self.organization.increment_message_count_for(incoming_web_count=1)

    def has_exceeded_quota_and_notify_users(self):
        return self.organization.has_exceeded_quota_and_notify_users()


class ImportSubmissionView(View):
    def post(self, request, form_code):
        manager = get_database_manager(request.user)
        feeds_dbm = get_feeds_database(request.user)
        project_id = request.GET["project_id"]
        form_model = get_form_model_by_code(manager, form_code)
        user_profile = NGOUserProfile.objects.get(user=request.user)
        organization = Organization.objects.get(org_id=user_profile.org_id)
        submission_importer = SubmissionImporter(manager, feeds_dbm, request.user, form_model,
                                                 SubmissionQuotaService(organization))
        response = submission_importer.import_submission(request)
        send_to_carbon(create_path('submissions.import'), 1)
        return HttpResponse(
            json.dumps(
                {
                    "success": self._successful(response),
                    "question_map": self._get_question_code_map(form_model, request),
                    "success_submissions": response.saved_entries,
                    "errored_submission_details": response.errored_entrie_details,
                    "message": response.message,
                    "total_submissions": response.total_submissions,
                    "quota_over": self._is_submission_quota_over(response)
                }))

    def _is_submission_quota_over(self, response):
        return True if response.ignored_entries else False

    def _successful(self, response):
        return True if response.saved_entries \
                           and not response.ignored_entries \
            and not response.errored_entrie_details else False

    @method_decorator(csrf_view_exempt)
    @method_decorator(csrf_response_exempt)
    @method_decorator(login_required)
    @method_decorator(session_not_expired)
    @method_decorator(is_not_expired)
    def dispatch(self, *args, **kwargs):
        return super(ImportSubmissionView, self).dispatch(*args, **kwargs)

    def _get_question_code_map(self, form_model, request):
        submission_headers_for_user = form_model.form_fields
        return OrderedDict([(field["code"], field["label"]) for field in submission_headers_for_user])
