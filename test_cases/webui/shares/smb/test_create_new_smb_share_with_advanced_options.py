import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.smb import SMB


@pytest.mark.parametrize('user_data', get_data_list('user'))
@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'))
@pytest.mark.parametrize('smb_acl_data', get_data_list('shares/smb_acl'))
def test_create_new_smb_share_with_advanced_options(user_data, smb_data, smb_acl_data) -> None:
    # Environment setup
    COM.create_non_admin_user_by_api(smb_acl_data['user'], smb_acl_data['user'] + ' Full', 'testing', 'True')
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    # note creating 'generic' dataset will cause smb share creation to prompt for acl configuration
    DATASET.create_dataset_by_api(smb_data['path'])

    COM.login_to_truenas(user_data['username'], user_data['password'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('smb')

    # Add SMB Share
    running = COM.is_service_running('service-status-cifs')
    COMSHARE.click_add_share_button('smb')
    COMSHARE.set_share_path(smb_data['path'])
    COMSHARE.set_share_name(smb_data['name'])
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
    if running:
        SMB.confirm_smb_service_dialog()
        COM.cancel_confirm_dialog()
    else:
        COM.cancel_confirm_dialog()
        SMB.confirm_smb_service_dialog()

    # Verify Advanced Options
    COMSHARE.click_edit_share('smb', smb_data['name'])
    COMSHARE.click_advanced_options()
    assert COM.is_checked('guestok')
    assert COM.is_checked('enable')
    assert SMB.assert_share_watch_list('admin')
    assert SMB.assert_share_ignore_list('nogroup')
    COM.close_right_panel()

    # Environment Teardown
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    COM.delete_user_by_api(smb_acl_data['user'])
    NAV.navigate_to_dashboard()
