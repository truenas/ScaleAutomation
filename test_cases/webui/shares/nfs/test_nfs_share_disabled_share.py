import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
def test_nfs_share_disabled_share(nfs_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    DATASET.create_dataset_by_api(nfs_data['api_path'], 'NFS')
    COMSHARE.create_share_by_api('nfs', '', nfs_data['api_path'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs')

    # Disable the NFS share
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
    COM.unset_checkbox('enabled')
    COM.click_save_button()

    # Handle start/restart service popup
    COMSHARE.handle_share_service_dialog('nfs')
    assert not COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path'])

    # Verify share attachment to dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(nfs_data['dataset_name'])
    assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs')
    assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs')

    # Verify share displayed on shares page is disabled
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    assert not COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path'])

    # TODO: Add in CLI test component to ensure share cannot be used when disabled. TE-1415

    # clean up
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    NAV.navigate_to_dashboard()
