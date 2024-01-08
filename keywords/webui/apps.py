from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
import xpaths


class Apps:
    @classmethod
    def click_app(cls, name: str) -> None:
        """
        This method clicks the given app

        :param name: is the name of the app
        """
        COM.click_on_element(f'//ix-app-card//*[contains(text(),"{name}")]')
        WebUI.wait_until_not_visible(xpaths.common_xpaths.any_text('Please wait'))

    @classmethod
    def click_discover_apps(cls) -> None:
        """
        This method clicks the discover apps button
        """
        COM.click_link('discover-apps')

    @classmethod
    def click_install_app(cls, name: str) -> None:
        """
        This method installs the given named app.

        :param name: is the name of the app
        """
        if COM.is_visible(xpaths.common_xpaths.button_field('setup-pool')):
            COM.click_button('setup-pool')
            COM.select_option('pool', 'pool-tank')
            COM.click_button('choose')
            WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Configuring...', 1), shared_config['LONG_WAIT'])
        if COM.is_visible(xpaths.common_xpaths.any_text('Install Another Instance')):
            cls.click_discover_apps()
            COM.set_search_field(name)
            cls.click_app(name)
        COM.click_button(COM.convert_to_tag_format(name) + '-install')
        if COM.is_dialog_visible('Information', 1):
            COM.assert_confirm_dialog()

    @classmethod
    def delete_app(cls, name: str) -> None:
        """
        This method deletes the given named app.

        :param name: is the name of the app
        """
        NAV.navigate_to_apps()
        COM.set_checkbox(COM.convert_to_tag_format(name))
        COM.click_button('bulk-actions-menu')
        COM.click_button('delete-selected')
        COM.assert_confirm_dialog()
        assert WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Deleting...', 1), shared_config['WAIT'])
        assert not cls.is_app_installed(name)

    @classmethod
    def is_app_installed(cls, name: str) -> bool:
        """
        This method returns True if the given app is already installed otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is installed otherwise it returns False.
        """
        # Delay to wait for Apps section populate
        WebUI.delay(2)
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//ix-app-row//div[contains(text(),"{COM.convert_to_tag_format(name)}")]'))

    @classmethod
    def set_app_values(cls, name: str) -> None:
        match name:
            case 'WG-Easy':
                cls.set_wg_easy_fields()
            case 'WebDAV':
                cls.set_webdav_fields(name)
            case _:
                print(f'App {name} not configured for install.')

    @classmethod
    def set_webdav_fields(cls, name: str) -> None:
        print(f'App {name} not configured for install.')
        name = COM.convert_to_tag_format(name)
        DATASET.create_dataset_by_api('tank/' + name)
        COM.click_button('add-item-shares')
        COM.set_input_field('name', name)
        COM.set_input_field('host-path', '/mnt/tank/' + name)

    @classmethod
    def set_wg_easy_fields(cls) -> None:
        print(f'App WG-Easy no configuration needed for install.')
