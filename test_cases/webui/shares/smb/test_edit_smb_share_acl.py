import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.permissions import Permissions as PERM
from keywords.webui.smb import SMB


@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'))
def test_edit_smb_share_acl(smb_data) -> None:
    # Environment setup
    API_DELETE.delete_share('smb', smb_data['name'])
    API_DELETE.delete_dataset(smb_data['path'])
    # note creating 'generic' dataset will cause smb share creation to prompt for acl configuration
    API_POST.create_dataset(smb_data['path'])
    API_POST.create_share('smb', smb_data['name'], "/mnt/"+smb_data['path'])

    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('smb') is True

    # Edit ACL Permissions
    SMB.click_edit_share_filesystem_acl(smb_data['name'])
    if COM.assert_page_header('Select a preset ACL'):
        COM.click_button('cancel')
    assert COM.assert_page_header('Edit ACL') is True
    PERM.set_dataset_owner(smb_data['acl_owner'])
    PERM.set_dataset_owner_group(smb_data['acl_group'])
    COM.set_checkbox('apply-owner')
    COM.set_checkbox('apply-group')
    PERM.click_save_acl_button()

    # Verify ACL Permissions of Dataset
    COM.assert_page_header('Datasets')
    assert DATASET.assert_dataset_selected(smb_data['name']) is True
    assert DATASET.assert_dataset_owner(smb_data['acl_owner']) is True
    assert DATASET.assert_dataset_group(smb_data['acl_group']) is True

    # Environment Teardown
    API_DELETE.delete_share('smb', smb_data['name'])
    API_DELETE.delete_dataset(smb_data['path'])
    NAV.navigate_to_dashboard()
