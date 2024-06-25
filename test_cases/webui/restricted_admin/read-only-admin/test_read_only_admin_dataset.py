import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import shared_config
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation
from keywords.webui.snapshots import Snapshots


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
        This setup fixture create the dataset and read-only admin for all test cases.
        """
        API_POST.create_dataset(f'{data["pool"]}/{data["acl_parent_dataset"]}', 'SMB')
        API_POST.create_dataset(f'{data["pool"]}/{data["acl_parent_dataset"]}/{data["acl_child_dataset"]}', 'SMB')
        API_POST.create_dataset(f'{data["pool"]}/{data["generic_parent_dataset"]}', 'GENERIC')
        API_POST.create_dataset(f'{data["pool"]}/{data["generic_parent_dataset"]}/{data["generic_child_dataset"]}', 'GENERIC')
        # API_POST.create_snapshot(f'{data["pool"]}/{data["acl_parent_dataset"]}', data['snapshot_name'])
        shared_config['snapshot_name'] = API_POST.create_snapshot(f'{data["pool"]}/{data["acl_parent_dataset"]}', data['snapshot_name']).json()['snapshot_name']

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_test(self, data):
        """
        This teardown fixture delete the dataset and read-only admin for all test cases.
        """
        yield
        # Return to dataset page or there will be an error when deleting the dataset.
        Navigation.navigate_to_datasets()
        # API_DELETE.delete_snapshot(f'{data["pool"]}/{data["acl_parent_dataset"]}@{data["snapshot_name"]}', recursive=True)
        API_DELETE.delete_snapshot(f'{data["pool"]}/{data["acl_parent_dataset"]}@{shared_config["snapshot_name"]}', recursive=True)
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["acl_parent_dataset"]}', recursive=True, force=True)
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["generic_parent_dataset"]}', recursive=True, force=True)

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See The Dataset")
    def test_read_only_admin_can_see_the_datasets_and_its_children(self, data):
        """
        This test verifies the read-only admin is able to see datasets and its children.n:
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

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

    @allure.tag("Read")
    @allure.story("Read Only Admin Can View Dataset Details")
    def test_read_only_admin_can_view_dataset_details(self, data):
        """
        This test verifies the read-only admin is able to view dataset details.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
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

    @allure.tag("Read")
    @allure.story("Read Only Admin Can View Dataset Space Management Information")
    def test_read_only_admin_can_view_space_management_information(self, data):
        """
        This test verifies the read-only admin is able to view space management information.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
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

    @allure.tag("Read")
    @allure.story("Read Only Admin Can Access Dataset Quotas For Users And Group")
    def test_read_only_admin_can_access_quota_for_users_and_group(self, data):
        """
        This test verifies the read-only admin is able to access Quotas for users and group.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.is_space_management_card_visible()
        Datasets.click_manage_group_quotas_link(data['pool'], data["acl_parent_dataset"])
        assert Datasets.is_group_quotas_page_visible()

        Navigation.navigate_to_datasets()
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.is_space_management_card_visible()
        Datasets.click_manage_user_quotas_link(data['pool'], data["acl_parent_dataset"])
        assert Datasets.is_user_quotas_page_visible()

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able To Access Dataset ACL Permissions")
    def test_read_only_admin_can_not_access_acl_permissions(self, data):
        """
        This test verifies the read-only admin is not able to access ACL permissions.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is able to access ACL permissions
        Navigation.navigate_to_datasets()
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.is_permissions_card_visible()
        assert Datasets.assert_edit_dataset_permissions_button_is_restricted() is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able To Dataset Access Unix Permissions")
    def test_read_only_admin_can_not_access_unix_permissions(self, data):
        """
        This test verifies the read-only admin is not able to access Unix permissions.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is able to access Unix permissions
        Navigation.navigate_to_datasets()
        Datasets.select_dataset(data["generic_parent_dataset"])
        assert Datasets.is_permissions_card_visible()
        assert Datasets.assert_edit_dataset_permissions_button_is_restricted() is True

    @allure.tag("Create", "Delete")
    @allure.story("Read Only Admin Is Not Able To Add And Delete Dataset")
    def test_read_only_admin_is_not_able_to_add_and_delete_dataset(self, data):
        """
        This test verifies the read-only admin is not able to:
        - Add a dataset from the pool dataset
        - Add a dataset from a dataset in the pool
        - Delete a dataset
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is not able to add a dataset from the pool dataset
        assert Datasets.assert_selected_dataset_name(data["pool"]) is True
        assert Datasets.assert_add_dataset_button_is_restricted() is True

        # Verify the read-only admin is not able to add a dataset from a dataset in the pool
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_parent_dataset"]) is True
        assert Datasets.assert_add_dataset_button_is_restricted() is True

    @allure.tag("Create")
    @allure.story("Read Only Admin Is Not Able To Add A Zvol")
    def test_read_only_admin_is_not_able_to_add_a_zvol(self, data):
        """
        This test verifies the read-only admin is not able to add a zvol.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is not able to add a zvol
        assert Datasets.assert_selected_dataset_name(data["pool"]) is True
        assert Datasets.assert_add_zvol_button_is_restricted() is True

    @allure.tag("Update")
    @allure.story("Read Only Admin Is Not Able To Modify A Dataset")
    def test_read_only_admin_is_not_able_to_modify_a_dataset(self, data):
        """
        This test verifies the read-only admin is not able to modify a dataset.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is not able to modify a dataset
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_parent_dataset"]) is True
        assert Datasets.assert_edit_dataset_button_is_restricted() is True

    @allure.tag("Update")
    @allure.story("Read Only Admin Is Not Able To Modify Dataset Space Management Capacity Settings")
    def test_read_only_admin_is_notable_to_modify_space_management_capacity_settings(self, data):
        """
        This test verifies the read-only admin is not able to modify space management capacity settings.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is not able to modify space management capacity settings
        assert Datasets.is_space_management_card_visible()
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_parent_dataset"]) is True
        assert Datasets.assert_edit_dataset_space_management_button_is_restricted() is True

    @allure.tag("Update")
    @allure.story("Read Only Admin Is Not Able To Modify Dataset Groups And Users Quotas")
    def test_read_only_admin_is_not_able_to_modify_groups_and_users_quotas(self, data):
        """
        This test verifies the read-only admin is not able to modify groups and users quotas.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is not able to modify users and groups quotas
        assert Datasets.is_space_management_card_visible()
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_parent_dataset"]) is True
        Datasets.click_manage_group_quotas_link(data['pool'], data["acl_parent_dataset"])
        assert Datasets.is_group_quotas_page_visible()
        assert Datasets.assert_add_quota_button_is_restricted() is True

        Navigation.navigate_to_datasets()
        assert Datasets.is_space_management_card_visible()
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_parent_dataset"]) is True
        Datasets.click_manage_user_quotas_link(data['pool'], data["acl_parent_dataset"])
        assert Datasets.is_user_quotas_page_visible()
        assert Datasets.assert_add_quota_button_is_restricted() is True

    @allure.tag("Update")
    @allure.story("Read Only Admin Is Not Able To Create Dataset Snapshots")
    def test_read_only_admin_is_not_able_to_create_snapshots(self, data):
        """
        This test verifies the read-only admin is not able to create snapshots.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is not able to create snapshots
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_parent_dataset"]) is True
        assert Datasets.assert_create_snapshot_button_is_restricted() is True

    @allure.tag("Update")
    @allure.story("Read Only Admin Is Not Able To Delete Clone Rollback And Hold A Dataset Snapshot")
    def test_read_only_admin_is_not_able_to_delete_clone_rollback_and_hold_a_snapshot(self, data):
        """
        This test verifies the read-only admin is not able to delete snapshots.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()

        # Verify the read-only admin is not able to delete snapshots
        Datasets.select_dataset(data["acl_parent_dataset"])
        assert Datasets.assert_selected_dataset_name(data["acl_parent_dataset"]) is True
        assert Datasets.assert_data_protection_card_visible() is True
        Datasets.click_manage_snapshots_link()

        assert Snapshots.assert_dataset_snapshot_page_header(f'{data["pool"]}/{data["acl_parent_dataset"]}') is True
        # assert Snapshots.assert_snapshot_is_visible(data['snapshot_name']) is True
        assert Snapshots.assert_snapshot_is_visible(shared_config['snapshot_name']) is True
        Snapshots.expand_snapshot_by_name(shared_config['snapshot_name'])

        # verify the read-only admin is not able to delete snapshots
        assert Snapshots.assert_delete_button_is_restricted(shared_config['snapshot_name']) is True

        # verify the read-only admin is not able to clone a snapshots
        assert Snapshots.assert_clone_to_new_snapshot_button_is_restricted(shared_config['snapshot_name']) is True

        # verify the read-only admin is not able to roll back a snapshots
        assert Snapshots.assert_rollback_button_is_restricted(shared_config['snapshot_name']) is True

        # verify the read-only admin is not able to change the hold checkbox
        assert Snapshots.assert_hold_checkbox_is_restricted(shared_config['snapshot_name']) is True
