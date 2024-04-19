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
class Test_NFS_Share_Card_UI:
    """
    This test class covers the NFS share card UI test cases.
    """
    @pytest.fixture(scope="function", autouse=True)
    def setup_test(self):
        """
        This fixture creates all the dataset and NFS shares for the test.
        """
        NAV.navigate_to_shares()
        COMSHARE.delete_all_shares_by_share_type('nfs')
        API_POST.stop_service('nfs')
        NAV.navigate_to_dashboard()
        API_POST.create_dataset("tank/shareone", 'NFS')
        API_POST.create_dataset("tank/sharetwo", 'NFS')
        API_POST.create_dataset("tank/sharethree", 'NFS')
        API_POST.create_dataset("tank/sharefour", 'NFS')
        API_POST.create_dataset("tank/sharefive", 'NFS')
        API_POST.create_share('nfs', '', "/mnt/tank/shareone")
        API_POST.create_share('nfs', '', "/mnt/tank/sharetwo")
        API_POST.create_share('nfs', '', "/mnt/tank/sharethree")
        API_POST.create_share('nfs', '', "/mnt/tank/sharefour")
        API_POST.create_share('nfs', '', "/mnt/tank/sharefive")

        # Navigate to the Shares page
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('nfs') is True

    @pytest.fixture(scope="function", autouse=True)
    def tear_down_test(self):
        """
        This fixture deletes all the dataset and NFS shares for the test.
        """
        yield
        API_DELETE.delete_share('nfs', "tank/shareone")
        API_DELETE.delete_share('nfs', "tank/sharetwo")
        API_DELETE.delete_share('nfs', "tank/sharethree")
        API_DELETE.delete_share('nfs', "tank/sharefour")
        API_DELETE.delete_share('nfs', "tank/sharefive")
        API_DELETE.delete_dataset("tank/shareone", recursive=True, force=True)
        API_DELETE.delete_dataset("tank/sharetwo", recursive=True, force=True)
        API_DELETE.delete_dataset("tank/sharethree", recursive=True, force=True)
        API_DELETE.delete_dataset("tank/sharefour", recursive=True, force=True)
        API_DELETE.delete_dataset("tank/sharefive", recursive=True, force=True)

    @allure.tag("Read")
    @allure.story("NFS Share Card UI")
    def test_nfs_share_card_ui(self, nfs_data):
        """
        Summary: This verifies that the NFS share card UI is displayed as expected.

        Test Steps:
        1. This test verifies the following UI elements are displayed:
            - Actions menu button
            - Actions menu start service button
            - Actions menu stop service button
            - Add share button
            - Share enabled slider
            - Share edit button
            - Share delete button
        2. Create 5 shares and verify only 4 are displayed before clicking on View all.
        3. Click on View all and verify that all shares are displayed.
        4. Verify that the share controls previously checked are still displayed after clicking on View all.
        """

        # Verify NFS Card on Sharing page UI
        assert COMSHARE.is_share_service_stopped('nfs') is True
        assert COMSHARE.start_share_service_by_actions_menu('nfs') is True
        assert COMSHARE.stop_share_service_by_actions_menu('nfs') is True
        assert COMSHARE.assert_share_card_add_button('nfs') is True
        assert COMSHARE.assert_share_card_actions_menu_button('nfs') is True
        assert COMSHARE.assert_share_card_enabled_button_by_name('nfs', "/mnt/tank/shareone") is True
        assert COMSHARE.assert_share_card_action_button_by_name('nfs', "/mnt/tank/shareone", 'edit') is True
        assert COMSHARE.assert_share_card_action_button_by_name('nfs', "/mnt/tank/shareone", 'delete') is True
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
