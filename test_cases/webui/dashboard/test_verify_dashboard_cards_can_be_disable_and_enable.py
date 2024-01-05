import pytest
from helper.global_config import shared_config
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('card', shared_config['DASHBOARD_CARDS'].keys())
class Test_Verify_Dashboard_Cards_Can_Be_Disable_And_Enable:
    @classmethod
    def setup_class(cls):
        # Ensure we are on the dashboard.
        Navigation.navigate_to_dashboard()
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        Dashboard.set_all_cards_visible()

    @staticmethod
    def disable_and_verify_the_card_is_not_on_dashboard(card):
        Dashboard.disable_card(shared_config['DASHBOARD_CARDS'][card])
        assert Common.is_card_not_visible(card) is True

    @staticmethod
    def enable_verify_the_card_is_back_on_dashboard(card):
        Dashboard.enable_card(shared_config['DASHBOARD_CARDS'][card])
        assert Common.is_card_visible(card) is True
