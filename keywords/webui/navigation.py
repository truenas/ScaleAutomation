import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM


class Navigation:
    @classmethod
    def navigate_to(cls, location: str, header: str) -> None:
        """
        This method navigates to the given location and verifies the given page header displays

        :param location: location to be navigating too
        :param header: header of the page being navigated too
        """
        WebUI.wait_until_clickable(xpaths.common_xpaths.link_field(location + '-menu'))
        WebUI.xpath(xpaths.common_xpaths.link_field(location + '-menu')).click()
        WebUI.wait_until_visible(xpaths.common_xpaths.any_header(header, 1))
        assert COM.is_visible(xpaths.common_xpaths.any_header(header, 1))
        WebUI.delay(2)

    @classmethod
    def navigate_to_apps(cls) -> None:
        """
        This method navigates to the Dashboard page
        """
        cls.navigate_to('apps', 'Installed')

    @classmethod
    def navigate_to_dashboard(cls) -> None:
        """
        This method navigates to the Dashboard page
        """
        cls.navigate_to('dashboard', 'Dashboard')

    @classmethod
    def navigate_to_datasets(cls) -> None:
        """
        This method navigates to the Shares page
        """
        cls.navigate_to('datasets', 'Datasets')

    @classmethod
    def navigate_to_shares(cls) -> None:
        """
        This method navigates to the Shares page
        """
        cls.navigate_to('shares', 'Sharing')
