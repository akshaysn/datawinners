DW.CancelWarningDialog = function (options) {
    var self = this;
    var _successCallBack = options.successCallBack;
    var isQuestionnaireModified = options.isQuestionnaireModified;
    var _cancelCallback = options["cancelCallback"]|| function(){};
    var _ignoreCallback = options["ignoreCallback"]|| function(){};
    var _redirect = options["actionCallback"] || function () {
        window.location.href = self.redirect_url;
        return true;
    };

    this.init = function () {
        var canceDialogDiv = options.cancelDialogDiv || "#cancel_questionnaire_warning_message";
        var dialogId = canceDialogDiv.substring(1) + "_dialog_section";
        self.cancelDialog = $('<div id='+ dialogId +'>').html($(canceDialogDiv).html());
        self.ignoreButton = self.cancelDialog.find(".no_button");
        self.saveButton = self.cancelDialog.find(".yes_button");
        self.cancelButton = self.cancelDialog.find("#cancel_dialog");
        _initializeDialog();
        _initializeIgnoreButtonHandler();
        _initializeCancelButtonHandler();
        _initializeSaveButtonHandler();
        return this;
    };

    this.show = function(){
        self.cancelDialog.dialog("open");
    }

    var _initializeDialog = function () {
        self.cancelDialog.dialog({
            title: gettext("You Have Unsaved Changes"),
            modal: true,
            autoOpen: false,
            width: 550,
            closeText: 'hide'
        });
    };

    var _initializeIgnoreButtonHandler = function () {
        self.ignoreButton.bind('click', function (event) {
            _ignoreCallback();
            self.cancelDialog.dialog("close");
            return _redirect(event);
        });
    };

    var _initializeCancelButtonHandler = function () {
        self.cancelButton.bind('click', function () {
            _cancelCallback();
            self.cancelDialog.dialog("close");
            return false;
        });
    };

    var _initializeSaveButtonHandler = function () {
        self.saveButton.bind('click', function (event) {
            if(options.validate()) {
                _successCallBack(function () {
                    self.cancelDialog.dialog("close");
                    return _redirect(event);
                });
            }
            self.cancelDialog.dialog("close");
        });
    };

    this.initializeLinkBindings = function () {
        var default_ignore_links = ".add_link, .preview-navigation a, .sms_tester, .delete_project, #dw_help_link";
        var ignore_links = options.ignore_links ? default_ignore_links + "," + options.ignore_links : default_ignore_links;

        $("a[href]:visible, a#back_to_create_options, a#cancel_questionnaire").not(ignore_links).bind('click', {self: this}, function (event) {
            var that = event.data.self;
            self.redirect_url = $(this).attr("href");
            if (isQuestionnaireModified()) {
                self.cancelDialog.dialog("open");
                return false;
            }
            else
                return _redirect();
        });
    };

};