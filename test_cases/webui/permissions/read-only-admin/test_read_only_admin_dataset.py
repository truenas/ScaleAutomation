import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation
from keywords.webui.permissions import Permissions


@allure.tag('Read Only Admin', 'Dataset', "Users", 'Permissions')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
@pytest.mark.parametrize('data', get_data_list('read_only_admin_dataset'), scope='class')
class Test_Read_Only_Admin_Dataset:
    """
    This test class tests read-only admin dataset
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self, data):
        """
        Thi
        """
        API_POST.create_read_only_admin(data['username'], data['fullname'], data['password'])
        API_POST.create_dataset(f'{data["pool"]}/{data["acl_parent_dataset"]}', 'SMB')
        API_POST.create_dataset(f'{data["pool"]}/{data["acl_parent_dataset"]}/{data["acl_child_dataset"]}', 'SMB')
        API_POST.create_dataset(f'{data["pool"]}/{data["generic_parent_dataset"]}', 'GENERIC')
        API_POST.create_dataset(f'{data["pool"]}/{data["generic_parent_dataset"]}/{data["generic_child_dataset"]}', 'GENERIC')

        Common.logoff_truenas()
        Common.login_to_truenas(data['username'], data['password'])

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_test(self, data):
        yield
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["acl_parent_dataset"]}', recursive=True, force=True)
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["generic_parent_dataset"]}', recursive=True, force=True)
        API_DELETE.delete_user(data['username'])
        Common.logoff_truenas()
        Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])

    @allure.tag("Read")
    @allure.story("Read Only Admin Can Read The Dataset UI")
    def test_read_only_admin_can_read_the_dataset_ui(self, data):
        """
        This test verifies the read-only admin is able to:
        - See the datasets and their children
        - View dataset details
        - View Space Management information
        - Access Quotas for users and group
        - See permissions including accessing ACL permissions for the dataset
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

        # verify the parent and child datasets are accessible and visible
        Datasets.select_dataset(data["pool"])
        assert Datasets.assert_selected_dataset_name('tank') is True
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_parent_dataset"]) is True
        Datasets.select_dataset(data["acl_child_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_child_dataset"]) is True
        Datasets.select_dataset(data["generic_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["generic_parent_dataset"]) is True
        Datasets.select_dataset(data["generic_child_dataset"])
        assert Datasets.assert_selected_dataset_name(data["generic_child_dataset"]) is True

        # Verify the read-only admin can view all dataset details
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Common.is_card_visible('Dataset Details') is True
        assert Datasets.assert_details_type('FILESYSTEM') is True
        assert Datasets.assert_details_sync('STANDARD') is True
        assert Datasets.assert_details_compression_level('Inherit (LZ4)') is True
        assert Datasets.assert_details_enable_atime('OFF') is True
        assert Datasets.assert_details_zfs_deduplication('OFF') is True
        assert Datasets.assert_details_case_sensitivity('ON') is True
        assert Datasets.assert_details_path(data["acl_parent_dataset"]) is True
        assert Datasets.assert_edit_dataset_button() is True
        assert Datasets.assert_delete_dataset_button() is True

        # Verify the read-only admin can view all space management information
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.is_space_management_card_visible() is True
        assert Datasets.assert_total_allocation_size('KiB') is True
        assert Datasets.assert_data_written_size('KiB') is True
        assert Datasets.assert_space_available_to_dataset_size('GiB') is True
        assert Datasets.assert_user_quotas('Quotas set for ') is True
        assert Datasets.assert_user_quotas(' user') is True
        assert Datasets.assert_group_quotas('Quotas set for ') is True
        assert Datasets.assert_group_quotas(' group') is True

        # Verify the read-only admin is able to access Quotas for users and group
        assert Datasets.is_space_management_card_visible()
        Datasets.click_manage_group_quotas_link(data['pool'], data["acl_parent_dataset"])
        assert Datasets.is_group_quotas_page_visible()

        Navigation.navigate_to_datasets()
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.is_space_management_card_visible()
        Datasets.click_manage_user_quotas_link(data['pool'], data["acl_parent_dataset"])
        assert Datasets.is_user_quotas_page_visible()

        # Verify the read-only admin is able to access ACL permissions
        Navigation.navigate_to_datasets()
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.is_permissions_card_visible()
        Datasets.click_edit_permissions_button()
        assert Permissions.assert_edit_acl_page_header()

        # Verify the read-only admin is able to access Unix permissions
        Navigation.navigate_to_datasets()
        Datasets.select_dataset(data["generic_parent_dataset"])
        assert Datasets.is_space_management_card_visible()
        assert Datasets.is_permissions_card_visible()
        Datasets.click_edit_permissions_button()
        assert Permissions.assert_edit_permissions_page_header()

        # Return to dataset page or there will be an error when deleting the dataset.
        Navigation.navigate_to_datasets()
