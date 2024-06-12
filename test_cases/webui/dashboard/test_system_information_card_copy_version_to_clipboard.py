import allure
from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-System-Info-Version")
class Test_Verify_System_Information_Card_Copy_Version_To_Clipboard:

    @allure.tag("Read")
    @allure.story("Verify System Info Card Version")
    def test_get_the_system_information_version(self):
        """
        This test verifies the System Info version is copied to clipboard
        1. Verify the System Info version is copied to clipboard
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_system_information_card_visible() is True
        assert Dashboard.assert_system_information_version_clipboard_copy() is True
