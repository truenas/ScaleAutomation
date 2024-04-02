import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DAT
from keywords.webui.permissions import Permissions as PERM
from keywords.webui.navigation import Navigation as NAV
from keywords.ssh.common import Common_SSH as COM_SSH
from keywords.ssh.permissions import Permissions_SSH as PERM_SSH


@pytest.mark.parametrize('nfs4_acl_preset', get_data_list('dataset_permission/nfs4_acl_preset'), scope='class')
class Test_NFSv4_Presets:
    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self, nfs4_acl_preset) -> None:
        """
        This method creates the dataset and sets it with the NFSv4 permissions preset.
        """
        API_POST.start_service('ssh')
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_DELETE.delete_dataset(nfs4_acl_preset['api_path'])
        API_POST.create_dataset(nfs4_acl_preset['api_path'], "SMB")
        API_POST.set_dataset_permissions_user_and_group(nfs4_acl_preset['api_path'], nfs4_acl_preset['owner_name'], nfs4_acl_preset['group_name'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()
        DAT.click_dataset_location(nfs4_acl_preset['dataset'])
        DAT.click_edit_permissions_button()
        COM.assert_page_header('Edit ACL')
        PERM.assert_owner_input('admin')
        PERM.assert_owner_group_input('admin')
        PERM.click_use_preset_button()
        COM.select_option('preset-name', nfs4_acl_preset['preset_name'])
        COM.click_button('continue')
        PERM.click_save_acl_button()

    @pytest.fixture(scope='class', autouse=True)
    def teardown_test(self, nfs4_acl_preset):
        """
        This method clears any test users after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_dataset(nfs4_acl_preset['api_path'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_dashboard()

    def test_verify_nfsv4_presets_via_UI(self, nfs4_acl_preset) -> None:
        """
        This test verifies the UI on the permissions card of the dataset that has been set with the NFSv4 Permissions preset.
        """
        assert PERM.assert_dataset_owner(nfs4_acl_preset['owner_name']) is True
        assert PERM.assert_dataset_group(nfs4_acl_preset['group_name']) is True
        assert PERM.verify_dataset_permissions_type('Click an item to view NFSv4 permissions') is True
        assert PERM.verify_dataset_owner_permissions_name(nfs4_acl_preset['owner_@']) is True
        assert PERM.verify_dataset_owner_permissions(nfs4_acl_preset['owner_@_perm'], nfs4_acl_preset['owner_name']) is True
        assert PERM.verify_dataset_group_permissions_name(nfs4_acl_preset['group_@']) is True
        assert PERM.verify_dataset_group_permissions(nfs4_acl_preset['group_@_perm'], nfs4_acl_preset['group_name']) is True
        assert PERM.verify_dataset_permissions_edit_button() is True
        if not nfs4_acl_preset['gba'].__contains__('null'):
            assert PERM.verify_dataset_builtin_admin_group_permissions_name(nfs4_acl_preset['gba']) is True
            assert PERM.verify_dataset_builtin_admin_group_permissions(nfs4_acl_preset['gba_perm'], nfs4_acl_preset['gba']) is True
        if not nfs4_acl_preset['everyone_@'].__contains__('null'):
            assert PERM.verify_dataset_everyone_permissions_name(nfs4_acl_preset['everyone_@'])
            assert PERM.verify_dataset_everyone_permissions(nfs4_acl_preset['everyone_@_perm'], nfs4_acl_preset['everyone_@']) is True

    def test_verify_nfsv4_presets_via_SSH(self, nfs4_acl_preset) -> None:
        """
        This test verifies that the dataset that has been set with the NFSv4 Permissions preset and has the changes reflected via SSH.
        """
        # Verify the dataset is set with NFSv4 ACL
        assert PERM_SSH.verify_getfacl_contains_permissions(nfs4_acl_preset['full_path'], nfs4_acl_preset['getfacl_file'], 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions(nfs4_acl_preset['full_path'], nfs4_acl_preset['getfacl_hash_owner'], 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions(nfs4_acl_preset['full_path'], nfs4_acl_preset['getfacl_hash_group'], 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions(nfs4_acl_preset['full_path'], nfs4_acl_preset['getfacl_acl_flags'], 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions(nfs4_acl_preset['full_path'], nfs4_acl_preset['getfacl_owner@'], 'NFSv4') is True
        assert PERM_SSH.verify_getfacl_contains_permissions(nfs4_acl_preset['full_path'], nfs4_acl_preset['getfacl_group@'], 'NFSv4') is True
        if not nfs4_acl_preset['everyone_@'].__contains__('null'):
            assert PERM_SSH.verify_getfacl_contains_permissions(nfs4_acl_preset['full_path'], nfs4_acl_preset['getfacl_everyone@'], 'NFSv4') is True
        if not nfs4_acl_preset['gba'].__contains__('null'):
            assert PERM_SSH.verify_getfacl_contains_permissions(nfs4_acl_preset['full_path'], nfs4_acl_preset['getfacl_gba'], 'NFSv4') is True
