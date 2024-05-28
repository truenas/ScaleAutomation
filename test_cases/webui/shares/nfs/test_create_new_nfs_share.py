import allure
import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV


@allure.tag("NFS Shares")
@allure.epic("Shares")
@allure.feature("NFS")
@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
class Test_Create_NFS_Share:
    """
    This test class covers the NFS share create test cases.
    """

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, nfs_data):
        """
        This fixture sets the dataset for the NFS share test
        """
        API_POST.create_dataset(nfs_data['api_path'], 'NFS')
        API_POST.stop_service('nfs')

        # Navigate to Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, nfs_data):
        """
        This fixture delete the dataset and the NFS share after the test is completed.
        """
        yield
        API_DELETE.delete_share('nfs', nfs_data['api_path'])
        API_DELETE.delete_dataset(nfs_data['api_path'], recursive=True, force=True)

    @allure.tag("Create")
    @allure.story("Create New NFS Share")
    def test_create_new_nfs_share(self, nfs_data):
        """
        This test creates a new NFS share with the given data.
        """

        # Create new NFS share
        COMSHARE.click_add_share_button('nfs')
        COMSHARE.set_share_path(nfs_data['api_path'])
        COMSHARE.set_share_description(nfs_data['description'])
        COM.set_checkbox('enabled')
        COM.click_save_button()

        # Handle start/restart service popup
        COMSHARE.handle_share_service_dialog('nfs', 'start')

        # Verify share attachment to dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs') is True
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs') is True

        # Verify share displayed on shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        assert COMSHARE.assert_share_description('nfs', nfs_data['description']) is True
        assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path']) is True
