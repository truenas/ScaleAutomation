import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.nfs import NFS


@pytest.mark.parametrize('user_data', get_data_list('user'))
@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
def test_create_new_nfs_share(user_data, nfs_data) -> None:
    # set up environment prior to testing
    COMSHARE.delete_share_by_api('nfs', nfs_data['path'])
    DATASET.delete_dataset_by_api(nfs_data['path'])
    DATASET.create_dataset_by_api(nfs_data['path'], 'NFS')
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs')
    # Create new NFS share
    COMSHARE.click_add_share_button('nfs')
    COMSHARE.set_share_path(nfs_data['path'])
    COMSHARE.set_share_description(nfs_data['description'])
    COM.set_checkbox('enabled')
    COM.click_save_button()
    # Handle start/restart service popup
    COMSHARE.handle_share_service_dialog('nfs')
    # Verify share attachment to dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(nfs_data['dataset_name'])
    assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs')
    assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs')
    # Verify share displayed on shares page
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_path('nfs', nfs_data['full_path'])
    assert COMSHARE.assert_share_description('nfs', nfs_data['description'])
    assert COMSHARE.is_share_enabled('nfs', nfs_data['full_path'])

    # clean up
    COMSHARE.delete_share_by_api('nfs', nfs_data['path'])
    DATASET.delete_dataset_by_api(nfs_data['path'])
    NAV.navigate_to_dashboard()