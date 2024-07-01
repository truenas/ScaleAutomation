import allure
import pytest

import xpaths
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
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
        API_POST.create_non_admin_user('third_party', 'third_party', 'test')
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
        COM.select_option('shell', 'shell-' + ssh_shell_access['shell_xpath'])
        COM.click_save_button_and_wait_for_right_panel()

    @pytest.fixture(scope='class', autouse=True)
    def teardown_class(self) -> None:
        """
        This method tears down the class by deleting the created user
        """
        yield
        API_DELETE.delete_user('third_party')

    @allure.tag("Update")
    @allure.story("Edit User Shell Type and Verify Connection")
    def test_assert_shell_type(self, ssh_shell_access) -> None:
        """
        This test will assert the shell type of the user matches the set shell and the shell allows login if not nologin.
        """
        assert COM.is_visible(xpaths.local_users.user_shell_type(ssh_shell_access['username'], ssh_shell_access['full_shell_path'])) is True
        assert SSH.assert_shell_type(ssh_shell_access['shell_return'], ssh_shell_access['shell_type']) is True
        assert SSH.assert_shell_type(ssh_shell_access['etc_passwd'], ssh_shell_access['shell_type'], 'third_party', 'test') is True
