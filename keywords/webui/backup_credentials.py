import xpaths
from keywords.webui.common import Common as COM


class Backup_Credentials:

    @classmethod
    def assert_cloud_credentials_card_visible(cls) -> bool:
        """
        This method returns True if the Cloud Credentials card is visible, otherwise it returns False.

        :return: True if the Cloud Credentials card is visible, otherwise it returns False.

        Example:
            - Backup_Credentials.assert_cloud_credentials_card_visible()
        """
        return COM.is_card_visible('Cloud Credentials')

    @classmethod
    def assert_ssh_connections_card_visible(cls) -> bool:
        """
        This method returns True if the SSH Connections card is visible, otherwise it returns False.

        :return: True if the SSH Connections card is visible, otherwise it returns False.

        Example:
            - Backup_Credentials.assert_ssh_connections_card_visible()
        """
        return COM.is_card_visible('SSH Connections')

    @classmethod
    def assert_ssh_keypairs_card_visible(cls) -> bool:
        """
        This method returns True if the SSH Keypairs card is visible, otherwise it returns False.

        :return: True if the SSH Keypairs card is visible, otherwise it returns False.

        Example:
            - Backup_Credentials.assert_ssh_keypairs_card_visible()
        """
        return COM.is_card_visible('SSH Keypairs')

    @classmethod
    def click_edit_cloud_credentials_by_name(cls, name: str) -> None:
        """
        This method clicks the edit button for the Cloud Credential by the given name

        :param name: the name of the Cloud Credential

        Example:
            - Backup_Credentials.click_edit_cloud_credentials_by_name('name')
        """
        COM.click_button(xpaths.backup_credentials.cloud_credential_edit_button(COM.convert_to_tag_format(name)))
        assert COM.assert_right_panel_header('Cloud Credentials') is True

    @classmethod
    def click_edit_ssh_connection_by_name(cls, name: str) -> None:
        """
        This method clicks the edit button for the SSH Connections by the given name

        :param name: the name of the SSH Connections

        Example:
            - Backup_Credentials.click_edit_ssh_connection_by_name('name')
        """
        COM.click_button(xpaths.backup_credentials.ssh_connection_edit_button(COM.convert_to_tag_format(name)))
        assert COM.assert_right_panel_header('Edit SSH Connection') is True

    @classmethod
    def click_edit_ssh_keypair_by_name(cls, name: str) -> None:
        """
        This method clicks the edit button for the SSH Keypair by the given name

        :param name: the name of the SSH Keypair

        Example:
            - Backup_Credentials.click_edit_ssh_keypair_by_name('name')
        """
        COM.click_button(xpaths.backup_credentials.ssh_keypairs_edit_button(COM.convert_to_tag_format(name)))
        assert COM.assert_right_panel_header('SSH Keypairs') is True
