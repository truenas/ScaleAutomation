import allure
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
from keywords.ssh.permissions import Permissions_SSH as PERM_SSH
from keywords.ssh.common import Common_SSH as COM_SSH


@allure.tag("Datasets", "Dataset Permissions", "POSIX")
@allure.epic("Datasets")
@allure.feature("Dataset Permissions")
@pytest.mark.parametrize('posix_acl_recursive_permissions', get_data_list('dataset_permission/posix_acl_recursive_permissions'), scope='class')
class Test_POSIX_Recursive_Permissions:
    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self, posix_acl_recursive_permissions):
        """
        This method creates the dataset and navigates to datasets before testing.
        """
        API_POST.start_service('ssh')
        API_DELETE.delete_dataset(posix_acl_recursive_permissions['grandchild_api_path'])
        API_DELETE.delete_dataset(posix_acl_recursive_permissions['child_api_path'])
        API_DELETE.delete_dataset(posix_acl_recursive_permissions['api_path'])
        API_POST.create_dataset(posix_acl_recursive_permissions['api_path'])
        API_POST.create_dataset(posix_acl_recursive_permissions['child_api_path'])
        API_POST.create_dataset(posix_acl_recursive_permissions['grandchild_api_path'])
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        COM_SSH.get_output_from_ssh(f'sudo touch {posix_acl_recursive_permissions["full_path"]}/test_file.txt', private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        COM_SSH.get_output_from_ssh(f'sudo touch {posix_acl_recursive_permissions["child_full_path"]}/test_file.txt',
                                    private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        COM_SSH.get_output_from_ssh(f'sudo touch {posix_acl_recursive_permissions["grandchild_full_path"]}/test_file.txt',
                                    private_config['IP'], private_config['USERNAME'], private_config['PASSWORD'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()
        DAT.click_dataset_location(posix_acl_recursive_permissions['dataset'])
        assert PERM.assert_dataset_owner(posix_acl_recursive_permissions['initial_owner']) is True
        assert PERM.assert_dataset_group(posix_acl_recursive_permissions['initial_group']) is True
        DAT.click_edit_permissions_button()
        PERM.click_set_acl_button()
        COM.assert_dialog_visible('Select a preset ACL')
        COM.click_radio_button("use-preset-select-a-preset-acl")
        COM.select_option('preset-name', posix_acl_recursive_permissions['preset_name'])
        COM.click_button('continue')
        COM.assert_page_header('Edit ACL')
        PERM.set_dataset_owner(posix_acl_recursive_permissions['new_owner'])
        PERM.set_dataset_owner_group(posix_acl_recursive_permissions['new_owner_group'])
        PERM.set_apply_owner_checkbox()
        PERM.set_apply_group_checkbox()
        COM.unset_checkbox('permissions-write')
        COM.set_checkbox('recursive')
        COM.assert_confirm_dialog()
        COM.set_checkbox('traverse')
        PERM.click_save_acl_button()

    @pytest.fixture(scope='class', autouse=True)
    def teardown_test(self, posix_acl_recursive_permissions):
        """
        This method clears any test users after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_dataset(posix_acl_recursive_permissions['grandchild_api_path'])
        API_DELETE.delete_dataset(posix_acl_recursive_permissions['child_api_path'])
        API_DELETE.delete_dataset(posix_acl_recursive_permissions['api_path'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_dashboard()

    @allure.tag("Read")
    @allure.story("Dataset Recursive Permissions Using UI")
    @allure.issue('NAS-128726', 'NAS-128726')
    def test_recursive_permissions_via_UI(self, posix_acl_recursive_permissions):
        """
        This test verifies the ability to use recursive permissions application and verifies the permissions via WebUI
        """
        # Parent dataset verification
        assert PERM.assert_dataset_owner(posix_acl_recursive_permissions['new_owner']) is True
        assert PERM.assert_dataset_group(posix_acl_recursive_permissions['new_owner_group']) is True
        assert PERM.verify_dataset_permissions_type('POSIX Permissions') is True
        assert PERM.verify_dataset_owner_permissions_name(posix_acl_recursive_permissions['user_obj']) is True
        assert PERM.verify_dataset_owner_permissions(posix_acl_recursive_permissions['user_obj_perm'], posix_acl_recursive_permissions['new_owner']) is True
        assert PERM.verify_dataset_group_permissions_name(posix_acl_recursive_permissions['group_obj']) is True
        assert PERM.verify_dataset_group_permissions(posix_acl_recursive_permissions['group_obj_perm'], posix_acl_recursive_permissions['new_owner_group']) is True
        assert PERM.verify_dataset_other_permissions_name() is True
        assert PERM.verify_dataset_other_permissions(posix_acl_recursive_permissions['other_perm']) is True
        assert PERM.verify_dataset_owner_default_permissions_name(posix_acl_recursive_permissions['user_obj_default']) is True
        assert PERM.verify_dataset_owner_default_permissions(posix_acl_recursive_permissions['user_obj_default_perm'], posix_acl_recursive_permissions['user_obj_default']) is True
        assert PERM.verify_dataset_group_default_permissions_name(posix_acl_recursive_permissions['group_obj_default']) is True
        assert PERM.verify_dataset_group_default_permissions(posix_acl_recursive_permissions['group_obj_default_perm'], posix_acl_recursive_permissions['group_obj_default']) is True
        assert PERM.verify_dataset_other_default_permissions_name() is True
        assert PERM.verify_dataset_other_default_permissions(posix_acl_recursive_permissions['other_default_perm']) is True
        assert PERM.verify_dataset_permissions_edit_button() is True
        # Child dataset verification
        DAT.expand_dataset(posix_acl_recursive_permissions['dataset'])
        # Possible expected failure below for: NAS-128726
        DAT.click_dataset_location(posix_acl_recursive_permissions['child_dataset'])
        assert PERM.assert_dataset_owner(posix_acl_recursive_permissions['new_owner']) is True
        assert PERM.assert_dataset_group(posix_acl_recursive_permissions['new_owner_group']) is True
        assert PERM.verify_dataset_permissions_type('POSIX Permissions') is True
        assert PERM.verify_dataset_owner_permissions_name(posix_acl_recursive_permissions['children_user_obj']) is True
        assert PERM.verify_dataset_owner_permissions(posix_acl_recursive_permissions['children_user_obj_perm'], posix_acl_recursive_permissions['new_owner']) is True
        assert PERM.verify_dataset_group_permissions_name(posix_acl_recursive_permissions['group_obj']) is True
        assert PERM.verify_dataset_group_permissions(posix_acl_recursive_permissions['group_obj_perm'], posix_acl_recursive_permissions['new_owner_group']) is True
        assert PERM.verify_dataset_other_permissions_name() is True
        assert PERM.verify_dataset_other_permissions(posix_acl_recursive_permissions['other_perm']) is True
        assert PERM.verify_dataset_owner_default_permissions_name(posix_acl_recursive_permissions['user_obj_default']) is True
        assert PERM.verify_dataset_owner_default_permissions(posix_acl_recursive_permissions['children_user_obj_default_perm'], posix_acl_recursive_permissions['user_obj_default']) is True
        assert PERM.verify_dataset_group_default_permissions_name(posix_acl_recursive_permissions['group_obj_default']) is True
        assert PERM.verify_dataset_group_default_permissions(posix_acl_recursive_permissions['group_obj_default_perm'], posix_acl_recursive_permissions['group_obj_default']) is True
        assert PERM.verify_dataset_other_default_permissions_name() is True
        assert PERM.verify_dataset_other_default_permissions(posix_acl_recursive_permissions['other_default_perm']) is True
        assert PERM.verify_dataset_permissions_edit_button() is True
        # Grandchild dataset verification
        DAT.expand_dataset(posix_acl_recursive_permissions['child_dataset'])
        DAT.click_dataset_location(posix_acl_recursive_permissions['grandchild_dataset'])
        assert PERM.assert_dataset_owner(posix_acl_recursive_permissions['new_owner']) is True
        assert PERM.assert_dataset_group(posix_acl_recursive_permissions['new_owner_group']) is True
        assert PERM.verify_dataset_permissions_type('POSIX Permissions') is True
        assert PERM.verify_dataset_owner_permissions_name(posix_acl_recursive_permissions['user_obj']) is True
        assert PERM.verify_dataset_owner_permissions(posix_acl_recursive_permissions['children_user_obj_perm'], posix_acl_recursive_permissions['new_owner']) is True
        assert PERM.verify_dataset_group_permissions_name(posix_acl_recursive_permissions['group_obj']) is True
        assert PERM.verify_dataset_group_permissions(posix_acl_recursive_permissions['group_obj_perm'], posix_acl_recursive_permissions['new_owner_group']) is True
        assert PERM.verify_dataset_other_permissions_name() is True
        assert PERM.verify_dataset_other_permissions(posix_acl_recursive_permissions['other_perm']) is True
        assert PERM.verify_dataset_owner_default_permissions_name(posix_acl_recursive_permissions['user_obj_default']) is True
        assert PERM.verify_dataset_owner_default_permissions(posix_acl_recursive_permissions['children_user_obj_default_perm'], posix_acl_recursive_permissions['user_obj_default']) is True
        assert PERM.verify_dataset_group_default_permissions_name(posix_acl_recursive_permissions['group_obj_default']) is True
        assert PERM.verify_dataset_group_default_permissions(posix_acl_recursive_permissions['group_obj_default_perm'], posix_acl_recursive_permissions['group_obj_default']) is True
        assert PERM.verify_dataset_other_default_permissions_name() is True
        assert PERM.verify_dataset_other_default_permissions(posix_acl_recursive_permissions['other_default_perm']) is True
        assert PERM.verify_dataset_permissions_edit_button() is True

    @allure.tag("Read")
    @allure.story("Dataset Recursive Permissions Using SSH")
    def test_recursive_permissions_via_SSH(self, posix_acl_recursive_permissions):
        """
        This test verifies the ability to use recursive permissions application and verifies the permissions via SSH
        """
        # Parent dataset verification
        assert PERM_SSH.assert_dataset_has_posix_acl('/mnt/tank', posix_acl_recursive_permissions['dataset'], posix_acl_recursive_permissions['ls_output']) is True
        assert PERM_SSH.assert_file_has_posix_acl(posix_acl_recursive_permissions['full_path'], 'test_file.txt', posix_acl_recursive_permissions['file_ls_output']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['file_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['owner_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['group2_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['other_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['default_user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['default_group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['default_other_cli']) is True
        # Child dataset verification
        assert PERM_SSH.assert_dataset_has_posix_acl(posix_acl_recursive_permissions['full_path'], posix_acl_recursive_permissions['child_dataset'], posix_acl_recursive_permissions['child_ls_output']) is True
        assert PERM_SSH.assert_file_has_posix_acl(posix_acl_recursive_permissions['child_full_path'], 'test_file.txt', posix_acl_recursive_permissions['file_ls_output']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['child_file_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['children_owner_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['children_group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['children_user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['children_group2_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['children_other_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['children_default_user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['children_default_group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['children_default_other_cli']) is True
        # Grandchild dataset verification
        assert PERM_SSH.assert_dataset_has_posix_acl(posix_acl_recursive_permissions['child_full_path'], posix_acl_recursive_permissions['grandchild_dataset'], posix_acl_recursive_permissions['grandchild_ls_output']) is True
        assert PERM_SSH.assert_file_has_posix_acl(posix_acl_recursive_permissions['grandchild_full_path'], 'test_file.txt', posix_acl_recursive_permissions['grandchild_file_ls_output']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['grandchild_file_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['children_owner_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['children_group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['children_user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['children_group2_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['children_other_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['children_default_user_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['children_default_group_cli']) is True
        assert PERM_SSH.verify_getfacl_contains_permissions(posix_acl_recursive_permissions['grandchild_full_path'], posix_acl_recursive_permissions['children_default_other_cli']) is True
