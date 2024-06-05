import allure
import pytest

from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-System-Info")
class Test_Verify_System_Information_Card_UI:

    @allure.tag("Read")
    @allure.story("Verify System Info UI")
    def test_the_system_info_card_overview(self):
        """
        This test verifies System Info Card UI
        1. Verify System Info Card Overview UI
        """
        assert Dashboard.is_system_information_card_visible() is True
        assert Dashboard.assert_system_information_overview() is True
