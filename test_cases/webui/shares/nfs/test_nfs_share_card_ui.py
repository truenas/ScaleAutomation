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
    API_POST.stop_service('nfs')
    DATASET.delete_dataset_by_api("tank/shareone")
    DATASET.delete_dataset_by_api("tank/sharetwo")
    DATASET.delete_dataset_by_api("tank/sharethree")
    DATASET.delete_dataset_by_api("tank/sharefour")
    DATASET.delete_dataset_by_api("tank/sharefive")
    NAV.navigate_to_shares()
    COMSHARE.delete_all_shares_by_sharetype('nfs')

    # Create more than four NFS Shares to trigger the "View All" button
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

    # Verify NFS Card on Sharing page UI
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs')
    assert COMSHARE.is_share_service_stopped('nfs')
    assert COMSHARE.start_share_service_by_actions_menu('nfs')
    assert COMSHARE.stop_share_service_by_actions_menu('nfs')
    assert COMSHARE.assert_share_card_add_button('nfs')
    assert COMSHARE.assert_share_card_actions_menu_button('nfs')
    assert COMSHARE.assert_share_card_enabled_button_by_name('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_share_card_button_by_name('nfs', "/mnt/tank/shareone", 'edit')
    assert COMSHARE.assert_share_card_button_by_name('nfs', "/mnt/tank/shareone", 'delete')
    assert COMSHARE.assert_share_card_view_all_button('nfs')

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
    assert COMSHARE.assert_share_view_all_page_add_button('nfs')
    assert COMSHARE.assert_share_view_all_page_enabled_button('nfs', "/mnt/tank/shareone")
    assert COMSHARE.assert_share_view_all_page_button_by_name('nfs', "/mnt/tank/shareone", 'edit')
    assert COMSHARE.assert_share_view_all_page_button_by_name('nfs', "/mnt/tank/shareone", 'delete')

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
