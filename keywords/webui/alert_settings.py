from helper.webui import WebUI
from keywords.webui.common import Common as COM


class Alert_Settings:

    @classmethod
    def assert_alert_category_save_button_restricted(cls, category: str) -> None:
        """
        This method returns True if the update page header is visible otherwise it returns False.

        :param category: name of the category.
        :return: True if the update page header is visible otherwise it returns False.
        """
        COM.click_button("categories")
        WebUI.delay(0.1)
        COM.click_button(f'category-{category}')
        assert COM.assert_button_is_restricted('save') is True
