/**
* jQuery Inline Edit
* Copyright (c) 2009 Markus Hedlund, Mimmin AB
* Version 1.0
* Licensed under MIT license
* http://www.opensource.org/licenses/mit-license.php
* http://labs.mimmin.com/inlineedit
*
*
* Adds inline edit to html elements with classes editableSingle and editableMulti.
* Elements must have class to identify type of data and id.
* Types are linked to urls
*
* Example:
* <li class="editableSingle categoryName id3">
*
* Javascript:
* $.inlineEdit({categoryName: 'category/edit/id/'});
*
*
* Or:
* <td class="editableSingle videoTitle id3"></td>
* <td class="editableMulti videoDescription id3"></td>
*
* Javascript:
* $.inlineEdit({
*     videoTitle: '/video/edit/title/',
*     videoDescription: '/video/edit/description/'
* });
*/

(function($){
$.inlineEdit = function(urls, options){

	var editableUrls = urls;

	var options = jQuery.extend({
        save_label:"Save",
        cancel_label:"Cancel",
		afterSave: function(){},
        beforeSave: function(){},
		afterRemove: function(){},
		getId: getId,
		filterElementValue: function($o){return $o.text();},
		animate: true,
		colors: {
			success: 'green',
			error: 'red'/*,
			standard: '#000'*/
		}
	}, options);

	var initialValues = {};
	var editableFields = false;
	var linkClicked = false;

	if ($('.editableSingle, .editableMulti').length > 0) {
		var simpleMode = $('.editableSingle, .editableMulti')[0].tagName.toLowerCase() != 'td';
		options.colors.standard = $('.editableSingle, .editableMulti').eq(0).css('color');
	}

	$('.editableSingle').click(function(){
		if (linkClicked) {
			linkClicked = false;
			return;
		}

		if (!editableFields || $('.editField').length < editableFields) {
			var value = options.filterElementValue($(this));
			saveInitialValue($(this));
			$(this).addClass('isEditing').css('color', options.colors.standard).stop();

			if ($('.editFieldFirst').length == 0) {
				editableFields = $(this).siblings('.editableSingle, .editableMulti').length + 1;
				$(this).html('<div class="editFieldWrapper"><input type="text" value=""  class="editField editFieldFirst" /></div>');

				if (!simpleMode) {
				   $(this).siblings('.editableSingle, .editableMulti').click();
				} else {
					editableFields = 1;
				}

				addSaveControllers(function(){
					$('.editFieldFirst').focus();
				});
			} else {
				$(this).html('<div class="editFieldWrapper"><input type="text" value="" class="editField" /></div>');
			}
//          The value for the editbox is set separately to handle strings enclosed in quotes e.g "Some Text"
            $(this).find(".editFieldWrapper input").val(value);
		}
	});

	$('.editableMulti').click(function(){
		if (linkClicked) {
			linkClicked = false;
			return false;
		}

		if (!editableFields || $('.editField').length < editableFields) {
			var value = options.filterElementValue($(this));
			saveInitialValue($(this));
			$(this).addClass('isEditing').css('color', options.colors.standard).stop();

			if ($('.editFieldFirst').length == 0) {
				editableFields = $(this).siblings('.editableSingle, .editableMulti').length + 1;
				$(this).html('<div class="editFieldWrapper"><textarea class="editField editFieldFirst"></textarea></div>');

				if (!simpleMode) {
				   $(this).siblings('.editableSingle, .editableMulti').click();
				}

				addSaveControllers(function(){
					$('.editFieldFirst').focus();
				});
			} else {
				$(this).html('<div class="editFieldWrapper"><textarea class="editField"></textarea></div>');
			}
            //          The value for the editbox is set separately to handle strings enclosed in quotes e.g "Some Text"
            $(this).find(".editFieldWrapper textarea").val(value);
		}
	});

	$('.editableSingle a, .editableMulti a').click(function(){
		linkClicked = true;
	});

	function addSaveControllers(callback)
	{
        var editFieldSection;

        if ($('.editFieldWrapper:last').parent().hasClass('removable')) {
             editFieldSection = $('<div class="editFieldSaveControllers"><button>Save</button>' +
                ', <a href="javascript:;" class="editFieldRemove">Remove</a>' +
                '<a href="javascript:;" class="editFieldCancel">Cancel</a></div>');

   			 $('.editFieldWrapper:last').append(editFieldSection);
		} else {
            editFieldSection = $('<div class="editFieldSaveControllers"><span class="error"><span class="error_arrow_left"></span><span class="message"></span></span><button>' + options.save_label+  '</button>' +
				'<a href="javascript:;" class="editFieldCancel">' + options.cancel_label+ '</a></div>');
			$('.editFieldWrapper:last').append(editFieldSection);
		}

		$('.editFieldSaveControllers > button').click(function(){
            editSave(editFieldSection);
        });
		$('.editFieldSaveControllers > a.editFieldCancel').click(editCancel);
		$('.editFieldSaveControllers > a.editFieldRemove').click(editRemove);
		$('input.editField').keydown(function(e){
			if (e.keyCode == 13) {
				// Enter
				editSave(editFieldSection);
			} else if (e.keyCode == 27) {
				// Escape
				editCancel();
			}
		});

		if (options.animate) {
			$('.editFieldWrapper').slideDown(500, callback);
		} else {
			$('.editFieldWrapper').show();
			callback();
		}
	}

	function editCancel(e)
	{
		linkClicked = typeof(e) != 'undefined';   // If e is set, call comes from mouse click

		$('.editField').each(function(){
			var $td = $(this).parents('.editableSingle, .editableMulti');
			removeEditField($td, getInitialValue($td), false);
		});
	}

	function editRemove()
	{
		linkClicked = true;

		if (!confirm('Are you sure that you want to remove this?')) {
			return false;
		}

		$('.editFieldSaveControllers > button, .editField').attr('disabled', 'disabled').html('Removing...');

		var $td = $('.editField').eq(0).parents('.editableSingle, .editableMulti');
		var url = editableUrls.remove;
		var id = options.getId($td);

		$.ajax({
			url: url + id,
			type: 'POST',
			success: function(msg){
				$('.editField').each(function(){
					var $td = $(this).parents('.editableSingle, .editableMulti');

					if (msg == 1) {
						if (options.animate) {
							$td.slideUp(500, function(){
								$(this).remove();
							});
						} else {
							$td.remove();
						}
					} else {
						removeEditField($td, getInitialValue($td), true, options.colors.error);
					}
				});

				options.afterRemove({
					success: msg == 1,
					id: id
				});
			},
			error: function(){
				$('.editField').each(function(){
					var $td = $(this).parents('.editableSingle, .editableMulti');
					removeEditField($td, getInitialValue($td), false, options.colors.error);
				});
			}
		});
	}

	function removeEditField($td, value, animateColor, fromColor)
	{
		var f = function(){
			$td.text(value).removeClass('isEditing');
			if (animateColor) {
				$td.css('color', fromColor)/*.animate({color: options.colors.standard},5000)*/;
				setTimeout(function(){
					$td.css('color', options.colors.standard);
				}, 2000);
			} else if (typeof(fromColor) != 'undefined') {
				$td.css('color', fromColor);
			}
		};

		if (options.animate) {
			$td.children('.editFieldWrapper').slideUp(500, f);
		} else {
			$td.children('.editFieldWrapper').hide();
			f();
		}
	}

	function saveInitialValue($td)
	{
		var index = options.getId($td) + getTypeAndUrl($td).type;
		initialValues[index] = $td.text();
	}

	function getInitialValue($td)
	{
		var index = options.getId($td) + getTypeAndUrl($td).type;
		return initialValues[index];
	}

	function getId($td)
	{
		var id;
		$.each($td.attr('class').split(' '), function(index, name){
			if (name.match(/^id[0-9]*$/)) {
				id = name.match(/^id([0-9]*)$/)[1];
				return false;
			}
		});
		return id;
	}

	function getTypeAndUrl($td)
	{
		var typeAndUrl;
		$.each(editableUrls, function(index, name){
			if ($td.hasClass(index)) {
				typeAndUrl = {type: index, url: name};
				return false;
			}
		});
		return typeAndUrl;
	}

	function editSave(editFieldSection)
	{
        options.beforeSave(editFieldSection);
		$('.editFieldSaveControllers > button, .editField').attr('disabled', 'disabled');
        $(".editFieldSaveControllers .error").hide();
		$('.editField').each(function(){
			var $td = $(this).parents('.editableSingle, .editableMulti');
			var typeAndUrl = getTypeAndUrl($td);
			var url = typeAndUrl.url;   // Get save URL
			var id = options.getId($td);
			var value = $(this).val();
			var color = options.colors.standard;

			$.ajax({
				url: url + id,
				data: {data: value},
				type: 'POST',
				success: function(resp){
					if (resp.status == "success") {
						removeEditField($td, value, true, options.colors.success);
					} else {
                        $(".editFieldSaveControllers .error .message").text(resp.message);
                        $(".editFieldSaveControllers .error").show()
                        $('.editFieldSaveControllers > button, .editField').removeAttr('disabled');
					}

					options.afterSave({
						success: resp.status == "success",
						type: typeAndUrl.type,
						id: id,
						value: value,
                        editFieldSection: editFieldSection
					});
				},
				error: function(){
					removeEditField($td, getInitialValue($td), false, options.colors.error);
				}
			});
		});
	}
};
})(jQuery);