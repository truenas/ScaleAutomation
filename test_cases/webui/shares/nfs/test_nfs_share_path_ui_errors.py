import allure
import pytest
from helper.data_config import get_data_list
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
        DATASET.create_dataset_by_api(nfs_data['api_path'], 'NFS')
        DATASET.create_dataset_by_api(nfs_data['api_path_alt'], 'NFS')
        COMSHARE.create_share_by_api('nfs', '', nfs_data['api_path'])
        COMSHARE.create_share_by_api('nfs', '', nfs_data['api_path_alt'])

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, nfs_data):
        """
        This fixture deletes all datasets and NFS shares for the test.
        """
        yield
        COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
        COMSHARE.delete_share_by_api('nfs', nfs_data['api_path_alt'])
        DATASET.delete_dataset_by_api(nfs_data['api_path'])
        DATASET.delete_dataset_by_api(nfs_data['api_path_alt'])

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
        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs')

        # Trigger the nonexistent path error
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
        COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
        COMSHARE.set_share_path('nonexistent')
        COMSHARE.set_share_description(nfs_data['description'])
        COM.set_checkbox('enabled')
        COM.click_save_button()

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_path_nonexistant()
        assert COM.is_save_button_disabled()

        # Trigger the Path is required error
        COM.clear_input_field('path', True)

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_path_required()
        assert COM.is_save_button_disabled()

        # Trigger the duplicate share error
        COMSHARE.set_share_path(nfs_data['api_path_alt'])
        COM.click_save_button()

        # Assert error message displays and saving disabled
        assert NFS.assert_error_nfs_share_path_duplicate(nfs_data['share_page_path_alt'])
        assert COM.is_save_button_disabled()

        # Verify share still in original state when editing is cancelled
        COM.close_right_panel()
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
        assert not COMSHARE.assert_share_description('nfs', nfs_data['description'])
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path'])

        # Verify share attachment to dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs')
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs')
        DATASET.select_dataset(nfs_data['dataset_name_alt'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name_alt'], 'nfs')
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name_alt'], 'nfs')
