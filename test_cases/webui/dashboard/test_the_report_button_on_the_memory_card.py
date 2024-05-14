import allure
import pytest

from keywords.webui.dashboard import Dashboard
from keywords.webui.reporting import Reporting


@allure.tag("Dashboard", "Reporting", "Memory")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Reporting")
@allure.issue("NAS-128992", "NAS-128992")
class Test_Verify_The_Report_Button_On_The_Memory_Card:

    @allure.tag("Read")
    @allure.story("Verify Memory Cards on Reporting")
    def verify_all_cards_on_the_memory_reporting_page(self):
        """
        This test verifies Memory Cards on Reporting page
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_memory_card_visible() is True
        Dashboard.click_the_memory_report_button()

        # verify all cards on the memory reporting page
        assert Reporting.assert_reporting_page_breadcrumb() is True
        assert Reporting.assert_memory_reporting_page_header() is True
        assert Reporting.is_physical_memory_utilization_card_visible() is True
        assert Reporting.is_swap_utilization_card_visible() is True
