$(document).ready(function () {
    var LAST_NAME_COLUMN_INDEX = 2;
    var dt = $('#subjects_table').dataTable({
        "bProcessing": true,
        "bServerSide": true,
        "bResetDisplay": true,
        "aLengthMenu": [10, 25, 50, 100],
        "iDisplayLength": 25,
        "sDom": "ipfrtipl",
        "sInput": "",
        "aoColumnDefs": [
            { "sClass": "center",
                "sTitle": "<input type='checkbox'id='checkall-checkbox'></input>",
                "fnRender": function (data) {
                    return '<input type="checkbox" value=' + data.aData[data.aData.length - 1] + ' />';
                },
                "aTargets": [0]
            },
            {"bSortable": false, "aTargets": [0]}
        ],
        "oLanguage": {"sInfoFiltered": "",
            "sLengthMenu": "Show _MENU_ " + subject_type,
            "sProcessing": "<img class=\"search-loader\"src=\"/media/images/ajax-loader.gif\"></img>",
            "sInfo": "<b>_START_ to _END_</b> of _TOTAL_ " + subject_type,
            "sInfoEmpty": "<b> 0 to 0</b> of 0 " + subject_type,
            "sEmptyTable": $('#no_registered_subject_message').clone().removeAttr("hidden").html(),
            "oPaginate": {"sFirst": "", "sPrevious": "◀", "sNext": "▶", "sLast": ""}},
        "sPaginationType": "dw_pagination",
        "sAjaxSource": '/entity/subjects/' + subject_type.toLowerCase() + '/ajax/',
        "sAjaxDataProp": "subjects",
        "sServerMethod": "GET",
        "fnInitComplete": function (oSettings) {
            $(".action_bar").clone(true).insertBefore(".dataTables_info").addClass('margin_top_10').removeAttr('hidden').show();
            new DW.ActionsMenu();
            oSettings.select_all_checkbox = new DW.SubjectSelectAllCheckbox(this);
        },
        "fnPreDrawCallback": function (oSettings) {
            new DW.SubjectPagination().deactivate_select_across_pages();
            if (oSettings.select_all_checkbox) oSettings.select_all_checkbox.un_check();
        },
        "fnDrawCallback": function (oSettings) {
            $(".styled_table thead input:checkbox").attr("disabled", oSettings.fnRecordsDisplay() == 0)
        },
        "aaSorting": [
            [ LAST_NAME_COLUMN_INDEX, "asc"]
        ],
        "fnServerData": function (sSource, aoData, fnCallback, oSettings) {
            oSettings.jqXHR = $.ajax({
                "dataType": 'json',
                "type": "GET",
                "url": sSource,
                "data": aoData,
                "success": function (result) {
                    $.each(result.subjects, function (i, subject) {
                        subject.unshift('')
                    });
                    fnCallback(result);
                },
                "error": function () {
                },
                "global": false
            });
        }
    });

    $("select[name='subjects_table_length']").change(function () {
        $('#subjects_table').dataTable({"bRetrieve": true}).fnPageChange("first")
    });

    $("#subjects_table_filter").find("input").attr('placeholder', 'Enter any information you want to find');

    $('#subjects_table_filter').live('change', function () {
            new DW.SubjectPagination(dt).deactivate_select_across_pages();
        }
    );
});


