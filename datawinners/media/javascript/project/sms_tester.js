$(document).ready(function() {
    $(document).ajaxStop($.unblockUI);
    $("#response_info").hide();

    $(".sms_tester_form").dialog({
        autoOpen: false,
        width: 1200,
        modal: true,
        title: gettext("Test SMS Questionnaire"),
        zIndex:1100,
        open: function(){
            $(".questionnaire_preview1").load(sms_questionnaire_preview_link, function() {
                $('.printBtn').addClass('none');
                $('#org_number').text($('.org-number strong').text());
            });
        }
    });

    $("#send_sms").unbind('click').click(function() {
        $.blockUI({ message: '<h1><img src="/media/images/ajax-loader.gif"/><span class="loading">' + gettext("Just a moment") + '...</span></h1>' ,css: { width:'275px', zIndex:1000000}});
        $.post('/test_sms_submission/', {'message':$("#id_message").val(), 'content':$("#id_message").val(), 'test_mode':true}, function(response) {
                    $("#id_message").val(response);
                    if (is_outgoing_sms_replies_enabled == 'True')
                        $("#response_info").show();
                });
    });
    $("#clear_sms").unbind('click').click(function() {
                    $("#id_message").val("");
                    $("#response_info").hide();
    });
    
});