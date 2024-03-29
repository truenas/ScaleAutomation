from helper.global_config import shared_config
from platform import system
from subprocess import run, PIPE


class Local_Command_Line:
    """
    Attributes:
        status: This return True if the command succeeded otherwise it returns False.
        stdout: This return the standard output of the command.
        stderr: This return the standard error of the command.
    """
    def __init__(self, command: str, wsl: bool = True):
        """
        This method run the command line and gets status, stdout and stderr.

        :param command: is the command line text to run.
        :param wsl: is optional and if True, the command will be run in WSL. The default is True.

        Example:
            - Local_Command_Line('ls')
            - Local_Command_Line('ls', wsl=False)
        """
        wsl_cmd = 'wsl -- ' if wsl is True else ''
        command_start = wsl_cmd if system() == "Windows" else ''
        self.process = run(command_start + command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.status = False if self.process.returncode != 0 else True


class SSH_Command_Line:
    """
        Attributes:
            status: This return True if the ssh command succeeded otherwise it returns False.
            stdout: This return the standard output of the ssh command.
            stderr: This return the standard error of the ssh command.
        """
    def __init__(self, command: str, ip: str, username: str, password: str = None):
        """
        This method run the command line through SSH, and gets status, stdout and stderr.

        :param command: is the command to run with SSH.
        :param ip: is the IP of the targeted system to run the SSH command.
        :param username: is the username of the user of the targeted system.
        :param password: is optional and is the password of the user of the targeted system. If the password is not
        provided SSH will expect an SSH Key from the host to be setup on the targeted system.
        """
        ssh_option = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o VerifyHostKeyDNS=no -o LogLevel=quiet"
        sshpass = f'sshpass -p {password} ' if password else f'eval `ssh-agent` ; ssh-add {shared_config["KEYPATH"]} ; '
        print("@@@ COMMAND: " + f'{sshpass}ssh {ssh_option} {username}@{ip} "{command}"')
        self.process = Local_Command_Line(f'{sshpass}ssh {ssh_option} {username}@{ip} "{command}"')
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.status = self.process.status
        print("@@@ STDOUT: " + self.stdout)
        print("@@@ STDERR: " + self.stderr)
        print("@@@ STATUS: " + str(self.status))
