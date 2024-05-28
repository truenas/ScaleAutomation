from helper.cli import SSH_Command_Line
from helper.global_config import private_config


class SSH_SMB:

    @classmethod
    def add_smb_test_files(cls, user: str, dataset_path: str, ip: str) -> None:
        """
        This method adds the files used for testing smb permissions

        :param user: is the user to be sending files to the smb share
        :param dataset_path: is the path if the smb share
        :param ip: the IP of the smb share box
        """
        SSH_Command_Line('cd ~; touch putfile', private_config['SMB_ACL_IP'], user, 'testing')
        SSH_Command_Line(f'cd /mnt/{dataset_path}/; touch getfile', ip, user, 'testing')
        SSH_Command_Line(f'cd /mnt/{dataset_path}/; touch deletefile', ip, user, 'testing')
        SSH_Command_Line(f'cd /mnt/{dataset_path}/; echo "touch execfile2.txt" >> /mnt/{dataset_path}/execfile.sh', ip, user, 'testing')

    @classmethod
    def assert_directory_exists(cls, directory: str, share: str, user: str, password: str, ad: bool = False) -> bool:
        """
        This returns True if the given directory exists, otherwise it returns False.

        :param directory: is the name of the directory to validate
        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user
        :param ad: whether the user is an AD user

        :return: True if the given directory exists, otherwise it returns False.

        Example:
        - SMB.assert_directory_exists('myDir', 'myShare', 'user', 'password')
        - SMB.assert_directory_exists('myDir', 'myShare', 'user', 'password', True)
        """
        return cls.assert_target_command(directory, share, user, password, ad, "")

    @classmethod
    def assert_file_exists(cls, file: str, share: str, user: str, password: str, ad: bool = False) -> bool:
        """
        This returns True if the given file exists, otherwise it returns False.

        :param file: is the name of the file to validate
        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user
        :param ad: whether the user is an AD user

        :return: True if the given file exists, otherwise it returns False.

        Example:
        - SMB.assert_file_exists('myFile', 'myShare', 'user', 'password')
        - SMB.assert_file_exists('myFile', 'myShare', 'user', 'password', True)
        """
        return cls.assert_target_command(file, share, user, password, ad, "")

    @classmethod
    def assert_target_command(cls, target: str, share: str, user: str, password: str, ad: bool = False,
                              target_type: str = "") -> bool:
        """
        This method executes commands on given target.

        :param target: is the target to use in the commands [file / directory]
        :param share: is the name of the smb share to have acl permissions set
        :param ad: is the name of the smb share to have acl permissions set
        :param user: is the name of the smb share to have acl permissions set
        :param password: is the name of the smb share to have acl permissions set
        :param target_type: type of command to use against the target

        :return: True if the dataset is accessible with execute access, False otherwise.
        """
        set_target = False
        set_command = ""
        use_ad = ""
        if ad is True:
            use_ad = "-W AD03 "
        match target_type:
            case "delete_dir":
                set_target = True
                set_command = "rmdir"
            case "delete_file":
                set_target = True
                set_command = "rm"
            case "put_dir":
                set_target = True
                set_command = "mkdir"
            case "put_file":
                set_target = True
                set_command = "put"
                SSH_Command_Line(f'cd smbdirectory; touch {target}; chmod 777 {target}', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])

        if set_target:
            cls.smbclient_command(share, use_ad, user, password, f"'{set_command} {target}'")
        response = cls.smbclient_command(share, use_ad, user, password, "'ls'")
        return response.stdout.__contains__(target)

    @classmethod
    def assert_user_can_access(cls, share: str, user: str, password: str) -> bool:
        """
        This returns True if the share can be accessed by the given user, otherwise it returns False.

        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user

        :return: True if the share can be accessed by the given user, otherwise it returns False.

        Example:
        - SMB.assert_guest_access()
        """
        response = SSH_Command_Line(f'smbclient //{private_config["IP"]}/{share} -W AD03 -U {user}%{password} -c \'pwd\'', private_config['SMB_ACL_IP'], private_config['SMB_USERNAME'], private_config['SMB_PASSWORD'])
        return response.stdout.__contains__(share)

    @classmethod
    def assert_user_can_delete_directory(cls, directory: str, share: str, user: str, password: str, ad: bool = False) -> bool:
        """
        This returns True if the given directory is deleted, otherwise it returns False.

        :param directory: is the name of the directory to delete
        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user
        :param ad: whether the user is an AD user

        :return: True if the given directory is deleted, otherwise it returns False.

        Example:
        - SMB.assert_user_can_delete_directory('myDir', 'myShare', 'user', 'password')
        - SMB.assert_user_can_delete_directory('myDir', 'myShare', 'user', 'password', True)
        """
        return not cls.assert_target_command(directory, share, user, password, ad, "delete_dir")

    @classmethod
    def assert_user_can_delete_file(cls, file: str, share: str, user: str, password: str, ad: bool = False) -> bool:
        """
        This returns True if the given file is deleted, otherwise it returns False.

        :param file: is the name of the file to delete
        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user
        :param ad: whether the user is an AD user

        :return: True if the given file is deleted, otherwise it returns False.

        Example:
        - SMB.assert_user_can_delete_file('myFile', 'myShare', 'user', 'password')
        - SMB.assert_user_can_delete_file('myFile', 'myShare', 'user', 'password', True)
         """
        return not cls.assert_target_command(file, share, user, password, ad, "delete_file")

    @classmethod
    def assert_user_can_put_directory(cls, directory: str, share: str, user: str, password: str, ad: bool = False) -> bool:
        """
        This returns True if the given directory is put, otherwise it returns False.

        :param directory: is the name of the directory to put
        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user
        :param ad: whether the user is an AD user

        :return: True if the given directory is put, otherwise it returns False.

        Example:
        - SMB.assert_user_can_put_directory('myDir', 'myShare', 'user', 'password')
        - SMB.assert_user_can_put_directory('myDir', 'myShare', 'user', 'password', True)
        """
        return cls.assert_target_command(directory, share, user, password, ad, "put_dir")

    @classmethod
    def assert_user_can_put_file(cls, file: str, share: str, user: str, password: str, ad: bool = False) -> bool:
        """
        This returns True if the given file is put, otherwise it returns False.

        :param file: is the name of the file to put
        :param share: is the name of the share to access
        :param user: is the name of the system SMB user
        :param password: is the password of the SMB user
        :param ad: whether the user is an AD user

        :return: True if the given file is put, otherwise it returns False.

        Example:
        - SMB.assert_user_can_put_file('myFile', 'myShare', 'user', 'password')
        - SMB.assert_user_can_put_file('myFile', 'myShare', 'user', 'password', True)
        """
        return cls.assert_target_command(file, share, user, password, ad, "put_file")

    @classmethod
    def delete_smb_test_files(cls, user: str) -> None:
        """
        This method deletes the files used for testing smb permissions

        :param user: is the user to be sending files to the smb share
        """
        SSH_Command_Line('rm * | grep file', private_config['SMB_ACL_IP'], user, 'testing')

    @classmethod
    def smbclient_command(cls, share: str, use_ad: str, user: str, password: str, command: str) -> SSH_Command_Line:
        """
        This method sets the values for an SMB_ACL_ENTRY

        :param share: is the name of the smb share to have acl permissions set
        :param use_ad: is the name of the smb share to have acl permissions set
        :param user: is the name of the smb share to have acl permissions set
        :param password: is the name of the smb share to have acl permissions set
        :param command: is the name of the smb share to have acl permissions set

        :return: True if the given file is put, otherwise it returns False.

        Example:
        - SMB.assert_user_can_put_file('myFile', 'myShare', 'user', 'password')
        - SMB.assert_user_can_put_file('myFile', 'myShare', 'user', 'password', True)
        """
        return SSH_Command_Line(f'cd smbdirectory; smbclient //{private_config["IP"]}/{share} {use_ad}-U {user}%{password} -c {command}', private_config["SMB_ACL_IP"], private_config["SMB_USERNAME"], private_config["SMB_PASSWORD"])
