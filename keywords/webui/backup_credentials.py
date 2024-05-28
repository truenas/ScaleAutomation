from keywords.webui.common import Common


class Backup_Credentials:

    @classmethod
    def assert_cloud_credentials_card_visible(cls) -> bool:
        """
        This method returns True if the Cloud Credentials card is visible, otherwise it returns False.

        :return: True if the Cloud Credentials card is visible, otherwise it returns False.

        Example:
            - Backup_Credentials.assert_cloud_credentials_card_visible()
        """
        return Common.is_card_visible('Cloud Credentials')

    @classmethod
    def assert_ssh_connections_card_visible(cls) -> bool:
        """
        This method returns True if the SSH Connections card is visible, otherwise it returns False.

        :return: True if the SSH Connections card is visible, otherwise it returns False.

        Example:
            - Backup_Credentials.assert_ssh_connections_card_visible()
        """
        return Common.is_card_visible('SSH Connections')

    @classmethod
    def assert_ssh_keypairs_card_visible(cls) -> bool:
        """
        This method returns True if the SSH Keypairs card is visible, otherwise it returns False.

        :return: True if the SSH Keypairs card is visible, otherwise it returns False.

        Example:
            - Backup_Credentials.assert_ssh_keypairs_card_visible()
        """
        return Common.is_card_visible('SSH Keypairs')