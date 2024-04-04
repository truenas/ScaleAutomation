import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DAT
from keywords.webui.permissions import Permissions as PERM
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.nfs import NFS
from keywords.ssh.nfs import SSH_NFS as NFS_SSH


@allure.tag("NFS Shares")
@allure.epic("Shares")
@allure.feature("NFS")
class Test_Authorized_IP_Address:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, nfs_data):
        """
        This method sets up the environment for the test.
        """
        assert NFS_SSH.unmount_nfs_share('auth_ip') is True
        API_DELETE.delete_share('nfs', 'tank/auth_ip_test')
        API_DELETE.delete_dataset('tank/auth_ip_test', recursive=True, force=True)
        API_POST.start_service('nfs')
        API_POST.create_dataset('tank/auth_ip_test', 'NFS')
        API_POST.create_share('nfs', '', '/mnt/tank/auth_ip_test')
        NAV.navigate_to_datasets()
        DAT.click_dataset_location('ip_auth_test')
        DAT.click_edit_permissions_button()
        PERM.set_other_access('Read | Write | Execute')
        COM.click_save_button_and_wait_for_progress_bar()
        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True
        assert COMSHARE.assert_share_path('nfs', '/mnt/tank/auth_ip_test') is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, nfs_data):
        """
        This method deletes the share, dataset and unmounts the NFS share on the client.
        """
        yield
        API_DELETE.delete_share('nfs', 'tank/auth_ip_test')
        API_DELETE.delete_dataset('tank/auth_ip_test', recursive=True, force=True)
        assert NFS_SSH.unmount_nfs_share('auth_ip') is True

    @allure.tag("Authorized IP Address")
    @allure.story("NFS Share Authorized IP Address")
    def test_nfs_share_authorized_ip_address(self, nfs_data):
        """
        This test edits the NFS share with an authorized IP and verifies that the share can/cannot be mounted.
        """
        # Edit the NFS share and set a valid authorized ip address
        assert COMSHARE.assert_share_path('nfs', '/mnt/tank/auth_ip_test') is True
        COMSHARE.click_edit_share('nfs', '/mnt/tank/auth_ip_test')
        COM.set_checkbox('enabled')
        NFS.click_add_hosts_button()
        NFS.set_host_and_ip(private_config['NFS_CLIENT_IP'])
        COM.click_save_button_and_wait_for_right_panel()
        # COMSHARE.handle_share_service_dialog('nfs')
        # Verify share can mount
        assert COMSHARE.is_share_enabled('nfs', '/mnt/tank/auth_ip_test') is True
        assert NFS_SSH.mount_nfs_share('/mnt/tank/auth_ip_test', 'auth_ip') is True
        if NFS_SSH.verify_share_mounted('auth_ip', 'root', 'root', 'drwxr-xr-x') is True:
            assert NFS_SSH.verify_share_read_access('auth_ip') is True
            assert NFS_SSH.verify_share_write_access('auth_ip') is True
            assert NFS_SSH.verify_share_execute_access('auth_ip') is True
            assert NFS_SSH.verify_share_delete_access('auth_ip') is True
        assert NFS_SSH.unmount_nfs_share('auth_ip') is True
        # Edit the NFS share and set an invalid authorized ip address
        COMSHARE.click_edit_share('nfs', '/mnt/tank/auth_ip_test')
        NFS.set_host_and_ip(private_config['NFS_CLIENT_IP']+'1')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share cannot mount
        assert COMSHARE.is_share_enabled('nfs', '/mnt/tank/auth_ip_test') is True
        assert NFS_SSH.mount_nfs_share('/mnt/tank/auth_ip_test', 'auth_ip') is False
        if NFS_SSH.verify_share_mounted('auth_ip', 'root', 'root', 'drwxr-xr-x') is True:
            assert NFS_SSH.verify_share_read_access('auth_ip') is False
            assert NFS_SSH.verify_share_write_access('auth_ip') is False
            assert NFS_SSH.verify_share_execute_access('auth_ip') is False
            assert NFS_SSH.verify_share_delete_access('auth_ip') is False

