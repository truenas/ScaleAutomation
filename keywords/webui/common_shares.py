import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from helper.api import Response


class Common_Shares:
    @classmethod
    def assert_share_card_displays(cls, sharetype: str) -> bool:
        """
        This method returns True if the share card is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the share card is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//ix-{sharetype}-card'))

    @classmethod
    def assert_share_card_row_ui_delete_button(cls, sharetype: str, name: str) -> bool:
        """
        This method returns True if the Delete button on the specified share card's share row is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Delete button on the specified share card's share row is visible otherwise it returns False.
        """
        return cls.assert_share_card_row_ui_button(sharetype, name, 'delete')

    @classmethod
    def assert_share_card_row_ui_edit_button(cls, sharetype: str, name: str) -> bool:
        """
        This method returns True if the Edit button on the specified share card's share row is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Edit button on the specified share card's share row is visible otherwise it returns False.
        """
        return cls.assert_share_card_row_ui_button(sharetype, name, 'edit')

    @classmethod
    def assert_share_card_row_ui_enabled_button(cls, sharetype: str, name: str) -> bool:
        """
        This method returns True if the Enabled button on the specified share card's share row is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Enabled button on the specified share card's share row is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.share_enabled_slider(sharetype, name))

    @classmethod
    def assert_share_card_row_ui_button(cls, sharetype: str, name: str, button: str) -> bool:
        """
        This method returns True if the specified button on the specified share card's share row is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :param button: The button type to verify
        :return: True if the specified button on the specified share card's share row is visible otherwise it returns False.
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{sharetype}-share-{name.lower()}-{button}-row-action'
        path = path.replace('--', '-')
        return COM.is_visible(xpaths.common_xpaths.button_field(path))

    @classmethod
    def assert_share_card_ui_add_button(cls, sharetype: str) -> bool:
        """
        This method returns True if the Add button on the specified share card is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the Add button on the specified share card is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.button_field(f'{sharetype}-share-add'))

    @classmethod
    def assert_share_card_ui_actions_menu_button(cls, sharetype: str) -> bool:
        """
        This method returns True if the Actions Menu button on the specified share card is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the Actions Menu button on the specified share card is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.button_share_page_share_actions_menu(sharetype))

    @classmethod
    def assert_share_card_ui_view_all_button(cls, sharetype: str) -> bool:
        """
        This method returns True if the View All button on the specified share card is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the View All button on the specified share card is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.link_field(f'{sharetype}-share-view-all'))

    @classmethod
    def assert_share_description(cls, sharetype: str, desc: str) -> bool:
        """
        This method sets the description for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param desc: description of the given share
        :return: True if the share description is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'description', desc))

    @classmethod
    def assert_share_name(cls, sharetype: str, name: str) -> bool:
        """
        This method sets the name for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'name', name))

    @classmethod
    def assert_share_path(cls, sharetype: str, path: str) -> bool:
        """
        This method asserts the path for the share row of the given share.

        :param sharetype: type of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'path', path))

    @classmethod
    def assert_share_view_all_page_ui_add_button(cls, sharetype: str) -> bool:
        """
        This method returns True if the Add button on the View All page for the sharetype is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the Add button on the View All page for the sharetype is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.button_field(f'add-{sharetype}-share'))

    @classmethod
    def assert_share_view_all_page_ui_delete_button(cls, sharetype: str, name: str) -> bool:
        """
        This method returns True if the Delete button on the View All page for the sharetype is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Delete button on the View All page for the sharetype is visible otherwise it returns False.
        """
        return cls.assert_share_view_all_page_ui_button(sharetype, name, 'edit')

    @classmethod
    def assert_share_view_all_page_ui_edit_button(cls, sharetype: str, name: str) -> bool:
        """
        This method returns True if the Edit button on the View All page for the sharetype is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Edit button on the View All page for the sharetype is visible otherwise it returns False.
        """
        return cls.assert_share_view_all_page_ui_button(sharetype, name, 'edit')

    @classmethod
    def assert_share_view_all_page_ui_enabled_button(cls, sharetype: str, name: str) -> bool:
        """
        This method returns True if the Enabled button on the View All page for the sharetype is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Enabled button on the View All page for the sharetype is visible otherwise it returns False.
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        loc = xpaths.common_xpaths.any_xpath(f'//*[@data-test="toggle-enabled-{sharetype}-share-{name}-row-toggle"]')
        loc = loc.replace('--', '-')
        return COM.is_visible(loc)

    @classmethod
    def assert_share_view_all_page_ui_button(cls, sharetype: str, name: str, button: str) -> bool:
        """
        This method returns True if the specified button on the View All page for the sharetype is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :param button: The button type to verify
        :return: True if the specified button on the View All page for the sharetype is visible otherwise it returns False.
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        loc = xpaths.common_xpaths.button_field(f'{sharetype}-share-{name}-{button}-row-action')
        loc = loc.replace('--', '-')
        return COM.is_visible(loc)

    @classmethod
    def assert_view_all_page_share_path(cls, sharetype: str, path: str) -> bool:
        """
        This method sets the path for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        if sharetype == 'nfs':
            path = path.replace('/', '-')
        loc = xpaths.common_xpaths.any_xpath(f'//*[@data-test="text-path-{sharetype}-share-{path}-row-text"]')
        loc = loc.replace('--', '-')
        return COM.is_visible(loc)

    @classmethod
    def click_add_share_button(cls, sharetype: str):
        """
        This method clicks the add share button on the Shares page for the specified sharetype

        :param sharetype: type of the given share
        """
        WebUI.xpath(xpaths.common_xpaths.button_field(f'{sharetype}-share-add')).click()
        assert COM.is_visible(xpaths.common_xpaths.any_header(f'Add {sharetype.upper()}', 3))

    @classmethod
    def click_advanced_options(cls) -> None:
        """
        This method clicks the advanced options button.
        """
        assert COM.is_visible(xpaths.common_xpaths.button_field('toggle-advanced-options'))
        COM.click_button('toggle-advanced-options')

    @classmethod
    def click_delete_share(cls, sharetype: str, name: str) -> None:
        """
        This method clicks the delete share button of the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{sharetype}-share-{name.lower()}-delete-row-action'
        path = path.replace('--', '-')
        WebUI.xpath(xpaths.common_xpaths.button_field(path)).click()

    @classmethod
    def click_edit_share(cls, sharetype: str, name: str) -> None:
        """
        This method clicks the edit share button of the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{sharetype}-share-{name.lower()}-edit-row-action'
        WebUI.xpath(xpaths.common_xpaths.button_field(path)).click()
        WebUI.wait_until_visible(xpaths.common_xpaths.any_header(f'Edit {sharetype.upper()}', 3))

    @classmethod
    def create_share_by_api(cls, sharetype: str, name: str, path: str) -> Response:
        """
        This method creates the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return API_POST.create_share(sharetype, name, "/mnt/"+path)

    @classmethod
    def delete_all_shares_by_sharetype(cls, sharetype: str):
        """
        This method deletes the all shares by the given sharetype.

        :param sharetype: type of the given share
        """
        loc = f'//*[contains(@data-test,"-delete-row-action") and starts-with(@data-test,"button-card-{sharetype}")]'
        while COM.is_visible(loc):
            COM.click_on_element(loc)
            COM.assert_confirm_dialog()

    @classmethod
    def delete_share_by_api(cls, sharetype: str, name: str) -> Response:
        """
        This method deletes the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share name is visible otherwise it returns False.
        """
        return API_DELETE.delete_share(sharetype, name)

    @classmethod
    def handle_share_service_dialog(cls, sharetype: str):
        """
        This method handles the service dialog to start or restart a share service when a share is created or edited

        :param sharetype: type of the given share
        """
        name = ''
        if sharetype == 'smb':
            WebUI.wait_until_visible(xpaths.common_xpaths.any_text('SMB Service'))
        if sharetype == 'nfs':
            WebUI.wait_until_visible(xpaths.common_xpaths.any_text(f'{sharetype.upper()} share created'))
        if COM.is_visible(xpaths.common_xpaths.button_field('enable-service')):
            name = 'enable-service'
        if COM.is_visible(xpaths.common_xpaths.button_field('restart-service')):
            name = 'restart-service'
        if name != '':
            WebUI.xpath(xpaths.common_xpaths.button_field(name)).click()
        WebUI.delay(2)

    @classmethod
    def is_share_enabled(cls, sharetype: str, name: str) -> bool:
        """
        This method return True if the xpath element is clickable before timeout otherwise it returns False.

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share is enabled otherwise it returns False.
        """
        return bool(WebUI.xpath(xpaths.common_xpaths.share_enabled_slider(sharetype, name)).get_property('ariaChecked'))

    @classmethod
    def assert_share_service_in_expected_state(cls, xpath: str, expected_text: str, expected_state: bool) -> bool:
        """
        This method returns True if the service status button on the shares page displays and if the api service response
        matches the state param, otherwise it returns False.

        :param xpath: is the service xpath.
        :param expected_text: is the text displayed by the service status icon on the sharing page.
        :param expected_state: the expected state to assert against for the api call response.
        :return: True if the service matches the state param, otherwise it returns False.

        Example:
            - cls.assert_share_service_in_expected_state(xpath, 'RUNNING', True)
        """
        state = False
        icon_text = WebUI.xpath(xpaths.common_xpaths.button_field('service-status-'+xpath)).get_property('innerText')
        if (icon_text == expected_text) & (API_POST.is_service_running(xpath) is expected_state):
            state = True
        return state

    @classmethod
    def is_share_service_running(cls, xpath: str) -> bool:
        """
        This method return True if the service status button on the shares page displays RUNNING, otherwise it returns False.

        :param xpath: is the service xpath.
        :return: True if the service is running, otherwise it returns False.

        Example:
            - assert COMSHARE.is_share_service_running('cifs')
        """
        return cls.assert_share_service_in_expected_state(xpath, 'RUNNING', True)

    @classmethod
    def is_share_service_stopped(cls, xpath: str) -> bool:
        """
        This method return True if the service status button on the shares page displays STOPPED, otherwise it returns False.

        :param xpath: is the service xpath.
        :return: True if the service is STOPPED, otherwise it returns False.

        Example:
            - Common.is_share_service_STOPPED('cifs)
        """
        return cls.assert_share_service_in_expected_state(xpath, 'STOPPED', False)

    @classmethod
    def is_share_visible(cls, sharetype: str, name: str) -> bool:
        """
        This method return True if the given share is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share is visible otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.data_test_field(f'text-name-card-{sharetype}-share-{name.lower()}-row-text'))

    @classmethod
    def set_share_description(cls, desc: str) -> None:
        """
        This method sets the description for the share on the Edit Share right panel
        """
        COM.is_visible(xpaths.common_xpaths.input_field('comment'))
        COM.set_input_field('comment', desc)

    @classmethod
    def set_share_name(cls, name: str) -> None:
        """
        This method sets the name for the share on the Edit Share right panel
        """
        COM.is_visible(xpaths.common_xpaths.input_field('name'))
        COM.set_input_field('name', name)

    @classmethod
    def set_share_path(cls, path: str) -> None:
        """
        This method sets the path for the share on the Edit Share right panel
        """
        COM.is_visible(xpaths.common_xpaths.input_field('path'))
        COM.set_input_field('path', '/mnt/'+path)

    @classmethod
    def start_share_service_by_actions_menu(cls, service: str) -> bool:
        """
        This method starts the specified share service by the actions menu on the sharing page and returns True if the service
        successfully changed to STARTED, otherwise returns False.

        :param service: is the service name.
        :return: True if the service successfully changed to STARTED, otherwise returns False.
        """
        cls.toggle_share_service_state_by_actions_menu(service, 'on')
        return cls.is_share_service_running(service)

    @classmethod
    def stop_share_service_by_actions_menu(cls, service: str) -> bool:
        """
        This method stops the specified share service by the actions menu on the sharing page and returns True if the service
        successfully changed to STOPPED, otherwise returns False.

        :param service: is the service name.
        :return: True if the service successfully changed to STOPPED, otherwise returns False.
        """
        cls.toggle_share_service_state_by_actions_menu(service, 'off')
        return cls.is_share_service_stopped(service)

    @classmethod
    def toggle_share_service_state_by_actions_menu(cls, service: str, toggle: str):
        """
        This method toggles the specified share service by the actions menu on the sharing page and returns True if the service
        successfully changed to the expected state, otherwise returns False.

        :param service: is the service name.
        :param toggle: direction in which to toggle the service.
        """
        COM.click_on_element(xpaths.common_xpaths.button_share_page_share_actions_menu(service))
        if service == 'smb':
            service = 'cifs'
        COM.click_button(f'{service}-actions-menu-turn-{toggle}-service')
        text = 'STOPPED'
        if toggle == 'on':
            text = 'RUNNING'
        WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f"""//*[@data-test="button-service-status-{service}"]//*[contains(text(),"{text}")]"""))
