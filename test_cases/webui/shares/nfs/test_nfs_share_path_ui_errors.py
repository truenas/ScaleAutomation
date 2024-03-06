import allure
import pytest
from helper.data_config import get_data_list
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
class Test_NFS_Share_Path_UI_Errors:
    """
    This test class covers the NFS share path UI errors test cases.
    """

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, nfs_data):
        """
        This fixture creates all datasets and NFS shares for the test.
        """
        API_POST.create_dataset(nfs_data['api_path'], 'NFS')
        API_POST.create_dataset(nfs_data['api_path_alt'], 'NFS')
        API_POST.create_share('nfs', '', nfs_data['api_path'])
        API_POST.create_share('nfs', '', nfs_data['api_path_alt'])

        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, nfs_data):
        """
        This fixture deletes all datasets and NFS shares for the test.
        """
        yield
        API_DELETE.delete_share('nfs', nfs_data['api_path'])
        API_DELETE.delete_share('nfs', nfs_data['api_path_alt'])
        API_DELETE.delete_dataset(nfs_data['api_path'], recursive=True, force=True)
        API_DELETE.delete_dataset(nfs_data['api_path_alt'], recursive=True, force=True)

    @allure.tag("Update")
    @allure.story('NFS Share Path UI Errors')
    def test_nfs_share_path_ui_errors(self, nfs_data) -> None:
        """
        This test case covers the following:
         - Trigger the nonexistent path error
         - Trigger the Path is required error
         - Trigger the duplicate share error
         - Verify share still in original state when editing is cancelled
        """

        # Trigger the nonexistent path error
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        COMSHARE.set_share_path('nonexistent')
        COMSHARE.set_share_description(nfs_data['description'])
        COM.set_checkbox('enabled')
        COM.click_save_button()

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_path_nonexistent() is True
        assert COM.is_save_button_disabled() is True

        # Trigger the Path is required error
        COM.clear_input_field('path', True)

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_path_required() is True
        assert COM.is_save_button_disabled() is True

        # Trigger the duplicate share error
        COMSHARE.set_share_path(nfs_data['api_path_alt'])
        COM.click_save_button()

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_path_duplicate(nfs_data['share_page_path_alt']) is True
        assert COM.is_save_button_disabled() is True

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
        DATASET.select_dataset(nfs_data['dataset_name_alt'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name_alt'], 'nfs') is True
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name_alt'], 'nfs') is True
