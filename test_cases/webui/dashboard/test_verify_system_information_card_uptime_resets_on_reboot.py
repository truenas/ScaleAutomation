import pytest
from helper.data_config import get_data_list
from helper.webui import WebUI
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard


class Test_Verify_System_Information_Card_Uptime_Resets_on_Reboot:
    @pytest.fixture(scope='class')
    def uptime(self):
        return {}

    @staticmethod
    def on_the_dashboard_get_the_system_information_uptime(uptime):
        assert Dashboard.assert_dashboard_page_header_is_visible()
        assert Dashboard.is_system_information_card_visible()
        uptime['old'] = Dashboard.get_system_information_uptime()

    @staticmethod
    @pytest.mark.parametrize('user_data', get_data_list('user'))
    def then_reboot_and_log_back_in(user_data):
        Common.reboot_system()
        Common.set_login_form(user_data['username'], user_data['password'])
        assert Dashboard.assert_dashboard_page_header_is_visible()

    @staticmethod
    def verify_the_new_system_the_sysinfo_uptime_with_the_old(uptime):
        uptime['new'] = Dashboard.get_system_information_uptime()
        assert uptime['old'] != uptime['new']
