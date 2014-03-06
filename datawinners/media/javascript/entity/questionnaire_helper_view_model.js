var questionnaireHelperModel = {
        selectedTemplateId: ko.observable(),
        showQuestionnaireCreationOptions: ko.observable(),
        templateData: ko.observable(),

        chooseTemplate: function (template) {
            var template_id = template.id;
            questionnaireHelperModel.selectedTemplateId(template_id);
            questionnaireHelperModel.templateData(DW.getTemplateData(template_id));
        },
        removeTemplateId: function () {
            questionnaireHelperModel.selectedTemplateId(null);
        },
        templateGroupingData: ko.observable(),
        getTemplates: function () {
            questionnaireHelperModel.removeTemplateId();
            setTimeout(function () {
                if (DW.templateGroupingDataCache) {
                    questionnaireHelperModel.templateGroupingData(DW.templateGroupingDataCache.categories);
                }
                else {
                    $.ajax({
                        type: 'GET',
                        url: "/project/templates/",
                        success: function (data) {
                            DW.templateGroupingDataCache = data;
                            questionnaireHelperModel.templateGroupingData(data.categories);
                        }
                    })
                }
            }, 0);
        },
        gotoQuestionnaireLoader: function (question_template_id) {
            location.hash = 'questionnaire/load/' + question_template_id;
        },
        setQuestionnaireCreationType: function () {
            var selectedOption = $('#questionnaire_types').accordion('option', 'active');
            if (selectedOption == 0) {
                location.hash = 'questionnaire/new';
            }
            else if (selectedOption == 1 || 2) {
                var question_template_id = questionnaireHelperModel.selectedTemplateId();
                questionnaireHelperModel.gotoQuestionnaireLoader(question_template_id);
            }
        }
    }
    ;