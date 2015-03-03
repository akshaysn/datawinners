# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from nose.plugins.attrib import attr

from framework.base_test import HeadlessRunnerTest
from pages.registrationpage.registration_page import RegistrationPage
from registration_data import *
from testdata.test_data import DATA_WINNER_REGISTER_PAGE, DATA_WINNER_REGISTRATION_COMPLETE_PAGE


def register_and_get_email(driver):
    driver.go_to(DATA_WINNER_REGISTER_PAGE)
    registration_page = RegistrationPage(driver)
    return registration_page.successful_registration_with(REGISTRATION_DATA_FOR_SUCCESSFUL_REGISTRATION)


class TestRegistrationPage(HeadlessRunnerTest):

    @attr('functional_test')
    def test_register_ngo_with_existing_email_address(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(EXISTING_EMAIL_ADDRESS)
        self.assertEquals(registration_page.get_error_message(), EXISTING_EMAIL_ADDRESS_ERROR_MESSAGE)
        a = self.driver.switch_to_active_element()
        self.assertEqual(a.get_attribute("value"), EXISTING_EMAIL_ADDRESS.get(ORGANIZATION_OFFICE_PHONE))

    @attr('functional_test')
    def test_register_ngo_with_unmatched_passwords(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(UNMATCHED_PASSWORD)
        self.assertEquals(registration_page.get_error_message(), UNMATCHED_PASSWORD_ERROR_MESSAGE)

    @attr('functional_test')
    def test_register_ngo_with_white_space_passwords(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(WHITE_SPACE_IN_SOME_FIELDS)
        self.assertEquals(registration_page.get_error_message(), WHITE_SPACES_ERROR_MESSAGE)


    @attr('functional_test')
    def test_register_ngo_without_entering_data(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(WITHOUT_ENTERING_REQUIRED_FIELDS)
        self.assertRegexpMatches(registration_page.get_error_message(), WITHOUT_ENTERING_REQUIRED_FIELDS_ERROR_MESSAGE)

    @attr('functional_test')
    def test_register_ngo_with_invalid_web_url(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(INVALID_WEBSITE_URL)
        self.assertEquals(registration_page.get_error_message(), INVALID_WEBSITE_URL_ERROR_MESSAGE)

    @attr('functional_test')
    def test_register_organization_sector_have_the_right_select_options(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        sectors_drop_down = self.driver.find_drop_down(ORGANIZATION_SECTOR_DROP_DOWN_LIST)
        self.assertIn('Please Select', sectors_drop_down.text)
        self.assertIn('Food Security', sectors_drop_down.text)
        self.assertIn('Other', sectors_drop_down.text)

    @attr('functional_test')
    def test_content_box_exist_in_registration_page(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        self.driver.wait_for_page_load()
        about_datawinners_box = self.driver.find_elements_(by_css("h5"))
        self.assertEqual('About DataWinners', about_datawinners_box[0].text)
        self.assertEqual('Subscription Details', about_datawinners_box[1].text)

    @attr('functional_test')
    def test_content_box_exist_in_registration_complete_page(self):
        self.driver.go_to(DATA_WINNER_REGISTRATION_COMPLETE_PAGE)
        self.driver.wait_for_page_load()
        about_datawinners_box = self.driver.find_elements_(by_css("h5"))
        self.assertEqual('About DataWinners', about_datawinners_box[0].text)
        self.assertEqual('Subscription Details', about_datawinners_box[1].text)

    @attr('functional_test')
    def test_price_page_link_in_content_box(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        price_link = self.driver.find(
            by_xpath("//div[@class='grid_7 right_hand_section alpha omega subscription_details']//a"))
        price_link.click()
        new_tab = self.driver.window_handles[1]
        self.driver.switch_to_window(new_tab)
        self.driver.wait_for_page_with_title(8, "Pricing")
        self.assertEqual("Pricing", self.driver.get_title())
        self.driver.switch_to_window(self.driver.window_handles[0])

    @attr('functional_test')
    def test_register_without_preferred_payment(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_confirmation_page, email = registration_page.successful_registration_with(
            WITHOUT_PREFERRED_PAYMENT)
        self.assertEquals(registration_confirmation_page.registration_success_message(), REGISTRATION_SUCCESS_MESSAGE)

    @attr('functional_test')
    def test_register_ngo_with_begin_end_spaced_password(self):
        self.driver.go_to(DATA_WINNER_REGISTER_PAGE)
        registration_page = RegistrationPage(self.driver)
        registration_page.register_with(BEGIN_END_SPACED_PASSWORD)
        self.assertEquals(BEGIN_END_SPACED_PASSWORD_ERROR_MESSAGE, registration_page.get_error_message())

