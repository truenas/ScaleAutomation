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
class Test_Delete_NFS_Share:
    """
    This test class covers the NFS share delete test cases.
    """

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, nfs_data):
        """
        This fixture sets the dataset and the NFS share for the test.
        """
        API_POST.create_dataset(nfs_data['api_path'], 'NFS')
        API_POST.create_share('nfs', '', "/mnt/"+nfs_data['api_path'])

        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True

    @pytest.fixture(scope='function', autouse=True)
    def tear_down_test(self, nfs_data):
        """
        This fixture delete the dataset after the test is completed.
        """
        yield
        API_DELETE.delete_dataset(nfs_data['api_path'], recursive=True, force=True)

    @allure.tag("Delete")
    @allure.story('Delete NFSv3 Share')
    def test_delete_new_nfsv3_share(self, nfs_data):
        """
        This test verifies the NFSv3 share can be deleted.

        Test Steps:
        1. Delete the NFSv3 share.
        3. Navigate to the datasets page and verify that the share is still detached from the dataset.
        4. Navigate to the shares page and verify that the share is not displayed on the shares page.
        """
        # Delete NFS share
        assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path']) is True
        COMSHARE.click_delete_share('nfs', nfs_data['share_page_path'])
        COM.assert_confirm_dialog()

        # Verify share detached from dataset
        NAV.navigate_to_datasets()
        DATASET.expand_dataset('tank')
        DATASET.select_dataset(nfs_data['dataset_name'])
        assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs') is False
        assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs') is False

        # Verify share deleted from Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.is_share_visible('nfs', nfs_data['share_page_path']) is False