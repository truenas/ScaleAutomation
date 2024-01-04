from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation
from keywords.webui.update import Update


class Test_Verify_The_Check_For_Update_Button_On_The_Dashboard:
    @classmethod
    def setup_class(cls):
        # Ensure we are on the dashboard.
        Navigation.navigate_to_dashboard()

    @staticmethod
    def on_the_dashboard_click_on_the_check_update_button():
        assert Dashboard.assert_dashboard_page_header_is_visible()
        assert Dashboard.is_system_information_card_visible()
        Dashboard.click_check_update_button()

    @staticmethod
    def verify_all_dashboard_cards_are_visible():
        assert Update.assert_update_page_header()
        assert Update.is_check_for_updates_daily_text_present()
