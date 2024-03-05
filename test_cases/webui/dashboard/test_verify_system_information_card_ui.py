import allure

from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-System-Info")
class Test_Verify_System_Information_Card_UI:

    @allure.tag("Read")
    @allure.story("Verify System Info UI")
    def verify_the_system_info_card_ui(self):
        """
        This test verifies System Info Card UI
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_system_information_card_visible() is True
        assert Dashboard.assert_system_information_ui() is True
