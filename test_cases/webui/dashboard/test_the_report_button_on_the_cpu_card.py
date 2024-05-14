import allure
import pytest

from keywords.webui.dashboard import Dashboard
from keywords.webui.reporting import Reporting


@allure.tag("Dashboard", "Reporting", "CPU")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Reporting")
class Test_Verify_The_Report_Button_On_The_CPU_Card:

    @allure.tag("Read")
    @allure.story("Verify CPU Cards on Reporting")
    def verify_all_cpu_cards_on_cpu_reporting_page(self):
        """
        This test verifies CPU Cards on Reporting page
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_cpu_card_visible() is True
        Dashboard.click_the_cpu_report_button()

        # verify all cpu cards on cpu reporting page
        assert Reporting.assert_reporting_page_breadcrumb() is True
        assert Reporting.assert_cpu_reporting_page_header() is True
        assert Reporting.is_cpu_usage_card_visible() is True
        assert Reporting.is_system_load_card_visible() is True
