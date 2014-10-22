DW.instruction_and_preview = function (preview_url, preview_navigation_item, preview_type) {
    this.preview_url = preview_url;
    this.preview_navigation_item = preview_navigation_item;
    this.preview_type = preview_type;
};

DW.instruction_and_preview.prototype = {
    bind_preview_navigation_item: function () {
        var that = this;
        $(this.preview_navigation_item).click(function () {
            DW.trackEvent('questionnaire', that.preview_type + '-preview-clicked');
            DW.instruction_and_preview.remove_sms_questionnaire_print();
            if ($("#questionnaire_preview_instruction").css("display") == "none") {
                if(!(questionnaireViewModel.validateQuestionnaireDetails() && questionnaireViewModel.validateSelectedQuestion()))
                    return false;
                that.load_preview_content();
            }
            else
                that.load_preview_content();
        });
    },

    load_preview_content: function () {
        var post_data = this.get_post_data();
        var that = this;
        $.blockUI({ message: '<h1><img src="/media/images/ajax-loader.gif"/><span class="loading">' + gettext("Just a moment") + '...</span></h1>', css: { width: '275px'}});
        $(".shadow-background").removeClass("shadow-background");
        $(that.preview_navigation_item).addClass("shadow-background");

        $.post(this.preview_url, post_data, function (response_data) {
            $("#questionnaire_content").html(response_data);
            $('.errorlist').remove();
            $("#questionnaire_preview_instruction").show();
            that.post_callback();
            $.unblockUI();
        }, 'html');
    },

    get_post_data: function () {
        return {'questionnaire-code': $('#questionnaire-code').val(),
            'question-set': JSON.stringify(ko.toJS(questionnaireViewModel.questions()), null, 2),
            'profile_form': basic_project_info(),
            'project_state': "Test",
            'csrfmiddlewaretoken': $('#question_form input[name=csrfmiddlewaretoken]').val()};
    },

    post_callback: function () {
    }
};

DW.web_instruction_and_preview = function () {
};
DW.web_instruction_and_preview.prototype = new DW.instruction_and_preview(web_preview_link, '.navigation-web-preview', 'web');
DW.web_instruction_and_preview.prototype.post_callback = function () {
    $("#questionnaire_preview_instruction .help_icon").tooltip({
        position: "top right",
        relative: true,
        opacity: 0.8,
        events: {
            def: "mouseover,mouseout",
            input: "focus,blur",
            widget: "focus mouseover,blur mouseout",
            tooltip: "click,click"
        }

    }).dynamic({ bottom: { direction: 'down', bounce: true } });
};

DW.sms_instruction_and_preview = function() {
};
DW.sms_instruction_and_preview.prototype = new DW.instruction_and_preview(sms_preview_link, '.navigation-sms-preview', 'sms');
DW.sms_instruction_and_preview.prototype.post_callback = function () {
    var questionnaire = $(".sms-questionnaire").clone();
    questionnaire.addClass("sms-questionnaire");
    questionnaire.hide();
    questionnaire.appendTo($("body"));
    $("body > div").addClass("none_for_print");
};

DW.smart_phone_instruction_and_preview = function(){
};
DW.smart_phone_instruction_and_preview.prototype = new DW.instruction_and_preview(smart_phone_preview_link, '.navigation-smart-phone-preview', 'smart-phone');
DW.smart_phone_instruction_and_preview.prototype.get_post_data = function () {
    return {};
};

DW.instruction_and_preview.bind_cancel_button = function () {
    $(".close_preview").live('click', function () {
        $("#questionnaire_content").html("");
        $("#questionnaire_preview_instruction").hide();
        $(".shadow-background").removeClass("shadow-background");
        DW.instruction_and_preview.remove_sms_questionnaire_print();
        $("body > div").removeClass("none_for_print");
    });
};

DW.instruction_and_preview.remove_sms_questionnaire_print = function () {
    $("body > .sms-questionnaire").remove()
}

DW.instruction_and_preview.bind_print_button = function () {
    $(".printBtn").live('click', function (event) {
        window.print();
        event.preventDefault();
    });
};

$(function () {
    DW.instruction_and_preview.bind_cancel_button();
    DW.instruction_and_preview.bind_print_button();
});