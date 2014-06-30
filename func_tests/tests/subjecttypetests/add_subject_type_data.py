# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


ENTITY_TYPE = 'entity_type'
ERROR_MESSAGE = 'message'
SUCCESS_MESSAGE = 'message'

# valid entity data
VALID_ENTITY = {ENTITY_TYPE: "Hospital", SUCCESS_MESSAGE: "hospital"}
# already exist entity
ALREADY_EXIST_ENTITY = {ENTITY_TYPE: "Clinic", ERROR_MESSAGE: "Clinic already exists."}
# Blank entity
BLANK = {ENTITY_TYPE: "", ERROR_MESSAGE: u"You can't leave this empty."}
INVALID_ENTITY = {ENTITY_TYPE: "W@terpo!nt", ERROR_MESSAGE: u"Please use only letters (a-z), numbers, and spaces."}
SUCCESSFULLY_DELETED_SUBJECT_TYPE_MSG = u"Identification Number Type(s) successfully deleted."
DELETE = "delete"


