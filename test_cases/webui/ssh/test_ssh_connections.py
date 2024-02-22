import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common as COM
from keywords.webui.ssh_connection import SSH_Connection as SSH
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('ssh', get_data_list('ssh_connections')[4:5], scope='class')
@allure.tag("SSH_Connections")
@allure.epic("Credentials")
@allure.feature("Backup Credentials-SSH Connections")
class Test_SSH:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, ssh) -> None:
        """
        This method sets up each test to start with ssh connections and keypairs deleted
        """
        API_DELETE.delete_ssh_connection(ssh['connection_name'])
        API_DELETE.delete_ssh_keypairs(ssh['keypair_name'])
        NAV.navigate_to_backup_credentials()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, ssh) -> None:
        """
        This method clears any test ssh connections and keypairs after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_ssh_connection(ssh['connection_name'])
        API_DELETE.delete_ssh_keypairs(ssh['keypair_name'])

    @allure.tag("Create")
    @allure.story("Create SSH Connection")
    def test_create_ssh_connection(self, ssh) -> None:
        """
        This test verifies creating a new ssh connection
        """
        url = private_config["REP_DEST_IP"]
        if ssh['connection_name'].__contains__("self"):
            url = private_config["IP"]

        SSH.click_add_ssh_connection_button()

        SSH.set_ssh_connection_name(ssh['connection_name'])
        SSH.set_url(url)
        SSH.set_admin_credentials(private_config["SSH_USERNAME"], private_config["SSH_PASSWORD"])
        SSH.set_username(private_config["SSH_USERNAME"])
        SSH.set_passwordless_sudo_checkbox()
        SSH.click_generate_new_private_key()
        COM.click_save_button()

        assert SSH.is_ssh_connection_visible(ssh['connection_name']) is True

    @allure.tag("Delete")
    @allure.story("Delete SSH Connection")
    def test_delete_ssh_connection(self, ssh) -> None:
        """
        This test verifies deleting a new ssh connection
        """
        # add connection and key pair if they don't already exist
        if SSH.is_ssh_connection_visible(ssh['connection_name']) is False:
            assert SSH.assert_ssh_connection_exists(ssh['connection_name'])

        SSH.click_delete_ssh_connection_button(ssh['connection_name'])
        assert SSH.is_ssh_connection_visible(ssh['connection_name']) is False

    @allure.tag("Delete")
    @allure.story("Delete SSH Keypair")
    def test_delete_ssh_keypair(self, ssh) -> None:
        """
        This test verifies deleting a new ssh keypair
        """
        # add connection and key pair if they don't already exist
        if SSH.is_ssh_connection_visible(ssh['connection_name']) is False:
            assert SSH.assert_ssh_connection_exists(ssh['connection_name'])

        assert SSH.is_ssh_keypair_visible(ssh['keypair_name']) is True
        SSH.click_delete_ssh_keypair_button(ssh['keypair_name'])
        assert SSH.is_ssh_keypair_visible(ssh['keypair_name']) is False
