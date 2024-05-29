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
def test_edit_smb_share(smb_data) -> None:
    # Environment setup
    API_DELETE.delete_share('smb', smb_data['name'])
    API_DELETE.delete_share('smb', smb_data['name_alt'])
    API_DELETE.delete_dataset(smb_data['path'])
    API_DELETE.delete_dataset(smb_data['path_alt'])
    API_POST.start_service('cifs')
    API_POST.create_dataset(smb_data['path'], 'SMB')
    API_POST.create_dataset(smb_data['path_alt'], 'SMB')
    API_POST.create_share('smb', smb_data['name'], "/mnt/"+smb_data['path'])

    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('smb')

    # Edit SMB Share
    COMSHARE.click_edit_share('smb', smb_data['name'])
    COMSHARE.set_share_name(smb_data['name_alt'])
    COMSHARE.set_share_path(smb_data['path_alt'])
    SMB.set_share_purpose(smb_data['purpose_alt'])
    COMSHARE.set_share_description(smb_data['description_alt'])
    COM.unset_checkbox('enabled')
    COM.click_save_button()
    COMSHARE.handle_share_service_dialog('smb', 'restart')

    # Verify Share attached to Dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(smb_data['name_alt'])
    assert DATASET.assert_dataset_share_attached(smb_data['name_alt'], 'smb')
    assert DATASET.assert_dataset_roles_share_icon(smb_data['name_alt'], 'smb')

    # Verify share on share page
    NAV.navigate_to_shares()
    assert not COMSHARE.assert_share_name('smb', smb_data['name'])
    assert COMSHARE.assert_share_name('smb', smb_data['name_alt'])
    assert COMSHARE.assert_share_path('smb', smb_data['path_alt'])
    assert COMSHARE.assert_share_description('smb', smb_data['description_alt'])
    assert not COMSHARE.is_share_enabled('smb', smb_data['name_alt'])

    # Environment Teardown
    API_DELETE.delete_share('smb', smb_data['name'])
    API_DELETE.delete_dataset(smb_data['path'])
    API_DELETE.delete_share('smb', smb_data['name_alt'])
    API_DELETE.delete_dataset(smb_data['path_alt'])
    NAV.navigate_to_dashboard()
