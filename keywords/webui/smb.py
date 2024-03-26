import xpaths
from helper.cli import SSH_Command_Line
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.ssh.smb import SSH_SMB as SSHSMB
from keywords.webui.common import Common as COM


class SMB:

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

        :param who: is the name of the who.
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

        :param who: is the name of the who.
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
    def assert_smb_acl_ad_who_user_dropdown_values(cls) -> bool:
        """
        This method returns True if the AD who user dropdown values exist, otherwise returns False.

        :param who: is the name of the who.
        :return: True if the AD who user dropdown values exist, otherwise returns False.

        Example:
            - SMB.assert_smb_acl_who('user')
        """
        assert COM.is_visible('//*[@data-test="input-user"]') is True
        COM.click_on_element('//*[@data-test="input-user"]')
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
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_header(f'Share ACL for', 3)) is True

    @classmethod
    def click_edit_share_filesystem_acl(cls, name: str) -> None:
        """
        This method clicks the edit share filesystem acl button of the given share by the share type.

        :param name: name of the given share

        Example:
            - SMB.click_edit_share_filesystem_acl('share')
        """
        COM.click_button(f'card-smb-share-{name.lower()}-security-row-action')
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_header(f'Edit ACL', 1)) is True

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
        COM.click_on_element(f'//*[@data-test="input-ignore-list"]')
        name = COM.convert_to_tag_format('ignore-list-'+name)
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
        COM.click_on_element(f'//*[@data-test="select-purpose"]')
        # purpose = purpose.replace(' ', '-').lower()
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
        COM.click_on_element(f'//*[@data-test="input-watch-list"]')

        name = COM.convert_to_tag_format('watch-list-'+name)
        COM.click_on_element(f'//*[@data-test="option-{name}"]')

    @classmethod
    def verify_smb_audit_page_opens(cls) -> None:
        """
        This method verifies the Audit page is opens with SMB filter entered.

        Example:
            - SMB.verify_smb_audit_page_opens()
        """
        if COM.assert_page_header('Services'):
            COM.click_link('cifs-logs')
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
            COM.click_link('cifs-sessions')
        elif COM.assert_page_header('Sharing'):
            COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu('SMB'))
            COM.click_button('cifs-actions-menu-sessions')
        assert COM.is_visible(xpaths.common_xpaths.link_field('breadcrumb-sharing')) is True
        assert COM.assert_page_header('SMB Status') is True
