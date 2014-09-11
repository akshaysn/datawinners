# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.dataanalysispage.data_analysis_locator import *
import time
from pages.submissionlogpage.submission_log_page import SubmissionLogPage
from pages.websubmissionpage.web_submission_page import WebSubmissionPage


class DataAnalysisPage(SubmissionLogPage):
    def __init__(self, driver):
        super(DataAnalysisPage, self).__init__(driver)

    def get_all_data_on_nth_row(self, row):
        row_data = []
        time.sleep(2)
        column_count = self.get_number_of_columns(row)
        if column_count == 1:
            return self.get_empty_datatable_text()
        for col in range(1, column_count + 1):
            row_data.append(self.get_cell_value(row, col))
        return row_data

    def navigate_to_web_submission_tab(self):
        self.driver.find(by_css('.secondary_tab>li:nth-child(4) a')).click()
        return WebSubmissionPage(self.driver)

    def navigate_to_all_data_record_page(self):
        """
        Function to navigate all data record page

        Return data all data record
         """
        self.driver.find(ALL_DATA_RECORDS_LINK).click()
        self.driver.wait_for_element(20, by_css("table.submission_table"))
        return SubmissionLogPage(self.driver)