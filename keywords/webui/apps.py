from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
import xpaths


class Apps:
    @classmethod
    def assert_custom_app_ui(cls) -> bool:
        """
        This method returns True if custom app UI is validated otherwise it returns False.

        :return: True if custom app UI is validated otherwise it returns False.

        Example:
            - Apps.assert_custom_app_ui()
        """
        status = True
        # Initially set testObj to right panel header
        test_obj = xpaths.common_xpaths.any_header('Install Custom App', 1)
        close_add_button = False
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath('//*[@class="search-card"]'), shared_config['WAIT'])
        for key in shared_config['CUSTOM_APP_UI']:
            text = shared_config['CUSTOM_APP_UI'].get(key)
            click_add_button = False
            close_checkbox = False

            if key in shared_config['CUSTOM_APP_UI_LEGEND_LIST']:
                test_obj = xpaths.common_xpaths.any_xpath(f'//legend[contains(text(),"{text}")]')
                WebUI.xpath(xpaths.common_xpaths.any_xpath(f'//*[@class="section ng-star-inserted" and contains(text(),"{text}")]')).click()
            if key in shared_config['CUSTOM_APP_UI_BUTTON_LIST']:
                test_obj = xpaths.common_xpaths.button_field(f'add-item-{text}')
                click_add_button = True
            if key in shared_config['CUSTOM_APP_UI_INPUT_LIST']:
                test_obj = xpaths.common_xpaths.input_field(text)
                if key in ["Run As Group", "Memory Limit", "Portal IP", "Port"]:
                    close_checkbox = True
            if key in shared_config['CUSTOM_APP_UI_SELECT_LIST']:
                test_obj = xpaths.common_xpaths.select_field(text)
            if key in shared_config['CUSTOM_APP_UI_CHECKBOX_LIST']:
                test_obj = xpaths.common_xpaths.checkbox_field(text)
                if key in ["Configure Container User", "Enable Resource Limits", "Enable WebUI Portal", "Use Node IP"]:
                    COM.click_on_element(test_obj)

            # Verify if Button expansion is needed
            if click_add_button is True:
                COM.click_on_element(test_obj)
                close_add_button = True

            # Verify if element exists
            if not COM.is_visible(test_obj):
                status = False

            # Verify if close Button collapse is needed
            if close_add_button and click_add_button is False:
                # If key is last field in Add expansion, click close_button to collapse Add expansion.
                if key in ["Command", "Arg", "Environment Variable Value", "IPAM Type", "Nameserver", "Search Entry", "Option Value", "Protocol", "Read Only", "Memory Backed Mount Path", "Dataset Name", "Add Capabilities"]:
                    COM.click_button('remove-from-list')
                    close_add_button = False

            # If key is last field in checkbox expansion, set test_obj to expansion checkbox object.
            match key:
                case "Run As Group":
                    test_obj = xpaths.common_xpaths.checkbox_field(shared_config['CUSTOM_APP_UI'].get('Configure Container User'))
                case "Memory Limit":
                    test_obj = xpaths.common_xpaths.checkbox_field(shared_config['CUSTOM_APP_UI'].get('Enable Resource Limits'))
                case "Portal IP":
                    test_obj = xpaths.common_xpaths.checkbox_field(shared_config['CUSTOM_APP_UI'].get('Use Node IP'))
                case "Port":
                    test_obj = xpaths.common_xpaths.checkbox_field(shared_config['CUSTOM_APP_UI'].get('Enable WebUI Portal'))
            if close_checkbox:
                COM.click_on_element(test_obj)

        return status

    @classmethod
    def assert_start_app(cls, name: str) -> bool:
        """
        This method returns True if given app is started otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is started otherwise it returns False.

        Example:
            - Apps.assert_start_app('WG Easy')
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
                WebUI.refresh()
                # WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('bulk-actions-menu'), shared_config['WAIT'])
                COM.click_button('bulk-actions-menu')
                WebUI.save_screenshot(COM.convert_to_tag_format(name)+'_bulk_actions_menu_2')
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

        Example:
            - Apps.assert_stop_app('WG Easy')
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

        Example:
            - Apps.click_app('WG Easy')
        """
        COM.click_on_element(f'//ix-app-card//h3[contains(text(),"{name}")]')
        WebUI.wait_until_not_visible(xpaths.common_xpaths.any_text('Please wait'))

    @classmethod
    def click_custom_app(cls) -> None:
        """
        This method clicks the custom apps button

        Example:
            - Apps.click_custom_app()
        """
        COM.click_link('custom-app')

    @classmethod
    def click_discover_apps(cls) -> None:
        """
        This method clicks the discover apps button

        Example:
            - Apps.click_discover_apps()
        """
        COM.click_link('discover-apps')

    @classmethod
    def click_install_app(cls, name: str) -> None:
        """
        This method clicks the given named app install button.

        :param name: is the name of the app

        Example:
            - Apps.click_install_app('WG Easy')
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
        if WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Information', 1), shared_config['SHORT_WAIT']) is False:
            COM.assert_confirm_dialog()
        # if COM.is_dialog_visible('Information', 1):
        WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Please wait', 1), shared_config['LONG_WAIT'])

    @classmethod
    def delete_app(cls, name: str) -> None:
        """
        This method deletes the given named app.

        :param name: is the name of the app

        Example:
            - Apps.delete_app('WG Easy')
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
    def edit_app(cls, name: str) -> None:
        """
        This method clicks the edit app button for the given named app.

        :param name: is the name of the app

        Example:
            - Apps.edit_app('WG Easy')
    """
        name = COM.convert_to_tag_format(name)
        COM.click_on_element(f'//ix-app-row//div[contains(text(),"{name}")]')
        COM.click_button(f'{name}-edit')
        assert COM.assert_page_header(f'Edit {name}')

    @classmethod
    def get_app_status(cls, name: str) -> str:
        """
        This method returns the status for the given app.

        :param name: is the name of the app
        :return: the status for the given app.

        Example:
            - Apps.get_app_status('WG Easy')
    """
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

        Example:
            - Apps.is_app_deployed('WG Easy')
        """
        # Delay to wait for Apps section populate
        name = COM.convert_to_tag_format(name)
        WebUI.wait_until_not_visible(xpaths.common_xpaths.any_child_parent_target(
            f'//*[text()="{name}"]',
            'ix-app-row',
            '*[contains(text(),"Deploying")]'), shared_config['EXTRA_LONG_WAIT'])
        return cls.get_app_status(name) != 'Deploying'

    @classmethod
    def is_app_installed(cls, name: str) -> bool:
        """
        This method returns True if the given app is already installed otherwise it returns False.

        :param name: is the name of the app
        :return: True if given app is installed otherwise it returns False.

        Example:
            - Apps.is_app_installed('WG Easy')
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

        Example:
            - Apps.is_app_running('WG Easy')
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

        Example:
            - Apps.is_app_stopped('WG Easy')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_child_parent_target(
            f'//*[text()="{COM.convert_to_tag_format(name)}"]',
            'ix-app-row',
            '*[contains(text(),"Stopped")]'), shared_config['LONG_WAIT'])

    @classmethod
    def navigate_to_app_section(cls, name: str) -> None:
        """
        This method clicks the app section located on the right panel

        :param name: is the name of the app section

        Example:
            - Apps.navigate_to_app_section('WG Easy')
        """
        WebUI.xpath(xpaths.common_xpaths.any_xpath(f'//*[@class="section ng-star-inserted" and contains(text(),"{name}")]')).click()

    @classmethod
    def set_app_values(cls, name: str) -> None:
        """
        This method sets the given app required fields to install

        :param name: is the name of the app section

        Example:
            - Apps.set_app_values('WG Easy')
        """
        match name:
            case 'WG-Easy':
                cls.set_wg_easy_fields()
            case 'WebDAV':
                cls.set_webdav_fields(name)
            case _:
                print(f'App {name} not configured for install.')

    @classmethod
    def set_webdav_fields(cls, name: str) -> None:
        """
        This method sets the WebDAV app required fields to install

        :param name: is the name of the app section

        Example:
            - Apps.set_webdav_fields('WebDAV')
        """
        name = COM.convert_to_tag_format(name)
        DATASET.create_dataset_by_api('tank/' + name)
        COM.click_button('add-item-shares')
        COM.set_input_field('name', name)
        COM.set_input_field('host-path', '/mnt/tank/' + name, True)

    @classmethod
    def set_wg_easy_fields(cls) -> None:
        """
        This method sets the WG Easy app required fields to install (none are required)

        Example:
            - Apps.set_wg_easy_fields()
        """
        print(f'App WG-Easy no configuration needed for install.')

    @classmethod
    def verify_app_installed(cls, name: str) -> bool:
        """
        This method verifies the given app is installed

        :param name: name of app to verify is installed

        Example:
            - Apps.verify_app_installed('WG Easy')
        """
        if Apps.is_app_installed(name) is False:
            Apps.click_discover_apps()
            COM.set_search_field(name)
            Apps.click_app(name)
            Apps.click_install_app(name)
            Apps.set_app_values(name)
            COM.click_save_button()
            assert COM.assert_page_header('Installed', shared_config['LONG_WAIT'])
        assert Apps.is_app_installed(name) is True
        return Apps.is_app_deployed(name) is True
