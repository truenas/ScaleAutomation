import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.permissions import Permission as PERM
from keywords.webui.smb import SMB


@pytest.mark.parametrize('user_data', get_data_list('user'))
@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'))
def test_edit_smb_share_acl(user_data, smb_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    # note creating 'generic' dataset will cause smb share creation to prompt for acl configuration
    DATASET.create_dataset_by_api(smb_data['path'])
    COMSHARE.create_share_by_api('smb', smb_data['name'], smb_data['path'])

    COM.login_to_truenas(user_data['username'], user_data['password'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('smb')

    # Edit ACL Permissions
    SMB.click_edit_share_filesystem_acl(smb_data['name'])
    if COM.assert_page_header('Select a preset ACL'):
        COM.click_button('cancel')
    assert COM.assert_page_header('Edit ACL')
    PERM.set_dataset_owner(smb_data['acl_owner'])
    PERM.set_dataset_owner_group(smb_data['acl_group'])
    COM.set_checkbox('apply-owner')
    COM.set_checkbox('apply-group')
    COM.click_button('save-acl')

    # Verify ACL Permissions of Dataset
    COM.assert_page_header('Datasets')
    assert DATASET.assert_dataset_selected(smb_data['name'])
    assert DATASET.assert_dataset_owner(smb_data['acl_owner'])
    assert DATASET.assert_dataset_group(smb_data['acl_group'])

    # Environment Teardown
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    NAV.navigate_to_dashboard()
