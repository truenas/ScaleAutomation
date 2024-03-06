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


@pytest.mark.parametrize('unix_perms', get_data_list('dataset_permission/unix_permissions'), scope='class')
class Test_Unix_Permissions:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, unix_perms) -> None:
        """
        This method creates the dataset and navigates to datasets before testing.
        """
        API_POST.create_dataset(unix_perms['pool']+'/'+unix_perms['dataset'])
        API_POST.set_dataset_permissions_user_and_group(unix_perms['pool']+'/'+unix_perms['dataset'], unix_perms['username'], unix_perms['groupname'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, unix_perms):
        """
        This method clears any test users after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_dataset(unix_perms['pool']+'/'+unix_perms['dataset'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_dashboard()

    def test_verify_dataset_permissions_card_ui(self, unix_perms) -> None:
        """
        This test verifies the UI on the permissions card of the dataset that has been set with Unix Permissions.
        """
        DAT.click_dataset_location(unix_perms['dataset'])
        assert PERM.verify_dataset_owner(unix_perms['username']) is True
        assert PERM.verify_dataset_group(unix_perms['username']) is True
        assert PERM.verify_dataset_permissions_type('Unix Permissions') is True
        assert PERM.verify_dataset_owner_permissions_name(unix_perms['username']) is True
        assert PERM.verify_dataset_owner_permissions('Read | Write | Execute') is True
        assert PERM.verify_dataset_group_permissions_name(unix_perms['groupname']) is True
        assert PERM.verify_dataset_group_permissions('Read | Execute') is True
        assert PERM.verify_dataset_other_permissions_name() is True
        assert PERM.verify_dataset_other_permissions('Read | Execute') is True
        assert PERM.verify_dataset_permissions_edit_button() is True

    def test_edit_dataset_permissions_card_via_webui(self, unix_perms) -> None:
        """
        This test verifies edits the dataset via WebUI and checks that the changes display and the access level via cli is the same.
        """
        DAT.click_dataset_location(unix_perms['dataset'])
        DAT.click_edit_permissions_button()
        PERM.set_dataset_user(unix_perms['username'])
        PERM.set_dataset_group(unix_perms['username'])
        PERM.set_apply_user_checkbox()
        PERM.set_apply_group_checkbox()
        PERM.set_user_access_mode('UserPermissions')
        PERM.set_group_access_mode('GroupPermissions')
        PERM.set_other_access_mode('OtherPermissions')
        COM.click_save_button_and_wait_for_progress_bar()
        assert PERM.verify_dataset_owner(unix_perms['username']) is True
        assert PERM.verify_dataset_group(unix_perms['username']) is True
        assert PERM.verify_dataset_permissions_type('Unix Permissions') is True
        assert PERM.verify_dataset_owner_permissions_name(unix_perms['username']) is True
        assert PERM.verify_dataset_owner_permissions('UserPermissions') is True
        assert PERM.verify_dataset_group_permissions_name(unix_perms['groupname']) is True
        assert PERM.verify_dataset_group_permissions('GroupPermissions') is True
        assert PERM.verify_dataset_other_permissions_name() is True
        assert PERM.verify_dataset_other_permissions('OtherPermissions') is True
        assert PERM.verify_dataset_permissions_edit_button() is True
        PERM.assert_access('user', 'permissions')
        PERM.assert_access('group', 'permissions')
        PERM.assert_access('other', 'permissions')



