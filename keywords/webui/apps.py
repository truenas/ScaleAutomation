from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
import xpaths


class Apps:
    @classmethod
    def assert_start_app(cls, name: str) -> bool:
        """
        This method returns True if given app is started otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is started otherwise it returns False.
        """
        child = f'//*[text()="{COM.convert_to_tag_format(name)}"]'
        parent = 'ix-app-row'
        if COM.assert_page_header('Installed') is False:
            NAV.navigate_to_apps()
        status = cls.get_app_status(name)
        match status:
            case 'Running':
                COM.set_checkbox(COM.convert_to_tag_format(name))
                COM.click_button('bulk-actions-menu')
                COM.click_button('stop-selected')
                assert cls.is_app_stopped(name)
            case 'Stopped':
                pass
            case _:
                WebUI.wait_until_not_visible(xpaths.common_xpaths.any_child_parent_target(
                    child,
                    parent,
                    f'*[contains(text(),{status})]'), shared_config['LONG_WAIT'])
        if cls.get_app_status(name) != 'Running':
            COM.set_checkbox(COM.convert_to_tag_format(name))
            # wait for actions menu to refresh available actions
            WebUI.delay(0.2)
            assert cls.is_app_stopped(name)
            COM.click_button('bulk-actions-menu')
            WebUI.save_screenshot(COM.convert_to_tag_format(name)+'_bulk_actions_menu')
            if WebUI.xpath(xpaths.common_xpaths.button_field('start-selected')).get_attribute('disabled'):
                # COM.click_button('bulk-actions-menu')
                WebUI.refresh()
                WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('bulk-actions-menu'), shared_config['MEDIUM_WAIT'])
                COM.click_button('bulk-actions-menu')
            COM.click_button('start-selected')
            WebUI.wait_until_not_visible(xpaths.common_xpaths.any_child_parent_target(
                child,
                parent,
                f'*[contains(text(),"Starting")]'), shared_config['LONG_WAIT'])
            assert cls.is_app_deployed(name)
            assert cls.is_app_running(name)
            WebUI.refresh()
        return cls.is_app_running(name)

    @classmethod
    def assert_stop_app(cls, name: str) -> bool:
        """
        This method returns rue if given app is stopped otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is stopped otherwise it returns False.
        """
        if COM.assert_page_header('Installed') is False:
            NAV.navigate_to_apps()
        child = f'//*[text()="{COM.convert_to_tag_format(name)}"]'
        parent = 'ix-app-row'
        status = cls.get_app_status(name)
        match status:
            case 'Stopped':
                COM.set_checkbox(COM.convert_to_tag_format(name))
                COM.click_button('bulk-actions-menu')
                COM.click_button('start-selected')
                assert cls.is_app_running(name)
            case 'Running':
                pass
            case _:
                WebUI.wait_until_not_visible(xpaths.common_xpaths.any_child_parent_target(
                    child,
                    parent,
                    f'*[contains(text(),{status})]'), shared_config['LONG_WAIT'])
        if cls.get_app_status(name) != 'Stopped':
            COM.set_checkbox(COM.convert_to_tag_format(name))
            COM.click_button('bulk-actions-menu')
            COM.click_button('stop-selected')
            assert WebUI.wait_until_visible(xpaths.common_xpaths.any_child_parent_target(
                f'//*[text()="{COM.convert_to_tag_format(name)}"]',
                'ix-app-row',
                '*[contains(text(),"Stopped")]'), shared_config['LONG_WAIT'])
        return cls.get_app_status(name) == 'Stopped'

    @classmethod
    def click_app(cls, name: str) -> None:
        """
        This method clicks the given app

        :param name: is the name of the app
        """
        COM.click_on_element(f'//ix-app-card//h3[contains(text(),"{name}")]')
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
        This method clicks the given named app install button.

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
        WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Please wait', 1), shared_config['LONG_WAIT'])

    @classmethod
    def delete_app(cls, name: str) -> None:
        """
        This method deletes the given named app.

        :param name: is the name of the app
        """
        if COM.assert_page_header('Installed') is False:
            NAV.navigate_to_apps()
        COM.set_checkbox(COM.convert_to_tag_format(name))
        COM.click_button('bulk-actions-menu')
        COM.click_button('delete-selected')
        COM.assert_confirm_dialog()
        WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Deleting...', 1), shared_config['WAIT'])
        assert not cls.is_app_installed(name)

    @classmethod
    def get_app_status(cls, name: str) -> str:
        return WebUI.xpath(xpaths.common_xpaths.any_child_parent_target(
            f'//*[text()="{COM.convert_to_tag_format(name)}"]',
            'ix-app-row',
            'ix-app-status-cell')).text

    @classmethod
    def is_app_deployed(cls, name: str) -> bool:
        """
        This method returns True if the given app is already installed otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is installed otherwise it returns False.
        """
        # Delay to wait for Apps section populate
        name = COM.convert_to_tag_format(name)
        WebUI.wait_until_not_visible(xpaths.common_xpaths.any_child_parent_target(
            f'//*[text()="{name}"]',
            'ix-app-row',
            '*[contains(text(),"Deploying")]'), shared_config['EXTRA_LONG_WAIT'])
        return WebUI.get_text(f'//*[text()="{name}"]/ancestor::ix-app-row/descendant::ix-app-status-cell') != 'Deploying'

    @classmethod
    def is_app_installed(cls, name: str) -> bool:
        """
        This method returns True if the given app is already installed otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is installed otherwise it returns False.
        """
        # Delay to wait for Apps section populate
        WebUI.delay(2)
        if COM.is_visible(xpaths.common_xpaths.button_field("check-available-apps")):
            return False
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f'//ix-app-row//div[contains(text(),"{COM.convert_to_tag_format(name)}")]'), shared_config['MEDIUM_WAIT'])

    @classmethod
    def is_app_running(cls, name: str) -> bool:
        """
        This method returns True if the given app is already installed otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is installed otherwise it returns False.
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_child_parent_target(
            f'//*[text()="{COM.convert_to_tag_format(name)}"]',
            'ix-app-row',
            '*[contains(text(),"Running")]'), shared_config['LONG_WAIT'])

    @classmethod
    def is_app_stopped(cls, name: str) -> bool:
        """
        This method returns True if the given app is already installed otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is installed otherwise it returns False.
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_child_parent_target(
            f'//*[text()="{COM.convert_to_tag_format(name)}"]',
            'ix-app-row',
            '*[contains(text(),"Stopped")]'), shared_config['LONG_WAIT'])

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
        name = COM.convert_to_tag_format(name)
        DATASET.create_dataset_by_api('tank/' + name)
        COM.click_button('add-item-shares')
        COM.set_input_field('name', name)
        COM.set_input_field('host-path', '/mnt/tank/' + name, True)

    @classmethod
    def set_wg_easy_fields(cls) -> None:
        print(f'App WG-Easy no configuration needed for install.')
