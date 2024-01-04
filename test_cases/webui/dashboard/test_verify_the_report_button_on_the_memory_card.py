from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation
from keywords.webui.reporting import Reporting


class Test_Verify_The_Report_Button_On_The_Memory_Card:
    @classmethod
    def setup_class(cls):
        # Ensure we are on the dashboard.
        Navigation.navigate_to_dashboard()

    @staticmethod
    def on_the_dashboard_click_on_the_memory_report_button():
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_memory_card_visible() is True
        Dashboard.click_the_memory_report_button()

    @staticmethod
    def verify_all_links_on_the_truenas_help_card():
        assert Reporting.assert_reporting_page_breadcrumb() is True
        assert Reporting.assert_memory_reporting_page_header() is True
        assert Reporting.is_physical_memory_utilization_card_visible() is True
        assert Reporting.is_swap_utilization_card_visible() is True
