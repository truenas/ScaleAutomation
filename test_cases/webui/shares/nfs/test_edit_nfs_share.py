import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.nfs import NFS


@allure.tag("NFS Shares")
@allure.epic("Shares")
@allure.feature("NFS")
@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
class Test_Edit_NFS_Share:
    """
    This test class covers the edit NFS share test cases.
    """

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, nfs_data):
        """
        This fixture sets the dataset and the NFS share for the test.

        """
        # Ensure NFS service is started or some weird failure will occur when the test that disable it runs before.
        API_POST.start_service('nfs')
        API_POST.create_dataset(nfs_data['api_path'], 'NFS')
        API_POST.create_dataset(nfs_data['api_path_alt'], 'NFS')
        API_POST.create_share('nfs', '', "/mnt/"+nfs_data['api_path'])

        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, nfs_data):
        """
        This fixture delete the dataset and Shares after the test is completed.
        """
        yield
        API_DELETE.delete_share('nfs', nfs_data['api_path'])
        API_DELETE.delete_share('nfs', nfs_data['api_path_alt'])
        API_DELETE.delete_dataset(nfs_data['api_path'], recursive=True, force=True)
        API_DELETE.delete_dataset(nfs_data['api_path_alt'], recursive=True, force=True)

    @allure.tag("Update")
    @allure.story("Edit NFSv3 Share Advanced Options")
    def test_edit_nfsv3_share_advanced_options(self, nfs_data):
        """
        Summary: This test creates an NFS and configures it with advanced options in the UI.

        Test Steps:
        1. Edit the NFSv3 share and configure it with advanced options:
            - Authorized network address
            - Authorized ip address
            - Read only
            - Maproot user
            - Maproot group
            - Security type
        3. Navigate to the datasets page and verify that the share is attached to the dataset.
        4. Navigate to the shares page and verify that the share is displayed on the shares page.
        5. Re-edit the NFSv3 share and configure it with new advanced options:
            - Unset read only
            - Unset maproot user
            - Unset maproot group
            - Set mapall user
            - Set mapall group
        6. Navigate to the datasets page and verify that the share is attached to the dataset.
        7. Navigate to the shares page and verify that the share is displayed on the shares page.
        """

        # Edit the NFSv3 share with advanced options
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        COM.set_checkbox('enabled')
        NFS.click_add_networks_button()
        NFS.set_network(private_config['NETWORK'])
        NFS.set_network_mask(private_config['MASK'])
        NFS.click_add_hosts_button()
        NFS.set_host_and_ip(private_config['AUTH_HOST'])
        COMSHARE.click_advanced_options()
        COM.set_checkbox('ro')
        NFS.set_maproot_user('admin')
        NFS.set_maproot_group('admin')
        COM.select_then_deselect_input_field('comment')
        NFS.set_security_type('sys')
        COMSHARE.set_share_description(nfs_data['description'])
        COM.select_then_deselect_input_field('comment')
        COM.click_save_button_and_wait_for_progress_bar()

        # Handle start/restart service popup
        COMSHARE.handle_share_service_dialog('nfs')

        # Verify share attachment to new dataset and no attachment to old dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs') is True
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs') is True

        # Verify edited share displayed on shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        assert COMSHARE.assert_share_description('nfs', nfs_data['description']) is True
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is True

        # Edit the NFSv3 share with second set of advanced options
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path_with_desc'])
        COMSHARE.click_advanced_options()
        COM.unset_checkbox('ro')
        NFS.unset_maproot_user()
        NFS.unset_maproot_group()
        NFS.set_mapall_user('admin')
        NFS.set_mapall_group('admin')
        COM.select_then_deselect_input_field('comment')
        COM.click_save_button_and_wait_for_progress_bar()

        # Verify share attachment to new dataset and no attachment to old dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs') is True
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs') is True

        # Verify edited share displayed on shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        assert COMSHARE.assert_share_description('nfs', nfs_data['description']) is True
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is True

    @allure.tag("Update")
    @allure.story("Edit NFSv3 Share With Existing Dataset")
    def test_edit_nfsv3_share_with_existing_dataset(self, nfs_data):
        """
        Summary: This test edits a created share and attaches it to a different existing dataset and verifies the
        attachment has changed to the new dataset.

        Test Steps:
        1. Edit the NFSv3 share and configure it with different existing dataset.
        2. Navigate to the datasets page and verify that the share is attached to the new dataset.
        3. Navigate to the shares page and edit the share and configure it with the previous dataset.
        4. Navigate to the datasets page and verify that the share is attached to the previous dataset.
        """

        # Edit the NFSv3 share
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        COMSHARE.set_share_path(nfs_data['api_path_alt'])
        COMSHARE.set_share_description(nfs_data['description_alt'])
        COM.set_checkbox('enabled')
        COM.click_save_button_and_wait_for_progress_bar()

        # Handle start/restart service popup
        COMSHARE.handle_share_service_dialog('nfs')

        # Verify share attachment to new dataset and no attachment to old dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name_alt'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name_alt'], 'nfs') is True
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name_alt'], 'nfs') is True
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs') is False
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs') is False

        # Verify edited share displayed on shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path_alt']) is True
        assert COMSHARE.assert_share_description('nfs', nfs_data['description_alt']) is True
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path_alt']) is True
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is False
        assert COMSHARE.assert_share_description('nfs', nfs_data['description']) is False

    @allure.tag("Update")
    @allure.story("Edit NFS Share With Nonexistent Dataset")
    def test_edit_nfs_share_with_nonexistent_dataset(self, nfs_data):
        """
        Summary: This test edits a created share and attaches it a nonexistent dataset and verifies the share
        cannot be saved and does not detach from the existing dataset.

        Test Steps:
        1. Edit the NFS share and configure it with a nonexistent dataset.
        2. Verify the share cannot be saved.
        3. Navigate to the datasets page and verify that the share is still attached to the previous dataset.
        4. Navigate to the shares page and verify that the share is still displayed on the shares page.
        """

        # Edit the NFS share with nonexistent path
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        COMSHARE.set_share_path('nonexistent')
        COMSHARE.set_share_description(nfs_data['description'])
        COM.set_checkbox('enabled')
        COM.click_save_button_and_wait_for_progress_bar()

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_path_nonexistent() is True
        COM.click_error_dialog_close_button()
        COM.close_right_panel()

        # Verify share still in original state when editing is cancelled
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        assert COMSHARE.assert_share_description('nfs', nfs_data['description']) is False
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is True

        # Verify share attachment to dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs') is True
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs') is True

    @allure.tag("Update")
    @allure.story("Edit NFSv3 Share Advanced UI Errors")
    def test_nfs_share_advanced_ui_errors(self, nfs_data):
        """
        Summary: This test creates an NFS share and verifies the advanced UI errors display.

        Test Steps:
        1. Edit the NFS share and verify that the following errors are displayed when expected:
            - Trigger the maproot user required error
            - Trigger mapall user override error
            - Trigger invalid ip error
            - Trigger network is required error
            - Trigger Authorized Hosts and IP addresses is required error
        2. Verify share still in original state when editing is cancelled.
        3. Navigate to the datasets page and verify that the share is attached to the dataset.
        """

        # Trigger the maproot user required error
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        COM.set_checkbox('enabled')
        COMSHARE.click_advanced_options()
        NFS.set_maproot_group('admin')
        COM.click_save_button_and_wait_for_progress_bar()

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_maproot_user_required() is True
        COM.click_error_dialog_close_button()

        # Trigger mapall user override error
        NFS.set_maproot_user('admin')
        NFS.set_mapall_user('admin')
        COM.click_save_button_and_wait_for_progress_bar()

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_mapall_user_override() is True
        COM.click_error_dialog_close_button()
        NFS.unset_maproot_user()
        NFS.unset_mapall_user()
        COM.select_then_deselect_input_field('comment')

        # Trigger invalid ip error
        NFS.click_add_networks_button()
        NFS.set_network('1')

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_network_invalid_ip() is True
        assert COM.is_save_button_disabled() is True
        NFS.click_remove_from_list_button()

        # Trigger network is required error
        NFS.click_add_networks_button()
        NFS.set_network_mask('32')

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_network_is_required() is True
        assert COM.is_save_button_disabled() is True
        NFS.click_remove_from_list_button()

        # Trigger Authorized Hosts and IP addresses is required error
        NFS.click_add_hosts_button()
        NFS.set_host_and_ip('')

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_authorized_hosts_required() is True
        assert COM.is_save_button_disabled() is True
        NFS.click_remove_from_list_button()

        # Verify share still in original state when editing is cancelled
        COM.close_right_panel()
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        assert COMSHARE.assert_share_description('nfs', nfs_data['description']) is False
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is True

        # Verify share attachment to dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs') is True
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs') is True

    @allure.tag("Update")
    @allure.story("Disable NFSv3 Share")
    def test_nfsv3_share_disabled_share(self, nfs_data):
        """
        Summary: This test edits a created share and disables it and verifies that the share is still attached to the dataset.

        Test Steps:
        1. Edit the NFSv3 share and disable it.
        2. Navigate to the datasets page and verify that the share is still attached to the previous dataset.
        3. Navigate to the shares page and verify that the share is still displayed on the shares page.
        """

        # Disable the NFS share
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        COM.unset_checkbox('enabled')
        COM.click_save_button_and_wait_for_progress_bar()

        # Handle start/restart service popup
        COMSHARE.handle_share_service_dialog('nfs')
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is False

        # Verify share attachment to dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs') is True
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs') is True

        # Verify share displayed on shares page is disabled
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is False

        # TODO: Add in CLI test component to ensure share cannot be used when disabled. TEN-902
