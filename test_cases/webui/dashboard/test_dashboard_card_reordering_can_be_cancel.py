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
        Dashboard.set_original_card_position('TrueNAS Help')
        Dashboard.set_original_card_position('Network')
        Dashboard.set_original_card_position('Memory')
        Dashboard.set_original_card_position('CPU')

        WebUI.refresh()

    @allure.tag("Update")
    @allure.story("Move Network card to CPU card Position and Cancel")
    def verify_the_network_card_move_to_cpu_card_position_and_cancel(self):
        """
        This test verifies moving Cards 'Network' and 'Network' then canceling doesn't change card positions
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        # TODO: the cards position below might need to be updated when all the card are implemented.
        assert Dashboard.assert_card_position(2, 'Network') is True
        assert Dashboard.assert_card_position(4, 'CPU') is True
        Dashboard.click_the_configure_button()
        Dashboard.move_card_a_to_card_b_position('CPU', 'Network')
        assert Dashboard.assert_card_position(3, 'Network') is True
        assert Dashboard.assert_card_position(2, 'CPU') is True
        Dashboard.click_the_cancel_reorder_button()

        # verify the system the help card to cpu card position did not change after the cancellation
        assert Dashboard.assert_card_position(2, 'Network') is True
        assert Dashboard.assert_card_position(4, 'CPU') is True
