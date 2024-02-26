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


@pytest.mark.parametrize('dat_perm', get_data_list('dataset_permissions'), scope='class')
class Test_Unix_Permissions:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, dat_perm) -> None:
        """
        This method
        """
        API_DELETE.delete_user(dat_perm['username'])
        API_POST.create_non_admin_user(dat_perm['username'], dat_perm['fullname'], dat_perm['password'], 'True')
        API_POST.create_dataset(dat_perm['dataset_name'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, dat_perm):
        """
        This method clears any test users after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_user(dat_perm['username'])
        API_DELETE.delete_dataset(dat_perm['dataset_name'])
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_dashboard()

    def test_verify_dataset_permissions_card_ui(self, dat_perm) -> None:
        """
        This test verifies the UI on the permissions card of the dataset that has been set with Unix Permissions.
        """
        DAT.click_dataset_location(dat_perm['dataset_name'])
        assert PERM.verify_dataset_owner(dat_perm['username'])
        assert PERM.verify_dataset_group(dat_perm['username'])
        assert PERM.verify_dataset_permissions_type('Unix Permissions')
        assert PERM.verify_dataset_owner_permissions_name(dat_perm['username'])
        assert PERM.verify_dataset_owner_permissions('Read | Write | Execute')
        assert PERM.verify_dataset_group_permissions_name(dat_perm['groupname'])
        assert PERM.verify_dataset_group_permissions('Read | Execute')
        assert PERM.verify_dataset_other_permissions_name()
        assert PERM.verify_dataset_other_permissions('Read | Execute')
        assert PERM.verify_dataset_permissions_edit_button()


