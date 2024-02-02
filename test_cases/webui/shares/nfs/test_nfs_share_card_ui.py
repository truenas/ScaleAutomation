import pytest

from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
def test_nfs_share_card_ui(nfs_data) -> None:
    # Environment setup
    DATASET.delete_dataset_by_api("tank/shareone")
    DATASET.delete_dataset_by_api("tank/sharetwo")
    DATASET.delete_dataset_by_api("tank/sharethree")
    DATASET.delete_dataset_by_api("tank/sharefour")
    DATASET.delete_dataset_by_api("tank/sharefive")
    # create_multiple_shares(five)
    COMSHARE.delete_share_by_api('nfs', "tank/shareone")
    COMSHARE.delete_share_by_api('nfs', "tank/sharetwo")
    COMSHARE.delete_share_by_api('nfs', "tank/sharethree")
    COMSHARE.delete_share_by_api('nfs', "tank/sharefour")
    COMSHARE.delete_share_by_api('nfs', "tank/sharefive")
    
    # Create more than four NFS Shares to trigger the "View All" button
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
    NAV.navigate_to_shares()

    # Verify NFS Card on Sharing page UI
    assert COMSHARE.assert_share_card_displays('nfs')
    assert COMSHARE.is_share_service_stopped('nfs')
    assert COMSHARE.start_share_service_by_actions_menu('nfs')
    assert COMSHARE.stop_share_service_by_actions_menu('nfs')
    assert COMSHARE.assert_share_card_ui_add_button('nfs')
    assert COMSHARE.assert_share_card_ui_actions_menu_button('nfs')
    assert COMSHARE.assert_share_card_row_ui_enabled_button('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_share_card_row_ui_edit_button('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_share_card_row_ui_delete_button('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_share_card_ui_view_all_button('nfs')

    # Verify only four shares display regularly
    assert COMSHARE.assert_share_path('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_share_path('nfs', "/mnt/tank/sharetwo")
    assert COMSHARE.assert_share_path('nfs', "/mnt/tank/sharethree")
    assert COMSHARE.assert_share_path('nfs', "/mnt/tank/sharefour")
    assert not COMSHARE.assert_share_path('nfs', "/mnt/tank/sharefive")

    # Verify all shares display after clicking the View All button
    COM.click_link(f'nfs-share-view-all')
    assert COM.assert_page_header('NFS')
    assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/sharetwo")
    assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/sharethree")
    assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/sharefour")
    assert COMSHARE.assert_view_all_page_share_path('nfs', "/mnt/tank/sharefive")

    # Verify NFS View All page UI
    assert COMSHARE.assert_share_view_all_page_ui_add_button('nfs')
    assert COMSHARE.assert_share_view_all_page_ui_enabled_button('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_share_view_all_page_ui_edit_button('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_share_view_all_page_ui_delete_button('nfs', "/mnt/tank/shareone")

    # clean up
    DATASET.delete_dataset_by_api("tank/shareone")
    DATASET.delete_dataset_by_api("tank/sharetwo")
    DATASET.delete_dataset_by_api("tank/sharethree")
    DATASET.delete_dataset_by_api("tank/sharefour")
    DATASET.delete_dataset_by_api("tank/sharefive")
    COMSHARE.delete_share_by_api('nfs', "tank/shareone")
    COMSHARE.delete_share_by_api('nfs', "tank/sharetwo")
    COMSHARE.delete_share_by_api('nfs', "tank/sharethree")
    COMSHARE.delete_share_by_api('nfs', "tank/sharefour")
    COMSHARE.delete_share_by_api('nfs', "tank/sharefive")
    NAV.navigate_to_dashboard()
