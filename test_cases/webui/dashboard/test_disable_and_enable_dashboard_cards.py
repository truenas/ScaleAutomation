import allure
import pytest
from helper.global_config import shared_config
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard


@allure.tag('Dashboard')
@allure.epic('Dashboard')
@allure.feature('Dashboard-Card-Enable/Disable')
@pytest.mark.skip('This test will need to be rework when Add implementation is completed.')
# TODO: Card are delete or added now and it works a different way them before. This test will need to redone or removed
class Test_Verify_Dashboard_Cards_Can_Be_Disable_And_Enable:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        assert Dashboard.assert_dashboard_page_header_is_visible() is True

    @allure.tag("Update")
    @allure.story('Disable Cards')
    @pytest.mark.parametrize('card', shared_config['DASHBOARD_CARDS_TOGGLE'].keys())
    def verify_disable_the_card_is_not_on_dashboard(self, card):
        """
        This test verifies disabling Card, card does not display
        """
        Dashboard.enable_card(shared_config['DASHBOARD_CARDS_TOGGLE'][card])
        Dashboard.disable_card(shared_config['DASHBOARD_CARDS_TOGGLE'][card])
        assert Common.is_card_not_visible(card) is True

    @allure.tag("Update")
    @allure.story('Enable Cards')
    @pytest.mark.parametrize('card', shared_config['DASHBOARD_CARDS_TOGGLE'].keys())
    def verify_enable_the_card_is_on_dashboard(self, card):
        """
        This test verifies enabling Card, card displays
        """
        Dashboard.disable_card(shared_config['DASHBOARD_CARDS_TOGGLE'][card])
        Dashboard.enable_card(shared_config['DASHBOARD_CARDS_TOGGLE'][card])
        assert Common.is_card_visible(card) is True
