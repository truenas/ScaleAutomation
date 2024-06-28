import allure
import pytest

from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.ssh_connection import SSH_Connection as SSH
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.local_users import Local_Users as LU


@pytest.mark.parametrize('ssh_shell_access', get_data_list('ssh_shell_access'), scope='class')
@allure.tag("SSH_Connections")
@allure.epic("Credentials")
@allure.feature("Backup Credentials-SSH Connections")
class Test_SSH_Shell_Access:

    @pytest.fixture(scope='class', autouse=True)
    def setup_class(self) -> None:
        """
        This method sets up the class by starting the SSH service and navigating to local users
        """
        API_POST.start_service('ssh')
        NAV.navigate_to_local_users()

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, ssh_shell_access) -> None:
        """
        This method sets up each test to start by editing the shell type of the user
        """
        assert LU.is_user_visible(ssh_shell_access['username']) is True
        LU.expand_user(ssh_shell_access['username'])
        LU.click_user_edit_button()
        COM.set_checkbox('ssh-password-enabled')
        COM.select_option('shell', 'shell-' + ssh_shell_access['shell_type'])
        COM.click_save_button_and_wait_for_right_panel()

    @allure.tag("Create")
    @allure.story("Create SSH Connection")
    def test_assert_shell_type(self, ssh_shell_access) -> None:
        """
        This test will assert the shell type of the user matches the set shell
        """

        assert SSH.assert_shell_type(ssh_shell_access['shell_return'], ssh_shell_access['shell_type']) is True

