# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import re

from nose.plugins.attrib import attr

from framework.base_test import HeadlessRunnerTest
from framework.utils.common_utils import by_css
from pages.languagespage.customized_language_locator import ACCOUNT_WIDE_MESSAGE_TEXTBOXES_LOCATOR, \
    DATA_SENDER_NOT_REGISTERED_LOCATOR
from pages.languagespage.customized_languages_page import CustomizedLanguagePage
from pages.loginpage.login_page import login
from pages.smstesterpage.sms_tester_page import SMSTesterPage
from testdata.test_data import DATA_WINNER_SMS_TESTER_PAGE, CUSTOMIZE_MESSAGES_URL
from tests.testsettings import UI_TEST_TIMEOUT


default_messages = [u'Error. You are not registered as a Data Sender. Please contact your supervisor.',
                        u'Error. Questionnaire Code {Submitted Questionnaire Code} is incorrect. Find the Code on the top of the printed Questionnaire and resend SMS starting with this Code.',
                        u'Thank you {Name of Data Sender}.We registered your {Identification Number Type} {Name of Identification Number} {Submitted Identification Number}.',
                        u'Error. {Submitted Identification Number} already exists. Register your {Identification Number Type} with a different Identification Number.']

class TestAccountWideSMS(HeadlessRunnerTest):
    @classmethod
    def setUpClass(cls):
        HeadlessRunnerTest.setUpClass()
        login(cls.driver, landing_page="customizemessages/")

    def setUp(self):
        self.language_page = CustomizedLanguagePage(self.driver)

    def tearDown(self):
        self.driver.go_to(CUSTOMIZE_MESSAGES_URL)
        self.language_page = CustomizedLanguagePage(self.driver)
        self.language_page.revert_account_messages_to_default()
        self.language_page.save_changes()

    def check_default_account_messages(self):
        messages = self.language_page.get_all_account_wide_messages()
        self.assertListEqual(default_messages, messages)

    @attr('functional_test')
    def test_default_messages(self):
        self.check_default_account_messages()

    @attr('functional_test')
    def test_language_change_has_no_effect_on_account_wide_section(self):
        self.language_page = CustomizedLanguagePage(self.driver)
        self.language_page.select_language("French", wait_for_load=True)
        self.check_default_account_messages()

    @attr('functional_test')
    def test_should_show_warning_message_when_account_message_edited(self):
        changed_messages = [message + "new message" for message in default_messages]

        self.change_account_messages()
        self.driver.find(by_css("#global_subjects_link")).click()
        self.verify_warning_dialog_present()
        self.driver.find_visible_element(by_css(".cancel_button")).click()
        self.assertListEqual(changed_messages ,  self.language_page.get_all_account_wide_messages())

        self.driver.find(by_css("#global_subjects_link")).click()
        self.verify_warning_dialog_present()
        self.driver.find_visible_element(by_css(".no_button")).click()

        self.driver.find(by_css("#global_languages_link")).click()
        self.language_page = CustomizedLanguagePage(self.driver)
        self.check_default_account_messages()

        self.change_account_messages()
        self.driver.find(by_css("#global_subjects_link")).click()
        self.verify_warning_dialog_present()
        self.driver.find_visible_element(by_css(".yes_button")).click()

        self.driver.wait_until_element_is_not_present(UI_TEST_TIMEOUT, by_css(".blockPage"))
        self.driver.find(by_css("#global_languages_link")).click()
        self.language_page = CustomizedLanguagePage(self.driver)
        self.assertListEqual(changed_messages,  self.language_page.get_all_account_wide_messages())

    @attr('functional_test')
    def test_warning_and_error_conditions(self):
        self.change_account_messages()
        self.assertEquals(4,self.driver.find_visible_elements_(by_css(".account_message_warning_message")).__len__())
        self.assertListEqual([u'Any changes you make to this text will apply for all Data Senders.']*4, [e.text for e in self.driver.find_visible_elements_(by_css(".account_message_warning_message"))])
        self.language_page.clear_custom_message(DATA_SENDER_NOT_REGISTERED_LOCATOR)
        self.assertListEqual(['Enter reply SMS text.'], [e.text for e in self.driver.find_elements_(by_css(".validationText"))])
        # self.language_page.set_custom_message_for(DATA_SENDER_NOT_REGISTERED_LOCATOR, "a"*160)
        # self.language_page.set_custom_message_for(DATA_SENDER_NOT_REGISTERED_LOCATOR, "a")
        # self.assertEquals("a" * 160, self.language_page.get_all_account_wide_messages()[0])

    @attr('functional_test')
    def test_modify_automatic_messages(self):
        changed_messages = [message + "new message" for message in default_messages]

        self.change_account_messages()
        self.language_page.save_changes()
        self.language_page.refresh()
        self.assertListEqual(changed_messages,  self.language_page.get_all_account_wide_messages())

    @attr('functional_test')
    def test_should_use_modified_account_wide_sms_messages_to_send_reply(self):

        new_custom_messages = [u'Error. You are not registered as a Data Sender. Please contact your supervisor.new message',
                        u'Error. Questionnaire Code {Submitted Questionnaire Code} is incorrect. Find the Code on the top of the printed Questionnaire and resend SMS starting with this Code.new message',
                        u'Thank you {Name of Data Sender}.We registered your {Identification Number Type} {Name of Identification Number} {Submitted Identification Number}.new message',
                        u'Error. {Submitted Identification Number} already exists. Register your {Identification Number Type} with a different Identification Number.new message']
        self.change_account_messages()
        self.language_page.save_changes()

        self.driver.go_to(DATA_WINNER_SMS_TESTER_PAGE)
        sms_tester_page = SMSTesterPage(self.driver)

        incorrect_ds_number_data =  {"from": "4444444", "to": '919880734937', "sms": "qcode sender_name 45 cid001" }
        sms_tester_page.send_sms_with(incorrect_ds_number_data)
        message = sms_tester_page.get_response_message()
        self.assertEquals(new_custom_messages[0],message)

        incorrect_qcode_data =  {"from": "1234123413", "to": '919880734937', "sms": "wrcode sender_name 45 cid001" }
        sms_tester_page.send_sms_with(incorrect_qcode_data)
        message = sms_tester_page.get_response_message()
        self.assertEquals('Error. Questionnaire Code wrcode is incorrect. Find the Code on the top of the printed Questionnaire and resend SMS starting with this Code.new message',message)

        success_subject_registration_data =  {"from": "1234123413", "to": '919880734937', "sms": "peo fname lname location 4,4 898989898" }
        sms_tester_page.send_sms_with(success_subject_registration_data)
        success_message = sms_tester_page.get_response_message()
        registered_short_code = re.match('.*(peo\d+).*', success_message).groups()[0]
        self.assertEquals('Thank you Tester.We registered your people lname '+registered_short_code+ '.new message',success_message)

        error_subject_registration = {"from": "1234123413", "to": '919880734937', "sms": "peo fname lname location 4,4 898989898 "+ registered_short_code }
        sms_tester_page.send_sms_with(error_subject_registration)
        message = sms_tester_page.get_response_message()
        self.assertIn('new message',message)

        self.driver.go_to(CUSTOMIZE_MESSAGES_URL)
        self.language_page = CustomizedLanguagePage(self.driver)

    def clear_all_messages(self):
        [r.clear() for r in self.driver.find_elements_(ACCOUNT_WIDE_MESSAGE_TEXTBOXES_LOCATOR)]


    def change_account_messages(self,messages=None):
        for element in self.driver.find_elements_(ACCOUNT_WIDE_MESSAGE_TEXTBOXES_LOCATOR):
            self.language_page.update_custom_message("new message",element)

    def verify_warning_dialog_present(self):
        self.driver.find_visible_element(by_css(".ui-dialog-titlebar"))

