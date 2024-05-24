import xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.api.post import API_POST
from keywords.webui.system_services import System_Services as SS


class Common_Shares:

    @classmethod
    def assert_card_add_share_button_is_restricted(cls, share_type: str):
        """
        This method verifies that the add share button is locked and not clickable.

        :param share_type: type of the given share
        :return: True if the add share button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_card_add_share_button_is_restricted('smb')
        """
        return COM.assert_button_is_restricted(f'{COM.convert_to_tag_format(share_type)}-share-add')

    @classmethod
    def assert_card_edit_filesystem_acl_permissions_button_is_restricted(cls, share_name: str) -> bool:
        """
        This method returns True if the edit filesystem ACL button is locked and not clickable
        otherwise it returns False.

        :param share_name: The name of the share. Example: share1 is share-1
        :return: True if the edit filesystem ACL button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_card_edit_filesystem_acl_permissions_button_is_restricted('share-1')
        """
        name = COM.convert_to_tag_format(share_name)
        return COM.assert_button_is_restricted(f'card-smb-share-{name}-security-row-action')

    @classmethod
    def assert_card_edit_share_acl_permissions_button_is_restricted(cls, share_name: str) -> bool:
        """
        This method returns True if the edit share ACL button is locked and not clickable otherwise it returns False.

        :param share_name: The name of the share. Example: share1 is share-1
        :return: True if the edit share ACL button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_card_edit_share_acl_permissions_button_is_restricted('share-1')
        """
        return COM.assert_button_is_restricted(f'card-smb-share-{share_name}-share-row-action')

    @classmethod
    def assert_card_iscsi_configure_button_is_restricted(cls) -> bool:
        """
        This method returns True if the configure button is locked and not clickable otherwise it returns False.

        :return: True if the configure button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_configure_button_is_restricted()
        """
        return COM.assert_button_is_restricted('iscsi-share-configure')

    @classmethod
    def assert_card_iscsi_delete_button_is_restricted(cls, target_name: str) -> bool:
        """
        This method returns True if the delete button is locked and not clickable otherwise it returns False.

        :param target_name: The name of the iSCSI target Example: target1 is target-1
        :return: True if the delete button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_iscsi_delete_button_is_restricted('target-1')
        """
        return COM.assert_button_is_restricted(f'card-iscsi-target-{target_name}-delete-row-action')

    @classmethod
    def assert_card_iscsi_wizard_button_is_restricted(cls):
        """
        This method returns True if the iSCSI wizard button is locked and not clickable otherwise it returns False.

        :return: True if the iSCSI wizard button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_iscsi_wizard_button_is_restricted()
        """
        return COM.assert_button_is_restricted('iscsi-share-wizard')

    @classmethod
    def assert_card_share_delete_button_is_restricted(cls, share_type: str, name: str) -> bool:
        """
         This method verifies that the delete button is locked and not clickable.

         :param share_type: type of the given share
         :param name: name of the given share
         :return: True if the delete button is locked and not clickable otherwise it returns False.

         Example:
            - Common_Shares.assert_share_delete_button_is_restricted('smb', 'share-1')
        """
        return COM.assert_button_is_restricted(f'card-{share_type}-share-{name.lower()}-delete-row-action')

    @classmethod
    def assert_card_share_enabled_toggle_is_enabled(cls, share_type: str, name: str) -> bool:
        """
        This method returns True if the Enabled toggle is enabled, otherwise it returns False.

        :param share_type: type of the given share [smb/nfs]
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Enabled toggle is locked and not clickable, otherwise it returns False.

        Example:
           - Common_Shares.assert_card_share_enabled_toggle_is_enabled('smb', 'share-1')
           - Common_Shares.assert_card_share_enabled_toggle_is_enabled('nfs', 'tank/nfsshare')
        """
        name = COM.convert_to_tag_format(name)
        share_type = COM.convert_to_tag_format(share_type)
        xpath = xpaths.sharing.share_enabled_toggle(share_type, name)
        return COM.get_element_property(xpath, 'ariaChecked') == 'true'

    @classmethod
    def assert_card_share_enabled_toggle_is_locked_and_disabled(cls, share_type: str, name: str) -> bool:
        """
        This method verifies that the Enabled toggle is locked and not clickable.

        :param share_type: type of the given share [smb/nfs]
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Enabled toggle is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_share_enabled_toggle_is_locked_and_disabled('smb', 'share-1')
           - Common_Shares.assert_share_enabled_toggle_is_locked_and_disabled('nfs', 'tank/nfsshare')
        """
        return COM.assert_toggle_is_restricted(f'enabled-card-{share_type}-share-{name}-row-toggle')

    @classmethod
    def assert_card_share_has_no_shares(cls, share_type: str) -> bool:
        """
        This method returns True if the given share has no shares, otherwise it returns False.

        :return: True if the given share has no shares, otherwise it returns False.

        Example:
            - Common_Share.assert_card_share_has_no_shares('smb')
            - Common_Share.assert_card_share_has_no_shares('nfs')
            - Common_Share.assert_card_share_has_no_shares('iscsi')
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(
            f'//ix-{share_type}-card//h3[contains(text(),"No records have been added yet")]'))

    @classmethod
    def assert_disable_share_service_is_restricted(cls, share_type: str) -> bool:
        """
        This method verifies that the disable share service button is locked and not clickable.

        :param share_type: type of the given share
        :return: True if the disable share service button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_disable_share_service_is_restricted('smb')
        """
        COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu(share_type))
        share_type = SS.return_backend_service_name(share_type, False)
        result = COM.assert_button_is_restricted(f'{share_type}-actions-menu-turn-off-service')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_enable_share_service_is_restricted(cls, share_type: str) -> bool:
        """
        This method verifies that the enable share service button is locked and not clickable.

        :param share_type: type of the given share
        :return: True if the enable share service button is locked and not clickable otherwise it returns False.

        Example:
           - Common_Shares.assert_enable_share_service_is_restricted('smb')
        """
        COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu(share_type))
        share_type = SS.return_backend_service_name(share_type, False)
        result = COM.assert_button_is_restricted(f'{share_type}-actions-menu-turn-on-service')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_iscsi_target_is_visible(cls, target_name: str) -> bool:
        """
        This method returns True if the iSCSI target is visible otherwise it returns False.

        :param target_name: The name of the iSCSI target Example: target1 is target-1
        :return: True if the iSCSI target is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_iscsi_target_is_visible('target-1')
        """
        return WebUI.wait_until_visible(xpaths.sharing.iscsi_card_target_name(target_name))

    @classmethod
    def assert_share_card_actions_menu_dropdown(cls, sharetype: str) -> bool:
        """
        This method returns True if the action menu values on the specified share card are visible otherwise it returns False.

        :param sharetype: type of the given share [smb/nfs/iscsi]
        :return: True if the action menu values on the specified share card are visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_actions_menu_dropdown('smb')
        """
        COM.click_on_element(f'//ix-{sharetype}-card//*[contains(@data-test,"actions-menu")]')
        sharetype = SS.return_backend_service_name(sharetype, False)
        xpath = f'//*[@data-test="button-{sharetype}-actions-menu-'
        if cls.is_share_service_running(sharetype):
            assert COM.is_visible(xpath+'turn-off-service"]') is True
        else:
            assert COM.is_visible(xpath+'turn-on-service"]') is True
        assert COM.is_visible(xpath+'config-service"]') is True
        if not sharetype.__eq__('iscsitarget'):
            assert COM.is_visible(xpath+'sessions"]') is True
        if sharetype.__eq__('cifs'):
            assert COM.is_visible(xpath+'logs"]') is True
        return True

    @classmethod
    def assert_share_card_action_button_by_name(cls, share_type: str, name: str, button: str) -> bool:
        """
        This method returns True if the specified button on the specified share card's share row is visible
         otherwise it returns False.

        :param share_type: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :param button: The button type to verify
        :return: True if the specified button on the specified share card's share row is visible
         otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_action_button_by_name('smb', 'share1', 'edit')
        """
        if share_type == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{share_type}-share-{name.lower()}-{button}-row-action'
        path = path.replace('--', '-')
        return COM.is_visible(xpaths.common_xpaths.button_field(path))

    @classmethod
    def assert_share_card_actions_menu_button(cls, share_type: str) -> bool:
        """
        This method returns True if the Actions Menu button on the specified share card is visible
        otherwise it returns False.

        :param share_type: type of the given share
        :return: True if the Actions Menu button on the specified share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_actions_menu_button('smb')
        """
        return COM.is_visible(xpaths.common_xpaths.button_share_actions_menu(share_type))

    @classmethod
    def assert_share_card_add_button(cls, share_type: str) -> bool:
        """
        This method returns True if the Add button on the specified share card is visible otherwise it returns False.

        :param share_type: type of the given share
        :return: True if the Add button on the specified share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_add_button('smb')
        """
        return COM.is_visible(xpaths.common_xpaths.button_field(f'{share_type}-share-add'))

    @classmethod
    def assert_share_card_displays(cls, share_type: str) -> bool:
        """
        This method returns True if the share card is visible otherwise it returns False.

        :param share_type: type of the given share [smb/nfs/iscsi]
        :return: True if the share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_displays('smb')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f'//ix-{share_type}-card'))

    @classmethod
    def assert_share_card_enabled_button_by_name(cls, share_type: str, name: str) -> bool:
        """
        This method returns True if the Enabled button on the specified share card's share row is visible
        otherwise it returns False.

        :param share_type: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Enabled button on the specified share card's share row is visible
         otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_enabled_button_by_name('smb', 'share1')
        """
        return COM.is_visible(xpaths.common_xpaths.share_enabled_slider(share_type, name))

    @classmethod
    def assert_share_card_status(cls, share_type: str) -> bool:
        """
        This method returns True if the Status button on the specified share card is visible otherwise it returns False.

        :param share_type: type of the given share [smb/nfs/iscsi]
        :return: True if the Status button on the specified share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_status('smb')
        """
        share_type = SS.return_backend_service_name(share_type, False)
        return COM.is_visible(xpaths.common_xpaths.button_field(f'service-status-{share_type}'))

    @classmethod
    def assert_share_card_table_header(cls, share_type: str) -> bool:
        """
        This method returns True if the table header values on the specified share card are visible
        otherwise it returns False.

        :param share_type: type of the given share [smb/nfs/iscsi]
        :return: True if the table header values on the specified share card are visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_table_header('smb')
        """
        xpath = f'//ix-{share_type}-card//*[@data-test="row-header"]'
        match share_type:
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
    def assert_share_card_view_all_button(cls, share_type: str) -> bool:
        """
        This method returns True if the View All button on the specified share card is visible
         otherwise it returns False.

        :param share_type: type of the given share
        :return: True if the View All button on the specified share card is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_card_view_all_button('smb')
        """
        return COM.is_visible(xpaths.common_xpaths.link_field(f'{share_type}-share-view-all'))

    @classmethod
    def assert_share_configuration_field_visible(cls, share_type: str, field: str) -> bool:
        """
        This method returns True if the given configuration field is visible for the given share type, otherwise it returns False.

        :param share_type: is the type of the share [smb/nfs/iscsi]
        :param field: is the name of the field
        :return: True if the given configuration field is visible, otherwise it returns False.

        Example:
            - Common_Shares.assert_share_configuration_field_visible('smb', 'name')
            - Common_Shares.assert_share_configuration_field_visible('nfs', 'path')
            - Common_Shares.assert_share_configuration_field_visible('iscsi', 'portal')
        """
        xpath = ""
        if share_type.lower() == 'smb':
            match field.lower():
                case "path":
                    xpath = xpaths.common_xpaths.input_field("path")
                case "name":
                    xpath = xpaths.common_xpaths.input_field("name")
                case "purpose":
                    xpath = xpaths.common_xpaths.select_field("purpose")
                case "description":
                    xpath = xpaths.common_xpaths.input_field("comment")
                case "enabled":
                    xpath = xpaths.common_xpaths.checkbox_field("enabled")
                case "save":
                    xpath = xpaths.common_xpaths.button_field("save")
                case "advanced options":
                    xpath = xpaths.common_xpaths.button_field("toggle-advanced-options")
        if share_type.lower() == 'nfs':
            match field:
                case "path":
                    xpath = xpaths.common_xpaths.input_field("path")
                case "description":
                    xpath = xpaths.common_xpaths.input_field("comment")
                case "enabled":
                    xpath = xpaths.common_xpaths.checkbox_field("enabled")
                case "add network":
                    xpath = xpaths.common_xpaths.button_field("add-item-networks")
                case "add hosts":
                    xpath = xpaths.common_xpaths.button_field("add-item-hosts")
                case "save":
                    xpath = xpaths.common_xpaths.button_field("save")
                case "advanced options":
                    xpath = xpaths.common_xpaths.button_field("toggle-advanced-options")
        if share_type.lower() == 'iscsi':
            match field:
                case "target name":
                    xpath = xpaths.common_xpaths.input_field("name")
                case "target alias":
                    xpath = xpaths.common_xpaths.input_field("alias")
                case "add networks":
                    xpath = xpaths.common_xpaths.button_field("add-item-authorized-networks")
                case "add groups":
                    xpath = xpaths.common_xpaths.button_field("add-item-add-groups")
                case "portal":
                    xpath = xpaths.common_xpaths.select_field("portal")
                case "initiator":
                    xpath = xpaths.common_xpaths.select_field("initiator")
                case "authentication method":
                    xpath = xpaths.common_xpaths.select_field("authmethod")
                case "authentication group":
                    xpath = xpaths.common_xpaths.select_field("auth")
                case "save":
                    xpath = xpaths.common_xpaths.button_field("save")
        if share_type.lower() == 'smart':
            match field.lower():
                case "all disks":
                    xpath = xpaths.common_xpaths.checkbox_field("all-disks")
                case "disks":
                    xpath = xpaths.common_xpaths.select_field("disks")
                case "type":
                    xpath = xpaths.common_xpaths.select_field("type")
                case "description":
                    xpath = xpaths.common_xpaths.input_field("desc")
                case "schedule":
                    xpath = xpaths.common_xpaths.select_field("schedule-presets")
                case "save":
                    xpath = xpaths.common_xpaths.button_field("save")

        return COM.is_visible(xpath)

    @classmethod
    def assert_share_description(cls, share_type: str, desc: str) -> bool:
        """
        This method sets the description for the share on the Edit Share right panel

        :param share_type: type of the given share
        :param desc: description of the given share
        :return: True if the share description is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_description('smb', 'share1')
        """
        return COM.is_visible(xpaths.common_xpaths.card_share_attribute(share_type, 'description', desc))

    @classmethod
    def assert_share_name(cls, share_type: str, name: str) -> bool:
        """
        This method sets the name for the share on the Edit Share right panel

        :param share_type: type of the given share
        :param name: name of the given share
        :return: True if the share name is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_name('smb', 'share1')
        """
        return COM.is_visible(xpaths.common_xpaths.card_share_attribute(share_type, 'name', name))

    @classmethod
    def assert_share_path(cls, share_type: str, path: str) -> bool:
        """
        This method asserts the path for the share row of the given share.

        :param share_type: type of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_path('smb', '/mnt/share1')
        """
        return COM.is_visible(xpaths.common_xpaths.card_share_attribute(share_type, 'path', path))

    @classmethod
    def assert_share_row_name(cls, share_type: str, name: str) -> bool:
        """
        This method returns True if the given share row name is visible, otherwise it returns False.

        :param share_type: type of the given share
        :param name: name or path of the given share
        :return: True if the given share row name is visible, otherwise it returns False.

        Example:
           - Common_Shares.assert_share_row_name('smb', 'share1')
           - Common_Shares.assert_share_row_name('nfs', '/mnt/tank/nfs-share')
           - Common_Shares.assert_share_row_name('iscsi', 'iscsi-share')
        """
        first_col = ''
        match(share_type.lower()):
            case 'smb':
                share_type = share_type + "-share"
                first_col = 'name'
            case 'nfs':
                share_type = share_type + "-share"
                first_col = 'path'
                if name.startswith("/"):
                    name = name.replace('/', '', 1)
            case 'iscsi':
                share_type = share_type + "-target"
                first_col = 'target-name'
        xpath = xpaths.sharing.share_row_name(first_col, share_type, COM.convert_to_tag_format(name))
        return COM.is_visible(xpath)

    @classmethod
    def assert_share_service_in_expected_state(cls, xpath: str, expected_text: str, expected_state: bool) -> bool:
        """
        This method returns True if the service status button on the shares page displays and if the api service
         response matches the state param, otherwise it returns False.

        :param xpath: is the service xpath.
        :param expected_text: is the text displayed by the service status icon on the sharing page.
        :param expected_state: the expected state to assert against for the api call response.
        :return: True if the service matches the state param, otherwise it returns False.

        Example:
            - cls.assert_share_service_in_expected_state(xpath, 'RUNNING', True)
        """
        state = False
        xpath = SS.return_backend_service_name(xpath, False)
        icon_text = COM.get_element_property(xpaths.common_xpaths.button_field('service-status-'+xpath), 'innerText')
        if (icon_text == expected_text) & (API_POST.is_service_running(xpath) is expected_state):
            state = True
        return state

    @classmethod
    def assert_share_view_all_page_add_button(cls, share_type: str) -> bool:
        """
        This method returns True if the Add button on the View All page for the share_type is visible
         otherwise it returns False.

        :param share_type: type of the given share
        :return: True if the Add button on the View All page for the share_type is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_view_all_page_add_button('smb')
        """
        return COM.is_visible(xpaths.common_xpaths.button_field(f'add-{share_type}-share'))

    @classmethod
    def assert_share_view_all_page_button_by_name(cls, share_type: str, name: str, button: str) -> bool:
        """
        This method returns True if the specified button on the View All page for the share_type is visible
        otherwise it returns False.

        :param share_type: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :param button: The button type to verify
        :return: True if the specified button on the View All page for the share_type is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_share_view_all_page_button_by_name('smb', 'share1', 'edit')
        """
        if share_type == 'nfs':
            name = name.replace('/', '-')
        loc = xpaths.common_xpaths.button_field(f'{share_type}-share-{name}-{button}-row-action')
        loc = loc.replace('--', '-')
        return COM.is_visible(loc)

    @classmethod
    def assert_share_view_all_page_enabled_button(cls, share_type: str, name: str) -> bool:
        """
        This method returns True if the Enabled button on the View All page for the share_type is visible
        otherwise it returns False.

        :param share_type: type of the given share
        :param name: The name(SMB)/path(NFS) of the share
        :return: True if the Enabled button on the View All page for the share_type is visible
        otherwise it returns False.

        Example:
           - Common_Shares.assert_share_view_all_page_enabled_button('smb', 'share1')
        """
        if share_type == 'nfs':
            name = name.replace('/', '-')
        loc = xpaths.common_xpaths.any_xpath(f'//*[@data-test="toggle-enabled-{share_type}-share-{name}-row-toggle"]')
        loc = loc.replace('--', '-')
        return COM.is_visible(loc)

    @classmethod
    def assert_view_all_page_share_path(cls, share_type: str, path: str) -> bool:
        """
        This method sets the path for the share on the Edit Share right panel

        :param share_type: type of the given share
        :param path: path of the given share
        :return: True if the share name is visible otherwise it returns False.

        Example:
           - Common_Shares.assert_view_all_page_share_path('smb', '/mnt/share1')
        """
        if share_type == 'nfs':
            path = path.replace('/', '-')
        loc = xpaths.common_xpaths.any_xpath(f'//*[@data-test="text-path-{share_type}-share-{path}-row-text"]')
        loc = loc.replace('--', '-')
        return COM.is_visible(loc)

    @classmethod
    def click_add_share_button(cls, share_type: str):
        """
        This method clicks the add share button on the Shares page for the specified share_type

        :param share_type: type of the given share

        Example:
           - Common_Shares.click_add_share_button('smb')
        """
        COM.click_button(f'{share_type}-share-add')
        assert COM.is_visible(xpaths.common_xpaths.any_header(f'Add {share_type.upper()}', 3)) is True

    @classmethod
    def click_advanced_options(cls) -> None:
        """
        This method clicks the advanced options button.

        Example:
           - Common_Shares.click_advanced_options()
        """
        COM.click_button('toggle-advanced-options')
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Basic Options')) is True

    @classmethod
    def click_basic_options(cls) -> None:
        """
        This method clicks the basic options button.

        Example:
           - Common_Shares.click_basic_options()
        """
        COM.click_button('toggle-advanced-options')
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Advanced Options')) is True

    @classmethod
    def click_delete_share(cls, share_type: str, name: str) -> None:
        """
        This method clicks the delete share button of the given share by the share type.

        :param share_type: type of the given share
        :param name: name of the given share

        Example:
           - Common_Shares.click_delete_share('smb', 'share1')
        """
        if share_type == 'nfs':
            name = name.replace('/', '-')
        path = f'card-{share_type}-share-{name.lower()}-delete-row-action'
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
        target_name = COM.convert_to_tag_format(target_name)
        COM.click_button(f'card-iscsi-target-{target_name}-edit-row-action')

    @classmethod
    def click_edit_share(cls, share_type: str, name: str) -> None:
        """
        This method clicks the edit share button of the given share by the share type.

        :param share_type: type of the given share
        :param name: name of the given share

        Example:
           - Common_Shares.click_edit_share('smb', 'share1')
        """
        path = f'card-{share_type}-share-{name.lower()}-edit-row-action'
        path = COM.convert_to_tag_format(path)
        COM.click_button(path)
        assert WebUI.wait_until_visible(xpaths.common_xpaths.close_right_panel()) is True
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_header(f'Edit {share_type.upper()}', 3)) is True

    @classmethod
    def click_share_card_header_link(cls, share_type: str) -> None:
        """
        This method clicks the share card header link of the given share type.

        :param share_type: type of the given share

        Example:
           - Common_Shares.click_share_card_header_link('smb')
        """
        COM.click_link(f'{share_type}-share-open-in-new')

    @classmethod
    def delete_all_shares_by_share_type(cls, share_type: str):
        """
        This method deletes the all shares by the given share_type.

        :param share_type: type of the given share [smb/nfs/iscsi]

        Example:
           - Common_Shares.delete_all_shares_by_share_type('smb')
        """
        NAV.navigate_to_shares()
        loc = f'//*[contains(@data-test,"-delete-row-action") and starts-with(@data-test,"button-card-{share_type}")]'
        while COM.is_visible(loc):
            COM.click_on_element(loc)
            COM.assert_confirm_dialog()

    @classmethod
    def handle_share_service_dialog(cls, share_type: str, timeout: int = shared_config['MEDIUM_WAIT']) -> None:
        """
        This method handles the service dialog to start or restart a share service when a share is created or edited

        :param share_type: type of the given share
        :param timeout: Optional, timeout in seconds, defaults to shared_config['WAIT']

        Example:
           - Common_Shares.handle_share_service_dialog('smb')
           - Common_Shares.handle_share_service_dialog('nfs', 5)
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_text(f'{share_type.upper()} Service'), timeout) is True
        if COM.is_visible(xpaths.common_xpaths.button_field('enable-service')):
            COM.click_button('enable-service')
            assert COM.assert_progress_bar_not_visible() is True
        elif COM.is_visible(xpaths.common_xpaths.button_field('restart-service')):
            COM.click_button('restart-service')
            assert COM.assert_progress_spinner_not_visible() is True
        assert WebUI.wait_until_not_visible(xpaths.common_xpaths.close_right_panel()) is True
        # WebUI.delay(2)

    @classmethod
    def is_share_enabled(cls, share_type: str, name: str) -> bool:
        """
        This method return True if the xpath element is clickable before timeout otherwise it returns False.

        :param share_type: type of the given share
        :param name: name of the given share
        :return: True if the share is enabled otherwise it returns False.

        Example:
           - Common_Shares.is_share_enabled('smb', 'share1')
        """
        val = COM.get_element_property(xpaths.common_xpaths.share_enabled_slider(share_type, name), 'ariaChecked')
        val = val.capitalize()
        return eval(val)

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
            - Common.is_share_service_STOPPED('smb')
        """
        return cls.assert_share_service_in_expected_state(xpath, 'STOPPED', False)

    @classmethod
    def is_share_visible(cls, share_type: str, name: str) -> bool:
        """
        This method return True if the given share is visible otherwise it returns False.

        :param share_type: type of the given share
        :param name: name of the given share
        :return: True if the share is visible otherwise it returns False.

        Example:
           - Common_Shares.is_share_visible('smb', 'share1')
        """
        return COM.is_visible(xpaths.common_xpaths.data_test_field(f'text-name-card-{share_type}-share-{name.lower()}-row-text'))

    @classmethod
    def set_share_configuration_field(cls, field: str, value: str = "") -> None:
        """
        This method sets the given configuration field to the given share type

        :param field: is the name of the given field
        :param value: is the value of the given field is to be set to

        Example:
            - Common_Share.set_share_configuration_field_visible('smb', 'name', 'smbshare')
            - Common_Share.set_share_configuration_field_visible('nfs', 'enabled', "true")
            - Common_Share.set_share_configuration_field_visible('iscsi', 'ip address', '0.0.0.0')
        """
        match field.lower():
            case "path" | "name" | "description" | "dataset" | "volsize":
                COM.set_input_field(field, value, True)
            case "purpose" | "disk" | "target" | "portal":
                COM.select_option(field, value)
            case "enabled":
                COM.set_checkbox_by_state(field, eval(value.capitalize()))

    @classmethod
    def set_share_dataset_path(cls, path: str) -> None:
        """
        This method sets the dataset path for the share on the Edit Share right panel

        :param path: The path of the given dataset

        Example:
           - Common_Shares.set_share_dataset_path('/mnt/tank/iscsi-share')
        """
        COM.is_visible(xpaths.common_xpaths.input_field('dataset'))
        COM.set_input_field('dataset', path)

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
    def set_share_enabled_toggle(cls, share_type: str, name: str) -> None:
        """
        This method sets the given share toggle.

        :param share_type: type of the given share [smb/nfs]
        :param name: The name(SMB)/path(NFS) of the share

        Example:
           - Common_Shares.set_share_enabled_toggle('smb', 'share-1')
           - Common_Shares.set_share_enabled_toggle('nfs', 'tank/nfsshare')
        """
        name = COM.convert_to_tag_format(f'enabled-card-{share_type}-share-{name}-row-toggle')
        COM.set_toggle_by_state(name, True)

    @classmethod
    def set_share_name(cls, name: str, tab: bool = False) -> None:
        """
        This method sets the name for the share on the Edit Share right panel

        :param name: The name of the given share
        :param tab: whether to tab out of the field or not

        Example:
           - Common_Shares.set_share_name('share1')
           - Common_Shares.set_share_name('share1', True)
        """
        COM.is_visible(xpaths.common_xpaths.input_field('name'))
        COM.set_input_field('name', name, tab)

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
    def set_share_volsize(cls, size: str) -> None:
        """
        This method sets the size for the share on the Edit Share right panel

        :param size: The size to set

        Example:
           - Common_Shares.set_share_volsize('10')
        """
        COM.is_visible(xpaths.common_xpaths.input_field('volsize'))
        COM.set_input_field('volsize', size)

    @classmethod
    def start_share_service_by_actions_menu(cls, service: str) -> bool:
        """
        This method starts the specified share service by the actions menu on the sharing page and returns True if the
        service successfully changed to STARTED, otherwise returns False.

        :param service: is the service name.
        :return: True if the service successfully changed to STARTED, otherwise returns False.

        Example:
            - Common_Shares.start_share_service_by_actions_menu('smb')
        """
        if cls.is_share_service_running(service) is False:
            cls.toggle_share_service_state_by_actions_menu(service, 'on')
        return cls.is_share_service_running(service)

    @classmethod
    def stop_share_service_by_actions_menu(cls, service: str) -> bool:
        """
        This method stops the specified share service by the actions menu on the sharing page and returns True if the
         service successfully changed to STOPPED, otherwise returns False.

        :param service: is the service name.
        :return: True if the service successfully changed to STOPPED, otherwise returns False.

        Example:
            - Common_Shares.stop_share_service_by_actions_menu('smb')
        """
        if cls.is_share_service_stopped(service) is False:
            cls.toggle_share_service_state_by_actions_menu(service, 'off')
        return cls.is_share_service_stopped(service)

    @classmethod
    def toggle_share_service_state_by_actions_menu(cls, service: str, toggle: str):
        """
        This method toggles the specified share service by the actions menu on the sharing page and returns True if the
        service successfully changed to the expected state, otherwise returns False.

        :param service: is the service name.
        :param toggle: direction in which to toggle the service.

        Example:
            - Common_Shares.toggle_share_service_state_by_actions_menu('smb', 'on')
        """
        COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu(service))
        service = SS.return_backend_service_name(service, False)
        # if service == 'smb':
        #     service = 'cifs'
        COM.click_button(f'{service}-actions-menu-turn-{toggle}-service')
        text = 'STOPPED'
        if toggle == 'on':
            text = 'RUNNING'
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f"""//*[@data-test="button-service-status-{service}"]//*[contains(text(),"{text}")]""")) is True

    @classmethod
    def unset_share_enabled_toggle(cls, share_type: str, name: str) -> None:
        """
        This method unsets the given share toggle.

        :param share_type: type of the given share [smb/nfs]
        :param name: The name(SMB)/path(NFS) of the share

        Example:
           - Common_Shares.unset_share_enabled_toggle('smb', 'share-1')
           - Common_Shares.unset_share_enabled_toggle('nfs', 'tank/nfsshare')
        """
        name = COM.convert_to_tag_format(f'enabled-card-{share_type}-share-{name}-row-toggle')
        COM.set_toggle_by_state(name, False)
