import allure
from keywords.webui.dashboard import Dashboard


@allure.tag('Dashboard')
@allure.epic('Dashboard')
@allure.feature('Dashboard-Card-Visible')
class Test_Verify_All_Dashboard_Cards_Are_Visible:

    @allure.tag("Update")
    @allure.story('Set All Cards Visible')
    def set_all_dashboard_cards_visible(self):
        """
        This test verifies all Cards are visible
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        Dashboard.set_all_cards_visible()

        # verify all dashboard cards are visible
        assert Dashboard.is_system_information_card_visible() is True
        assert Dashboard.is_truenas_help_card_visible() is True
        assert Dashboard.is_cpu_card_visible() is True
        assert Dashboard.is_memory_card_visible() is True
        assert Dashboard.is_storage_card_visible() is True
        assert Dashboard.is_network_card_visible() is True
