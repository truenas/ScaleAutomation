import allure
import pytest
from time import sleep
from helper.global_config import shared_config
from keywords.webui.dashboard import Dashboard
from keywords.webui.reporting import Reporting


@allure.epic('Dashboard')
@allure.feature('Storage Card')
class Test_Verify_The_Report_Button_On_The_Storage_Card:
    @allure.story('The Report Button On The Storage Card Works')
    def test_verifying_the_report_button_on_the_storage_card_works(self):
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_storage_card_visible() is True
        Dashboard.click_the_storage_report_button()
        # Verify storage reporting page open
        assert Reporting.assert_reporting_page_breadcrumb() is True
        assert Reporting.assert_storage_reporting_page_header() is True
        assert Reporting.is_disk_i_o_card_visible('sd') is True
