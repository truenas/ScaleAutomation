import allure

from keywords.webui.apps import Apps


@allure.tag("Apps", "Custom App UI")
@allure.epic("Apps")
@allure.feature("Apps-Custom")
class Test_Custom_App_UI:

    @allure.tag("Read")
    @allure.story("Verify Custom App UI")
    def test_custom_app_ui(self):
        """
        This test verifies the ui for custom app
        """
        Apps.click_discover_apps()
        Apps.click_custom_app()
        assert Apps.assert_custom_app_ui() is True
