import allure
import pytest
from keywords.webui.dashboard import Dashboard
from keywords.webui.update import Update


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Update")
@pytest.mark.skip(reason="The System Information card is missing in the Dashboard UI")
# TODO: Add back System Information Card test when it is reimplemented in the UI
@allure.issue('NAS-128451', 'NAS-128451')
class Test_Verify_The_Check_For_Update_Button_On_The_Dashboard:

    @allure.tag("Read")
    @allure.story("Verify Update Daily Text")
    def test_the_check_for_update_button_works(self):
        """
        This test verifies update daily text displays
        """
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.is_system_information_card_visible() is True
        Dashboard.click_check_update_button()

        # verify update daily text is visible
        assert Update.assert_update_page_header() is True
        assert Update.is_check_for_updates_daily_text_present() is True
