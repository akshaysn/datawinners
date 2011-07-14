from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from datawinners import utils
from datawinners.main.utils import get_database_manager
from datawinners.project import models
from datawinners.project.views import project_overview, project_data, project_results
from mangrove.form_model.form_model import FormModel
from datawinners.submission.models import DatawinnerLog

@login_required(login_url='/login')
@utils.is_new_user
def index(request):
    project_list = []
    analysis = log = ""
    disabled = "disabled"
    manager = get_database_manager(request)
    rows = models.get_all_projects(dbm=manager)
    for row in rows:
        project_id = row['value']['_id']
        project = models.get_project(project_id, dbm=manager)
        questionnaire = manager.get(project['qid'], FormModel)
        questionnaire_code=questionnaire.form_code
        link = reverse(project_overview, args=[project_id])
        if project.state == models.PROJECT_ACTIVE_STATUS:
            disabled=""
            analysis = reverse(project_data, args=[project_id, questionnaire_code])
            log=reverse(project_results, args=[project_id, questionnaire_code])

        project = dict(name=row['value']['name'], created=row['value']['created'], type=row['value']['project_type'],
                       link=link, log=log, analysis=analysis)
        project_list.append(project)
    return render_to_response('alldata/index.html', {'projects': project_list, 'disabled':disabled}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def failed_submissions(request):
    logs = DatawinnerLog.objects.all()
    return render_to_response('alldata/failed_submissions.html', {'logs': logs}, context_instance=RequestContext(request))