import xpaths
from helper.cli import SSH_Command_Line
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.api.post import API_POST


class SMB:
    @classmethod
    def add_smb_acl_entry_by_api(cls, who: str, userid: int, permission: str, perm_type: str):
        """
        This method sets the values for an SMB_ACL_ENTRY

        :param who: is the type of user to have acl permissions: [USER/GROUP/BOTH]
        :param userid: is the id of the user/group used in the 'who' parameter as an integer
        :param permission: is the permission to be assigned: [FULL/CHANGE/READ]
        :param perm_type: is the permission type to be assigned: [ALLOWED/DENIED]
        """
        API_POST.add_smb_acl_entry(who, userid, permission, perm_type)

    @classmethod
    def assert_guest_access(cls, share: str, user: str = private_config['SMB_USERNAME'], password: str = private_config['SMB_PASSWORD']) -> bool:
        """
        This returns True if the share can be accessed by a guest user, otherwise it returns False.

        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user

        :return: True if the share ignore list contains the given name otherwise it returns False.

        Example:
        - SMB.assert_guest_access()
        """
        # response = SSH_Command_Line(f'smbclient //{private_config["IP"]}/{share} -U nonexistent%nopassword -c \'pwd\'', private_config['SMB_ACL_IP'], user, password)
        # return response.stdout.__contains__(share)
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
        # SSH_Command_Line(f'smbclient //{private_config["IP"]}/{share} -U nonexistent%nopassword -c \'rm {file}\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        # response = SSH_Command_Line(f'smbclient //{private_config["IP"]}/{share} -U nonexistent%nopassword -c \'ls\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        # return not response.stdout.__contains__(file)
        return cls.assert_user_can_delete_file(file, share, 'nonexistent', 'nopassword')

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
        # SSH_Command_Line(f'cd smbdirectory; touch {file}; chmod 777 {file}', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        # SSH_Command_Line(f'cd smbdirectory; smbclient //{private_config["IP"]}/{share} -U nonexistent%nopassword -c \'put {file}\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        # response = SSH_Command_Line(f'cd smbdirectory; smbclient //{private_config["IP"]}/{share} -U nonexistent%nopassword -c \'ls\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        # return response.stdout.__contains__(file)
        return cls.assert_user_can_put_file(file, share, 'nonexistent', 'nopassword')

    @classmethod
    def assert_share_ignore_list(cls, name: str) -> bool:
        """
        This returns True if the share ignore list contains the given name otherwise it returns False.

        :param name: name to verify in the ignore list
        :return: True if the share ignore list contains the given name otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@formcontrolname="ignore_list"]//*[contains(text(),"{name}")]'))

    @classmethod
    def assert_share_watch_list(cls, name: str) -> bool:
        """
        This returns True if the share watch list contains the given name otherwise it returns False.

        :param name: name to verify in the watch list
        :return: True if the share watch list contains the given name otherwise it returns False.
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@formcontrolname="watch_list"]//*[contains(text(),"{name}")]'))

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
    def assert_user_can_delete_file(cls, file: str, share: str, user: str, password: str, ad: bool = False) -> bool:
        """
        This returns True if the given file is deleted, otherwise it returns False.

        :param file: is the name of the file to delete
        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user
        :param ad: whether the user is an AD user

        :return: True if the given file is deleted, otherwise it returns False.

        Example:
        - SMB.assert_user_can_delete_file('myFile', 'myShare')
        """
        use_ad = ""
        if ad is True:
            use_ad = "-W AD03 "
        SSH_Command_Line(f'smbclient //{private_config["IP"]}/{share} {use_ad}-U {user}%{password} -c \'rm {file}\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        response = SSH_Command_Line(f'smbclient //{private_config["IP"]}/{share} {use_ad}-U {user}%{password} -c \'ls\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        return not response.stdout.__contains__(file)

    @classmethod
    def assert_user_can_put_file(cls, file: str, share: str, user: str, password: str, ad: bool = False) -> bool:
        """
        This returns True if the given file is put, otherwise it returns False.

        :param file: is the name of the file to put
        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user
        :param ad: whether the user is an AD user

        :return: True if the given file is put, otherwise it returns False.

        Example:
        - SMB.assert_user_can_put_file('myFile', 'myShare', 'user', 'password')
        - SMB.assert_user_can_put_file('myFile', 'myShare', 'user', 'password', True)
        """
        use_ad = ""
        if ad is True:
            use_ad = "-W AD03 "
        SSH_Command_Line(f'cd smbdirectory; touch {file}; chmod 777 {file}', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        SSH_Command_Line(f'cd smbdirectory; smbclient //{private_config["IP"]}/{share} {use_ad}-U {user}%{password} -c \'put {file}\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        response = SSH_Command_Line(f'cd smbdirectory; smbclient //{private_config["IP"]}/{share} {use_ad}-U {user}%{password} -c \'ls\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        return response.stdout.__contains__(file)

    @classmethod
    def click_edit_share_filesystem_acl(cls, name: str) -> None:
        """
        This method clicks the edit share filesystem acl button of the given share by the share type.

        :param name: name of the given share
        """
        COM.click_button(f'card-smb-share-{name.lower()}-security-row-action')
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_header(f'Edit ACL', 1)) is True

    @classmethod
    def delete_share_by_name(cls, sharetype: str, name: str, action: str) -> None:
        """
        This method deletes the given share on the Shares page
        """
        COM.click_on_element(xpaths.common_xpaths.button_share_action_by_name(sharetype, name, action))
        COM.assert_confirm_dialog()

    @classmethod
    def set_afp(cls) -> None:
        """
        This method sets the afp checkbox.
        """
        COM.set_checkbox('afp')

    @classmethod
    def set_audit_logging_enable(cls) -> None:
        """
        This method sets the audit logging enable checkbox.
        """
        COM.set_checkbox('enable')

    @classmethod
    def set_guest_ok(cls) -> None:
        """
        This method sets the guest ok checkbox.
        """
        COM.set_checkbox('guestok')

    @classmethod
    def set_ignore_list(cls, name: str) -> None:
        """
        This method adds the given name to the ignore list.

        :param name: name of the account to ignore
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('ignore-list'))
        COM.click_on_element(f'//*[@data-test="input-ignore-list"]')
        name = COM.convert_to_tag_format('ignore-list-'+name)
        COM.click_on_element(f'//*[@data-test="option-{name}"]')

    @classmethod
    def set_share_purpose(cls, purpose: str) -> None:
        """
        This method sets the purpose for the share on the Edit Share right panel
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.select_field('purpose')) is True
        COM.click_on_element(f'//*[@data-test="select-purpose"]')
        # purpose = purpose.replace(' ', '-').lower()
        purpose = COM.convert_to_tag_format(purpose)
        COM.click_on_element(f'//*[@data-test="option-purpose-{purpose}"]')

    @classmethod
    def set_smb_acl_by_api(cls, name: str):
        """
        This method sets the values for an SMB_ACL_ENTRY

        :param name: is the name of the smb share to have acl permissions set
        """
        API_POST.set_smb_acl(name)

    @classmethod
    def set_watch_list(cls, name: str) -> None:
        """
        This method adds the given name to the watch list.

        :param name: name of the account to watch
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('watch-list'))
        COM.click_on_element(f'//*[@data-test="input-watch-list"]')

        name = COM.convert_to_tag_format('watch-list-'+name)
        COM.click_on_element(f'//*[@data-test="option-{name}"]')

    @classmethod
    def verify_smb_audit_page_opens(cls):
        """
        This method verifies the Audit page is opens with SMB filter entered.
        """
        if COM.assert_page_header('Services'):
            COM.click_link('cifs-logs')
        elif COM.assert_page_header('Sharing'):
            COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu('SMB'))
            COM.click_button('cifs-actions-menu-logs')
        assert COM.assert_page_header('Audit') is True
        assert COM.assert_text_is_visible('"Service" = "SMB"') is True

    @classmethod
    def verify_smb_service_advanced_edit_ui(cls):
        """
        This method verifies the advanced edit UI of the SMB service.
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
    def verify_smb_service_basic_edit_ui(cls):
        """
        This method verifies the basic edit UI of the SMB service.
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
        """
        if COM.assert_page_header('Services'):
            COM.click_link('cifs-sessions')
        elif COM.assert_page_header('Sharing'):
            COM.click_on_element(xpaths.common_xpaths.button_share_actions_menu('SMB'))
            COM.click_button('cifs-actions-menu-sessions')
        assert COM.is_visible(xpaths.common_xpaths.link_field('breadcrumb-sharing')) is True
        assert COM.assert_page_header('SMB Status') is True
