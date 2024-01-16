import pytest
from keywords.webui.apps import Apps


class Test_Custom_App_UI:

    @staticmethod
    def verify_custom_app_ui() -> None:
        """
        This test verifies the ui for custom app
        """
        Apps.click_discover_apps()
        Apps.click_custom_app()
        assert Apps.assert_custom_app_ui() is True
