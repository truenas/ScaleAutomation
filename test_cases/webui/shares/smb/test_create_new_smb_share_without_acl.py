import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.smb import SMB


@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'))
def test_create_new_smb_share_without_acl(smb_data) -> None:
    # Environment setup
    API_DELETE.delete_share('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    # note creating 'generic' dataset will cause smb share creation to prompt for acl configuration
    API_POST.create_dataset(smb_data['path'])

    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('smb')

    # Add SMB Share
    running = COMSHARE.is_share_service_running('cifs')
    COMSHARE.click_add_share_button('smb')
    COMSHARE.set_share_name(smb_data['name'])
    COMSHARE.set_share_path(smb_data['path'])
    SMB.set_share_purpose(smb_data['purpose'])
    COMSHARE.set_share_description(smb_data['description'])
    COM.set_checkbox('enabled')
    COM.click_save_button()
    # dismiss acl configuration dialog
    if running:
        COMSHARE.handle_share_service_dialog('smb')
        COM.cancel_confirm_dialog()
    else:
        COM.cancel_confirm_dialog()
        COMSHARE.handle_share_service_dialog('smb')

    # Verify Share attached to Dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(smb_data['name'])
    assert DATASET.assert_dataset_share_attached(smb_data['name'], 'smb')
    assert DATASET.assert_dataset_roles_share_icon(smb_data['name'], 'smb')

    # Verify share on share page
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_name('smb', smb_data['name'])
    assert COMSHARE.assert_share_path('smb', smb_data['path'])
    assert COMSHARE.assert_share_description('smb', smb_data['description'])
    assert COMSHARE.is_share_enabled('smb', smb_data['name'])

    # Environment Teardown
    API_DELETE.delete_share('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    NAV.navigate_to_dashboard()
