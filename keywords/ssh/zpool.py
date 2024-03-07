from helper.cli import SSH_Command_Line
from helper.global_config import private_config
from keywords.ssh.common import Common_SSH


class Zpool_SSH:

    @classmethod
    def get_pool_status(cls, pool_name: str) -> SSH_Command_Line:
        """
        This method returns the zpool status output of the given pool
        :param pool_name: The name of the pool.
        :return: The zpool status output of the given pool

        Example:
            - Zpool_SSH.get_pool_status('test_pool')
        """
        command = f'sudo zpool status {pool_name}'
        return Common_SSH.get_output_from_ssh(command, private_config['IP'], private_config['SSH_USERNAME'], private_config['SSH_PASSWORD'])

    @classmethod
    def verify_pool_status_exist(cls, pool_name: str) -> bool:
        """
        This method returns True or False whether the given pool exists in zpool status output.
        :param pool_name: The name of the pool.
        :return: True if the given pool exists in zpool status output otherwise it returns False.

        Example:
            - Zpool_SSH.verify_pool_status_exist('test_pool')

        Usage:
            - assert Zpool_SSH.verify_pool_status_exist('test_pool') is True
        """
        return cls.get_pool_status(pool_name).status

    @classmethod
    def verify_pool_status_contain_text(cls, pool_name, text: str) -> bool:
        """
        This method returns True or False whether the given text exists in zpool status output.
        :param pool_name: The name of the pool.
        :param text: The text to verify that it exists in zpool status output.
        :return: True if the given text exists in zpool status output otherwise it returns False.

        Example:
            - Zpool_SSH.verify_pool_status_contain_text('test_pool', 'test')

        Usage:
            - assert Zpool_SSH.verify_pool_status_contain_text('test_pool', 'test') is True
        """
        return text in cls.get_pool_status(pool_name).stdout
