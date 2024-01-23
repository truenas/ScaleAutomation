import xpaths
from helper.global_config import private_config
from keywords.webui.common import Common as COM


class SSH_Connection:
    @classmethod
    def assert_ssh_connection_exists(cls, connection: str) -> bool:
        """
        This method verifies the given connection exists

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
            if ssh_username.__contains__('admin'):
                ssh_username = 'admin'
            cls.set_username(ssh_username)
            cls.set_passwordless_sudo_checkbox()
            cls.click_generate_new_private_key()
            COM.click_save_button()
        return cls.is_ssh_connection_visible(connection)

    @classmethod
    def click_generate_new_private_key(cls):
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
    def set_passwordless_sudo_checkbox(cls):
        """
        This method sets the enable passwordless sudo checkbox

        Example:
            - SSH_Connection.set_passwordless_sudo_checkbox()
        """
        if COM.is_visible(xpaths.common_xpaths.checkbox_field('sudo')):
            COM.set_checkbox('sudo')

    @classmethod
    def set_ssh_name_by_type(cls, sshtype: str, name: str) -> str:
        """
        This method returns the given connection by the connection type

        :param sshtype: is the type of the connection
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
    def set_username(cls, username):
        """
        This method sets the user for the ssh connection

        :param username: is the user

        Example:
            - SSH_Connection.set_username('myUser')
        """

        COM.set_input_field('username', username)
