import xpaths
from helper.cli import SSH_Command_Line
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


class SSH_Connection:
    @classmethod
    def assert_shell_type(cls, shell_return: str, shell_type: str) -> bool:
        """
        This method verifies the shell for the given user is set to the given shell type.

        :param shell_return: is the expected output of the /etc/passwd file
        :param shell_type: is the name of the shell

        Example:
            - SSH_Connection.assert_shell_type('admin', 'bash')
        """
        command = SSH_Command_Line(f'grep {shell_type} /etc/passwd', private_config['IP'], private_config['USERNAME'],
                                private_config['PASSWORD'])
        return shell_return in command.stdout

    @classmethod
    def assert_ssh_connection_exists(cls, connection: str) -> bool:
        """
        This method verifies the given connection exists and creates it if it doesn't

        :param connection: is the name of the given connection

        Example:
            - SSH_Connection.assert_ssh_connection_exists('myConnection')
        """
        if cls.is_ssh_connection_visible(connection) is False:
            COM.click_button('add-ssh-connection')
            COM.set_input_field('connection-name', connection)
            url = private_config['REP_DEST_IP']
            if connection.__contains__('self'):
                url = private_config['IP']
            cls.set_url(url)
            cls.set_admin_credentials(private_config['USERNAME'], private_config['PASSWORD'])
            ssh_username = 'root'
            if connection.__contains__('admin'):
                ssh_username = 'admin'
            cls.set_username(ssh_username)
            if connection.__contains__('admin'):
                cls.set_passwordless_sudo_checkbox()
            cls.click_generate_new_private_key()
            COM.click_save_button_and_wait_for_right_panel()
            NAV.navigate_to_backup_credentials()
        return cls.is_ssh_connection_visible(connection)

    @classmethod
    def click_add_ssh_keypairs_button(cls) -> None:
        """
        This method clicks the add ssh keypairs button

        Example:
            - SSH_Connection.click_add_ssh_keypairs_button()
        """
        COM.click_button('add-ssh-keypair')

    @classmethod
    def click_add_ssh_connection_button(cls) -> None:
        """
        This method clicks the add ssh connection button

        Example:
            - SSH_Connection.click_add_ssh_connection_button()
        """
        COM.click_button('add-ssh-connection')

    @classmethod
    def click_delete_ssh_keypair_button(cls, name) -> None:
        """
        This method clicks the delete ssh keypair button for the given keypair.
        Also deletes the SSH Connection if it exists

        :param name: is the name of the keypair

        Example:
            - SSH_Connection.click_delete_ssh_keypair_button('my SSH Keypair')
        """
        if cls.is_ssh_connection_visible(name):
            cls.click_delete_ssh_connection_button(name)
        name = COM.convert_to_tag_format(name)
        COM.click_button(f'ssh-keypair-{name}-key-delete-row-action')
        COM.assert_confirm_dialog()
        NAV.navigate_to_backup_credentials()

    @classmethod
    def click_delete_ssh_connection_button(cls, name) -> None:
        """
        This method clicks the delete ssh connection button for the given connection

        :param name: is the name of the connection

        Example:
            - SSH_Connection.click_delete_ssh_connection_button('my SSH Connection')
        """
        name = COM.convert_to_tag_format(name)
        COM.click_button(f'ssh-con-{name}-delete-row-action')
        COM.assert_confirm_dialog()

    @classmethod
    def click_edit_ssh_keypairs_button(cls, name) -> None:
        """
        This method clicks the edit ssh keypairs button for the given keypair

        :param name: is the name of the keypair

        Example:
            - SSH_Connection.click_edit_ssh_keypairs_button('my SSH keypair')
        """
        name = COM.convert_to_tag_format(name)
        COM.click_button(f'ssh-keypair-{name}-key-edit-row-action')
        assert COM.assert_right_panel_header('SSH Keypairs') is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True

    @classmethod
    def click_edit_ssh_keypairs_download_actions_button(cls) -> None:
        """
        This method clicks the edit ssh keypairs download actions button

        Example:
            - SSH_Connection.click_edit_ssh_keypairs_download_actions_button()
        """
        assert COM.is_visible(xpaths.common_xpaths.button_field('download-actions')) is True
        COM.click_button('download-actions')
        WebUI.wait_until_visible(xpaths.common_xpaths.button_field('download-private-key'))

    @classmethod
    def click_edit_ssh_keypairs_download_private_key_button(cls) -> None:
        """
        This method clicks the edit ssh keypairs download private key button

        Example:
            - SSH_Connection.click_edit_ssh_keypairs_download_private_key_button()
        """
        assert COM.is_visible(xpaths.common_xpaths.button_field('download-private-key')) is True
        COM.click_button('download-private-key')
        WebUI.delay(0.5)

    @classmethod
    def click_edit_ssh_keypairs_download_public_key_button(cls) -> None:
        """
        This method clicks the edit ssh keypairs download public key button

        Example:
            - SSH_Connection.click_edit_ssh_keypairs_download_public_key_button()
        """
        assert COM.is_visible(xpaths.common_xpaths.button_field('download-public-key'))
        COM.click_button('download-public-key')
        WebUI.delay(0.5)

    @classmethod
    def click_generate_new_private_key(cls) -> None:
        """
        This method sets the ssh connection to generate a new private key

        Example:
            - SSH_Connection.click_generate_new_private_key()
        """
        COM.select_option('private-key', 'private-key-generate-new')

    @classmethod
    def click_ssh_view_more_button(cls, sshtype: str) -> None:
        """
        This method clicks the given connection type view more button

        :param sshtype: is the type of the connection

        Example:
            - SSH_Connection.click_ssh_view_more_button('connection')
            - SSH_Connection.click_ssh_view_more_button('keypair')
        """
        if COM.is_visible(xpaths.ssh.button_ssh_view_more_type(sshtype)):
            COM.click_on_element(xpaths.ssh.button_ssh_view_more_type(sshtype))

    @classmethod
    def click_ssh_view_more_connection_button(cls) -> None:
        """
        This method clicks the connection view more button

        Example:
            - SSH_Connection.click_ssh_view_more_connection_button()
        """
        cls.click_ssh_view_more_button('connection')

    @classmethod
    def click_ssh_view_more_keypairs_button(cls) -> None:
        """
        This method clicks the keypair view more button

        Example:
            - SSH_Connection.click_ssh_view_more_keypairs_button()
        """
        cls.click_ssh_view_more_button('keypair')

    @classmethod
    def is_ssh_connection_visible(cls, name: str) -> bool:
        """
        This method returns True if the given connection is visible, otherwise False

        :param name: is the name of the connection
        :return: True if the given connection is visible, otherwise False.

        Example:
            - SSH_Connection.is_ssh_connection_visible('myConnection')
        """
        return cls.is_ssh_type_visible('connection', name)

    @classmethod
    def is_ssh_keypair_visible(cls, name: str) -> bool:
        """
        This method returns True if the given keypair is visible, otherwise False

        :param name: is the name of the keypair
        :return: True if the given keypair is visible, otherwise False.

        Example:
            - SSH_Connection.is_ssh_keypair_visible('myKeypair')
        """
        return cls.is_ssh_type_visible('keypair', name)

    @classmethod
    def is_ssh_type_visible(cls, sshtype: str, name: str) -> bool:
        """
        This method returns True if the given connection type is visible, otherwise False

        :param sshtype: is the type of the connection
        :param name: is the name of the connection
        :return: True if the given connection type is visible, otherwise False.

        Example:
            - SSH_Connection.is_ssh_type_visible('connection', 'myConnection')
            - SSH_Connection.is_ssh_type_visible('keypair', 'myConnection')
        """
        cls.click_ssh_view_more_button(sshtype)
        name = cls.set_ssh_name_by_type(sshtype, name)
        return COM.is_visible(xpaths.ssh.label_ssh_type_name(sshtype, name))

    @classmethod
    def set_admin_credentials(cls, user: str, password: str) -> None:
        """
        This method sets the admin user and password for the ssh connection

        :param user: is the admin user
        :param password: is the admin password

        Example:
            - SSH_Connection.set_admin_credentials('myAdmin', 'myPassword')
        """
        COM.set_input_field('admin-username', user)
        COM.set_input_field('password', password)

    @classmethod
    def set_passwordless_sudo_checkbox(cls) -> None:
        """
        This method sets the enable passwordless sudo checkbox

        Example:
            - SSH_Connection.set_passwordless_sudo_checkbox()
        """
        if COM.is_visible(xpaths.common_xpaths.checkbox_field('sudo')):
            COM.set_checkbox('sudo')

    @classmethod
    def set_ssh_keypair_name(cls, name) -> None:
        """
        This method sets the ssh keypair name to the given name

        :param name: is the ssh keypair name to set

        Example:
            - SSH_Connection.set_ssh_keypair_name('my Keypair Name')
        """
        COM.set_input_field('-name', name)

    @classmethod
    def set_ssh_connection_name(cls, name) -> None:
        """
        This method sets the ssh connection name to the given name

        :param name: is the ssh connection name to set

        Example:
            - SSH_Connection.set_ssh_connection_name('my Connection Name')
        """
        COM.set_input_field('connection-name', name)

    @classmethod
    def set_ssh_name_by_type(cls, sshtype: str, name: str) -> str:
        """
        This method returns the given connection by the connection type

        :param sshtype: is the type of the connection [connection/keypair]
        :param name: is the name of the connection
        :return: the given connection by the connection type.

        Example:
            - SSH_Connection.set_ssh_name_by_type('connection', 'myConnection')
            - SSH_Connection.set_ssh_name_by_type('keypair', 'myConnection')
        """
        if sshtype == "keypair":
            name = name + ' Key'
        return name

    @classmethod
    def set_url(cls, url: str) -> None:
        """
        This method sets the url field to the given url

        :param url: is the url to set

        Example:
            - SSH_Connection.set_url('10.1.1.0')
            - SSH_Connection.set_url('http://10.1.1.0')
        """
        if not url.startswith("http"):
            url = 'http://' + url
        COM.set_input_field('url', url)

    @classmethod
    def set_username(cls, username) -> None:
        """
        This method sets the user for the ssh connection

        :param username: is the user

        Example:
            - SSH_Connection.set_username('myUser')
        """

        COM.set_input_field('username', username)

    @classmethod
    def verify_ssh_service_advanced_edit_ui(cls) -> None:
        """
        This method verifies the advanced edit UI of the SSH service.
        """
        cls.verify_ssh_service_basic_edit_ui()
        assert COM.is_visible(xpaths.common_xpaths.select_field('bindiface')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('compression')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('sftp-log-level')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('sftp-log-facility')) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field('weak-ciphers')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('options')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True

    @classmethod
    def verify_ssh_service_basic_edit_ui(cls) -> None:
        """
        This method verifies the basic edit UI of the SSH service.
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('tcpport')) is True
        assert COM.is_visible(xpaths.common_xpaths.any_xpath('//*[@data-test="input"]')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('passwordauth')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('kerberosauth')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('tcpfwd')) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field('save')) is True
