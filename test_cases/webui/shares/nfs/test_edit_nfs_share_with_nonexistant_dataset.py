import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.nfs import NFS


@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
def test_edit_nfs_share_with_nonexistant_dataset(nfs_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    DATASET.create_dataset_by_api(nfs_data['api_path'], 'NFS')
    COMSHARE.create_share_by_api('nfs', '', nfs_data['api_path'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs')

    # Edit the NFS share with nonexistant path
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
    COMSHARE.set_share_path('nonexistant')
    COMSHARE.set_share_description(nfs_data['description'])
    COM.set_checkbox('enabled')
    COM.click_save_button()

    # Assert error message displays and saving disabled
    assert NFS.assert_error_nfs_share_path_nonexistant()
    assert COM.get_save_button_disabled_property()
    COM.close_right_panel()

    # Verify share still in original state when editing is cancelled
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    assert not COMSHARE.assert_share_description('nfs', nfs_data['description'])
    assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path'])

    # Verify share attachment to dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(nfs_data['dataset_name'])
    assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs')
    assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs')

    # clean up
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path_alt'])
    DATASET.delete_dataset_by_api(nfs_data['api_path_alt'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    NAV.navigate_to_dashboard()
