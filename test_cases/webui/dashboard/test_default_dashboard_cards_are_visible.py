import allure
from helper.webui import WebUI
from keywords.webui.dashboard import Dashboard


@allure.tag('Dashboard')
@allure.epic('Dashboard')
@allure.feature('Dashboard-Card-Visible')
class Test_Verify_Default_Dashboard_Cards_Are_Visible:

    @allure.tag("Update")
    @allure.story('Verify All Dashboard Cards Are Visible')
    def test_all_default_dashboard_cards_are_visible(self):
        """
        This test verifies all default dashboard cards are visible
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True

        # verify the default dashboard cards are visible
        assert Dashboard.is_system_information_card_visible() is True
        assert Dashboard.is_truenas_help_card_visible() is True
        assert Dashboard.is_cpu_card_visible() is True
        assert Dashboard.is_memory_card_visible() is True
        assert Dashboard.is_storage_card_visible() is True
        assert Dashboard.is_network_card_visible() is True
        WebUI.take_percy_snapshot('Default Dashboard Cards Are Visible')
