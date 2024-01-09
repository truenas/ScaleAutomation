from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation
from keywords.webui.update import Update


class Test_Verify_System_Information_Card_UI:

    @staticmethod
    def on_the_dashboard_verify_the_card_ui():
        assert Dashboard.assert_dashboard_page_header_is_visible()
        assert Dashboard.is_system_information_card_visible()
        assert Dashboard.assert_system_information_ui()
