import pytest
from time import sleep
from helper.global_config import shared_config
from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation
from keywords.webui.reporting import Reporting


class Test_Verify_The_Report_Button_On_The_Storage_Card:
    @classmethod
    def setup_class(cls):
        # Ensure we are on the dashboard.
        Navigation.navigate_to_dashboard()

    @staticmethod
    def on_the_dashboard_click_on_the_storage_report_button():
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_memory_card_visible() is True
        Dashboard.click_the_storage_report_button()

    @staticmethod
    def verify_storage_reporting_page_open():
        assert Reporting.assert_reporting_page_breadcrumb() is True
        assert Reporting.assert_storage_reporting_page_header() is True
        sleep(5)

    @staticmethod
    @pytest.mark.parametrize('disk', shared_config['DISK_LIST'])
    def verify_disk_exist_card(disk):
        assert Reporting.is_disk_i_o_card_visible(disk) is True
