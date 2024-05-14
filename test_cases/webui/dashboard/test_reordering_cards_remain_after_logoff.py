import allure
import pytest
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Reorder")
class Test_Verify_Reordering_Cards_Remain_After_Logoff:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        """
        This fixture resets the Dashboard cards back to original positions.
        """
        Dashboard.set_original_card_position('TrueNAS Help')
        Dashboard.set_original_card_position('Network')
        Dashboard.set_original_card_position('Memory')
        Dashboard.set_original_card_position('CPU')
        WebUI.refresh()

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self):
        """
        This fixture resets the Dashboard cards back to original positions.
        """
        yield
        WebUI.delay(5)
        Dashboard.set_original_card_position('TrueNAS Help')
        Dashboard.set_original_card_position('Network')
        Dashboard.set_original_card_position('Memory')
        Dashboard.set_original_card_position('CPU')

    @allure.tag("Update")
    @allure.story("Verify Card Reorder Remains After Re-Login")
    def verify_move_the_truenas_help_card_to_cpu_card_position_and_save(self):
        """
        This test verifies moving the sysinfo card to cpu card position and save and verify the card positions
        is kept after re-login.
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_card_position(1, 'TrueNAS Help') is True
        assert Dashboard.assert_card_position(4, 'CPU') is True
        Dashboard.click_the_configure_button()
        Dashboard.move_card_a_to_card_b_position('TrueNAS Help', 'CPU')
        assert Dashboard.assert_card_position(4, 'TrueNAS Help') is True
        assert Dashboard.assert_card_position(3, 'CPU') is True
        Dashboard.click_the_save_reorder_button()

        # After saving verify the TrueNAS Help card to CPU card position
        assert Dashboard.assert_card_position(4, 'TrueNAS Help') is True
        assert Dashboard.assert_card_position(3, 'CPU') is True

        # logoff and login
        Common.logoff_truenas()
        Common.set_login_form(private_config['USERNAME'], private_config['PASSWORD'])
        assert Dashboard.assert_dashboard_page_header_is_visible() is True

        # verify the system the TrueNAS Help card to CPU card position
        assert Dashboard.assert_card_position(4, 'TrueNAS Help') is True
        assert Dashboard.assert_card_position(3, 'CPU') is True
