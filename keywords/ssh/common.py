from helper.cli import Local_Command_Line, SSH_Command_Line
from helper.global_config import shared_config, private_config
from keywords.api.post import API_POST
from keywords.api.put import API_PUT


class Common_SSH:

    @classmethod
    def add_test_file(cls, file: str, file_path: str, ip: str = private_config['IP'],
                      user: str = private_config['SSH_USERNAME'],
                      password: str = private_config['SSH_PASSWORD']) -> None:
        """
        This method adds the given file to the given ip

        :param file: is the name of the file to add
        :param file_path: is the path of the file
        :param ip: is the ip of the system
        :param user: is the user accessing the system
        :param password: is the password of user accessing the system

        Example:
            - Common.add_test_file('myFile.txt', 'tank/path')
            - Common.add_test_file('myFile.txt', 'tank/path', '10.0.0.1', 'user', 'password')
        """
        SSH_Command_Line(f'sudo touch /mnt/{file_path}/{file}', ip, user, password)
        assert cls.assert_file_exists(file, file_path, ip, user, password) is True

    @classmethod
    def assert_file_exists(cls, file: str, file_path: str, ip: str = private_config['IP'],
                           user: str = private_config['SSH_USERNAME'],
                           password: str = private_config['SSH_PASSWORD']) -> bool:
        """
        This method verifies the given file exists in the given file path

        :param file: is the name of the file to add
        :param file_path: is the path of the file
        :param ip: is the ip of the system
        :param user: is the user accessing the system
        :param password: is the password of user accessing the system
        :return: returns True if the expected file does not exist, otherwise False
        """
        response = SSH_Command_Line(f'ls -al /mnt/{file_path}/{file}', ip, user, password)
        return file in response.stdout

    @classmethod
    def create_ssh_key(cls):
        """This method create the SSH key if it does not exist"""
        # don't recreate the file if it already exists.
        if Local_Command_Line(f"test -f {shared_config['KEYPATH']}").status is False:
            Local_Command_Line(f"ssh-keygen -t rsa -f {shared_config['KEYPATH']} -q -N ''")

    @classmethod
    def get_checksum_of_file(cls, ip: str, filename: str, user: str = private_config["SSH_USERNAME"], password: str = private_config["SSH_PASSWORD"]) -> str:
        """
        This method returns the checksum of the given file

        :param ip: the IP of the box
        :param filename: is the filename to get the checksum
        :param user: is the user to ssh into box with
        :param password: is the password of user

        Example:
            - Common_SSH.get_checksum_of_file('10.0.0.1', 'myfile.txt')
        """

        response = SSH_Command_Line(f'sha256sum {filename}', ip, user, password)
        return response.stdout[0:response.stdout.index(" ")]

    @classmethod
    def get_file_checksum(cls, filename: str, user: str = private_config["SSH_USERNAME"], password: str = private_config["SSH_PASSWORD"]) -> str:
        """
        This method returns the checksum of the given file

        :param filename: is the filename to get the checksum
        :param user: is the user to ssh into box with
        :param password: is the password of user

        Example:
            - Common_SSH.get_file_checksum('myfile.txt')
        """
        return cls.get_checksum_of_file(private_config['IP'], filename, user, password)

    @classmethod
    def get_output_from_ssh(cls, command: str, ip: str, user: str, password: str) -> SSH_Command_Line:
        """
        This method verify that the command through succeed and return its output.

        :param command: is the command line to run through ssh
        :param ip: is the IP of the ssh target
        :param user: is the username of the user to ssh
        :param password: is the password of the user to ssh
        :return: the output of the command ran through ssh.
        """
        return SSH_Command_Line(command, ip, user, password)

    @classmethod
    def get_smb_share_permission_response(cls, user: str, perm: str, value: str, cmd: str, state: str) -> bool:
        """
        This method gets the response for accessing SMB share with given permissions

        :param user: is the user accessing the smb share
        :param perm: is the permissions the user has for the smb share
        :param value: value to find in the response to validate correct permissions
        :param cmd: command to execute and test smb permissions
        :param state: state of whether the command should be successful or not [True/False]
        :return: returns True if the expected state after executing smb command, otherwise False
        """
        response = SSH_Command_Line(f'smbclient //{private_config["IP"]}/SMBSHARE -U {user}%testing -c \'{cmd}\'', private_config['SMB_ACL_IP'], user, 'testing')
        if "NT_STATUS_ACCESS_DENIED" in response.stdout:
            print(f'FAIL {perm} RESPONSE: {response.status} STATE: {bool(state)}')
            if perm == 'DELETE' and state == 'False':
                return False
            return bool(state) is False
        command = 'ls -al /mnt/tank/SMBSHARE/'
        ip = private_config['IP']
        if perm == 'READ':
            command = 'ls -al ~'
            ip = private_config['SMB_ACL_IP']
        response = SSH_Command_Line(command, ip, user, 'testing')
        # print(f'{perm} RESPONSE: {response.status}')
        # print(f'{perm} SUCCESS RESPONSE: {response.stdout}')
        # print(f'{perm} ERROR RESPONSE: {response.stderr}')
        if "NT_STATUS_ACCESS_DENIED" in response.stdout:
            return bool(state) is False
        return (value in response.stdout) == bool(state)

    @classmethod
    def get_remote_file_checksum(cls, filename: str, user: str = private_config["SSH_USERNAME"], password: str = private_config["SSH_PASSWORD"]) -> str:
        """
        This method returns the checksum of the given file

        :param filename: is the filename to get the checksum
        :param user: is the user to ssh into box with
        :param password: is the password of user

        Example:
            - Common_SSH.get_remote_file_checksum('myfile.txt')
        """
        return cls.get_checksum_of_file(private_config['REP_DEST_IP'], filename, user, password)

    @classmethod
    def get_ssh_pub_key(cls) -> str:
        """
        This method return the SSK public key

        :return: the SSH public key
        """
        return Local_Command_Line(f"cat {shared_config['KEYPATH']}.pub").stdout.strip()

    @classmethod
    def list_directory(cls, full_path: str, ip: str = private_config['IP'],
                       user: str = private_config['SSH_USERNAME'],
                       password: str = private_config['PASSWORD']) -> str:
        """
        This method lists the given directory of the given ip

        :param full_path: is the full directory path
        :param ip: the IP of the box
        :param user: is the user to be listing the directory
        :param password: is the password of the user

        Example:
            - Common_SSH.list_directory('/mnt/tank/dir', '10.0.0.1', 'user', 'password')
        """
        return SSH_Command_Line(f'ls -al {full_path}', ip, user, password).stdout

    @classmethod
    def remove_all_test_files(cls, file_path: str, ip: str = private_config['IP'],
                              user: str = private_config['SSH_USERNAME'],
                              password: str = private_config['SSH_PASSWORD']) -> None:
        """
        This method removes all files from the given file path

        :param file_path: is the path of the file
        :param ip: is the ip of the system
        :param user: is the user accessing the system
        :param password: is the password of user accessing the system

        Example:
            - Common.remove_all_test_files('tank/path')
            - Common.remove_all_test_files('tank/path', '10.0.0.1', 'user', 'password')
        """
        SSH_Command_Line(f'sudo rm -rf /mnt/{file_path}/', ip, user, password)

    @classmethod
    def set_host_ssh_key_and_enable_ssh_on_the_nas(cls, username: str):
        """
        This method set host SSH public key for the specified user and enable ssh service on the NAS

        :param username: the username to set the SSH public key on the NAS
        """
        cls.create_ssh_key()

        assert Local_Command_Line(f"test -f {shared_config['KEYPATH']}.pub").status
        assert API_PUT.set_user_ssh_public_key(username, cls.get_ssh_pub_key()).status_code == 200
        assert API_POST.start_service('ssh').status_code == 200
        assert API_PUT.enable_service_at_boot('ssh').status_code == 200

    @classmethod
    def verify_smb_share_read_permission(cls, user: str, read: str, file: str = 'getfile') -> bool:
        """
        This method verifies the Read permissions of connecting to a smb share

        :param user: user to execute smb command
        :param read: value of whether Read command should be successful
        :param file: name of the file to execute the smb command on
        :return: returns True if the expected Read value was returned, otherwise False
        """
        return cls.get_smb_share_permission_response(user, 'READ', file, f'get {file}', read)

    @classmethod
    def verify_smb_share_write_permission(cls, user: str, write: str, file: str = 'putfile') -> bool:
        """
        This method verifies the Write permissions of connecting to a smb share

        :param user: user to execute smb command
        :param write: value of whether Write command should be successful
        :param file: name of the file to execute the smb command on
        :return: returns True if the expected Write value was returned, otherwise False
        """
        return cls.get_smb_share_permission_response(user, 'WRITE', file, f'put {file}', write)

    @classmethod
    def verify_smb_share_exec_permission(cls, user: str, execute: str, file: str = 'execfile.sh') -> bool:
        """
        This method verifies the Execute permissions of connecting to a smb share

        :param user: user to execute smb command
        :param execute: value of whether Exec command should be successful
        :param file: name of the file to execute the smb command on
        :return: returns True if the expected Exec value was returned, otherwise False
        """
        return cls.get_smb_share_permission_response(user, 'EXEC', file, f'open {file}', execute)

    @classmethod
    def verify_smb_share_delete_permission(cls, user: str, delete: str, file: str = 'deletefile') -> bool:
        """
        This method verifies the Delete permissions of connecting to a smb share

        :param user: user to execute smb command
        :param delete: value of whether delete command should be successful
        :param file: name of the file to execute the smb command on
        :return: returns True if the expected Delete value was returned, otherwise False
        """
        return not cls.get_smb_share_permission_response(user, 'DELETE', file, f'rm {file}', delete)
