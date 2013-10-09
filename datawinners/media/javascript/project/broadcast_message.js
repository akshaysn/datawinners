DW.broadcast_sms=function(){
    this.clearElementId='#clear_broadcast_sms_form';
    this.formElementId="#broadcast_sms_form";
    this.idToElement="#id_to";
    this.messageCountElement="#messageCount";
    this.smsContentElement="#sms_content";
    this.maxSMSChar=160;
    this.additional_column=new DW.additional_column();

};

DW.broadcast_sms.prototype={
    init:function(){
        this.createSMSContentValidationRule();
        this.createAdditionalTelephoneValidationRule();
        if($('#id_to').val() != 'Additional')
            this.additional_column.hide();
        this.setMessageCount();
        this.updateToFieldText();
        this.updateToMenuItem();
    },

    createAdditionalTelephoneValidationRule:function(){
        this.additional_column.createAdditionalTelephoneValidationRule();
    },
    createSMSContentValidationRule:function(){
        var defaults = $(this.formElementId).validate({
            rules: {
                text:{
                    required:true
                }
            },
            wrapper: "div",
            errorPlacement: function(error, element) {
                error.insertAfter(element);
                error.addClass('error_arrow');  // add a class to the wrapper
            },
            submitHandler: function(form){
                var people_number = DW.broadcast_sms_handler.getPeopleNumber();
                if (people_number >= 100) {
                    DW.broadcast_warning.form = form;
                    $("#number_of_peoples").html(people_number);
                    DW.broadcast_warning.show_warning();
                } else {
                    form.submit();
                }

            }
        });

    },

    processAddtionalColumnValidation:function(){
        if (this.isAdditionalSelected()) {
            this.additional_column.processSelected();
        }
        else {
            this.additional_column.processUnSelected();
        }
        this.updateToFieldText();
    },

    isAdditionalSelected:function(){
        return $(this.idToElement).val() == "Additional";
    },
    setMessageCount:function(){
        $(this.messageCountElement).html("<b>"+ this.getSMSLength() + "</b> of "+this.maxSMSChar);
    },
    getSMSLength:function(){
        return $(this.smsContentElement).val().length;
    },
    clearContent:function(){
        $(this.smsContentElement).val("");
        $(this.additional_column.telephoneNumbersElementId).val("");
        $("#broadcast_sms_form label.error").each(function(){
            $(this).remove();
        });
        this.setMessageCount();
    },
    getSMSContent:function(){
        return $(this.smsContentElement).val()
    },
    limitCount:function () {
        if (this.getSMSLength() > this.maxSMSChar){
            $(this.smsContentElement).val(this.getSMSContent().substring(0, this.maxSMSChar));
        }
        this.setMessageCount();
    },
    getPeopleNumber:function() {
        if (this.isAdditionalSelected())
            return $("#id_others").val().split(',').length;
        return parseInt($(this.idToElement + ' :selected').attr('number'));
    },
    updateToFieldText:function() {
        $("#input_to > span > span:first-child").html($('#id_to option:selected').html());
        $("#input_to > span > span:last-child").html(this.getPeopleNumber() + " " + gettext("recipient(s)"));
        if (this.isAdditionalSelected()) {
            $("#input_to > span > span:last-child").hide();
        } else {
            $("#input_to > span > span:last-child").show();
        }
    },
    updateToMenuItem: function() {
        $("#All span").html($("#id_to option[value=All]").attr('number') + " " + gettext("recipient(s)"));
        $("#Associated span").html($("#id_to option[value=Associated]").attr('number') + " " + gettext("recipient(s)"));
    }
};


DW.additional_column=function(){
    this.additionalPeopleId="#additional_people_column";
    this.telephoneNumbersElementId='#id_others';
    this.telephone_number_rule="regexrule";
};

DW.additional_column.prototype={
    createAdditionalTelephoneValidationRule:function(){
        $.validator.addMethod(this.telephone_number_rule, function(value, element) {
            var text = $('#' + element.id).val();
            var re = new RegExp('^[0-9 ,]+$');
            var telephone_numbers = text.split(',');
            var each;
            var invalid = [];
            var telephone_number = "";
            for (each in telephone_numbers) {
                telephone_number = $.trim(telephone_numbers[each]);
                if (telephone_number.length > DW.digits_number_limit || !re.test(telephone_number)){
                    invalid.push(telephone_number);
                }
            }
            if (invalid.length) {
                $("#id_others").highlightTextarea('setWords', invalid);
                return false;
            }
            return true;
        }, interpolate(gettext("Enter local telephone number of %(limit)s digits or less"), {limit: DW.digits_number_limit}, true));
    },

    addRule:function(){
        $(this.telephoneNumbersElementId).rules("add", this.telephone_number_rule);
        $(this.telephoneNumbersElementId).rules("add", "required");

    },
    show:function(){
        $(this.additionalPeopleId).removeClass('none');
    },
    hide:function(){
        $(this.additionalPeopleId).addClass('none');
    },
    removeRule:function(){
        $(this.telephoneNumbersElementId).rules("remove", this.telephone_number_rule);
        $(this.telephoneNumbersElementId).rules("remove", "required");
    },
    processSelected:function(){
        this.addRule();
        this.show();

    },
    processUnSelected:function(){
        this.removeRule();
        this.hide();
        $(this.telephoneNumbersElementId).val("");
        $(this.telephoneNumbersElementId).valid();

    }
};


DW.getDigitsNumberLimit = function(){
    if (DW.ong_country == "NG") {
        return 11;
    }
    return 10;
};

$(document).ready(function() {
    DW.digits_number_limit = DW.getDigitsNumberLimit();
    DW.broadcast_sms_handler=new DW.broadcast_sms();
    DW.broadcast_sms_handler.init();

    $(DW.broadcast_sms_handler.smsContentElement).keyup(function() {
        DW.broadcast_sms_handler.limitCount();
    });

    $(DW.broadcast_sms_handler.smsContentElement).keydown(function() {
        DW.broadcast_sms_handler.limitCount();
    });

    $('#clear_broadcast_sms_form').click(function() {
        DW.broadcast_sms_handler.clearContent();
    });

    $("#to_list ul li a").bind("click", function(){
        $("#id_to").val($(this).attr("id"));
        DW.broadcast_sms_handler.processAddtionalColumnValidation();
    });

    var kwargs = {container: "#more_people_warning",
        title: gettext('Send Message?'),
        width: 350,
        height: 120,
        continue_handler: function(){
            this.form.submit();
        }
    }
    DW.broadcast_warning = new DW.warning_dialog(kwargs);

});