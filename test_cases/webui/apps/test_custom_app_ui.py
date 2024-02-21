import pytest

import xpaths.common_xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM


class Test_Custom_App_UI:

    @staticmethod
    def verify_custom_app_ui() -> None:
        """
        This test verifies the ui for custom app
        """
        Apps.click_discover_apps()
        Apps.click_custom_app()
        assert Apps.assert_custom_app_ui() is True
