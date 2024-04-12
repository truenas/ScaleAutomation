from helper.cli import SSH_Command_Line
from helper.global_config import private_config


class SSH_NFS:
    @classmethod
    def clear_share_contents(cls, mount_dir: str) -> bool:
        """
        This method clears the contents of the given share and returns true if the share is empty. Otherwise, it returns false.

        :param mount_dir: the path to the mounted directory.
        :return: true if the share is empty.
        """
        command = f"sudo rm -rf {mount_dir}/**"
        SSH_Command_Line(command, private_config['IP'], private_config['USERNAME'],
                         private_config['PASSWORD'])
        command2 = f"sudo ls {mount_dir}"
        value = SSH_Command_Line(command2, private_config['IP'], private_config['USERNAME'],
                                 private_config['PASSWORD'])
        return value.stdout is ""

    @classmethod
    def mount_nfs_share(cls, nas_path: str, mount_dir: str) -> bool:
        """
        This method mounts the given NAS share to the given path and returns true if the mount is successful. Otherwise, it returns false.

        :param nas_path: the path of the NFS share on the NAS.
        :param mount_dir: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if the mount is successful.
        """
        command = f'sudo mount -t nfs {private_config["IP"]}:{nas_path} ~/nfsshares/{mount_dir}'
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        response = SSH_Command_Line('mount', private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        expected_response = f'{private_config["IP"]}:{nas_path}'
        return expected_response and mount_dir in response.stdout

    @classmethod
    def unmount_nfs_share(cls, mount_dir: str) -> bool:
        """
        This method unmounts the given path and returns true if the path is no-longer mounted. Otherwise, it returns false.

        :param mount_dir: the path from 'nfsshares' to the directory to unmount.
        :return: true if the path is no-longer mounted.
        """
        command = f'sudo umount -f ~/nfsshares/{mount_dir}'
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        response = SSH_Command_Line('mount', private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return mount_dir not in response.stdout

    @classmethod
    def verify_share_delete_access(cls, nas_path: str, mount_dir: str) -> bool:
        """
        This method attempts to access the given dataset returns true if delete actions are successful.
        Otherwise, it returns false.

        :param nas_path: the path of the NFS share on the NAS.
        :param mount_dir: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if delete actions are successful.
        """
        file = cls.put_file_in_share(nas_path)
        command = f"cd ~/nfsshares ; rm -rf {mount_dir}/{file}"
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        value = SSH_Command_Line(f'sudo ls -al ~/nfsshares/{mount_dir}', private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return file not in value.stdout.lower()

    @classmethod
    def verify_share_execute_access(cls, mount_dir: str) -> bool:
        """
        This method attempts to access the given dataset returns true if execute actions are successful.
        Otherwise, it returns false.

        :param mount_dir: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if execute actions are successful.
        """
        file = f"test_exec_file.sh"
        cr_dir = f"test_exec_dir_internal"
        command = f'cd ~/nfsshares/test_execute_dir_external ; chmod 777 . ; touch {file} ;  echo -n "mkdir ~/nfsshares/{mount_dir}/{cr_dir}" | cat > {file} ; chmod 777 {file}'
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        command2 = f"cd ~/nfsshares/test_execute_dir_external ; ./{file}"
        SSH_Command_Line(command2, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        command3 = f"cd ~/nfsshares ; sudo ls -al {mount_dir}"
        value = SSH_Command_Line(command3, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        SSH_Command_Line(f"cd ~/nfsshares ; rm -rf {mount_dir}/{cr_dir}", private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return cr_dir in value.stdout.lower()

    @classmethod
    def verify_share_maproot_access(cls, mount_dir: str, permissions_code: str = "") -> bool:
        """
        This method attempts to access the share with maproot access and returns true if actions as the set maproot are successful. Otherwise, it returns false.

        :param permissions_code: the expected permissions code of the created directory.
        :param mount_dir: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if actions as the set maproot are successful
        """
        directory = f"test_maproot_dir"
        command = f"cd ~/nfsshares/{mount_dir} ; sudo mkdir {directory}"
        value = SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'],
                                 private_config['NFS_CLIENT_PASSWORD'])
        if "permission denied" in value.stderr.lower():
            print("Permission denied while running command.")
            return False
        command2 = f"sudo ls -al ~/nfsshares/{mount_dir}"
        value2 = SSH_Command_Line(command2, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'],
                                  private_config['NFS_CLIENT_PASSWORD'])
        SSH_Command_Line(f"cd ~/nfsshares ; sudo rm -rf {mount_dir}/{directory}", private_config['NFS_CLIENT_IP'],
                         private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return permissions_code in value2.stdout

    @classmethod
    def verify_share_mounted(cls, mount_dir: str, share_perms: str, ownership: str) -> bool:
        """
        This method cd's to the mount path, and returns true if the directory is mounted. Otherwise, it returns false.

        :param mount_dir: the path from 'nfsshares' to the directory the share is mounted to.
        :param share_perms: the expected permissions code of the NAS share dataset.
        :param ownership: the expected ownership of the NAS share dataset.
        :return: true if the directory ownership and permissions have changed to the share permissions.
        """
        command = f"sudo ls -al ~/nfsshares/{mount_dir}"
        value = SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return share_perms and ownership in value.stdout.lower()

    @classmethod
    def verify_share_read_access(cls, mount_dir: str) -> bool:
        """
        This method attempts to access the given dataset returns true if read actions are successful.
        Otherwise, it returns false.

        :param mount_dir: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if read actions are successful.
        """
        command = f"cd ~/nfsshares ; ls {mount_dir}"
        value = SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        if "permission denied" in value.stderr.lower():
            print("Permission denied while running command.")
            return False
        return True

    @classmethod
    def verify_share_write_access(cls, mount_dir: str) -> bool:
        """
        This method attempts to access the given dataset with the given username and returns true if write actions are successful.
        Otherwise, it returns false.

        :param mount_dir: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if write actions are successful.
        """
        file = f"test_write_file.txt"
        command = f"cd ~/nfsshares ; touch {mount_dir}/{file}"
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        command2 = f"cd ~/nfsshares ; sudo ls -al {mount_dir}"
        value = SSH_Command_Line(command2, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        SSH_Command_Line(f"cd ~/nfsshares ; rm -rf {mount_dir}/{file}", private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return file in value.stdout.lower()

    @classmethod
    def put_file_in_share(cls, share_path: str, file: str = "test_file.txt") -> str:
        """
        This method creates a file in the given dataset and returns the name of the file created.

        :param share_path: the path to the dataset the share is attached to.
        :param file: the name of the file to create. Defaults to test_file.txt.
        :return: the name of the file created.
        """
        command = f"sudo touch {share_path}/{file}"
        SSH_Command_Line(command, private_config['IP'], private_config['USERNAME'],
                         private_config['PASSWORD'])
        command2 = f"sudo ls -al {share_path}"
        value = SSH_Command_Line(command2, private_config['IP'], private_config['USERNAME'],
                                 private_config['PASSWORD'])
        assert file in value.stdout.lower()
        return file


