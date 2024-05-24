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
def test_create_new_smb_share_with_advanced_options(smb_data) -> None:
    # Environment setup
    API_DELETE.delete_share('smb', smb_data['name'])
    API_DELETE.delete_dataset(smb_data['path'])
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

    # Add Advanced Options
    COMSHARE.click_advanced_options()
    SMB.set_guest_ok()
    SMB.set_audit_logging_enable()
    SMB.set_watch_list('admin')
    SMB.set_ignore_list('nogroup')
    COM.click_save_button()
    # dismiss acl configuration dialog
    # if running:
    COM.cancel_confirm_dialog()
    COMSHARE.handle_share_service_dialog('smb')
    # else:
    #     COM.cancel_confirm_dialog()
    #     COMSHARE.handle_share_service_dialog('smb')

    # Verify Advanced Options
    COMSHARE.click_edit_share('smb', smb_data['name'])
    COMSHARE.click_advanced_options()
    assert COM.is_checked('guestok')
    assert COM.is_checked('enable')
    assert SMB.assert_share_watch_list('admin')
    assert SMB.assert_share_ignore_list('nogroup')
    COM.close_right_panel()

    # Environment Teardown
    API_DELETE.delete_share('smb', smb_data['name'])
    API_DELETE.delete_dataset(smb_data['path'])
    NAV.navigate_to_dashboard()
