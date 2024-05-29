import allure
import pytest

import xpaths
from helper.data_config import get_data_list
from helper.global_config import private_config, shared_config
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common as COM
from keywords.webui.backup_credentials import Backup_Credentials as BC
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


@allure.tag('Read Only Admin', 'Backup Credentials', "Users", 'Permissions')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
@pytest.mark.parametrize('cloud_cred', get_data_list('backup_credentials'), scope='class')
@pytest.mark.parametrize('rep', get_data_list('replication')[:1], scope='class')
class Test_Read_Only_Admin_Backup_Credential:

    @pytest.fixture(autouse=True, scope='class')
    def setup_cloud_sync(self, cloud_cred, rep, add_ssh_connection):
        """
        Summary: This setup fixture create the dataset and read-only admin for all test cases.
        """
        API_POST.create_cloud_sync_credential(cloud_cred['name'], cloud_cred['provider'], cloud_cred['access_key'], cloud_cred['secret_key'])
        COM.logoff_truenas()
        COM.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])
        COM.logoff_truenas()
        COM.login_to_truenas(shared_config['ROA_USER'], shared_config['ROA_PASSWORD'])
        NAV.navigate_to_backup_credentials()

    @pytest.fixture(autouse=True, scope='class')
    def teardown_cloud_sync(self, cloud_cred):
        """
        Summary: This teardown fixture delete the Cloud Sync Tasks and read-only admin for all test cases.
        """
        yield
        API_DELETE.delete_cloud_sync_credential(cloud_cred['name'])

    @pytest.fixture(scope='class')
    def add_ssh_connection(self, rep):
        """
        Summary: This fixture create the ssh connection for all test cases.
        """
        COM.logoff_truenas()
        COM.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])
        COM.logoff_truenas()
        COM.login_to_truenas(shared_config['ROA_USER'], shared_config['ROA_PASSWORD'])
        NAV.navigate_to_backup_credentials()

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See the Cloud Credentials")
    def test_read_only_admin_can_see_the_cloud_credentials(self, cloud_cred):
        """
        Summary: This test verifies the read-only admin is able to see Cloud Credentials.

        Test Steps:
        1. Verify the read-only admin is able to see Cloud Credentials
        """
        assert COM.is_card_visible('Cloud Credentials')
        assert COM.is_visible(xpaths.backup_credentials.cloud_credential_description(COM.convert_to_tag_format(cloud_cred['description']))) is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See the SSH Connections")
    def test_read_only_admin_can_see_the_ssh_connections(self, rep):
        """
        Summary: This test verifies the read-only admin is able to see SSH Connections.

        Test Steps:
        1. Verify the read-only admin is able to see SSH Connections
        """
        assert COM.is_card_visible('SSH Connections')
        assert COM.is_visible(xpaths.backup_credentials.ssh_connection_name(COM.convert_to_tag_format(rep['connection-name']))) is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See the SSH Keypairs")
    def test_read_only_admin_can_see_the_ssh_Keypairs(self, rep):
        """
        Summary: This test verifies the read-only admin is able to see SSH Keypairs.

        Test Steps:
        1. Verify the read-only admin is able to see SSH Keypairs
        """
        assert COM.is_card_visible('SSH Keypairs')
        assert COM.is_visible(xpaths.backup_credentials.ssh_keypairs_name(COM.convert_to_tag_format(rep['connection-name']))) is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Not Able to View the Configured Cloud Credentials Details")
    def test_read_only_admin_not_able_to_view_the_configured_cloud_credentials_details(self, cloud_cred):
        """
        Summary: This test verifies the read-only admin is not able to view the Configured Cloud Credentials details.

        Test Steps:
        1. Click Edit Cloud Credentials
        2. Verify Cloud Credentials detail fields are blank (access-key-id, secret-access-key.)
        3. Close right panel
        """
        BC.click_edit_cloud_credentials_by_name(cloud_cred['name'])
        assert COM.get_element_property(xpaths.common_xpaths.input_field('access-key-id'), 'innerText') == ""
        assert COM.get_element_property(xpaths.common_xpaths.input_field('secret-access-key'), 'innerText') == ""
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Read Only Admin Not Able to View the Configured SSH Connections Details")
    def test_read_only_admin_not_able_to_view_the_configured_ssh_connections_details(self, rep):
        """
        Summary: This test verifies the read-only admin is not able to view the Configured SSH Connections details.

        Test Steps:
        1. Click Edit SSH Connections
        2. Verify SSH Connections detail fields are blank (host, private-key, remote-host-key.)
        3. Close right panel
        """
        BC.click_edit_ssh_connection_by_name(rep['connection-name'])
        assert COM.get_element_property(xpaths.common_xpaths.input_field('host'), 'innerText') == ""
        assert COM.get_element_property(xpaths.common_xpaths.select_field('private-key'), 'innerText') == ""
        assert COM.get_element_property(xpaths.common_xpaths.textarea_field('remote-host-key'), 'innerText') == ""
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Read Only Admin Not Able to View the Configured SSH Keypairs Details")
    def test_read_only_admin_not_able_to_view_the_configured_ssh_keypairs_details(self, rep):
        """
        Summary: This test verifies the read-only admin is not able to view the Configured SSH Keypair details.

        Test Steps:
        1. Click Edit SSH Keypair
        2. Verify SSH Keypair detail fields are blank (private-key, public-key.)
        3. Close right panel
        """
        BC.click_edit_ssh_keypair_by_name(rep['connection-name'])
        assert COM.get_element_property(xpaths.common_xpaths.textarea_field('private-key'), 'innerText') == ""
        assert COM.get_element_property(xpaths.common_xpaths.textarea_field("public-key"), 'innerText') == ""
        COM.close_right_panel()
