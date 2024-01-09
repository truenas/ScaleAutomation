import pytest
from helper.data_config import get_data_list
from helper.webui import WebUI
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard


class Test_Verify_System_Information_Card_Copy_Version_To_Clipboard:
    @staticmethod
    def on_the_dashboard_get_the_system_information_uptime():
        assert Dashboard.assert_dashboard_page_header_is_visible()
        assert Dashboard.is_system_information_card_visible()
        assert Dashboard.assert_system_information_version_clipboard_copy()
