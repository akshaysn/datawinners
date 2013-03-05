import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from datawinners.accountmanagement.views import session_not_expired
from mangrove.form_model.form_model import get_form_model_by_code
from mangrove.utils.json_codecs import encode_json

from datawinners.accountmanagement.views import is_datasender
from datawinners.main.utils import get_database_manager, timebox
from datawinners.accountmanagement.views import is_not_expired
from project import header_helper, helper
from project.ExcelHeader import ExcelFileAnalysisHeader
from project.analysis import Analysis
from project.analysis_for_excel import AnalysisForExcel
from project.export_to_excel import _prepare_export_data, _create_excel_response
from project.utils import    project_info
from project.views.views import XLS_TUPLE_FORMAT
from datawinners.project.submission_utils.submission_formatter import SubmissionFormatter

performance_logger = logging.getLogger("performance")

@login_required(login_url='/login')
@session_not_expired
@is_datasender
@is_not_expired
@timebox
def project_data(request, project_id=None, questionnaire_code=None):
    analysis_result = get_analysis_response(request, project_id, questionnaire_code)
    if request.method == "GET":
        return render_to_response('project/data_analysis.html',
            analysis_result,
            context_instance=RequestContext(request))
    elif request.method == "POST":
        return HttpResponse(analysis_result)


# TODO : merge with the calling function
@timebox
def get_analysis_response(request, project_id, questionnaire_code):
    manager = get_database_manager(request.user)
    form_model = get_form_model_by_code(manager, questionnaire_code)

    #Analysis page wont hv any type since it has oly success submission data.
    filters = request.POST
    keyword = request.POST.get('keyword', '')
    analysis = Analysis(form_model, manager, helper.get_org_id_by_user(request.user), filters, keyword)
    analysis_result = analysis.analyse()

    performance_logger.info("Fetch %d submissions from couchdb." % len(analysis_result.field_values))
    if request.method == 'GET':
        project_infos = project_info(request, manager, form_model, project_id, questionnaire_code)
        header_info = header_helper.header_info(form_model)
        analysis_result_dict = analysis_result.analysis_result_dict
        analysis_result_dict.update(project_infos)
        analysis_result_dict.update(header_info)
        return analysis_result_dict

    elif request.method == 'POST':
        return encode_json(
            {
                'data_list': analysis_result.field_values, "statistics_result": analysis_result.statistics_result
            }
        )

@login_required(login_url='/login')
@session_not_expired
@is_datasender
@is_not_expired
@timebox
def export_data(request):
    project_name = request.POST.get(u"project_name")
    filters = request.POST
    keyword = request.POST.get('keyword', '')

    user = helper.get_org_id_by_user(request.user)
    manager = get_database_manager(request.user)

    questionnaire_code = request.POST.get('questionnaire_code')
    form_model = get_form_model_by_code(manager, questionnaire_code)

    submissions = AnalysisForExcel(form_model, manager, user, filters, keyword)
    formatted_values = SubmissionFormatter().get_formatted_values_for_list(submissions.get_raw_values(),
        tuple_format=XLS_TUPLE_FORMAT)
    header_list = ExcelFileAnalysisHeader(form_model).header_list
    exported_data, file_name = _prepare_export_data(None, project_name, header_list, formatted_values)
    return _create_excel_response(exported_data, file_name)
