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


