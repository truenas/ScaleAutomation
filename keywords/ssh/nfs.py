from helper.cli import SSH_Command_Line
from helper.global_config import private_config


class SSH_NFS:
    @classmethod
    def mount_nfs_share(cls, nas_path: str, mount_path: str) -> bool:
        """
        This method mounts the given NAS share to the given path and returns true if the mount is successful. Otherwise, it returns false.

        :param nas_path: the path of the NFS share on the NAS.
        :param mount_path: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if the mount is successful.
        """
        command = f'sudo mount -t nfs {private_config["IP"]}:{nas_path} ~/nfsshares/{mount_path}'
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        response = SSH_Command_Line('mount', private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        expected_response = f'{private_config["IP"]}:{nas_path}'
        return expected_response and mount_path in response.stdout

    @classmethod
    def unmount_nfs_share(cls, mount_path: str) -> bool:
        """
        This method unmounts the given path and returns true if the path is no-longer mounted. Otherwise, it returns false.

        :param mount_path: the path from 'nfsshares' to the directory to unmount.
        :return: true if the path is no-longer mounted.
        """
        command = f'sudo umount ~/nfsshares/{mount_path}'
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        response = SSH_Command_Line('mount', private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return mount_path not in response.stdout

    @classmethod
    def verify_share_delete_access(cls, mount_path: str) -> bool:
        """
        This method attempts to access the given dataset returns true if delete actions are successful.
        Otherwise, it returns false.

        :param mount_path: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if delete actions are successful.
        """
        file = f"test_delete_file.txt"
        command = f"cd ~/nfsshares ; sudo touch {mount_path}/{file}"
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        command2 = f"cd ~/nfsshares ; sudo ls -al {mount_path}"
        value = SSH_Command_Line(command2, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        assert file in value.stdout
        command3 = f"cd ~/nfsshares ; rm -rf {mount_path}/{file}"
        value2 = SSH_Command_Line(command3, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return file not in value2.stdout.lower()

    @classmethod
    def verify_share_execute_access(cls, mount_path: str) -> bool:
        """
        This method attempts to access the given dataset returns true if execute actions are successful.
        Otherwise, it returns false.

        :param mount_path: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if execute actions are successful.
        """
        file = f"test_exec_file.sh"
        cr_dir = f"test_exec_dir_internal"
        command = f'cd ~/nfsshares/test_execute_dir_external ; chmod 777 . ; touch {file} ;  echo -n "mkdir ~/nfsshares/{mount_path}/{cr_dir}" | cat > {file} ; chmod 777 {file}'
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        command2 = f"cd ~/nfsshares/test_execute_dir_external ; ./{file}"
        SSH_Command_Line(command2, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        command3 = f"cd ~/nfsshares ; sudo ls -al {mount_path}"
        value = SSH_Command_Line(command3, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return cr_dir in value.stdout.lower()

    @classmethod
    def verify_share_mounted(cls, mount_path: str, nas_owner: str, nas_group: str, share_perms: str) -> bool:
        """
        This method cd's to the mount path, and returns true if the directory is mounted. Otherwise, it returns false.

        :param mount_path: the path from 'nfsshares' to the directory the share is mounted to.
        :param nas_owner: the owner of the NAS share dataset.
        :param nas_group: the group of the NAS share dataset.
        :param share_perms: the expected permissions code of the NAS share dataset.
        :return: true if the directory is mounted.
        """
        command = f"cd ~/nfsshares/{mount_path} ; ls -al"
        value = SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        if "drwxr-xr-x" and f"{private_config['NFS_CLIENT_USERNAME']} {private_config['NFS_CLIENT_USERNAME']}" in value.stderr.lower():
            return False
        if share_perms and f"{nas_owner} {nas_group}" in value.stderr.lower():
            return True

    @classmethod
    def verify_share_read_access(cls, mount_path: str) -> bool:
        """
        This method attempts to access the given dataset returns true if read actions are successful.
        Otherwise, it returns false.

        :param mount_path: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if read actions are successful.
        """
        command = f"cd ~/nfsshares/{mount_path} ; ls -al"
        value = SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        if "permission denied" in value.stderr.lower():
            print("Permission denied while running command.")
            return False
        return True

    @classmethod
    def verify_share_write_access(cls, mount_path: str) -> bool:
        """
        This method attempts to access the given dataset with the given username and returns true if write actions are successful.
        Otherwise, it returns false.

        :param mount_path: the path from 'nfsshares' to the directory to mount the share to.
        :return: true if write actions are successful.
        """
        file = f"test_write_file.txt"
        command = f"cd ~/nfsshares ; touch {mount_path}/{file}"
        SSH_Command_Line(command, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        command2 = f"cd ~/nfsshares ; sudo ls -al {mount_path}"
        value = SSH_Command_Line(command2, private_config['NFS_CLIENT_IP'], private_config['NFS_CLIENT_USERNAME'], private_config['NFS_CLIENT_PASSWORD'])
        return file in value.stdout.lower()
