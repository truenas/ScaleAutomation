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
class Test_Read_Only_Share:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        """
        This method sets up the environment for the test.
        """
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        assert NFS_SSH.unmount_nfs_share('read_only') is True
        API_DELETE.delete_share('nfs', 'tank/read_only_test')
        API_DELETE.delete_dataset('tank/read_only_test', recursive=True, force=True)
        API_POST.start_service('nfs')
        API_POST.start_service('ssh')
        API_POST.create_dataset('tank/read_only_test', 'NFS')
        API_POST.create_share('nfs', '', '/mnt/tank/read_only_test')
        NAV.navigate_to_datasets()
        DAT.click_dataset_location('read_only_test')
        DAT.click_edit_permissions_button()
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('user'), 'value') is True
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('group'), 'value') is True
        PERM.set_other_access('Read | Write | Execute')
        COM.click_save_button_and_wait_for_progress_bar()
        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True
        assert COMSHARE.assert_share_path('nfs', '/mnt/tank/read_only_test') is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self):
        """
        This method deletes the share, dataset and unmounts the NFS share on the client.
        """
        yield
        API_DELETE.delete_share('nfs', 'tank/read_only_test')
        API_DELETE.delete_dataset('tank/read_only_test', recursive=True, force=True)
        assert NFS_SSH.unmount_nfs_share('read_only') is True

    @allure.tag("Read Only")
    @allure.story("NFS Share Read Only")
    def test_read_only_share(self):
        """
        This test edits the NFS share with an authorized IP and verifies that the share can/cannot be mounted.
        """
        # Edit the NFS share and set it to read only
        assert COMSHARE.assert_share_path('nfs', '/mnt/tank/read_only_test') is True

        COMSHARE.click_edit_share('nfs', '/mnt/tank/read_only_test')
        COM.set_checkbox('enabled')
        COMSHARE.click_advanced_options()
        COM.set_checkbox('ro')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share can mount but only read access is granted
        assert COMSHARE.is_share_enabled('nfs', '/mnt/tank/read_only_test') is True
        assert NFS_SSH.mount_nfs_share('/mnt/tank/read_only_test', 'read_only') is True
        assert NFS_SSH.verify_share_mounted('read_only', 'drwxr-xrwx  2 root   root') is True
        assert NFS_SSH.verify_share_read_access('read_only') is True
        assert NFS_SSH.verify_share_write_access('read_only') is False
        assert NFS_SSH.verify_share_execute_access('read_only') is False
        assert NFS_SSH.verify_share_delete_access('/mnt/tank/read_only_test', 'read_only') is False
        assert NFS_SSH.unmount_nfs_share('read_only') is True
        # Edit the NFS share and unset read only
        COMSHARE.click_edit_share('nfs', '/mnt/tank/read_only_test')
        COMSHARE.click_advanced_options()
        COM.unset_checkbox('ro')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share can mount and now full access is granted
        assert COMSHARE.is_share_enabled('nfs', '/mnt/tank/read_only_test') is True
        assert NFS_SSH.mount_nfs_share('/mnt/tank/read_only_test', 'read_only') is True
        assert NFS_SSH.verify_share_mounted('read_only', 'drwxr-xrwx  2 root   root') is True
        assert NFS_SSH.verify_share_read_access('read_only') is True
        assert NFS_SSH.verify_share_write_access('read_only') is True
        assert NFS_SSH.verify_share_execute_access('read_only') is True
        assert NFS_SSH.verify_share_delete_access('/mnt/tank/read_only_test', 'read_only') is True

