from keywords.webui.common import Common
from keywords.webui.navigation import Navigation


class Advanced:

    @classmethod
    def get_debug_files(cls):
        """
        This method gets the debug logs.

        Example:
            - Advanced.get_debug_logs()
        """
        Navigation.navigate_to_system_settings_advanced()
        assert Common.assert_page_header('Advanced') is True
        Common.click_button('save-debug')
        assert Common.is_dialog_visible('Generate Debug File', 1) is True
        Common.assert_confirm_dialog()
        assert Common.is_dialog_visible('Saving Debug', 1) is True
        assert Common.assert_progress_bar_not_visible() is True
