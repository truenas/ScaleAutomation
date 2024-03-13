import allure
import pytest

from keywords.webui.dashboard import Dashboard
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation


@allure.tag('Dashboard')
@allure.epic('Dashboard')
@allure.feature('Dashboard-Card-Help-Links')
class Test_Verify_Links_On_The_TrueNAS_Help_Card:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        Dashboard.set_all_cards_visible()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        """
        This method resets the test back to Dashboard
        """
        yield
        Common.clear_extra_windows()
        Navigation.navigate_to_dashboard()

    @allure.tag("Read")
    @allure.story('Verify Help Card Copyright')
    def verify_the_truenas_help_card_copyright(self):
        """
        This test verifies Help Card copyright text displays
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_truenas_help_card_visible() is True
        assert Common.assert_copyright_text_is_correct() is True

    @allure.tag("Read")
    @allure.story('Verify Help Card Links')
    def verify_all_links_on_the_truenas_help_card(self):
        """
        This test verifies Help Card links display and go where expected
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_the_truenas_help_documentation_link() is True
        assert Dashboard.assert_the_truenas_help_truenas_community_forums_link() is True
        assert Dashboard.assert_the_truenas_help_truenas_newsletter_link() is True
        assert Dashboard.assert_the_truenas_help_open_source_link() is True
        assert Dashboard.assert_the_truenas_help_ixsystems_inc_link() is True
