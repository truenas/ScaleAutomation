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
from keywords.webui.system_services import System_Services as SERV


@allure.tag("NFS Shares")
@allure.epic("Shares")
@allure.feature("NFS")
class Test_Advanced_Configurations:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, nfs_advanced_config):
        """
        This method sets up the environment for the test.
        """
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config['mount_dir']) is True
        API_DELETE.delete_share('nfs', nfs_advanced_config["api_path"])
        API_DELETE.delete_dataset(nfs_advanced_config["api_path"], recursive=True, force=True)
        API_POST.start_service('nfs')
        API_POST.start_service('ssh')
        API_POST.create_dataset(nfs_advanced_config["api_path"], 'NFS')
        API_POST.create_share('nfs', '', nfs_advanced_config["share_page_path"])
        NAV.navigate_to_datasets()
        DAT.click_dataset_location(nfs_advanced_config["dataset_name"])
        DAT.click_edit_permissions_button()
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('user'), 'value') is True
        assert WebUI.wait_until_field_populates(xpaths.common_xpaths.input_field('group'), 'value') is True
        PERM.set_dataset_user(nfs_advanced_config["dataset_user"])
        PERM.set_dataset_group(nfs_advanced_config["dataset_group"])
        PERM.set_apply_user_checkbox()
        PERM.set_apply_group_checkbox()
        PERM.set_user_access(nfs_advanced_config["dataset_user_perms"])
        PERM.set_group_access(nfs_advanced_config["dataset_group_perms"])
        PERM.set_other_access(nfs_advanced_config["dataset_other_perms"])
        COM.click_save_button_and_wait_for_progress_bar()
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True
        assert COMSHARE.assert_share_path('nfs', nfs_advanced_config["share_page_path"]) is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, nfs_advanced_config):
        """
        This method deletes the share, dataset and unmounts the NFS share on the client.
        """
        yield
        API_DELETE.delete_share('nfs', nfs_advanced_config["api_path"])
        API_DELETE.delete_dataset(nfs_advanced_config["api_path"], recursive=True, force=True)
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True

    @allure.tag("Authorized IP Address")
    @allure.story("NFS Share Authorized IP Address")
    @pytest.mark.parametrize('nfs_advanced_config', get_data_list('shares/nfs_advanced_config')[:1])
    def test_nfs_share_authorized_ip_address(self, nfs_advanced_config):
        """
        This test edits the NFS share with an authorized IP and verifies that the share can/cannot be mounted.
        """
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
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
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
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is False

    @allure.tag("Read Only")
    @allure.story("NFS Share Read Only")
    @pytest.mark.parametrize('nfs_advanced_config', get_data_list('shares/nfs_advanced_config')[1:2])
    def test_read_only_share(self, nfs_advanced_config):
        """
        This test edits the NFS share with an authorized IP and verifies that the share can/cannot be mounted.
        """
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
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
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
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True

    @allure.tag("Authorized Network Address")
    @allure.story("NFS Share Authorized Network Address")
    @pytest.mark.parametrize('nfs_advanced_config', get_data_list('shares/nfs_advanced_config')[2:3])
    def test_nfs_share_authorized_network_address(self, nfs_advanced_config):
        """
        This test edits the NFS share with an authorized network address and verifies that the share can/cannot be mounted.
        """
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
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # Edit the NFS share and set an invalid network address
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        NFS.click_add_networks_button()
        NFS.set_network('123.44.5.66')
        NFS.set_network_mask('24')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify share cannot mount
        assert COMSHARE.is_share_enabled('nfs', nfs_advanced_config["share_page_path"]) is True
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is False

    @allure.tag("mapall user", "mapall group")
    @allure.story("NFS Share mapall user and mapall group")
    @pytest.mark.parametrize('nfs_advanced_config', get_data_list('shares/nfs_advanced_config')[3:4])
    def test_nfs_share_mapall_user_and_group(self, nfs_advanced_config):
        """
        This test edits the NFS share with a mapall user and group and verifies that the share can/cannot be mounted and
        access is appropriately granted.
        """
        # Edit the NFS share and set the mapall user
        assert COMSHARE.assert_share_path('nfs', nfs_advanced_config["share_page_path"]) is True
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COM.set_checkbox('enabled')
        COMSHARE.click_advanced_options()
        NFS.set_mapall_user(nfs_advanced_config["mapall_user"])
        COM.click_save_button_and_wait_for_right_panel()
        # Set NFS service to allow NFSv3 and NFSv4 protocols
        NAV.navigate_to_system_settings_services()
        SERV.click_edit_button_by_servicename('NFS')
        SERV.set_nfs_service_protocols('NFSv3, NFSv4')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify access is mapped
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # Edit the NFS share and set the mapall group
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True
        assert COMSHARE.assert_share_path('nfs', nfs_advanced_config["share_page_path"]) is True
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COMSHARE.click_advanced_options()
        NFS.set_mapall_group(nfs_advanced_config["mapall_group"])
        COM.click_save_button_and_wait_for_right_panel()
        # Verify access is mapped
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # unset mapall user and group
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COMSHARE.click_advanced_options()
        NFS.unset_mapall_user()
        NFS.unset_mapall_group()
        COM.click_save_button_and_wait_for_right_panel()
        # Verify access is not mapped
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_read_access(nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_write_access(nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.verify_share_execute_access(nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.verify_share_delete_access(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True

    @allure.tag("maproot user", "maproot group")
    @allure.story("NFS Share maproot user and maproot group")
    @pytest.mark.parametrize('nfs_advanced_config', get_data_list('shares/nfs_advanced_config')[4:5])
    def test_nfs_share_maproot_user_and_group(self, nfs_advanced_config):
        """
        This test edits the NFS share with a maproot user and group and verifies that the maproot is set be and
        access is appropriately granted.
        """
        assert COMSHARE.assert_share_path('nfs', nfs_advanced_config["share_page_path"]) is True
        # Set NFS service to allow NFSv3 and NFSv4 protocols
        NAV.navigate_to_system_settings_services()
        SERV.click_edit_button_by_servicename('NFS')
        SERV.set_nfs_service_protocols('NFSv3, NFSv4')
        COM.click_save_button_and_wait_for_right_panel()
        # Verify maproot is not set
        assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_maproot_access(nfs_advanced_config["mount_dir"]) is False
        # assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # Edit the NFS share and set the maproot user
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True
        assert COMSHARE.assert_share_path('nfs', nfs_advanced_config["share_page_path"]) is True
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COMSHARE.click_advanced_options()
        # WebUI.delay(5)
        NFS.set_maproot_user(nfs_advanced_config["maproot_user"])
        # WebUI.delay(5)
        COM.click_save_button_and_wait_for_right_panel()
        # Verify maproot user is set
        # assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        # assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_maproot_access(nfs_advanced_config["mount_dir"], nfs_advanced_config["maproot_user_permissions_code"]) is True
        # assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # Edit the NFS share and unset the maproot group
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COMSHARE.click_advanced_options()
        NFS.set_maproot_group(nfs_advanced_config["maproot_group"])
        COM.click_save_button_and_wait_for_right_panel()
        # Verify maproot user and group is set
        # assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        # assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_maproot_access(nfs_advanced_config["mount_dir"], nfs_advanced_config["maproot_both_permissions_code"]) is True
        # assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
        # Verify maproot user and group is not set
        COMSHARE.click_edit_share('nfs', nfs_advanced_config["share_page_path"])
        COMSHARE.click_advanced_options()
        NFS.unset_maproot_user()
        NFS.unset_maproot_group()
        COM.click_save_button_and_wait_for_right_panel()
        # assert NFS_SSH.mount_nfs_share(nfs_advanced_config["share_page_path"], nfs_advanced_config["mount_dir"]) is True
        # assert NFS_SSH.verify_share_mounted(nfs_advanced_config["mount_dir"], nfs_advanced_config["permissions_code"], nfs_advanced_config["dataset_ownership"]) is True
        assert NFS_SSH.verify_share_maproot_access(nfs_advanced_config["mount_dir"]) is False
        assert NFS_SSH.unmount_nfs_share(nfs_advanced_config["mount_dir"]) is True
