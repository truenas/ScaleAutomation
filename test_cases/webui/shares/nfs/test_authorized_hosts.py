import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.nfs import NFS
from keywords.ssh.nfs import SSH_NFS as NFS_SSH


@allure.tag("NFS Shares")
@allure.epic("Shares")
@allure.feature("NFS")
@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
class Test_Authorized_Hosts:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, nfs_data):
        """
        This method sets up the environment for the test.
        """
        assert NFS_SSH.unmount_nfs_share('auth_host') is True
        API_DELETE.delete_share('nfs', nfs_data['api_path'])
        API_DELETE.delete_dataset(nfs_data['api_path'], recursive=True, force=True)
        API_POST.start_service('nfs')
        API_POST.create_dataset(nfs_data['api_path'], 'NFS')
        API_POST.create_share('nfs', '', nfs_data['share_page_path'])

        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, nfs_data):
        """
        This method deletes the share, dataset and unmounts the NFS share on the client.
        """
        yield
        API_DELETE.delete_share('nfs', nfs_data['api_path'])
        API_DELETE.delete_dataset(nfs_data['api_path'], recursive=True, force=True)
        assert NFS_SSH.unmount_nfs_share('auth_host') is True

    @allure.tag("Authorized Hosts")
    @allure.story("Edit NFS Share Advanced Options")
    def test_nfs_share_authorized_hosts(self, nfs_data):
        """
        This test edits the NFS share with an authorized host and verifies that the share can/cannot be mounted.
        """
        # Edit the NFS share and set a valid authorized host
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        COM.set_checkbox('enabled')
        NFS.click_add_hosts_button()
        NFS.set_host_and_ip(private_config['NFS_CLIENT_IP'])
        COM.click_save_button_and_wait_for_right_panel()
        # COMSHARE.handle_share_service_dialog('nfs')
        # Verify share can mount
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is True
        assert NFS_SSH.mount_nfs_share(nfs_data['share_page_path'], 'auth_host') is True
        assert NFS_SSH.unmount_nfs_share('auth_host') is True
        # Edit the NFS share and set an invalid authorized host
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        NFS.set_host_and_ip(private_config['NFS_CLIENT_IP']+'1')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share cannot mount
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is True
        assert NFS_SSH.mount_nfs_share(nfs_data['share_page_path'], 'auth_host') is False

