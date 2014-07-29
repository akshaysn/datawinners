from datawinners.search.mapping import form_model_change_handler, entity_form_model_change_handler
from datawinners.search.submission_index import update_submission_search_index
from datawinners.search.subject_index import entity_search_update
from mangrove.datastore.documents import EntityDocument, FormModelDocument, SurveyResponseDocument, EntityFormModelDocument

from datawinners.search.datasender_index import update_datasender_for_project_change, create_ds_mapping

_postsave_registered = False
def register_postsave_handlers():
    global _postsave_registered
    if _postsave_registered: return
    EntityDocument.register_post_update(entity_search_update)
    EntityFormModelDocument.register_post_update(entity_form_model_change_handler)
    FormModelDocument.register_post_update(form_model_change_handler)
    FormModelDocument.register_post_update(update_datasender_for_project_change)
    SurveyResponseDocument.register_post_update(update_submission_search_index)
    _postsave_registered = True

register_postsave_handlers()