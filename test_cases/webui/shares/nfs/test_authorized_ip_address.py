import allure
import pytest

import xpaths
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
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
    def setup_test(self):
        """
        This method sets up the environment for the test.
        """
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        assert NFS_SSH.unmount_nfs_share('auth_ip') is True
        API_DELETE.delete_share('nfs', 'tank/auth_ip_test')
        API_DELETE.delete_dataset('tank/auth_ip_test', recursive=True, force=True)
        API_POST.start_service('nfs')
        API_POST.start_service('ssh')
        API_POST.create_dataset('tank/auth_ip_test', 'NFS')
        API_POST.create_share('nfs', '', '/mnt/tank/auth_ip_test')
        NAV.navigate_to_datasets()
        DAT.click_dataset_location('auth_ip_test')
        DAT.click_edit_permissions_button()
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('user'), 'value') is True
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('group'), 'value') is True
        PERM.set_other_access('Read | Write | Execute')
        COM.click_save_button_and_wait_for_progress_bar()
        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True
        assert COMSHARE.assert_share_path('nfs', '/mnt/tank/auth_ip_test') is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self):
        """
        This method deletes the share, dataset and unmounts the NFS share on the client.
        """
        yield
        API_DELETE.delete_share('nfs', 'tank/auth_ip_test')
        API_DELETE.delete_dataset('tank/auth_ip_test', recursive=True, force=True)
        assert NFS_SSH.unmount_nfs_share('auth_ip') is True

    @allure.tag("Authorized IP Address")
    @allure.story("NFS Share Authorized IP Address")
    def test_nfs_share_authorized_ip_address(self):
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
        # Verify share can mount
        assert COMSHARE.is_share_enabled('nfs', '/mnt/tank/auth_ip_test') is True
        assert NFS_SSH.mount_nfs_share('/mnt/tank/auth_ip_test', 'auth_ip') is True
        assert NFS_SSH.verify_share_mounted('auth_ip', 'drwxr-xrwx  2 root   root') is True
        assert NFS_SSH.verify_share_read_access('auth_ip') is True
        assert NFS_SSH.verify_share_write_access('auth_ip') is True
        assert NFS_SSH.verify_share_execute_access('auth_ip') is True
        assert NFS_SSH.verify_share_delete_access('/mnt/tank/auth_ip_test', 'auth_ip') is True
        assert NFS_SSH.unmount_nfs_share('auth_ip') is True
        # Edit the NFS share and set an invalid authorized ip address
        COMSHARE.click_edit_share('nfs', '/mnt/tank/auth_ip_test')
        NFS.set_host_and_ip(private_config['NFS_CLIENT_IP']+'1')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share cannot mount
        assert COMSHARE.is_share_enabled('nfs', '/mnt/tank/auth_ip_test') is True
        assert NFS_SSH.mount_nfs_share('/mnt/tank/auth_ip_test', 'auth_ip') is False
        assert NFS_SSH.verify_share_mounted('auth_ip', 'drwxr-xrwx  2 root   root') is False

