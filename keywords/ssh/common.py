from helper.cli import Local_Command_Line, SSH_Command_Line
from helper.global_config import shared_config, private_config
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from os import path


class Common_SSH:

    @classmethod
    def add_smb_test_files(cls, user: str, dataset_path: str, ip: str):
        """

        :param user: is the user to be sending files to the smb share
        :param dataset_path: is the path if the smb share
        :param ip: the IP of the smb share box
        """
        Local_Command_Line('cd ~; touch putfile')
        SSH_Command_Line(f'cd /mnt/{dataset_path}/; touch getfile', ip, user, 'testing')
        SSH_Command_Line(f'cd /mnt/{dataset_path}/; touch deletefile', ip, user, 'testing')
        SSH_Command_Line(f'cd /mnt/{dataset_path}/; echo "touch execfile2.txt" >> /mnt/{dataset_path}/execfile.sh', ip, user, 'testing')

    @classmethod
    def create_ssh_key(cls):
        """This method create the SSH key if it does not exist"""
        # don't recreate the file if it already exists.
        if path.exists(shared_config['KEYPATH']) is False:
            Local_Command_Line(f"yes | ssh-keygen -t rsa -f {shared_config['KEYPATH']} -q -N ''")

    @classmethod
    def get_output_from_ssh_key(cls, command: str, ip: str, user: str) -> str:
        """
        This method verify that the command through succeed and return its output.

        :param command: is the command line to run through ssh
        :param ip: is the IP of the ssh target
        :param user: is the username of the user to ssh
        :return: the output of the command ran through ssh.
        """
        results = SSH_Command_Line(command, ip, user)
        assert results.status is True, f'{results.stdout}\n{results.stderr}'
        return results.stdout

    @classmethod
    def get_permission_response(cls, user: str, perm: str, value: str, cmd: str, state: str) -> bool:
        response = SSH_Command_Line(f'smbclient //{private_config['IP']}/SMBSHARE -U {user}%testing -c "{cmd}"', private_config['IP'], user, 'testing')
        print(response)
        if "NT_STATUS_ACCESS_DENIED" in response:
            print(f'FAIL {perm} RESPONSE: {response} STATE: {bool(state)}')
            if perm == 'DELETE' and state == 'false':
                return False
            return bool(state) is False
        command = 'ls -al /mnt/tank/SMBSHARE/'
        ip = private_config['IP']
        if perm == 'READ':
            command = 'ls -al ~'
            ip = private_config['SMB_ACL_IP']
        response = SSH_Command_Line(command, ip, user, 'testing')
        print(f'GET {perm} RESPONSE: {response}')
        print(f'GET {perm} SUCCESS RESPONSE: {response.stdout}')
        print(f'GET {perm} ERROR RESPONSE: {response.stderr}')
        if "NT_STATUS_ACCESS_DENIED" in response:
            return bool(state) is False
        print(f'VALUE: {value} in {response}')
        return (value in response) == bool(state)

    @classmethod
    def get_ssh_pub_key(cls) -> str:
        """
        This method return the SSK public key

        :return: the SSH public key
        """
        return open(path.expanduser(f'{shared_config["KEYPATH"]}.pub'), 'r').read().strip()

    @classmethod
    def set_host_ssh_key_and_enable_ssh_on_the_nas(cls, username: str):
        """
        This method set host SSH public key for the specified user and enable ssh service on the NAS

        :param username: the username to set the SSH public key on the NAS
        """
        cls.create_ssh_key()
        assert API_PUT.set_user_ssh_public_key(username, cls.get_ssh_pub_key()).status_code == 200
        assert API_POST.start_service('ssh').status_code == 200
        assert API_PUT.enable_service_at_boot('ssh').status_code == 200

    @classmethod
    def verify_read_permission(cls, user: str, read: str, file: str = 'getfile') -> bool:
        return cls.get_permission_response(user, 'READ', file, f'get {file}', read)

    @classmethod
    def verify_write_permission(cls, user: str, write: str, file: str = 'putfile') -> bool:
        return cls.get_permission_response(user, 'WRITE', file, f'put {file}', write)

    @classmethod
    def verify_exec_permission(cls, user: str, exec: str, file: str = 'execfile.sh') -> bool:
        return cls.get_permission_response(user, 'EXEC', file, f'open {file}', exec)

    @classmethod
    def verify_delete_permission(cls, user: str, delete: str, file: str = 'deletefile') -> bool:
        return not cls.get_permission_response(user, 'DELETE', file, f'rm {file}', delete)
