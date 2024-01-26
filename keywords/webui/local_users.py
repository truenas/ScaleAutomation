import xpaths
from helper.webui import WebUI
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common as COM


class Local_Users:

    @classmethod
    def assert_error_user_home_directory_not_writable(cls) -> bool:
        """
        This method returns True if the home directory error message displays, otherwise False

        :return: returns True if the home directory error message displays, otherwise False

        Example
         - Local_Users.assert_error_user_home_directory_not_writable()
        """
        return COM.assert_text_is_visible('Home directory is not writable, leave this blank"')

    @classmethod
    def assert_error_user_samba_change_password(cls) -> bool:
        """
        This method returns True if the home directory error message displays, otherwise False

        :return: returns True if the home directory error message displays, otherwise False

        Example
         - Local_Users.assert_error_user_home_directory_not_writable()
        """
        return COM.assert_text_is_visible('Password must be changed in order to enable SMB authentication')

    @classmethod
    def assert_user_allow_all_sudo_commands(cls) -> bool:
        """
        This method returns True if the allow all sudo commands checkbox is set, otherwise False

        :return: returns True if the allow all sudo commands checkbox is set, otherwise False

        Example
         - Local_Users.assert_user_allow_all_sudo_commands()
        """
        return COM.is_checked('sudo-commands-all')

    @classmethod
    def assert_user_allow_all_sudo_commands_no_password(cls) -> bool:
        """
        This method returns True if the allow all sudo commands no password checkbox is set, otherwise False

        :return: returns True if the allow all sudo commands no password checkbox is set, otherwise False

        Example
         - Local_Users.assert_user_allow_all_sudo_commands_no_password()
        """
        return COM.is_checked('sudo-commands-nopasswd-all')

    @classmethod
    def assert_user_allowed_sudo_commands(cls, command) -> bool:
        """
        This method returns True if the given command is set for the user, otherwise False

        :param command: is the command of the user
        :return: returns True if the given command is set for the user, otherwise False

        Example
         - Local_Users.assert_user_allowed_sudo_commands('/usr/sbin/zfs')
        """
        return WebUI.xpath(f'//*[@formcontrolname="sudo_commands"]//*[contains(text(),"{command}")]').text == command

    @classmethod
    def assert_user_allowed_sudo_commands_disabled(cls) -> bool:
        """
        This method returns True if the allow sudo commands text field is disabled, otherwise False

        :return: returns True if the allow sudo commands text field is disabled, otherwise False

        Example
         - Local_Users.assert_user_allowed_sudo_commands_disabled()
        """
        return COM.get_input_property('sudo-commands', 'disabled')

    @classmethod
    def assert_user_allowed_sudo_commands_no_password(cls, command) -> bool:
        """
        This method returns True if the given command is set for the user, otherwise False

        :param command: is the command of the user
        :return: returns True if the given command is set for the user, otherwise False

        Example
         - Local_Users.assert_user_allowed_sudo_commands_no_password('/usr/bin')
        """
        return WebUI.xpath(f'//*[@formcontrolname="sudo_commands_nopasswd"]//*[contains(text(),"{command}")]').text == command

    @classmethod
    def assert_user_allowed_sudo_commands_no_password_disabled(cls) -> bool:
        """
        This method returns True if the allow sudo commands no password text field is disabled, otherwise False

        :return: returns True if the allow sudo commands no password text field is disabled, otherwise False

        Example
         - Local_Users.assert_user_allowed_sudo_commands_no_password_disabled()
        """
        return COM.get_input_property('sudo-commands-nopasswd', 'disabled')

    @classmethod
    def assert_user_authorized_keys(cls, key) -> bool:
        """
        This method returns True if the given key set for user authorized key, otherwise False

        :param key: is the ssh public key of the user
        :return: returns True if the given key set for user authorized key, otherwise False

        Example
         - Local_Users.assert_user_authorized_keys('key')
        """
        return COM.get_element_property(xpaths.common_xpaths.textarea_field('sshpubkey'), 'value') == key
        # return WebUI.xpath(xpaths.common_xpaths.textarea_field('sshpubkey')).text == key

    @classmethod
    def assert_user_lock_user(cls) -> bool:
        """
        This method returns True if the lock user checkbox is set, otherwise False

        :return: returns True if the lock user checkbox is set, otherwise False

        Example
         - Local_Users.assert_user_lock_user()
        """
        return COM.is_checked('locked')

    @classmethod
    def assert_user_samba_authentication(cls) -> bool:
        """
        This method returns True if the smb checkbox is set, otherwise False

        :return: returns True if the smb checkbox is set, otherwise False

        Example
         - Local_Users.assert_user_samba_authentication()
        """
        return COM.is_checked('smb')

    @classmethod
    def assert_user_shell(cls, shell) -> bool:
        """
        This method returns True if the given shell is set for the user, otherwise False

        :param shell: is the shell of the user
        :return: returns True if the given shell is set for the user, otherwise False

        Example
         - Local_Users.assert_user_shell('bash')
        """
        return WebUI.xpath(xpaths.common_xpaths.select_field('shell')).text == shell

    @classmethod
    def assert_user_ssh_password_login_enabled(cls) -> bool:
        """
        This method returns True if the ssh password login checkbox is set, otherwise False

        :return: returns True if the ssh password login checkbox is set, otherwise False

        Example
         - Local_Users.assert_user_ssh_password_login_enabled()
        """
        return COM.is_checked('ssh-password-enabled')

    @classmethod
    def click_add_user_button(cls) -> None:
        """
        This method clicks the add user button

        Example
         - Local_Users.click_add_user_button()
        """
        COM.click_button('add-user')

    @classmethod
    def click_user_delete_button(cls, username: str) -> None:
        """
        This method clicks the user delete button of the given user

        :param username: is the name of the user

        Example
         - Local_Users.click_user_delete_button('username')
        """
        name = COM.convert_to_tag_format(username)
        COM.click_button('delete-' + name)

    @classmethod
    def click_user_edit_button(cls) -> None:
        """
        This method clicks the edit user button on the expanded users section

        Example
         - Local_Users.click_user_edit_button()
        """
        COM.click_on_element(xpaths.common_xpaths.any_start_with_field('button-edit-'))

    @classmethod
    def confirm_delete_user_and_primary_group_by_full_name(cls, fullname: str) -> None:
        """
        This method confirms the user delete dialog and checks the delete primary group checkbox

        :param fullname: is the fullname of the user

        Example
         - Local_Users.click_user_delete_button('Full Name')
        """
        cls.confirm_delete_user_by_full_name(fullname, True)

    @classmethod
    def confirm_delete_user_by_full_name(cls, fullname: str, primary_group: bool = False) -> None:
        """
        This method confirms the user delete dialog and checks the delete primary group checkbox

        :param fullname: is the fullname of the user
        :param primary_group: is whether to delete the primary group as well

        Example
         - Local_Users.confirm_delete_user_by_full_name('Full Name')
         - Local_Users.confirm_delete_user_by_full_name('Full Name', True)
        """
        if COM.is_visible(xpaths.common_xpaths.any_text(fullname)):
            cls.expand_user_by_full_name(fullname)
            cls.click_user_delete_button(cls.get_username_from_full_name(fullname))
            if primary_group:
                if COM.is_visible(xpaths.common_xpaths.checkbox_field('delete-primary-group')):
                    WebUI.xpath(xpaths.common_xpaths.checkbox_field('delete-primary-group')).click()
            COM.click_button('delete')
            COM.assert_page_header('Delete User')

    @classmethod
    def confirm_home_warning_dialog(cls):
        """
        This method confirms the home directory change warning dialog

        Example
         - Local_Users.confirm_home_warning_dialog()
        """
        COM.assert_confirm_dialog()

    @classmethod
    def delete_user_by_api(cls, username) -> None:
        """
        This method deletes the given user by API call

        :param username: is the name of the user to delete

        Example
         - Local_Users.delete_user_by_api('username')
        """
        API_DELETE.delete_user(username)

    @classmethod
    def expand_user_by_full_name(cls, fullname: str) -> None:
        """
        This method expands the given user section

        :param fullname: is the fullname of the user to expand

        Example
         - Local_Users.expand_user_by_full_name('Full Name')
        """
        name = cls.get_username_from_full_name(fullname)
        name = COM.convert_to_tag_format(name)
        if COM.is_visible(xpaths.common_xpaths.button_field('edit-' + name)) is False:
            WebUI.xpath(xpaths.common_xpaths.any_text(fullname)).click()

    @classmethod
    def get_username_from_full_name(cls, fullname: str) -> str:
        """
        This method returns the username from the given fullname

        :param fullname: is the fullname of the user to expand
        :return: returns the username from the given fullname

        Example
         - Local_Users.get_username_from_full_name('Full Name')
        """
        name = WebUI.xpath(xpaths.common_xpaths.any_text(fullname)).text
        if name.__contains__(' fullname'):
            name = name.replace(' fullname', '')
        return name

    @classmethod
    def is_user_visible(cls, username: str) -> bool:
        """
        This method returns True if the given user displays, otherwise False

        :param username: is the name of the user
        :return: returns True if the given user displays, otherwise False

        Example
         - Local_Users.is_user_visible('username')
        """
        WebUI.refresh()
        name = COM.convert_to_tag_format(username)
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@data-test="row-{name}"]'))

    @classmethod
    def select_user_shell(cls, shell) -> None:
        """
        This method selects the given shell for the user

        :param shell: is the name of the user

        Example
         - Local_Users.select_user_shell('bash')
        """
        COM.select_option('shell', 'shell-'+shell)

    @classmethod
    def set_show_builtin_users_toggle(cls) -> None:
        """
        This method sets the show built-in users toggle

        Example
         - Local_Users.set_show_builtin_users_toggle()
        """
        COM.set_toggle('show-built-in-users')

    @classmethod
    def set_user_allow_all_sudo_commands_checkbox(cls) -> None:
        """
        This method sets the allow all sudo commands checkbox

        Example
         - Local_Users.set_user_allow_all_sudo_commands_checkbox()
        """
        COM.set_checkbox('sudo-commands-all')

    @classmethod
    def set_user_allow_all_sudo_commands_no_password_checkbox(cls) -> None:
        """
        This method sets the allow all sudo commands no password checkbox

        Example
         - Local_Users.set_user_allow_all_sudo_commands_no_password_checkbox()
        """
        COM.set_checkbox('sudo-commands-nopasswd-all')

    @classmethod
    def set_user_allowed_sudo_commands(cls, command) -> None:
        """
        This method adds the given sudo command for the user

        :param command: is the sudo command to be added

        Example
         - Local_Users.set_user_allowed_sudo_commands('/usr/sbin/zfs')
        """
        COM.set_input_field('sudo-commands', command)

    @classmethod
    def set_user_allowed_sudo_commands_no_password(cls, command) -> None:
        """
        This method adds the given sudo command no password for the user

        :param command: is the sudo command no password to be added

        Example
         - Local_Users.set_user_allowed_sudo_commands_no_password('/usr/bin')
        """
        COM.set_input_field('sudo-commands-nopasswd', command)

    @classmethod
    def set_user_authorized_keys(cls, key) -> None:
        """
        This method sets the ssh public key of the user

        :param key: is the ssh public key of the user

        Example
         - Local_Users.set_user_authorized_keys('key')
        """
        COM.set_textarea_field('sshpubkey', key, True)

    @classmethod
    def set_user_create_home_directory_checkbox(cls) -> None:
        """
        This method sets the create home directory checkbox

        Example
         - Local_Users.set_user_create_home_directory_checkbox()
        """
        COM.set_checkbox('home-create')

    @classmethod
    def set_user_email(cls, email) -> None:
        """
        This method sets the email of the user

        :param email: is the email of the user

        Example
         - Local_Users.set_user_email('email@nowhere.com')
        """
        COM.set_input_field('email', email)

    @classmethod
    def set_user_fullname(cls, fullname) -> None:
        """
        This method sets the fullname of the user

        :param fullname: is the fullname of the user

        Example
         - Local_Users.set_user_fullname('Full Name')
        """
        COM.set_input_field('full-name', fullname)

    @classmethod
    def set_user_home_directory(cls, home) -> None:
        """
        This method sets the home directory of the user to the given directory

        :param home: is the path of the home directory

        Example
         - Local_Users.set_user_home_directory('/mnt/tank/home')
        """
        COM.set_input_field('home', home)

    @classmethod
    def set_user_lock_user_checkbox(cls) -> None:
        """
        This method sets the lock user checkbox

        Example
         - Local_Users.set_user_lock_user_checkbox()
        """
        COM.set_checkbox('locked')

    @classmethod
    def set_user_password(cls, password) -> None:
        """
        This method sets the password of the user

        :param password: is the password of the user

        Example
         - Local_Users.set_user_password('password')
        """
        COM.set_input_field('password', password)

    @classmethod
    def set_user_password_confirm(cls, password) -> None:
        """
        This method sets the confirmation password of the user

        :param password: is the password of the user

        Example
         - Local_Users.set_user_password_confirm('password')
        """
        COM.set_input_field('password-conf', password)

    @classmethod
    def set_user_samba_authentication_checkbox(cls) -> None:
        """
        This method sets the smb checkbox

        Example
         - Local_Users.set_user_samba_authentication_checkbox()
        """
        COM.set_checkbox('smb')

    @classmethod
    def set_user_ssh_password_login_enabled_checkbox(cls) -> None:
        """
        This method sets the ssh password login enabled checkbox

        Example
         - Local_Users.set_user_ssh_password_login_enabled_checkbox()
        """
        COM.set_checkbox('ssh-password-enabled')

    @classmethod
    def set_user_username(cls, username) -> None:
        """
        This method sets the name of the user

        :param username: is the name of the user

        Example
         - Local_Users.set_user_username('username')
        """
        COM.set_input_field('username', username)

    @classmethod
    def unset_show_builtin_users_toggle(cls) -> None:
        """
        This method unsets the show built-in users toggle

        Example
         - Local_Users.unset_show_builtin_users_toggle()
        """
        COM.unset_toggle('show-built-in-users')
