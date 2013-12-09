import unittest
import datetime
from datawinners.accountmanagement.models import Organization, MessageTracker
from datawinners.accountmanagement.organization_id_creator import OrganizationIdCreator
from dateutil.relativedelta import relativedelta
from mock import Mock, patch


class TestOrganization(unittest.TestCase):
    def setUp(self):
        self.organization = self._prepare_organization()

    def tearDown(self):
        self.organization.delete()

    def test_should_increment_sms_api_usage_count(self):
        self.organization.increment_sms_api_usage_count()
        message_tracker = self._get_current_message_tracker_of_organization()
        self.assertEquals(1, message_tracker.sms_api_usage_count)

    def test_should_increment_message_count(self):
        self.organization.increment_all_message_count()
        message_tracker = self._get_current_message_tracker_of_organization()
        self.assertEquals(1, message_tracker.incoming_sms_count)
        self.assertEquals(1, message_tracker.outgoing_sms_count)

        message_tracker = self._get_current_message_tracker_of_organization()
        message_tracker.incoming_sms_count = 3
        message_tracker.outgoing_sms_count = 3
        message_tracker.save()

        self.organization.increment_all_message_count()
        message_tracker = self._get_current_message_tracker_of_organization()
        self.assertEquals(4, message_tracker.incoming_sms_count)
        self.assertEquals(4, message_tracker.outgoing_sms_count)

    def test_should_check_trial_org_message_count(self):
        self.assertFalse(self.organization.has_exceeded_message_limit())
        message_tracker = self._get_current_message_tracker_of_organization()
        message_tracker.incoming_sms_count = 51
        message_tracker.save()
        self.assertTrue(self.organization.has_exceeded_message_limit())

    def _prepare_organization(self):
        trial_organization = Organization(name='test_org_for_trial_account',
                                          sector='PublicHealth', address='add',
                                          city='Pune', country='IN',
                                          zipcode='411006', in_trial_mode=True,
                                          org_id=OrganizationIdCreator().generateId(),
                                          status='Activated')
        trial_organization.save()
        return trial_organization

    def _get_current_message_tracker_of_organization(self):
        current_month = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, 1)
        message_tracker = self.organization._get_message_tracker(current_month)
        return message_tracker

    def test_should_return_country_phone_code(self):
        country_code = self.organization.get_phone_country_code()
        self.assertEqual(country_code, "91")

    def test_should_increment_by_submission_type(self):
        increment_count_by_submission_type_dict = {'incoming_sms_count': 4,'incoming_sp_count':2, 'incoming_web_count':7}
        self.organization.increment_message_count_for(**increment_count_by_submission_type_dict)
        message_tracker = self._get_current_message_tracker_of_organization()
        for field_name, count in increment_count_by_submission_type_dict.items():
            self.assertEqual(getattr(message_tracker, field_name), count)
        
    def test_check_expired_organization(self):
        organization = self.organization
        active_date = datetime.datetime.now() - relativedelta(years=1)
        organization.active_date = active_date
        organization.status_changed_datetime = active_date
        self.assertTrue(organization.is_expired())

    def test_get_counters(self):
        today = datetime.datetime.today()
        mt_current_month = MessageTracker(month=datetime.date(today.year, today.month, 1),
            incoming_web_count=3, incoming_sms_count=40, incoming_sp_count=10, sms_api_usage_count=3,
            sms_registration_count=4, sent_reminders_count=10, send_message_count=30, outgoing_sms_count=40
        )
        mt_last_month = MessageTracker(month=datetime.date(today.year, today.month - 1, 1),
            incoming_web_count=10, incoming_sms_count=45, incoming_sp_count=7, sms_api_usage_count=3,
            sms_registration_count=4, sent_reminders_count=10, send_message_count=30, outgoing_sms_count=40
        )
        message_trackers = [mt_current_month, mt_last_month]

        expected = {'combined_total_submissions': 107, 'send_a_msg_current_month': 30, 'sent_via_api_current_month': 3,
                    'sms_reply_reminders': 50, 'sms_submission_current_month': 36, 'sp_submission_current_month': 10,
                    'total_sent_sms': 83, 'total_sms_current_month': 123, 'total_sms_submission': 77,
                    'total_sp_submission': 17, 'total_submission_current_month': 49, 'total_web_submission': 13,
                    'web_submission_current_month': 3}
        
        with patch.object(Organization, '_get_all_message_trackers') as get_all_message_trackers_mock:
            get_all_message_trackers_mock.return_value = message_trackers
            counters = self.organization.get_counters()
            self.assertEqual(counters, expected)

