$.valHooks.textarea = {
  get: function(elem){
      return elem.value.replace(/\r?\n/g, "\r\n");
  }
};


$(function(){

    var maxAllowedSMSCharacters = 160;

    var smsTextDialog = $("#send-sms-section");

    smsTextDialog.dialog({
        autoOpen: false,
        modal: true,
        title: gettext("Send an SMS"),
        zIndex: 200,
        width: 800,
        height: 600,
        close: function () {
            smsViewModel.clearSelection();
        }
    });

    $("#send_sms").on('click', function(){
        $("#send-sms-section").dialog('open');
    });

    var smsTextLengthCheck = function (e) {
        if (e.target.value.length > maxAllowedSMSCharacters) {
            $(this).val(e.target.value.substring(0, maxAllowedSMSCharacters));
        }

        smsViewModel.smsCharacterCount($(this).val().length + " of " + maxAllowedSMSCharacters + " characters used");
    };

    var smsTextElement = $("#sms-text");

    smsTextElement.keyup(smsTextLengthCheck);

    smsTextElement.keypress(function (e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        var enterKeyCode = 13;

        if(code == enterKeyCode && e.target.value.length + 2 > maxAllowedSMSCharacters){
            e.preventDefault();
            return false;
        }
        return true;
    });

    smsTextElement.keydown(smsTextLengthCheck);

    var smsViewModel = new SmsViewModel();
    window.smsViewModel = smsViewModel;

    ko.applyBindings(smsViewModel, smsTextDialog[0]);

});

function SmsViewModel(){
  var self = this;

  self.selectedSmsOption = ko.observable("");

  self.enableSendSms = ko.computed(function(){
      return this.selectedSmsOption() != undefined;
  }, self);

  self.showOtherContacts = ko.computed(function(){
      return this.selectedSmsOption() == 'Other People';
  }, self);

  self.smsText = DW.ko.createValidatableObservable({value: ""});

  self.smsCharacterCount = ko.observable("0 of 160 characters used");

  self.smsOptionList = ko.observableArray(['Other People']);

  self.smsSentSuccessful = ko.observable(false);

  self.othersList = DW.ko.createValidatableObservable({value: []});

  self.clearSelection = function(){
    self.selectedSmsOption("");
    self.smsText("");
    self.othersList([]);
    self._resetSuccessMessage();
    self._resetErrorMessages();
  };

  self.closeSmsDialog = function(){
    $("#send-sms-section").dialog('close');
    self.clearSelection();
  };


  self.validateSmsText = function(){

    if($("#sms-text").val() == ""){
        self.smsText.setError(gettext("This field is required."));
        return false;
    }
    else{
        self.smsText.clearError();
        return true;
    }

  };

  self.validateOthersList = function(){

    if(self.selectedSmsOption() == 'Other People' && self.othersList() == ""){
        self.othersList.setError(gettext("This field is required."));
        return false;
    }
    else{
        self.othersList.clearError();
        return true;
    }

  };

  self._resetSuccessMessage = function() {
    $("#sms-success").show().addClass("none");
  };

  self._resetErrorMessages = function() {
    $("#no-smsc").show().addClass("none");
    $("#failed-numbers").show().addClass("none");
  };

  self.validate = function(){
    return self.validateSmsText() && self.validateOthersList();
  };

  function _showFailedNumbersError(response) {
       if (response.failednumbers) {
            $("#failed-numbers").text(interpolate(gettext("failed numbers message: %(failed_numbers)s."), {"failed_numbers": response.failednumbers.join(", ")}, true));
            $("#failed-numbers").removeClass("none");
       }
  }

  function _showNoSMSCError(response) {
        if (response.nosmsc) {
              $("#no-smsc").removeClass("none");
        }
  }


  self.sendSms = function(){

      if(!self.validate()){
          return;
      }

      self._resetSuccessMessage();
      self._resetErrorMessages();

      $.post(send_sms_url, {
          'sms-text': $("#sms-text").val(),
          'others': self.othersList(),
          'recipient': self.selectedSmsOption(),
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      }).done(function(response){

          var response = $.parseJSON(response);

          if(response.successful){
              $("#sms-success").removeClass("none");
          }
          else {
              _showNoSMSCError(response);
              _showFailedNumbersError(response);
          }
      });
  };

}
