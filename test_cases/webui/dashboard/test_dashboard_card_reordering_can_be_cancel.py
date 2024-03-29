import allure
import pytest
from helper.webui import WebUI
from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Reorder")
class Test_Verify_A_Dashboard_Card_Reordering_Can_be_Cancel:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        """
        This fixture ensures that all Dashboard cards are at the original positions
        """
        Dashboard.set_original_card_position('sysinfo')
        Dashboard.set_original_card_position('help')
        Dashboard.set_original_card_position('cpu')
        # TODO: remove the following line when NAS-127796 is fixed
        WebUI.refresh()

    @allure.tag("Update")
    @allure.story("Move Card Help to CPU Position and Cancel")
    def verify_the_help_card_move_to_cpu_card_position_and_cancel(self):
        """
        This test verifies moving Cards 'System Info' and 'Help' then canceling doesn't change card positions
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_card_position(2, 'help') is True
        assert Dashboard.assert_card_position(3, 'cpu') is True
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('cpu', 'help')
        assert Dashboard.assert_card_position(3, 'help') is True
        assert Dashboard.assert_card_position(2, 'cpu') is True
        Dashboard.click_the_cancel_reorder_button()

        # verify the system the help card to cpu card position did not change after the cancellation
        assert Dashboard.assert_card_position(2, 'help') is True
        assert Dashboard.assert_card_position(3, 'cpu') is True
