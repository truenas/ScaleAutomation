from helper.cli import Interactive_Shell, pexpect
from helper.global_config import private_config


class CLI_SSH:

    @classmethod
    def assert_cli_command(cls, cli_command: str, output: str, user, password: str):
        """
        This method runs the cli command through ssh and asserts that the output is as expected

        :param cli_command: is the command line to run through ssh
        :param output: is the expected output of the command
        :param user: is the username of the user to ssh
        :param password: is the password of the user to ssh
        :return: the output of the command ran through ssh.

        Example:
            - CLI_SSH.assert_cli_command('system ls', 'reboot', 'user', 'password')
        """
        # send the cli command
        cli = cls.run_cli_command(cli_command, user, password)
        status = cli.expect(output)
        # assert that the output is as expected
        assert status == 0
        expected_output = str(cli.after)
        assert output in expected_output, expected_output
        # exit ssh session is not needed, but I keep it here for reference.
        # cli.sendline('exit')
        # Wait for the ssh session to close. Kept here for reference.
        # cli.expect(pexpect.EOF)
        cli.close()

        return status == 0

    @classmethod
    def run_cli_command(cls, cli_command: str, user, password: str) -> pexpect.spawn:
        """
        This method runs the cli command through ssh.

        :param cli_command: is the command line to run in cli.
        :param user: is the username of the user to ssh.
        :param password: is the password of the user to ssh.
        :return: the pexpect object of the SSH command.

        Example:
            - CLI_SSH.run_cli_command('system ls', 'user', 'password')
        """
        cli = Interactive_Shell.ssh(private_config['IP'], user, password)
        cli.sendline(f'cli -c "{cli_command}"')
        return cli
