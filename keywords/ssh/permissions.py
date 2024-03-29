from helper.cli import SSH_Command_Line
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.ssh.common import Common_SSH as SSH


class Permissions_SSH:
    @classmethod
    def assert_dataset_execute_access(cls, pool: str, dataset: str, username: str, password: str) -> bool:
        """
        This method attempts to access the given dataset with the given username and preform execute actions.

        :param pool: The name of the pool the dataset is in.
        :param dataset: The name of the dataset to be accessed.
        :param username: The username used for authentication.
        :param password: The password used for authentication.
        :return: True if the dataset is accessible with execute access, False otherwise.
        """
        # leaving commented for when we need to test file execution permissions.
        # file = f"{username}exec_file.sh"
        # cr_dir = f"{username}exec_dir"
        # command = f'cd /mnt/{pool}/test ; chmod 777 . ; touch {file} ;  echo -n "mkdir /mnt/{pool}/{dataset}/{cr_dir}" | cat > {file} ; chmod 777 {file}'
        # SSH.get_output_from_ssh(command, private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        # command2 = f"cd /mnt/{pool}/test ; ./{file}"
        # SSH.get_output_from_ssh(command2, private_config['IP'], username, password)
        # command3 = f"cd /mnt/{pool} ; sudo ls -al {dataset}"
        # value = SSH.get_output_from_ssh(command3, private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        # return cr_dir in value.stdout.lower()
        command = f"cd /mnt/{pool}/{dataset}"
        value = SSH.get_output_from_ssh(command, private_config['IP'], username, password)
        if "permission denied" in value.stderr.lower():
            print("Permission denied while running command.")
            return False
        return True

    @classmethod
    def assert_dataset_has_posix_acl(cls, path: str, dataset: str, permissions: str) -> bool:
        """
        This method returns True if the given dataset has the given POSIX ACL, otherwise it returns False.

        :param path: The path to the dataset.
        :param dataset: The name of the dataset.
        :param permissions: The permissions to verify.
        :return: True if the given dataset has the given POSIX ACL, otherwise it returns False.

        Example:
            - Permissions.assert_dataset_has_posix_acl('test-dataset', 'rwxrwx---+')
        """
        value = SSH.get_output_from_ssh(f'ls -l {path} | grep {dataset}', private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        # i = 0
        # while value.stdout == '':
        #     print("stdout is empty. Waiting 2 seconds and trying again. stdout: "+value.stdout)
        #     WebUI.delay(2)
        #     value = SSH.get_output_from_ssh(f'ls -l {path} | grep {dataset}', private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        #     i += 1
        #     if i >= 10:
        #         break
        print('ls_output: '+permissions)
        print('stdout: ' + value.stdout.lower())
        if permissions in value.stdout.lower():
            return True
        return False

    @classmethod
    def assert_dataset_read_access(cls, pool: str, dataset: str, username: str, password: str) -> bool:
        """
        This method attempts to access the given dataset with the given username and preform read actions.

        :param pool: The name of the pool the dataset is in.
        :param dataset: The name of the dataset to be accessed.
        :param username: The username used for authentication.
        :param password: The password used for authentication.
        :return: True if the dataset is accessible with read access, False otherwise.
        """
        command = f"cd /mnt/{pool} ; ls {dataset}"
        value = SSH.get_output_from_ssh(command, private_config['IP'], username, password)
        if "permission denied" in value.stderr.lower():
            print("Permission denied while running command.")
            return False
        return True

    @classmethod
    def assert_dataset_write_access(cls, pool: str, dataset: str, username: str, password: str) -> bool:
        """
        This method attempts to access the given dataset with the given username and preform write actions.

        :param pool: The name of the pool the dataset is in.
        :param dataset: The name of the dataset to be accessed.
        :param username: The username used for authentication.
        :param password: The password used for authentication.
        :return: True if the dataset is accessible with write access, False otherwise.
        """
        file = f"{username}file.txt"
        command = f"cd /mnt/{pool} ; touch {dataset}/{file}"
        SSH.get_output_from_ssh(command, private_config['IP'], username, password)
        command2 = f"cd /mnt/{pool} ; sudo ls -al {dataset}"
        value = SSH.get_output_from_ssh(command2, private_config['IP'], private_config['USERNAME'],
                                        private_config['PASSWORD'])
        return file in value.stdout.lower()

    @classmethod
    def clean_dataset_contents(cls, pool: str, dataset: str) -> None:
        """
        This method removes the files from the given dataset. Due to possible lack of permissions, this method must delete
        the files by name instead of by * as this will not work even with sudo and sudo -s.

        :param pool: The name of the pool the dataset is in.
        :param dataset: The name of the dataset to be cleaned.

        Example:
            - Permissions.clean_dataset_contents('tank', 'test-dataset')
        """
        command = f"sudo rm -rf /mnt/{pool}/{dataset}/unix_test_ownerfile.txt"
        value = SSH.get_output_from_ssh(command, private_config['IP'], private_config['USERNAME'],
                                        private_config['PASSWORD'])
        command2 = f"sudo rm -rf /mnt/{pool}/{dataset}/unix_test_groupuserfile.txt"
        value2 = SSH.get_output_from_ssh(command2, private_config['IP'], private_config['USERNAME'],
                                         private_config['PASSWORD'])
        command3 = f"sudo rm -rf /mnt/{pool}/{dataset}/unix_test_otheruserfile.txt"
        value3 = SSH.get_output_from_ssh(command3, private_config['IP'], private_config['USERNAME'],
                                         private_config['PASSWORD'])
        command4 = f"cd /mnt/{pool} ; sudo ls -al {dataset}"
        SSH.get_output_from_ssh(command4, private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        assert value.status is True and value2.status is True and value3.status is True

    @classmethod
    def verify_getfacl_contains_preset_permissions(cls, dataset_path: str, permissions: str) -> bool:
        """
        This method returns True if the given dataset has the given permissions using getfacl, otherwise it returns False.

        :param dataset_path: The path of the dataset
        :param permissions: The permissions to verify.
        :return: True if the given dataset has the given permissions using getfacl, otherwise it returns False.

        Example:
            - Permissions.verify_getfacl_contains_preset_permissions('/mnt/tank/test-dataset', 'user::rwx')
        """
        value = SSH.get_output_from_ssh(f'getfacl {dataset_path}', private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        if permissions in value.stdout.lower():
            return True
        return False
