import allure
import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.backup_credentials import Backup_Credentials
from keywords.webui.navigation import Navigation


class Test_Read_Only_Admin_Back_Credential:

    @pytest.fixture(autouse=True, scope='class')
    def setup_cloud_sync(self, cloud_sync):
        """
        Summary: This setup fixture create the dataset and read-only admin for all test cases.
        """
        API_POST.create_cloud_sync_credential(cloud_sync['name'], cloud_sync['provider'], cloud_sync['access_key'], cloud_sync['secret_key'])
        API_POST.create_cloud_sync_task(cloud_sync['name'], cloud_sync['description'])

        Navigation.navigate_to_backup_credentials()

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_cloud_sync(self, cloud_sync):
        """
        Summary: This teardown fixture delete the Cloud Sync Tasks and read-only admin for all test cases.
        """
        yield
        API_DELETE.delete_cloud_sync_task(cloud_sync['description'])
        API_DELETE.delete_cloud_sync_credential(cloud_sync['name'])

    @pytest.mark.parametrize('cloud_sync', get_data_list('backup_credentials'), scope='class')
    # A read-only or shares admin shall be able to view lists  of the cloud credentials configured on the system
    def test_read_only_admin_can_see_the_cloud_credentials(self, cloud_sync):
        assert Backup_Credentials.assert_cloud_credentials_card_visible() is True
        # assert

    # A read-only or shares admin shall be able to view lists of the SSH Connections configured on the system

    # A read-only or shares admin shall be able to view a list of the SSH key pairs configured on a system

    # A read-only or shares admin shall not be able to view details of credentials stored for cloud credentials

    # A read-only or shares admin shall not be able to view details of credentials stored for SSH connections

    # A read-only or shares admin shall not be able to view the values for SSH key pairs configured.
