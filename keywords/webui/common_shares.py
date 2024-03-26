import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.api.post import API_POST


class Common_Shares:

    @classmethod
    def assert_disable_share_service_is_locked_and_not_clickable(cls, share_type: str) -> bool:
        COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu(share_type))
        share_type = 'iscsitarget' if share_type == 'iscsi' else share_type
        result = COM.assert_button_is_locked_and_not_clickable(f'{share_type}-actions-menu-turn-off-service')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_enable_share_service_is_locked_and_not_clickable(cls, share_type: str) -> bool:
        COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu(share_type))
        share_type = 'iscsitarget' if share_type == 'iscsi' else share_type
        result = COM.assert_button_is_locked_and_not_clickable(f'{share_type}-actions-menu-turn-on-service')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_iscsi_configure_button_is_locked_and_not_clickable(cls) -> bool:
        """
        This method returns True if the configure button is locked and not clickable otherwise it returns False.

        :return: True if the configure button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_configure_button_is_locked_and_not_clickable()
        """
        return COM.assert_button_is_locked_and_not_clickable('iscsi-share-configure')

    @classmethod
    def assert_iscsi_delete_button_is_locked_and_not_clickable(cls, target_name: str) -> bool:
        """
        This method returns True if the delete button is locked and not clickable otherwise it returns False.

        :param target_name: The name of the iSCSI target Example: target1 is target-1
        :return: True if the delete button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_iscsi_delete_button_is_locked_and_not_clickable('target-1')
        """
        return COM.assert_button_is_locked_and_not_clickable(f'card-iscsi-target-{target_name}-delete-row-action')

    @classmethod
    def assert_iscsi_target_is_visible(cls, target_name: str) -> bool:
        """
        This method returns True if the iSCSI target is visible otherwise it returns False.

        :param target_name: The name of the iSCSI target Example: target1 is target-1
        :return: True if the iSCSI target is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_iscsi_target_is_visible('target-1')
        """
        return WebUI.wait_until_visible(xpaths.sharing.iscsi_target_name(target_name))

    @classmethod
    def assert_iscsi_wizard_button_is_locked_and_not_clickable(cls):
        """
        This method returns True if the iSCSI wizard button is locked and not clickable otherwise it returns False.

        :return: True if the iSCSI wizard button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_iscsi_wizard_button_is_locked_and_not_clickable()
        """
        return COM.assert_button_is_locked_and_not_clickable('iscsi-share-wizard')

    @classmethod
    def assert_share_card_action_button_by_name(cls, sharetype: str, name: str, button: str) -> bool:
        """
        This method returns True if the specified button on the specified share card's share row is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :param button: The button type to verify
        :return: True if the specified button on the specified share card's share row is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_action_button_by_name('smb', 'share1', 'edit')
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{sharetype}-share-{name.lower()}-{button}-row-action'
        path = path.replace('--', '-')
        return COM.is_visible(xpaths.common_xpaths.button_field(path))

    @classmethod
    def assert_share_card_actions_menu_button(cls, sharetype: str) -> bool:
        """
        This method returns True if the Actions Menu button on the specified share card is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the Actions Menu button on the specified share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_actions_menu_button('smb')
        """
        return COM.is_visible(xpaths.common_xpaths.button_share_actions_menu(sharetype))

    @classmethod
    def assert_share_card_add_button(cls, sharetype: str) -> bool:
        """
        This method returns True if the Add button on the specified share card is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the Add button on the specified share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_add_button('smb')
        """
        return COM.is_visible(xpaths.common_xpaths.button_field(f'{sharetype}-share-add'))

    @classmethod
    def assert_share_card_displays(cls, share_type: str) -> bool:
        """
        This method returns True if the share card is visible otherwise it returns False.

        :param share_type: type of the given share
        :return: True if the share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_displays('smb')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f'//ix-{share_type}-card'))

    @classmethod
    def assert_share_card_enabled_button_by_name(cls, sharetype: str, name: str) -> bool:
        """
        This method returns True if the Enabled button on the specified share card's share row is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Enabled button on the specified share card's share row is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_enabled_button_by_name('smb', 'share1')
        """
        return COM.is_visible(xpaths.common_xpaths.share_enabled_slider(sharetype, name))

    @classmethod
    def assert_share_card_status(cls, sharetype: str) -> bool:
        """
        This method returns True if the Status button on the specified share card is visible otherwise it returns False.

        :param sharetype: type of the given share [smb/nfs/iscsi]
        :return: True if the Status button on the specified share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_status('smb')
        """
        share = 'nfs'
        match sharetype:
            case 'smb':
                share = 'cifs'
            case 'iscsi':
                share = 'iscsitarget'
        return COM.is_visible(xpaths.common_xpaths.button_field(f'service-status-{share}'))

    @classmethod
    def assert_share_card_table_header(cls, sharetype: str) -> bool:
        """
        This method returns True if the table header values on the specified share card are visible otherwise it returns False.

        :param sharetype: type of the given share [smb/nfs/iscsi]
        :return: True if the table header values on the specified share card are visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_table_header('smb')
        """
        xpath = f'//ix-{sharetype}-card//*[@data-test="row-header"]'
        match sharetype:
            case 'smb':
                assert COM.get_element_property(xpath, 'innerText').__contains__('Name') is True
                assert COM.get_element_property(xpath, 'innerText').__contains__('Path') is True
                assert COM.get_element_property(xpath, 'innerText').__contains__('Description') is True
                assert COM.get_element_property(xpath, 'innerText').__contains__('Enabled') is True
            case 'nfs':
                assert COM.get_element_property(xpath, 'innerText').__contains__('Path') is True
                assert COM.get_element_property(xpath, 'innerText').__contains__('Description') is True
                assert COM.get_element_property(xpath, 'innerText').__contains__('Enabled') is True
            case 'iscsi':
                assert COM.get_element_property(xpath, 'innerText').__contains__('Target Name') is True
                assert COM.get_element_property(xpath, 'innerText').__contains__('Target Alias') is True
            case _:
                return False
        return True

    @classmethod
    def assert_share_card_view_all_button(cls, sharetype: str) -> bool:
        """
        This method returns True if the View All button on the specified share card is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the View All button on the specified share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_view_all_button('smb')
        """
        return COM.is_visible(xpaths.common_xpaths.link_field(f'{sharetype}-share-view-all'))

    @classmethod
    def assert_share_description(cls, sharetype: str, desc: str) -> bool:
        """
        This method sets the description for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param desc: description of the given share
        :return: True if the share description is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_description('smb', 'share1')
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'description', desc))

    @classmethod
    def assert_share_name(cls, sharetype: str, name: str) -> bool:
        """
        This method sets the name for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share name is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_name('smb', 'share1')
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'name', name))

    @classmethod
    def assert_share_path(cls, sharetype: str, path: str) -> bool:
        """
        This method asserts the path for the share row of the given share.

        :param sharetype: type of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_path('smb', '/mnt/share1')
        """
        return COM.is_visible(xpaths.common_xpaths.share_attribute(sharetype, 'path', path))

    @classmethod
    def assert_share_view_all_page_add_button(cls, sharetype: str) -> bool:
        """
        This method returns True if the Add button on the View All page for the sharetype is visible otherwise it returns False.

        :param sharetype: type of the given share
        :return: True if the Add button on the View All page for the sharetype is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_view_all_page_add_button('smb')
        """
        return COM.is_visible(xpaths.common_xpaths.button_field(f'add-{sharetype}-share'))

    @classmethod
    def assert_share_view_all_page_button_by_name(cls, sharetype: str, name: str, button: str) -> bool:
        """
        This method returns True if the specified button on the View All page for the sharetype is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :param button: The button type to verify
        :return: True if the specified button on the View All page for the sharetype is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_view_all_page_button_by_name('smb', 'share1', 'edit')
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        loc = xpaths.common_xpaths.button_field(f'{sharetype}-share-{name}-{button}-row-action')
        loc = loc.replace('--', '-')
        return COM.is_visible(loc)

    @classmethod
    def assert_share_view_all_page_enabled_button(cls, sharetype: str, name: str) -> bool:
        """
        This method returns True if the Enabled button on the View All page for the sharetype is visible otherwise it returns False.

        :param sharetype: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Enabled button on the View All page for the sharetype is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_view_all_page_enabled_button('smb', 'share1')
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        loc = xpaths.common_xpaths.any_xpath(f'//*[@data-test="toggle-enabled-{sharetype}-share-{name}-row-toggle"]')
        loc = loc.replace('--', '-')
        return COM.is_visible(loc)

    @classmethod
    def assert_view_all_page_share_path(cls, sharetype: str, path: str) -> bool:
        """
        This method sets the path for the share on the Edit Share right panel

        :param sharetype: type of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_view_all_page_share_path('smb', '/mnt/share1')
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

        Example:
           - Common_Shares.click_add_share_button('smb')
        """
        COM.click_button(f'{sharetype}-share-add')
        assert COM.is_visible(xpaths.common_xpaths.any_header(f'Add {sharetype.upper()}', 3)) is True

    @classmethod
    def click_advanced_options(cls) -> None:
        """
        This method clicks the advanced options button.

        Example:
           - Common_Shares.click_advanced_options()
        """
        COM.click_button('toggle-advanced-options')

    @classmethod
    def click_delete_share(cls, sharetype: str, name: str) -> None:
        """
        This method clicks the delete share button of the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share

        Example:
           - Common_Shares.click_delete_share('smb', 'share1')
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{sharetype}-share-{name.lower()}-delete-row-action'
        path = path.replace('--', '-')
        COM.click_button(path)

    @classmethod
    def click_edit_iscsi_target(cls, target_name: str) -> None:
        """
        This method clicks the edit button of the iSCSI target

        :param target_name: The name of the iSCSI target. Example: target1 is target-1

        Example:
           - Common_Shares.click_edit_iscsi_target('target-1')
        """
        COM.click_button(f'card-iscsi-target-{target_name}-edit-row-action')

    @classmethod
    def click_edit_share(cls, sharetype: str, name: str) -> None:
        """
        This method clicks the edit share button of the given share by the share type.

        :param sharetype: type of the given share
        :param name: name of the given share

        Example:
           - Common_Shares.click_edit_share('smb', 'share1')
        """
        if sharetype == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{sharetype}-share-{name.lower()}-edit-row-action'
        path = path.replace('--', '-')
        COM.click_button(path)
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_header(f'Edit {sharetype.upper()}', 3)) is True

    @classmethod
    def delete_all_shares_by_sharetype(cls, sharetype: str):
        """
        This method deletes the all shares by the given sharetype.

        :param sharetype: type of the given share

        Example:
           - Common_Shares.delete_all_shares_by_sharetype('smb')
        """
        NAV.navigate_to_shares()
        loc = f'//*[contains(@data-test,"-delete-row-action") and starts-with(@data-test,"button-card-{sharetype}")]'
        while COM.is_visible(loc):
            COM.click_on_element(loc)
            COM.assert_confirm_dialog()

    @classmethod
    def handle_share_service_dialog(cls, sharetype: str):
        """
        This method handles the service dialog to start or restart a share service when a share is created or edited

        :param sharetype: type of the given share

        Example:
           - Common_Shares.handle_share_service_dialog('smb')
        """
        name = ''
        if sharetype == 'smb':
            assert WebUI.wait_until_visible(xpaths.common_xpaths.any_text('SMB Service')) is True
        if COM.is_visible(xpaths.common_xpaths.button_field('enable-service')):
            name = 'enable-service'
        if COM.is_visible(xpaths.common_xpaths.button_field('restart-service')):
            name = 'restart-service'
        if name != '':
            COM.click_button(name)
        # WebUI.delay(2)
        assert COM.assert_progress_bar_not_visible() is True

    @classmethod
    def is_share_enabled(cls, sharetype: str, name: str) -> bool:
        """
        This method return True if the xpath element is clickable before timeout otherwise it returns False.

        :param sharetype: type of the given share
        :param name: name of the given share
        :return: True if the share is enabled otherwise it returns False.

        Example:
           - Common_Shares.is_share_enabled('smb', 'share1')
        """
        val = COM.get_element_property(xpaths.common_xpaths.share_enabled_slider(sharetype, name), 'ariaChecked')
        val = val.capitalize()
        return eval(val)

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
        icon_text = COM.get_element_property(xpaths.common_xpaths.button_field('service-status-'+xpath), 'innerText')
        if (icon_text == expected_text) & (API_POST.is_service_running(xpath) is expected_state):
            state = True
        return state

    @classmethod
    def is_share_service_running(cls, xpath: str) -> bool:
        """
        This method Verifies that the service status button on the shares page displays RUNNING, and that the API is
        also status is RUNNING.

        :param xpath: is the service xpath.
        :return: True if the service is running, otherwise it returns False.

        Example:
            - assert COMSHARE.is_share_service_running('cifs')
        """
        return cls.assert_share_service_in_expected_state(xpath, 'RUNNING', True)

    @classmethod
    def is_share_service_stopped(cls, xpath: str) -> bool:
        """
        This method verifies that the service status button on the shares page displays STOPPED, and that the API is
        also status is STOPPED.

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

        Example:
           - Common_Shares.is_share_visible('smb', 'share1')
        """
        return COM.is_visible(xpaths.common_xpaths.data_test_field(f'text-name-card-{sharetype}-share-{name.lower()}-row-text'))

    @classmethod
    def set_share_description(cls, desc: str) -> None:
        """
        This method sets the description for the share on the Edit Share right panel

        :param desc: The description of the given share

        Example:
           - Common_Shares.set_share_description('share1')
        """
        COM.is_visible(xpaths.common_xpaths.input_field('comment'))
        COM.set_input_field('comment', desc)

    @classmethod
    def set_share_name(cls, name: str) -> None:
        """
        This method sets the name for the share on the Edit Share right panel

        :param name: The name of the given share

        Example:
           - Common_Shares.set_share_name('share1')
        """
        COM.is_visible(xpaths.common_xpaths.input_field('name'))
        COM.set_input_field('name', name)

    @classmethod
    def set_share_path(cls, path: str) -> None:
        """
        This method sets the path for the share on the Edit Share right panel

        :param path: The path of the given share

        Example:
           - Common_Shares.set_share_path('share1')
        """
        COM.is_visible(xpaths.common_xpaths.input_field('path'))
        COM.set_input_field('path', '/mnt/'+path, True)

    @classmethod
    def start_share_service_by_actions_menu(cls, service: str) -> bool:
        """
        This method starts the specified share service by the actions menu on the sharing page and returns True if the service
        successfully changed to STARTED, otherwise returns False.

        :param service: is the service name.
        :return: True if the service successfully changed to STARTED, otherwise returns False.

        Example:
            - Common_Shares.start_share_service_by_actions_menu('cifs')
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

        Example:
            - Common_Shares.stop_share_service_by_actions_menu('cifs')
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

        Example:
            - Common_Shares.toggle_share_service_state_by_actions_menu('cifs', 'on')
        """
        COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu(service))
        if service == 'smb':
            service = 'cifs'
        COM.click_button(f'{service}-actions-menu-turn-{toggle}-service')
        text = 'STOPPED'
        if toggle == 'on':
            text = 'RUNNING'
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f"""//*[@data-test="button-service-status-{service}"]//*[contains(text(),"{text}")]""")) is True
