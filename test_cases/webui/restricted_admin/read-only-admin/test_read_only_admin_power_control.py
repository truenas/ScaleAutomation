import allure
from helper.global_config import shared_config
from keywords.ssh.cli import CLI_SSH
from keywords.webui.common import Common


@allure.tag('Read Only Admin', 'Power Control', 'Permissions')
@allure.epic('permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_Power_Control:
    @allure.story("Read Only Admin Cannot Restart The System From The WebUI")
    def test_read_only_admin_cannot_restart_the_system_from_the_webui(self):
        """
        This test verifies the read-only admin cannot restart the system from the webui
        1. Click on the power menu
        2. Verify that the Restart option is restricted
        """
        Common.assert_power_menu_option_is_restricted('Restart')

    @allure.story("Read Only Admin Cannot Restart The System From The CLI")
    def test_read_only_admin_cannot_reboot_the_system_from_the_cli(self):
        """
        This test verifies the read-only admin cannot reboot the system from the cli
        1. SSH into the system as read-only admin
        2. Run cli command system reboot to reboot the system
        3. Verify that the cli Namespace reboot not found is returned
        """
        CLI_SSH.assert_cli_command(
            'system reboot',
            'Namespace reboot not found',
            shared_config['ROA_USER'],
            shared_config['ROA_PASSWORD']
        )

    @allure.story("Read Only Admin Cannot Shut Down The System From The WebUI")
    def test_read_only_admin_cannot_shut_down_the_system_from_the_webui(self):
        """
        This test verifies the read-only admin cannot shut down the system from the webui
        1. Click on the power menu
        2. Verify that the Shutdown option is restricted
        """
        Common.assert_power_menu_option_is_restricted('Shut Down')

    @allure.story("Read Only Admin Cannot Shut Down The System From The CLI")
    def test_read_only_admin_cannot_shut_down_the_system_from_the_cli(self):
        """
        This test verifies the read-only admin cannot shut down the system from the cli
        1. SSH into the system as read-only admin
        2. Run cli command system shutdown to shut down the system
        3. Verify that the cli Namespace shutdown not found is returned
        """
        CLI_SSH.assert_cli_command(
            'system shutdown',
            'Namespace shutdown not found',
            shared_config['ROA_USER'],
            shared_config['ROA_PASSWORD']
        )

    @allure.story("Read Only Admin Can Log Out Of The WebUI")
    def test_read_only_admin_can_log_out_of_the_webui(self):
        """
        This test verifies the read-only admin is able to log out of the webui.
        1. Click on the power menu
        2. Click on the logout option
        3. Verify that the login form is visible
        4. Log back in as the read-only admin
        """
        Common.logoff_truenas()
        Common.login_to_truenas(shared_config['ROA_USER'], shared_config['ROA_PASSWORD'])
