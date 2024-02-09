from keywords.webui.dashboard import Dashboard


class Test_Verify_All_Dashboard_Cards_Are_Visible:
    @staticmethod
    def set_all_dashboard_cards_visible():
        assert Dashboard.assert_dashboard_page_header_is_visible()
        Dashboard.set_all_cards_visible()

    @staticmethod
    def verify_all_dashboard_cards_are_visible():
        assert Dashboard.is_system_information_card_visible()
        assert Dashboard.is_truenas_help_card_visible()
        assert Dashboard.is_cpu_card_visible()
        assert Dashboard.is_memory_card_visible()
        assert Dashboard.is_storage_card_visible()
        assert Dashboard.is_network_card_visible()