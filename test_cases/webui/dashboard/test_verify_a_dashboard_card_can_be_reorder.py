import allure
import pytest

from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Move-Card")
class Test_Verify_A_Dashboard_Card_Can_Be_Reorder:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        # reset the change
        Dashboard.set_original_card_position('sysinfo')
        Dashboard.set_original_card_position('help')

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
        assert Dashboard.assert_card_position(2, 'sysinfo') is True
        Dashboard.click_the_save_reorder_button()

        # verify the system information card position
        assert Dashboard.assert_card_position(2, 'sysinfo') is True
