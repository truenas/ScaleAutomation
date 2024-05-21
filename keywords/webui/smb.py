import xpaths
from helper.cli import SSH_Command_Line
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.ssh.smb import SSH_SMB as SSHSMB
from keywords.webui.common import Common as COM
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException


class SMB:
    @classmethod
    def assert_add_smb_share_button_is_restricted(cls):
        """
        This method returns True if add SMB share button is locked and not clickable, otherwise it returns False.

        :return: True if add SMB share button is locked and not clickable, otherwise it returns False.

        Example:
            - SMB.assert_add_smb_share_button_is_restricted()
        """
        return COM.assert_button_is_restricted('add-smb-share')

    @classmethod
    def assert_delete_share_button_is_restricted(cls, share_name: str) -> bool:
        """
        This method verifies that the delete button is locked and not clickable.

        :param share_name: The name of the share. Example: share1 is share-1
        :return: True if the delete button is locked and not clickable otherwise it returns False.

        Example:
           - SMB.assert_card_share_delete_button_is_restricted('share-1')
        """
        share_name = COM.convert_to_tag_format(share_name)
        result = COM.assert_button_is_restricted(f'smb-{share_name}-delete-row-action')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_edit_filesystem_acl_button_is_restricted(cls, share_name: str) -> bool:
        """
        This method verifies that the edit filesystem ACL button is locked and not clickable.

        :param share_name: The name of the share. Example: share1 is share-1
        :return: True if the edit filesystem ACL button is locked and not clickable otherwise it returns False.

        Example:
            - SMB.assert_edit_filesystem_acl_button_is_restricted('share-1')
        """
        share_name = COM.convert_to_tag_format(share_name)
        result = COM.assert_button_is_restricted(f'smb-{share_name}-security-row-action')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_edit_share_acl_button_is_restricted(cls, share_name: str) -> bool:
        """
        This method verifies that the edit share ACL button is locked and not clickable.

        :param share_name: The name of the share. Example: share1 is share-1
        :return: True if the edit share ACL button is locked and not clickable otherwise it returns False.

        Example:
            - SMB.assert_edit_share_acl_button_is_restricted('share-1')
        """
        share_name = COM.convert_to_tag_format(share_name)
        result = COM.assert_button_is_restricted(f'smb-{share_name}-share-row-action')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_enabled_toggle_is_restricted(cls, share_name: str) -> bool:
        """
        This method verifies that the enabled toggle is locked and not clickable.

        :param share_name: The name of the share. Example: share1 is share-1
        :return: True if the enabled toggle is locked and not clickable otherwise it returns False.

        Example:
            - SMB.assert_enabled_checkbox_is_restricted('share-1')
        """
        try:
            toggle = WebUI.xpath(xpaths.common_xpaths.toggle_field(f'enabled-smb-{share_name}-row-toggle'))
            toggle.click()
        except (ElementClickInterceptedException, TimeoutException):
            return True
        return False

    @classmethod
    def assert_edit_smb_panel_header(cls) -> bool:
        """
        This method asserts that the SMB edit panel header is displayed.

        :return: True if the SMB edit panel header is displayed, otherwise it returns False.

        Example:
            - SMB.assert_edit_smb_panel_header()
        """
        return COM.assert_right_panel_header('Edit SMB')

    @classmethod
    def assert_guest_access(cls, share: str, user: str = 'nonexistent', password: str = 'nopassword') -> bool:
        """
        This returns True if the share can be accessed by a guest user, otherwise it returns False.

        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user

        :return: True if the share ignore list contains the given name otherwise it returns False.

        Example:
            - SMB.assert_guest_access()
        """
        return cls.assert_user_can_access(share, user, password)

    @classmethod
    def assert_guest_delete_file(cls, file: str, share: str) -> bool:
        """
        This returns True if the given file is deleted, otherwise it returns False.

        :param file: is the name of the file to delete
        :param share: is the name of the share to access

        :return: True if the given file is deleted, otherwise it returns False.

        Example:
            - SMB.assert_guest_delete_file('myFile', 'myShare')
        """
        return SSHSMB.assert_user_can_delete_file(file, share, 'nonexistent', 'nopassword')

    @classmethod
    def assert_guest_put_file(cls, file: str, share: str) -> bool:
        """
        This returns True if the given file is put, otherwise it returns False.

        :param file: is the name of the file to put
        :param share: is the name of the share to access

        :return: True if the given file is put, otherwise it returns False.

        Example:
            - SMB.assert_guest_put_file('myFile', 'myShare')
        """
        return SSHSMB.assert_user_can_put_file(file, share, 'nonexistent', 'nopassword')

    @classmethod
    def assert_share_acl_configuration_field_visible(cls, field: str) -> bool:
        """
        This method verifies the given acl configuration field is visible for the smb share

        :param field: is the name of the field
        :return: True if the given acl configuration field is visible, otherwise it returns False.

        Example:
            - Common_Shares.assert_share_acl_configuration_field_visible('name')
        """
        xpath = ""
        match (field.lower()):
            case "add":
                xpath = xpaths.common_xpaths.button_field("add-item-add-entry")
            case "who":
                xpath = xpaths.common_xpaths.select_field("ae-who")
            case "permission":
                xpath = xpaths.common_xpaths.select_field("ae-perm")
            case "type":
                xpath = xpaths.common_xpaths.select_field("ae-type")
            case "save":
                xpath = xpaths.common_xpaths.button_field("save")

        return COM.is_visible(xpath)

    @classmethod
    def assert_share_description(cls, share_name: str, desc: str) -> bool:
        """
        This method verifies that the share description is visible on the Sharing SMB page.

        :param desc: is the description of the share
        :param share_name: is the name of the share
        :return: True if the share description is visible otherwise it returns False.

        Example:
            - SMB.assert_share_description('myDescription')
        """
        return COM.is_visible(xpaths.common_xpaths.page_share_attribute('smb', share_name, 'description', desc))

    @classmethod
    def assert_share_filesystem_acl_configuration_field_visible(cls, field: str) -> bool:
        """
        This method verifies the given filesystem acl configuration field is visible for the smb share

        :param field: is the name of the field
        :return: True if the given filesystem acl configuration field is visible, otherwise it returns False.

        Example:
            - Common_Shares.assert_share_filesystem_acl_configuration_field_visible('name')
        """
        xpath = ""
        match (field.lower()):
            case "owner":
                xpath = xpaths.common_xpaths.input_field("owner")
            case "owner group":
                xpath = xpaths.common_xpaths.input_field("owner-group")
            case "apply owner":
                xpath = xpaths.common_xpaths.checkbox_field("apply-owner")
            case "apply group":
                xpath = xpaths.common_xpaths.checkbox_field("apply-group")
            case "add item":
                xpath = xpaths.common_xpaths.button_field("add-acl-item")
            case "save acl":
                xpath = xpaths.common_xpaths.button_field("save-acl")
            case "strip acl":
                xpath = xpaths.common_xpaths.button_field("strip-acl")
            case "use preset":
                xpath = xpaths.common_xpaths.button_field("use-preset")
            case "save as preset":
                xpath = xpaths.common_xpaths.button_field("save-as-preset")
            case "access control entry":
                xpath = xpaths.common_xpaths.any_text("Access Control Entry")

        return COM.is_visible(xpath)

    @classmethod
    def assert_share_ignore_list(cls, name: str) -> bool:
        """
        This returns True if the share ignore list contains the given name otherwise it returns False.

        :param name: name to verify in the ignore list
        :return: True if the share ignore list contains the given name otherwise it returns False.

        Example:
            - SMB.assert_share_ignore_list('ignore-me')
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@formcontrolname="ignore_list"]//*[contains(text(),"{name}")]'))

    @classmethod
    def assert_share_name(cls, name: str) -> bool:
        """
        This method verifies that the share name is visible on the Sharing SMB page.

        :param name: is the name of the share
        :return: True if the share name is visible otherwise it returns False.

        Example:
            - SMB.assert_share_name('myShare')
        """
        return COM.is_visible(xpaths.common_xpaths.page_share_attribute('smb', name, 'name', name))

    @classmethod
    def assert_share_path(cls, share_name: str, path: str) -> bool:
        """
        This method verifies that the path for the share row of the given share on the Sharing SMB page.

        :param path: path of the given share
        :param share_name: name of the given share
        :return: True if the share name is visible otherwise it returns False.

        Example:
           - SMB.assert_share_path('/mnt/share1')
        """
        return COM.is_visible(xpaths.common_xpaths.page_share_attribute('smb', share_name, 'path', path))

    @classmethod
    def assert_share_watch_list(cls, name: str) -> bool:
        """
        This returns True if the share watch list contains the given name otherwise it returns False.

        :param name: name to verify in the watch list
        :return: True if the share watch list contains the given name otherwise it returns False.

        Example:
            - SMB.assert_share_watch_list('watch-me')
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@formcontrolname="watch_list"]//*[contains(text(),"{name}")]'))

    @classmethod
    def assert_sharing_smb_page_header(cls) -> bool:
        """
        This method verifies that the SMB sharing page header is displayed.

        :return: True if the SMB sharing page header is displayed, otherwise it returns False.

        Example:
            - SMB.assert_sharing_smb_page_header()
        """
        return COM.assert_page_header('SMB')

    @classmethod
    def assert_smb_acl_permission(cls, perm: str) -> bool:
        """
        This method returns True if the given permission is visible, otherwise returns False.

        :param perm: is the permission. [FULL/CHANGE/READ]
        :return: True if the given permission is visible, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_permission('FULL')
        """
        return COM.get_element_property(xpaths.common_xpaths.select_field('ae-perm'), 'innerText').__contains__(perm.upper())

    @classmethod
    def assert_smb_acl_permission_dropdown_values(cls) -> bool:
        """
        This method returns True if the permission dropdown values exist, otherwise returns False.

        :return: True if the permission dropdown values exist, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_who('user')
        """
        COM.click_on_element('//*[@data-test="select-ae-perm"]')
        assert COM.is_visible('//*[@data-test="option-ae-perm-full"]') is True
        assert COM.is_visible('//*[@data-test="option-ae-perm-change"]') is True
        assert COM.is_visible('//*[@data-test="option-ae-perm-read"]') is True
        COM.click_on_element('//*[@data-test="option-ae-perm-full"]')
        return True

    @classmethod
    def assert_smb_acl_type(cls, acl_type: str) -> bool:
        """
        This method returns True if the given acl_type is visible, otherwise returns False.

        :param acl_type: is the acl type. [ALLOWED/DENIED]
        :return: True if the given acl_type is visible, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_type('ALLOWED')
        """
        return COM.get_element_property(xpaths.common_xpaths.select_field('ae-type'), 'innerText').__contains__(acl_type.upper())

    @classmethod
    def assert_smb_acl_type_dropdown_values(cls) -> bool:
        """
        This method returns True if the type dropdown values exist, otherwise returns False.

        :return: True if the type dropdown values exist, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_who('user')
        """
        COM.click_on_element('//*[@data-test="select-ae-type"]')
        assert COM.is_visible('//*[@data-test="option-ae-type-allowed"]') is True
        assert COM.is_visible('//*[@data-test="option-ae-type-denied"]') is True
        COM.click_on_element('//*[@data-test="option-ae-type-allowed"]')
        return True

    @classmethod
    def assert_smb_acl_who(cls, who: str) -> bool:
        """
        This method returns True if the given who is visible, otherwise returns False.

        :param who: is the name of the who.
        :return: True if the given who is visible, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_who('user')
        """
        return COM.get_element_property(xpaths.common_xpaths.select_field('ae-who'), 'innerText').__contains__(who)

    @classmethod
    def assert_smb_acl_who_dropdown_values(cls) -> bool:
        """
        This method returns True if the who dropdown values exist, otherwise returns False.

        :return: True if the who dropdown values exist, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_who('user')
        """
        COM.click_on_element('//*[@data-test="select-ae-who"]')
        assert COM.is_visible('//*[@data-test="option-ae-who-user"]') is True
        assert COM.is_visible('//*[@data-test="option-ae-who-group"]') is True
        assert COM.is_visible('//*[@data-test="option-ae-who-everyone"]') is True
        COM.click_on_element('//*[@data-test="option-ae-who-everyone"]')
        return True

    @classmethod
    def assert_smb_acl_ad_who_group_dropdown_values(cls) -> bool:
        """
        This method returns True if the AD who user dropdown values exist, otherwise returns False.

        :return: True if the AD who user dropdown values exist, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_who('user')
        """
        assert COM.is_visible('//*[@data-test="input-group"]') is True
        COM.click_on_element('//*[@data-test="input-group"]')
        WebUI.delay(0.2)
        assert COM.is_visible('//*[@data-test="option-group-ad-03-enterprise-read-only-domain-controllers"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-domain-admins"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-domain-users"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-domain-guests"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-domain-computers"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-domain-controllers"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-cert-publishers"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-schema-admins"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-enterprise-admins"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-group-policy-creator-owners"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-read-only-domain-controllers"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-cloneable-domain-controllers"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-protected-users"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-key-admins"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-enterprise-key-admins"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-ras-and-ias-servers"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-allowed-rodc-password-replication-group"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-denied-rodc-password-replication-group"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-dnsadmins"]') is True
        assert COM.is_visible('//*[@data-test="option-group-ad-03-dnsupdateproxy"]') is True
        COM.click_on_element('//*[@data-test="input-group"]')
        return True

    @classmethod
    def assert_smb_acl_ad_who_user_dropdown_values(cls) -> bool:
        """
        This method returns True if the AD who user dropdown values exist, otherwise returns False.

        :return: True if the AD who user dropdown values exist, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_who('user')
        """
        assert COM.is_visible('//*[@data-test="input-user"]') is True
        COM.click_on_element('//*[@data-test="input-user"]')
        WebUI.delay(0.2)
        assert COM.is_visible('//*[@data-test="option-user-ad-03-administrator"]') is True
        assert COM.is_visible('//*[@data-test="option-user-ad-03-guest"]') is True
        assert COM.is_visible('//*[@data-test="option-user-ad-03-krbtgt"]') is True
        assert COM.is_visible('//*[@data-test="option-user-ad-03-defaultaccount"]') is True
        assert COM.is_visible('//*[@data-test="option-user-ad-03-centadmin"]') is True
        assert COM.is_visible('//*[@data-test="option-user-ad-03-ixuser"]') is True
        assert COM.is_visible('//*[@data-test="option-user-ad-03-duser-01"]') is True
        assert COM.is_visible('//*[@data-test="option-user-ad-03-nduser-01"]') is True
        COM.click_on_element('//*[@data-test="input-user"]')
        return True

    @classmethod
    def assert_user_can_access(cls, share: str, user: str, password: str) -> bool:
        """
        This returns True if the share can be accessed by the given user, otherwise it returns False.

        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user

        :return: True if the share can be accessed by the given user, otherwise it returns False.

        Example:
            - SMB.assert_guest_access()
        """
        response = SSH_Command_Line(f'smbclient //{private_config["IP"]}/{share} -W AD03 -U {user}%{password} -c \'pwd\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        return response.stdout.__contains__(share)

    @classmethod
    def click_edit_share_acl(cls, name: str) -> None:
        """
        This method clicks the edit share acl button of the given share by the share type.

        :param name: name of the given share

        Example:
            - SMB.click_edit_share_acl('share')
        """
        COM.click_button(f'card-smb-share-{COM.convert_to_tag_format(name)}-share-row-action')
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Share ACL for', 3)) is True

    @classmethod
    def click_edit_share_filesystem_acl(cls, name: str) -> None:
        """
        This method clicks the edit share filesystem acl button of the given share by the share type.

        :param name: name of the given share

        Example:
            - SMB.click_edit_share_filesystem_acl('share')
        """
        COM.click_button(f'card-smb-share-{name.lower()}-security-row-action')
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Edit ACL', 1)) is True

    @classmethod
    def click_edit_share(cls, share_name: str) -> None:
        """
        This method clicks the edit share button.

        Example:
            - SMB.click_edit_share()
        """
        COM.click_on_element(xpaths.smb.smb_share_options(share_name))
        COM.click_button('samba-options-edit')

    @classmethod
    def delete_share_by_name(cls, sharetype: str, name: str, action: str) -> None:
        """
        This method deletes the given share on the Shares page

        :param sharetype: name of the share type [smb/nfs/iscsi]
        :param name: name of the given share
        :param action: action to take

        Example:
            - SMB.delete_share_by_name('smb', 'share', 'delete')
        """
        COM.click_on_element(xpaths.common_xpaths.button_share_action_by_name(sharetype, name, action))
        COM.assert_confirm_dialog()

    @classmethod
    def set_afp(cls) -> None:
        """
        This method sets the afp checkbox.

        Example:
            - SMB.set_afp()
        """
        COM.set_checkbox('afp')

    @classmethod
    def set_audit_logging_enable(cls) -> None:
        """
        This method sets the audit logging enable checkbox.

        Example:
            - SMB.set_audit_logging_enable()
        """
        COM.set_checkbox('enable')

    @classmethod
    def set_guest_ok(cls) -> None:
        """
        This method sets the guest ok checkbox.

        Example:
            - SMB.set_guest_ok()
        """
        COM.set_checkbox('guestok')

    @classmethod
    def set_ignore_list(cls, name: str) -> None:
        """
        This method adds the given name to the ignore list.

        :param name: name of the account to ignore

        Example:
            - SMB.set_ignore_list()
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('ignore-list'))
        COM.click_on_element('//*[@data-test="input-ignore-list"]')
        name = COM.convert_to_tag_format(f'ignore-list-{name}')
        COM.click_on_element(f'//*[@data-test="option-{name}"]')

    @classmethod
    def set_share_purpose(cls, purpose: str) -> None:
        """
        This method sets the purpose for the share on the Edit Share right panel

        :param purpose: name of the purpose

        Example:
            - SMB.set_share_purpose('no purpose')
       """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.select_field('purpose')) is True
        COM.click_on_element('//*[@data-test="select-purpose"]')
        purpose = COM.convert_to_tag_format(purpose)
        COM.click_on_element(f'//*[@data-test="option-purpose-{purpose}"]')

    @classmethod
    def set_watch_list(cls, name: str) -> None:
        """
        This method adds the given name to the watch list.

        :param name: name of the account to watch

        Example:
            - SMB.set_watch_list('watch-me')
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('watch-list'))
        COM.click_on_element('//*[@data-test="input-watch-list"]')

        name = COM.convert_to_tag_format(f'watch-list-{name}')
        COM.click_on_element(f'//*[@data-test="option-{name}"]')

    @classmethod
    def verify_smb_audit_page_opens(cls) -> None:
        """
        This method verifies the Audit page is opens with SMB filter entered.

        Example:
            - SMB.verify_smb_audit_page_opens()
        """
        if COM.assert_page_header('Services'):
            COM.click_button('service-smb-receipt-long-row-action')
        elif COM.assert_page_header('Sharing'):
            COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu('SMB'))
            COM.click_button('cifs-actions-menu-logs')
        assert COM.assert_page_header('Audit') is True
        assert COM.assert_text_is_visible('"Service" = "SMB"') is True

    @classmethod
    def verify_smb_service_advanced_edit_ui(cls) -> None:
        """
        This method verifies the advanced edit UI of the SMB service.

        Example:
            - SMB.verify_smb_service_advanced_edit_ui()
        """
        cls.verify_smb_service_basic_edit_ui()
        assert COM.is_visible(xpaths.common_xpaths.select_field('unixcharset')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('loglevel')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('syslog')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('localmaster')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('aapl-extensions')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('multichannel')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('admin-group')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('guest')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('filemask')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('dirmask')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('bindip')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True

    @classmethod
    def verify_smb_service_basic_edit_ui(cls) -> None:
        """
        This method verifies the basic edit UI of the SMB service.

        Example:
            - SMB.verify_smb_service_basic_edit_ui()
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('netbiosname')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('netbiosalias')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('workgroup')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('description')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('enable-smb-1')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('ntlmv-1-auth')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True

    @classmethod
    def verify_smb_sessions_page_opens(cls):
        """
        This method verifies the SMB Sessions page is opens.

        Example:
            - SMB.verify_smb_sessions_page_opens()
        """
        if COM.assert_page_header('Services'):
            COM.click_button('service-smb-list-row-action')
        elif COM.assert_page_header('Sharing'):
            COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu('SMB'))
            COM.click_button('cifs-actions-menu-sessions')
        assert COM.is_visible(xpaths.common_xpaths.link_field('breadcrumb-sharing')) is True
        assert COM.assert_page_header('SMB Status') is True
