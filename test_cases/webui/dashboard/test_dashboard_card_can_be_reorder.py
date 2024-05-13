import allure
import pytest

from helper.webui import WebUI
from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Move-Card")
class Test_Verify_A_Dashboard_Card_Can_Be_Reorder:

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        """
        This fixture resets the Dashboard cards back to original positions
        """
        yield
        # TODO set_original_card_position card list will need to be updated when all cards are reimplemented
        Dashboard.set_original_card_position('TrueNAS Help')
        Dashboard.set_original_card_position('Network')

    @allure.tag("Update")
    @allure.story("Move System Info to Help Position")
    def verify_the_truenas_help_card_move_to_truenas_network_position(self):
        """
        This test verifies moving Cards 'System Info' and 'Help' positions is saved
        - After saving the card positions
        - After going in another page and going back to the dashboard
        - After refreshing the page
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        # TODO: In the future, the position of the cards below might change. This will need to be fixed in the future.
        assert Dashboard.assert_card_position(1, 'TrueNAS Help') is True
        assert Dashboard.assert_card_position(2, 'Network') is True
        Dashboard.click_the_configure_button()
        Dashboard.move_card_a_to_card_b_position('TrueNAS Help', 'Network')
        assert Dashboard.assert_card_position(2, 'TrueNAS Help') is True
        Dashboard.click_the_save_reorder_button()

        # verify the system information card position after the reordering is saved
        assert Dashboard.assert_card_position(2, 'TrueNAS Help') is True

        # Verify the card position remains after going in another page and going back to the dashboard.
        Navigation.navigate_to_shares()
        Navigation.navigate_to_dashboard()
        assert Dashboard.assert_card_position(2, 'TrueNAS Help') is True

        # Verify the card position remains after refreshing the page.
        WebUI.refresh()
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_truenas_help_card_visible() is True
        assert Dashboard.assert_card_position(2, 'TrueNAS Help') is True
