import allure
import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-System-Info-Uptime")
class Test_Verify_System_Information_Card_Uptime_Resets_on_Reboot:
    @pytest.fixture(scope='class')
    def uptime(self):
        return {}

    @allure.tag("Read")
    @allure.story("Verify System Info Uptime Resets on Reboot")
    @pytest.mark.parametrize('user_data', get_data_list('user'))
    def test_the_system_information_uptime(self, uptime, user_data):
        """
        This test verifies System Info Card uptime
        1. Get the System Info Card uptime
        2. Reboot and log back in
        3. Verify System Info Card new option does not match the old
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_system_information_card_visible() is True
        uptime['old'] = Dashboard.get_system_information_uptime()

        # reboot and log back in
        API_POST.reboot_system()
        Common.set_login_form(user_data['username'], user_data['password'])
        assert Dashboard.assert_dashboard_page_header_is_visible() is True

        # verify the new system the sysinfo uptime with the old
        uptime['new'] = Dashboard.get_system_information_uptime()
        assert uptime['old'] != uptime['new']
