from helper.global_config import shared_config
from platform import system
from subprocess import run, PIPE
if system() == 'Windows':
    import wexpect as pexpect
else:
    import pexpect



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
        wsl_cmd = 'wsl -- ' if wsl else ''
        command_start = wsl_cmd if system() == "Windows" else ''
        # print(f'COMMAND: {command_start}"{command}"')
        self.process = run(f'{command_start}{command}', shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.status = self.process.returncode == 0
        assert self.status


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
        # print("@@@ COMMAND:", f'{sshpass}ssh {ssh_option} {username}@{ip} "{command}"')
        self.process = Local_Command_Line(f'{sshpass}ssh {ssh_option} {username}@{ip} "{command}"')
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.status = self.process.status
        # print("@@@ STDOUT: " + self.stdout)
        # print("@@@ STDERR: " + self.stderr)
        # print("@@@ STATUS: " + str(self.status))


class Interactive_Shell:
    """
    Interactive_Shell is used to run an interactive shell command with pexpect.
    It only supports bash and zsh shells.

    You can interact with the shell using the following commands:
        - after get the output after the command. Used after the expect use.
        - before get the output before the command. Used after the expect use.
        - close to exit the shell session.
        - expect to wait for a response.
        - readline output the current line of text.
        - sendline to send a text to the shell.
    There is more options in the pexpect docs: https://pexpect.readthedocs.io/en/stable/api/pexpect.html
    """
    @classmethod
    def ssh(cls, ip: str, username: str, password: str = None) -> pexpect.spawn:
        """
        This method run the command line through SSH and allows interacting with the shell.

        :param ip: is the IP of the targeted system to run the SSH command.
        :param username: is the username of the user of the targeted system.
        :param password: is optional and is the password of the user of the targeted system. If the password is not
                         provided SSH will expect an SSH Key from the host to be setup on the targeted system.
        :return: the pexpect object of the SSH command.

        Code Example::

            shell = Interactive_Shell.ssh('0.0.0.0', 'user', 'password')
            shell.sendline('ls /')
            status = shell.expect('usr')
            if status == 0:
                shell.close()

        """
        ssh_option = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o VerifyHostKeyDNS=no " \
                     "-o LogLevel=quiet"
        sshpass = f'sshpass -p {password} ' if password else f'eval `ssh-agent` ; ssh-add {shared_config["KEYPATH"]} ; '
        if system() == "Windows":
            child = pexpect.spawn(f'wsl -- {sshpass}ssh {ssh_option} {username}@{ip}')
        else:
            child = pexpect.spawn(f'{sshpass}ssh {ssh_option} {username}@{ip}', encoding='utf-8')
        # This output the console output when .expect is used. It is very useful for debugging.
        # child.logfile = sys.stdout
        child.expect(shared_config['HOSTNAME'])
        return child
