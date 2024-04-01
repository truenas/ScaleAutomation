import pytest

from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DAT
from keywords.webui.permissions import Permissions as PERM
from keywords.webui.navigation import Navigation as NAV
from keywords.ssh.permissions import Permissions_SSH as PERM_SSH


class Test_NFSv4_UI_Create:
    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self) -> None:
        """
        This method sets up the environment for the test.
        """
        API_POST.start_service('ssh')
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_DELETE.delete_dataset('tank/ui_create_nfsv4')
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()

    @pytest.fixture(scope='class', autouse=True)
    def teardown_test(self):
        """
        This method clears any test users after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_dataset('tank/ui_create_nfsv4')
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_dashboard()

    def test_create_dataset_with_nfsv4_acl(self) -> None:
        """
        This test creates a new dataset and sets it with the NFSv4 ACL Type and verifies the permissions are set.
        """
        DAT.click_dataset_location('tank')
        DAT.click_add_dataset_button()
        DAT.set_dataset_name('ui_create_nfsv4')
        DAT.click_advanced_basic_options_button()
        DAT.set_dataset_acl_type('NFSv4')
        COM.assert_dialog_visible('ACL Types & ACL Modes')
        COM.click_dialog_close_button()
        COM.click_save_button()
        COM.assert_progress_bar_not_visible()
        NAV.navigate_to_dashboard()
        NAV.navigate_to_datasets()
        DAT.click_dataset_location('ui_create_nfsv4')
        DAT.click_edit_permissions_button()
        PERM.click_set_acl_button()
        COM.assert_dialog_visible('Select a preset ACL')
        COM.click_radio_button("use-preset-select-a-preset-acl")
        COM.select_option('preset-name', 'preset-name-nfs-4-open')
        COM.click_button('continue')
        COM.assert_page_header('Edit ACL')
        PERM.assert_owner_input('root')
        PERM.assert_owner_group_input('root')
        PERM.set_dataset_owner('admin')
        PERM.set_dataset_owner_group('admin')
        PERM.set_apply_owner_checkbox()
        PERM.set_apply_group_checkbox()
        PERM.click_save_acl_button()
        # Verify permissions via UI
        assert PERM.assert_dataset_owner('admin') is True
        assert PERM.assert_dataset_group('admin') is True
        assert PERM.verify_dataset_permissions_type('Click an item to view NFSv4 permissions') is True
        assert PERM.verify_dataset_owner_permissions_name('owner@ - admin') is True
        assert PERM.verify_dataset_owner_permissions('Allow | Full Control', 'admin') is True
        assert PERM.verify_dataset_group_permissions_name('group@ - admin') is True
        assert PERM.verify_dataset_group_permissions('Allow | Full Control', 'admin') is True
        assert PERM.verify_dataset_everyone_permissions_name('everyone@') is True
        assert PERM.verify_dataset_everyone_permissions('Allow | Modify', 'everyone@') is True
        assert PERM.verify_dataset_permissions_edit_button() is True
        # Verify permissions via SSH
        assert PERM_SSH.verify_getfacl_contains_permissions('/mnt/tank/ui_create_nfsv4', '# File: /mnt/tank/ui_create_nfsv4', 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions('/mnt/tank/ui_create_nfsv4', '# owner: 950', 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions('/mnt/tank/ui_create_nfsv4', '# group: 950', 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions('/mnt/tank/ui_create_nfsv4', '# trivial_acl: false', 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions('/mnt/tank/ui_create_nfsv4', '# ACL flags: none', 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions('/mnt/tank/ui_create_nfsv4', 'owner@:rwxpDdaARWcCos:fd-----:allow', 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions('/mnt/tank/ui_create_nfsv4', 'group@:rwxpDdaARWcCos:fd-----:allow', 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions('/mnt/tank/ui_create_nfsv4', 'everyone@:rwxpDdaARWc--s:fd-----:allow', 'NFSv4') is True

