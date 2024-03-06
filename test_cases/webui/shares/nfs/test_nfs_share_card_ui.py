import allure
import pytest

from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV


@allure.tag("NFS Shares")
@allure.epic("Shares")
@allure.feature("NFS")
@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
class Test_NFS_Share_Card_UI:
    """
    This test class covers the NFS share card UI test cases.
    """
    @pytest.fixture(scope="function", autouse=True)
    def setup_test(self):
        """
        This fixture creates all the dataset and NFS shares for the test.
        """
        API_POST.stop_service('nfs')
        DATASET.create_dataset_by_api("tank/shareone", 'NFS')
        DATASET.create_dataset_by_api("tank/sharetwo", 'NFS')
        DATASET.create_dataset_by_api("tank/sharethree", 'NFS')
        DATASET.create_dataset_by_api("tank/sharefour", 'NFS')
        DATASET.create_dataset_by_api("tank/sharefive", 'NFS')
        COMSHARE.create_share_by_api('nfs', '', "tank/shareone")
        COMSHARE.create_share_by_api('nfs', '', "tank/sharetwo")
        COMSHARE.create_share_by_api('nfs', '', "tank/sharethree")
        COMSHARE.create_share_by_api('nfs', '', "tank/sharefour")
        COMSHARE.create_share_by_api('nfs', '', "tank/sharefive")

    @pytest.fixture(scope="function", autouse=True)
    def tear_down_test(self):
        """
        This fixture deletes all the dataset and NFS shares for the test.
        """
        yield
        COMSHARE.delete_share_by_api('nfs', "tank/shareone")
        COMSHARE.delete_share_by_api('nfs', "tank/sharetwo")
        COMSHARE.delete_share_by_api('nfs', "tank/sharethree")
        COMSHARE.delete_share_by_api('nfs', "tank/sharefour")
        COMSHARE.delete_share_by_api('nfs', "tank/sharefive")
        DATASET.delete_dataset_by_api("tank/shareone")
        DATASET.delete_dataset_by_api("tank/sharetwo")
        DATASET.delete_dataset_by_api("tank/sharethree")
        DATASET.delete_dataset_by_api("tank/sharefour")
        DATASET.delete_dataset_by_api("tank/sharefive")

    @allure.tag("Read")
    @allure.story("NFS Share Card UI")
    def test_nfs_share_card_ui(self, nfs_data):
        """
        This test verifies the NFS share card UI.
        """
        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs')

        # Verify NFS Card on Sharing page UI
        assert COMSHARE.is_share_service_stopped('nfs') is True
        assert COMSHARE.start_share_service_by_actions_menu('nfs') is True
        assert COMSHARE.stop_share_service_by_actions_menu('nfs') is True
        assert COMSHARE.assert_share_card_add_button('nfs') is True
        assert COMSHARE.assert_share_card_actions_menu_button('nfs') is True
        assert COMSHARE.assert_share_card_enabled_button_by_name('nfs', "/mnt/tank/shareone") is True
        assert COMSHARE.assert_share_card_button_by_name('nfs', "/mnt/tank/shareone", 'edit') is True
        assert COMSHARE.assert_share_card_button_by_name('nfs', "/mnt/tank/shareone", 'delete') is True
        assert COMSHARE.assert_share_card_view_all_button('nfs') is True

        # Verify only four shares display regularly
        assert COMSHARE.assert_share_path('nfs', "/mnt/tank/shareone") is True
        assert COMSHARE.assert_share_path('nfs', "/mnt/tank/sharetwo") is True
        assert COMSHARE.assert_share_path('nfs', "/mnt/tank/sharethree") is True
        assert COMSHARE.assert_share_path('nfs', "/mnt/tank/sharefour") is True
        assert COMSHARE.assert_share_path('nfs', "/mnt/tank/sharefive") is False

        # Verify all shares display after clicking the View All button
        COM.click_link('nfs-share-view-all')
        assert COM.assert_page_header('NFS') is True
        assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/shareone") is True
        assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/sharetwo") is True
        assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/sharethree") is True
        assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/sharefour") is True
        assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/sharefive") is True

        # Verify NFS View All page UI
        assert COMSHARE.assert_share_view_all_page_add_button('nfs') is True
        assert COMSHARE.assert_share_view_all_page_enabled_button('nfs', "/mnt/tank/shareone") is True
        assert COMSHARE.assert_share_view_all_page_button_by_name('nfs', "/mnt/tank/shareone", 'edit') is True
        assert COMSHARE.assert_share_view_all_page_button_by_name('nfs', "/mnt/tank/shareone", 'delete') is True
