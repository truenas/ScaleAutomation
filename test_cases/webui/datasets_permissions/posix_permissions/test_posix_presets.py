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


@pytest.mark.parametrize('posix_acl_preset', get_data_list('dataset_permission/posix_acl_preset'), scope='class')
class Test_POSIX_Presets:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, posix_acl_preset) -> None:
        """
        This method creates the dataset and navigates to datasets before testing.
        """
        API_POST.start_service('ssh')
        API_DELETE.delete_dataset(posix_acl_preset['api_path'])
        API_POST.create_dataset(posix_acl_preset['api_path'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, posix_acl_preset):
        """
        This method clears any test users after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_dataset(posix_acl_preset['api_path'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_dashboard()

    def test_verify_posix_preset_permissions_via_UI(self, posix_acl_preset) -> None:
        """
        This test verifies the UI on the permissions card of the dataset that has been set with POSIX Preset Permissions.
        """
        DAT.click_dataset_location(posix_acl_preset['dataset'])
        DAT.click_edit_permissions_button()
        PERM.click_set_acl_button()
        COM.assert_dialog_visible('Select a preset ACL')
        COM.click_radio_button("use-preset-select-a-preset-acl")
        COM.select_option('preset-name', posix_acl_preset['preset_name'])
        COM.click_button('continue')
        COM.assert_page_header('Edit ACL')
        PERM.assert_owner_input('root')
        PERM.assert_owner_group_input('root')
        PERM.click_save_acl_button()
        assert PERM.assert_dataset_owner('root') is True
        assert PERM.assert_dataset_group('root') is True
        assert PERM.verify_dataset_permissions_type('POSIX Permissions') is True
        assert PERM.verify_dataset_owner_permissions_name(posix_acl_preset['user_obj']) is True
        assert PERM.verify_dataset_owner_permissions(posix_acl_preset['user_obj_perm'], 'root') is True
        assert PERM.verify_dataset_group_permissions_name(posix_acl_preset['group_obj']) is True
        assert PERM.verify_dataset_group_permissions(posix_acl_preset['group_obj_perm'], 'root') is True
        assert PERM.verify_dataset_other_permissions_name() is True
        assert PERM.verify_dataset_other_permissions(posix_acl_preset['other_perm']) is True
        assert PERM.verify_dataset_permissions_edit_button() is True
        assert PERM.verify_dataset_owner_default_permissions_name(posix_acl_preset['user_obj_default']) is True
        assert PERM.verify_dataset_owner_default_permissions(posix_acl_preset['user_obj_default_perm'], 'root') is True
        assert PERM.verify_dataset_group_default_permissions_name(posix_acl_preset['group_obj_default']) is True
        assert PERM.verify_dataset_group_default_permissions(posix_acl_preset['group_obj_default_perm'], 'root') is True
        assert PERM.verify_dataset_other_default_permissions_name() is True
        assert PERM.verify_dataset_other_default_permissions(posix_acl_preset['other_default_perm']) is True
        if posix_acl_preset['preset_name'].__contains__('posix-admin'):
            assert PERM.verify_dataset_mask_permissions_name() is True
            assert PERM.verify_dataset_mask_permissions(posix_acl_preset['mask_perm']) is True
            assert PERM.verify_dataset_mask_default_permissions_name() is True
            assert PERM.verify_dataset_mask_default_permissions(posix_acl_preset['mask_default_perm']) is True
            assert PERM.verify_dataset_builtin_admin_group_permissions_name() is True
            assert PERM.verify_dataset_builtin_admin_group_permissions(posix_acl_preset['gba_default_perm']) is True
            assert PERM.verify_dataset_builtin_admin_group_default_permissions_name() is True
            assert PERM.verify_dataset_builtin_admin_group_default_permissions(posix_acl_preset['gba_default_perm']) is True

    def test_verify_posix_preset_permissions_via_SSH(self, posix_acl_preset) -> None:
        """
        This test verifies that the dataset that has been set with POSIX Preset Permissions has the changes reflected via CLI.
        """
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        self.test_verify_posix_preset_permissions_via_UI(posix_acl_preset)
        # Verify the dataset is set with POSIX ACL
        assert PERM_SSH.assert_dataset_has_posix_acl(posix_acl_preset['dataset'], posix_acl_preset['ls_output']) is True
        # Verify the ACL presets on the dataset are properly created on the system
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['file_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['owner_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['group2_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['other_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['default_user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['default_group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['default_other_cli']) is True
        if posix_acl_preset['preset_name'].__contains__('posix-admin'):
            assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['mask_cli']) is True
            assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['default_mask_cli']) is True
            assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['group_builtin_administrators_cli']) is True
            assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_preset['full_path'], posix_acl_preset['default_group_builtin_administrators_cli']) is True

