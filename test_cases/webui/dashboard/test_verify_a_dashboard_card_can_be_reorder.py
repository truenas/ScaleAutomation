import allure
import pytest

from keywords.webui.dashboard import Dashboard
from helper.webui import WebUI


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Move-Card")
class Test_Verify_A_Dashboard_Card_Can_Be_Reorder:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        # reset the change
        WebUI.refresh()
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', Dashboard.get_dashboard_card_name_by_position(1))
        Dashboard.move_card_a_to_card_b_position('help', Dashboard.get_dashboard_card_name_by_position(2))
        Dashboard.click_the_save_reorder_button()
        WebUI.refresh()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        yield
        # reset the change
        WebUI.refresh()
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', Dashboard.get_dashboard_card_name_by_position(1))
        Dashboard.move_card_a_to_card_b_position('help', Dashboard.get_dashboard_card_name_by_position(2))
        Dashboard.click_the_save_reorder_button()
        WebUI.refresh()

    @allure.tag("Update")
    @allure.story("Move System Info to Help Position")
    def verify_the_system_information_card_move_to_truenas_help_card_position(self):
        """
        This test verifies moving Cards 'System Info' and 'Help' positions
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_card_position(1, 'sysinfo') is True
        assert Dashboard.assert_card_position(2, 'help') is True
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', 'help')
        Dashboard.click_the_save_reorder_button()

        # verify the system information card position
        assert Dashboard.assert_card_position(2, 'sysinfo') is True
