import pytest
from helper.data_config import get_data_list
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.nfs import NFS


@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
def test_nfs_share_advanced_ui_errors(nfs_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    DATASET.create_dataset_by_api(nfs_data['api_path'], 'NFS')
    COMSHARE.create_share_by_api('nfs', '', nfs_data['api_path'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs')

    # Trigger the maproot user required error
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
    COM.set_checkbox('enabled')
    COMSHARE.click_advanced_options()
    NFS.set_maproot_group('admin')
    WebUI.delay(1)
    COM.click_save_button()

    # Assert error message displays and saving disabled
    assert NFS.assert_error_nfs_share_maproot_user_required()
    assert COM.is_save_button_disabled()
    NFS.unset_maproot_group()

    # Trigger mapall user override error
    NFS.set_maproot_user('admin')
    NFS.set_mapall_user('admin')
    WebUI.delay(1)
    COM.click_save_button()

    # Assert error message displays and saving disabled
    assert NFS.assert_error_nfs_share_mapall_user_override()
    assert COM.is_save_button_disabled()
    NFS.unset_maproot_user()
    NFS.unset_mapall_user()
    WebUI.delay(1)
    COM.select_then_deselect_input_field('comment')

    # Trigger invalid ip error
    NFS.click_add_networks_button()
    NFS.set_network('1')

    # Assert error message displays and saving disabled
    assert NFS.assert_error_nfs_share_network_invalid_ip()
    assert COM.is_save_button_disabled()
    NFS.click_remove_from_list_button()
    WebUI.delay(1)

    # Trigger network is required error
    NFS.click_add_networks_button()
    NFS.set_network_mask('32')

    # Assert error message displays and saving disabled
    assert NFS.assert_error_nfs_share_network_is_required()
    assert COM.is_save_button_disabled()
    NFS.click_remove_from_list_button()
    WebUI.delay(1)

    # Trigger Authorized Hosts and IP addresses is required error
    NFS.click_add_hosts_button()
    NFS.set_host_and_ip('')
    WebUI.delay(1)

    # Assert error message displays and saving disabled
    assert NFS.assert_error_nfs_share_authorized_hosts_required()
    assert COM.is_save_button_disabled()
    NFS.click_remove_from_list_button()
    WebUI.delay(1)

    # Verify share still in original state when editing is cancelled
    COM.close_right_panel()
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
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    NAV.navigate_to_dashboard()
