import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
def test_edit_nfs_share_with_existing_dataset(nfs_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path_alt'])
    DATASET.create_dataset_by_api(nfs_data['api_path'], 'NFS')
    DATASET.create_dataset_by_api(nfs_data['api_path_alt'], 'NFS')
    COMSHARE.create_share_by_api('nfs', '', nfs_data['api_path'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs')

    # Edit the NFS share
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
    COMSHARE.set_share_path(nfs_data['api_path_alt'])
    COMSHARE.set_share_description(nfs_data['description_alt'])
    COM.set_checkbox('enabled')
    COM.click_save_button()

    # Handle start/restart service popup
    COMSHARE.handle_share_service_dialog('nfs')

    # Verify share attachment to new dataset and no attachment to old dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(nfs_data['dataset_name_alt'])
    assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name_alt'], 'nfs')
    assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name_alt'], 'nfs')
    DATASET.select_dataset(nfs_data['dataset_name'])
    assert not DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs')
    assert not DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs')

    # Verify edited share displayed on shares page
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path_alt'])
    assert COMSHARE.assert_share_description('nfs', nfs_data['description_alt'])
    assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path_alt'])
    assert not COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    assert not COMSHARE.assert_share_description('nfs', nfs_data['description'])

    # clean up
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path_alt'])
    DATASET.delete_dataset_by_api(nfs_data['api_path_alt'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    NAV.navigate_to_dashboard()
