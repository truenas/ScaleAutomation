import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.nfs import NFS


@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'))
def test_edit_nfs_share_advanced_options(nfs_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    DATASET.create_dataset_by_api(nfs_data['api_path'], 'NFS')
    COMSHARE.create_share_by_api('nfs', '', nfs_data['api_path'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('nfs')

    # Edit the NFS share with advanced options
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    COMSHARE.click_edit_share('nfs', nfs_data['share_page_path'])
    COM.set_checkbox('enabled')
    NFS.click_add_networks_button()
    WebUI.delay(1)
    NFS.set_network(private_config['NETWORK'])
    WebUI.delay(1)
    NFS.set_network_mask(private_config['MASK'])
    WebUI.delay(1)
    NFS.click_add_hosts_button()
    WebUI.delay(1)
    NFS.set_host_and_ip(private_config['AUTH_HOST'])
    WebUI.delay(1)
    COMSHARE.click_advanced_options()
    COM.set_checkbox('ro')
    NFS.set_maproot_user('admin')
    NFS.set_maproot_group('admin')
    WebUI.delay(1)
    COM.select_then_deselect_input_field('comment')
    WebUI.delay(1)
    NFS.set_security_type('sys')
    WebUI.delay(1)
    COMSHARE.set_share_description(nfs_data['description'])
    COM.select_then_deselect_input_field('comment')
    COM.click_save_button()

    # Handle start/restart service popup
    COMSHARE.handle_share_service_dialog('nfs')

    # Verify share attachment to new dataset and no attachment to old dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(nfs_data['dataset_name'])
    assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs')
    assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs')

    # Verify edited share displayed on shares page
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    assert COMSHARE.assert_share_description('nfs', nfs_data['description'])
    assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path'])

    # Edit the NFS share with second set of advanced options
    WebUI.delay(1)
    COMSHARE.click_edit_share('nfs', nfs_data['share_page_path_with_desc'])
    COMSHARE.click_advanced_options()
    COM.unset_checkbox('ro')
    NFS.unset_maproot_user()
    NFS.unset_maproot_group()
    NFS.set_mapall_user('admin')
    NFS.set_mapall_group('admin')
    WebUI.delay(1)
    COM.select_then_deselect_input_field('comment')
    COM.click_save_button()

    # Verify share attachment to new dataset and no attachment to old dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(nfs_data['dataset_name'])
    assert DATASET.assert_dataset_share_attached(nfs_data['dataset_name'], 'nfs')
    assert DATASET.assert_dataset_roles_share_icon(nfs_data['dataset_name'], 'nfs')

    # Verify edited share displayed on shares page
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_path('nfs', nfs_data['share_page_path'])
    assert COMSHARE.assert_share_description('nfs', nfs_data['description'])
    assert COMSHARE.is_share_enabled('nfs', nfs_data['share_page_path'])

    # clean up
    COMSHARE.delete_share_by_api('nfs', nfs_data['api_path_alt'])
    DATASET.delete_dataset_by_api(nfs_data['api_path_alt'])
    DATASET.delete_dataset_by_api(nfs_data['api_path'])
    NAV.navigate_to_dashboard()
