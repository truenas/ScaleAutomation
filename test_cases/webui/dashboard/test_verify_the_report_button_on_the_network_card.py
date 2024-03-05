import allure

from keywords.webui.dashboard import Dashboard
from keywords.webui.reporting import Reporting


@allure.tag("Dashboard", "Reporting", "Network")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Reporting")
class Test_Verify_The_Report_Button_On_The_Network_Card:

    @allure.tag("Read")
    @allure.story("Verify Network Cards on Reporting")
    def verify_all_network_cards_on_cpu_reporting_page(self):
        """
        This test verifies Network Cards on Reporting page
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_network_card_visible() is True
        Dashboard.click_the_network_report_button()

        # verify all network cards on cpu reporting page
        assert Reporting.assert_reporting_page_breadcrumb() is True
        assert Reporting.assert_network_reporting_page_header() is True
        assert Reporting.is_interface_traffic_card_visible() is True
