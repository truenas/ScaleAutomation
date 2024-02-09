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
        if COM.is_visible(xpaths.common_xpaths.any_text('Apps Service Not Configured')):
            COM.click_button('apps-settings')
            COM.click_button('choose-pool')
            COM.select_option('pool', 'pool-tank')
            COM.click_button('choose')
            WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Configuring...', 1), shared_config['LONG_WAIT'])
        Apps.click_discover_apps()
        Apps.click_custom_app()
        assert Apps.assert_custom_app_ui() is True
