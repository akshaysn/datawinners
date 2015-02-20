from django.contrib.auth.models import User
from django.utils.translation import ugettext
from datawinners.accountmanagement.models import NGOUserProfile
from datawinners.project.data_sender import DataSender
from datawinners.project.helper import NOT_AVAILABLE_DS, NOT_AVAILABLE
from mangrove.datastore.entity import Entity, get_by_short_code_include_voided
from mangrove.transport.repository.reporters import REPORTER_ENTITY_TYPE


# def combine_channels_for_tuple(data_senders_tuple_list):
#     data_senders = [DataSender.from_tuple(data_sender_tuple) for data_sender_tuple in data_senders_tuple_list]
#     return map(lambda d: (d.name, d.reporter_id, d.uid), set(data_senders))


def get_data_sender(manager, submission):
    if submission.owner_uid:
        try:
            data_sender_entity = Entity.get(manager, submission.owner_uid)
            return data_sender_entity.value("name"), data_sender_entity.short_code, data_sender_entity.id
        except Exception as e:
            pass #ignore and sending unknown datasender for backward compatibility.
    return NOT_AVAILABLE_DS, NOT_AVAILABLE

# def get_data_sender_by_reporter_id(dbm, reporter_id):
#     return get_by_short_code_include_voided(dbm, reporter_id, REPORTER_ENTITY_TYPE)

# def get_data_sender_by_source(manager, org_id, channel, source):
#     if channel == 'sms':
#         return get_data_sender_for_sms(manager, source)
#     else:
#         return get_data_sender_for_not_sms(org_id, email=source)


# def get_data_sender_for_sms(manager, source):
#     return tuple(data_sender_by_mobile(manager, source))


# def get_data_sender_for_not_sms(org_id, email):
#     try:
#         data_sender = data_sender_by_email(org_id, email)
#     except:
#         data_sender = (ugettext(NOT_AVAILABLE_DS), None, email)
#     return data_sender


# def data_sender_by_mobile(manager, mobile):
#     rows = manager.load_all_rows_in_view("datasender_by_mobile", startkey=[mobile], endkey=[mobile, {}])
#     return rows[0].key[1:] if len(rows) > 0 else [ugettext(NOT_AVAILABLE_DS), None]


# def data_sender_by_email(org_id, email):
#     data_sender = User.objects.get(email=email)
#     reporter_id = NGOUserProfile.objects.filter(user=data_sender, org_id=org_id)[0].reporter_id or "admin"
#     return data_sender.get_full_name(), reporter_id, email


def list_data_sender(org_id):
    ngo_user_profiles = list(NGOUserProfile.objects.filter(org_id=org_id).all())
    return [DataSender(each.user.email, each.user.get_full_name(), each.reporter_id or "admin") for each in
            ngo_user_profiles]