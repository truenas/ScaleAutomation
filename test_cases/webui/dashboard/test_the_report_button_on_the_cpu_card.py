import allure

from keywords.webui.dashboard import Dashboard
from keywords.webui.reporting import Reporting


@allure.tag("Dashboard", "Reporting", "CPU")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Reporting")
@allure.issue("NAS-128992", "NAS-128992")
class Test_Verify_The_Report_Button_On_The_CPU_Card:

    @allure.tag("Read")
    @allure.story("Verify Report Button on CPU Card")
    def test_verifying_the_report_button_on_the_cpu_card_works(self):
        """
        This test verifies CPU Cards on Reporting page
        1. Click on CPU report button
        2. Verify CPU reporting page open
        3. Verify all CPU cards on CPU reporting page
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_cpu_card_visible() is True
        Dashboard.click_the_cpu_report_button()

        # verify all cpu cards on cpu reporting page
        assert Reporting.assert_reporting_page_breadcrumb() is True
        assert Reporting.assert_cpu_reporting_page_header() is True
        assert Reporting.is_cpu_usage_card_visible() is True
        assert Reporting.is_system_load_card_visible() is True
