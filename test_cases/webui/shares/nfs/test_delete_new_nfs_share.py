import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
def test_delete_new_nfs_share(nfs_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    DATASET.create_dataset_by_api(nfs_data['api_path'], 'NFS')
    COMSHARE.create_share_by_api('nfs', '', nfs_data['api_path'])

    # Delete NFS share
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs')
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    COMSHARE.click_delete_share('nfs', nfs_data['share_page_path'])
    COM.assert_confirm_dialog()

    # Verify share detached from dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(nfs_data['dataset_name'])
    assert not DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs')
    assert not DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs')

    # Verify share deleted from Shares page
    NAV.navigate_to_shares()
    assert not COMSHARE.is_share_visible('nfs', nfs_data['share_page_path'])
    
    # Environment Teardown
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    NAV.navigate_to_dashboard()
