import allure
import pytest

from helper.webui import WebUI
from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Reorder")
class Test_Verify_A_Dashboard_Card_Reordering_Can_be_Cancel:

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        yield
        # reset the change
        WebUI.refresh()
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('help', 'cpu')
        Dashboard.click_the_save_reorder_button()
        WebUI.refresh()

    @allure.tag("Update")
    @allure.story("Move System Info to Help Position")
    def on_the_dashboard_move_the_help_card_to_cpu_card_position_and_cancel(self):
        """
        This test verifies moving Cards 'System Info' and 'Help' then canceling doesn't change card positions
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_card_position(2, 'help') is True
        assert Dashboard.assert_card_position(3, 'cpu') is True
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('help', 'cpu')
        assert Dashboard.assert_card_position(3, 'help') is True
        assert Dashboard.assert_card_position(2, 'cpu') is True
        Dashboard.click_the_cancel_reorder_button()

        # verify the system the help card to cpu card position did not change after the cancellation
        assert Dashboard.assert_card_position(2, 'help') is True
        assert Dashboard.assert_card_position(3, 'cpu') is True
