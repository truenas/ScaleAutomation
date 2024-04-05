import allure
import pytest

import xpaths
from helper.data_config import get_data_list
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


def setup_test(data_binding: list):
    """
    This method sets up the environment for the test.
    """
    API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
    API_PUT.enable_user_ssh_password(private_config['USERNAME'])
    assert NFS_SSH.unmount_nfs_share(data_binding['mount_dir']) is True
    API_DELETE.delete_share('nfs', data_binding["api_path"])
    API_DELETE.delete_dataset(data_binding["api_path"], recursive=True, force=True)
    API_POST.start_service('nfs')
    API_POST.start_service('ssh')
    API_POST.create_dataset(data_binding["api_path"], 'NFS')
    API_POST.create_share('nfs', '', data_binding["share_page_path"])
    NAV.navigate_to_datasets()
    DAT.click_dataset_location(data_binding["dataset_name"])
    DAT.click_edit_permissions_button()
    assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('user'), 'value') is True
    assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('group'), 'value') is True
    PERM.set_other_access(data_binding["dataset_other_perms"])
    COM.click_save_button_and_wait_for_progress_bar()
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs') is True
    assert COMSHARE.assert_share_path('nfs', data_binding["share_page_path"]) is True


@allure.tag("NFS Shares")
@allure.epic("Shares")
@allure.feature("NFS")
class Test_Advanced_Configurations:
    @pytest.fixture(scope='class', autouse=True)
    def tear_down_test(self):
        """
        This method deletes the share, dataset and unmounts the NFS share on the client.
        """
        yield
        API_DELETE.delete_share('nfs', 'tank/auth_ip_test')
        API_DELETE.delete_share('nfs', 'tank/read_only_test')
        API_DELETE.delete_share('nfs', 'tank/auth_network_test')
        API_DELETE.delete_dataset('tank/auth_ip_test', recursive=True, force=True)
        API_DELETE.delete_dataset('tank/read_only_test', recursive=True, force=True)
        API_DELETE.delete_dataset('tank/auth_network_test', recursive=True, force=True)
        assert NFS_SSH.unmount_nfs_share('auth_ip') is True
        assert NFS_SSH.unmount_nfs_share('read_only') is True
        assert NFS_SSH.unmount_nfs_share('auth_network') is True

    @allure.tag("Authorized IP Address")
    @allure.story("NFS Share Authorized IP Address")
    @pytest.mark.parametrize('nfs_advanced_config', get_data_list('shares/nfs_advanced_config')[:1])
    def test_nfs_share_authorized_ip_address(self, nfs_advanced_config):
        """
        This test edits the NFS share with an authorized IP and verifies that the share can/cannot be mounted.
        """
        setup_test(nfs_advanced_config)
        # Edit the NFS share and set a valid authorized ip address
        assert COMSHARE.assert_share_path('nfs', nfs_advanced_config["share_page_path"]) is True
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COM.set_checkbox('enabled')
        NFS.click_add_hosts_button()
        NFS.set_host_and_ip(private_config['NFS_CLIENT_IP'])
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share can mount
        assert COMSHARE.is_share_enabled('nfs', nfs_advanced_config["share_page_path"]) is True
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # Edit the NFS share and set an invalid authorized ip address
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        NFS.set_host_and_ip(private_config['NFS_CLIENT_IP']+'1')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share cannot mount
        assert COMSHARE.is_share_enabled('nfs', nfs_advanced_config["share_page_path"]) is True
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"]) is False

    @allure.tag("Authorized Network Address")
    @allure.story("NFS Share Authorized Network Address")
    @pytest.mark.parametrize('nfs_advanced_config', get_data_list('shares/nfs_advanced_config')[2:3])
    def test_nfs_share_authorized_network_address(self, nfs_advanced_config):
        """
        This test edits the NFS share with an authorized network address and verifies that the share can/cannot be mounted.
        """
        setup_test(nfs_advanced_config)
        # Edit the NFS share and set a valid authorized network address
        assert COMSHARE.assert_share_path('nfs', nfs_advanced_config["share_page_path"]) is True
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COM.set_checkbox('enabled')
        NFS.click_add_networks_button()
        assert COM.is_save_button_disabled() is True
        NFS.click_remove_from_list_button()
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share can mount
        assert COMSHARE.is_share_enabled('nfs', nfs_advanced_config["share_page_path"]) is True
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"],
                                       nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"],
                                            nfs_advanced_config["permissions_code"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"],
                                                  nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # Edit the NFS share and set an invalid network address
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        NFS.click_add_networks_button()
        NFS.set_network('192.168.1.52')
        NFS.set_network_mask('24')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share cannot mount
        assert COMSHARE.is_share_enabled('nfs', nfs_advanced_config["share_page_path"]) is True
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"],
                                       nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"],
                                            nfs_advanced_config["permissions_code"]) is False

    @allure.tag("Read Only")
    @allure.story("NFS Share Read Only")
    @pytest.mark.parametrize('nfs_advanced_config', get_data_list('shares/nfs_advanced_config')[1:2])
    def test_read_only_share(self, nfs_advanced_config):
        """
        This test edits the NFS share with an authorized IP and verifies that the share can/cannot be mounted.
        """
        setup_test(nfs_advanced_config)
        # Edit the NFS share and set it to read only
        assert COMSHARE.assert_share_path('nfs', nfs_advanced_config["share_page_path"]) is True
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COM.set_checkbox('enabled')
        COMSHARE.click_advanced_options()
        COM.set_checkbox('ro')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share can mount but only read access is granted
        assert COMSHARE.is_share_enabled('nfs', nfs_advanced_config["share_page_path"]) is True
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # Edit the NFS share and unset read only
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COMSHARE.click_advanced_options()
        COM.unset_checkbox('ro')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share can mount and now full access is granted
        assert COMSHARE.is_share_enabled('nfs', nfs_advanced_config["share_page_path"]) is True
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True

    