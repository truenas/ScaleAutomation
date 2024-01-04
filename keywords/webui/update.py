from keywords.webui.common import Common


class Update:

    @classmethod
    def assert_update_page_header(cls):
        """
        This method returns True if the update page header is visible otherwise it returns False.

        :return: True if the update page header is visible otherwise it returns False.
        """
        return Common.assert_page_header('Update')

    @classmethod
    def is_check_for_updates_daily_text_present(cls):
        """
        This method returns True if the check for updates daily text is visible otherwise it returns False.

        :return: True if the check for updates daily text is visible otherwise it returns False.
        """
        return Common.assert_text_is_visible('Check for Updates Daily and Download if Available')