from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation
from keywords.webui.reporting import Reporting


class Test_Verify_The_Report_Button_On_The_CPU_Card:

    @staticmethod
    def on_the_dashboard_click_on_the_cpu_report_button():
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_memory_card_visible() is True
        Dashboard.click_the_cpu_report_button()

    @staticmethod
    def verify_all_cpu_cards_on_cpu_reporting_page():
        assert Reporting.assert_reporting_page_breadcrumb() is True
        assert Reporting.assert_cpu_reporting_page_header() is True
        assert Reporting.is_cpu_usage_card_visible() is True
        assert Reporting.is_system_load_card_visible() is True
