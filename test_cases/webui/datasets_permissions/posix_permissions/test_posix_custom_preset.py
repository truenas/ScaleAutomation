import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DAT
from keywords.webui.permissions import Permissions as PERM
from keywords.webui.navigation import Navigation as NAV
from keywords.ssh.permissions import Permissions_SSH as PERM_SSH


@pytest.mark.parametrize('posix_acl_custom', get_data_list('dataset_permission/posix_acl_custom'), scope='class')
class Test_POSIX_Custom_Preset:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, posix_acl_custom) -> None:
        """
        This method creates the dataset and navigates to datasets before testing.
        """
        API_POST.start_service('ssh')
        API_DELETE.delete_dataset(posix_acl_custom['api_path'])
        API_POST.create_dataset(posix_acl_custom['api_path'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, posix_acl_custom):
        """
        This method clears any test users after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_dataset(posix_acl_custom['api_path'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_dashboard()

    @allure.issue("NAS-128038", name="NAS-128038")
    def test_verify_posix_preset_permissions(self, posix_acl_custom) -> None:
        """
        This test verifies the ability to create and use a custom POSIX ACL preset.
        """
        DAT.click_dataset_location(posix_acl_custom['dataset'])
        DAT.click_edit_permissions_button()
        PERM.click_set_acl_button()
        COM.assert_dialog_visible('Select a preset ACL')
        COM.click_radio_button("use-preset-create-a-custom-acl")
        COM.click_button('continue')
        COM.assert_page_header('Edit ACL')
        PERM.set_dataset_owner(posix_acl_custom['new_owner'])
        PERM.set_dataset_owner_group(posix_acl_custom['new_owner_group'])
        PERM.set_apply_owner_checkbox()
        PERM.set_apply_group_checkbox()
        PERM.click_add_item_button()
        PERM.select_ace_who(posix_acl_custom['who_tag'])
        # Expected failure below: https://ixsystems.atlassian.net/browse/NAS-128038
        COM.set_checkbox('permissions-read')
        COM.click_button('save-as-preset')
        COM.assert_dialog_visible('Save As Preset')
        COM.set_input_field('preset-name', posix_acl_custom['custom_name'])
        COM.click_save_button()
        PERM.click_save_acl_button()
        DAT.click_edit_permissions_button()
        PERM.click_use_preset_button()
        COM.select_option('preset-name', posix_acl_custom['preset_name'])
        COM.click_button('continue')
        PERM.click_save_acl_button()
        assert PERM.assert_dataset_owner(posix_acl_custom['new_owner']) is True
        assert PERM.assert_dataset_group(posix_acl_custom['new_owner_group']) is True
        assert PERM.verify_dataset_permissions_type('POSIX Permissions') is True
        assert PERM.verify_dataset_owner_permissions_name(posix_acl_custom['user_obj']) is True
        assert PERM.verify_dataset_owner_permissions(posix_acl_custom['user_obj_perm'], posix_acl_custom['new_owner']) is True
        assert PERM.verify_dataset_group_permissions_name(posix_acl_custom['group_obj']) is True
        assert PERM.verify_dataset_group_permissions(posix_acl_custom['group_obj_perm'], posix_acl_custom['new_owner_group']) is True
        assert PERM.verify_dataset_other_permissions_name() is True
        assert PERM.verify_dataset_other_permissions(posix_acl_custom['other_perm']) is True
        assert PERM.verify_dataset_permissions_edit_button() is True
        assert PERM.verify_dataset_mask_permissions_name() is True
        assert PERM.verify_dataset_mask_permissions(posix_acl_custom['mask_perm']) is True
        assert PERM_SSH.assert_dataset_has_posix_acl(posix_acl_custom['dataset'], posix_acl_custom['ls_output']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_custom['full_path'], posix_acl_custom['file_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_custom['full_path'], posix_acl_custom['owner_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_custom['full_path'], posix_acl_custom['group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_custom['full_path'], posix_acl_custom['user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_custom['full_path'], posix_acl_custom['group2_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_custom['full_path'], posix_acl_custom['other_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_preset_permissions(posix_acl_custom['full_path'], posix_acl_custom['mask_cli']) is True
