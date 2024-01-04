import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.smb import SMB


@pytest.mark.parametrize('user_data', get_data_list('user'))
@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'))
def test_edit_smb_share(user_data, smb_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    DATASET.create_dataset_by_api(smb_data['path'], 'SMB')
    DATASET.create_dataset_by_api(smb_data['path_alt'], 'SMB')
    COMSHARE.create_share_by_api('smb', smb_data['name'], smb_data['path'])

    COM.login_to_truenas(user_data['username'], user_data['password'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('smb')

    # Edit SMB Share
    COMSHARE.click_edit_share('smb', smb_data['name'])
    COMSHARE.set_share_path(smb_data['path_alt'])
    COMSHARE.set_share_name(smb_data['name_alt'])
    SMB.set_share_purpose(smb_data['purpose_alt'])
    COMSHARE.set_share_description(smb_data['description_alt'])
    COM.unset_checkbox('enabled')
    COM.click_save_button()
    SMB.confirm_smb_service_dialog()

    # Verify Share attached to Dataset
    NAV.navigate_to_datasets()
    DATASET.expand_dataset('tank')
    DATASET.select_dataset(smb_data['name_alt'])
    assert DATASET.assert_dataset_share_attached(smb_data['name_alt'])
    assert DATASET.assert_dataset_roles_smb_icon(smb_data['name_alt'])

    # Verify share on share page
    NAV.navigate_to_shares()
    assert not COMSHARE.assert_share_name('smb', smb_data['name'])
    assert COMSHARE.assert_share_name('smb', smb_data['name_alt'])
    assert COMSHARE.assert_share_path('smb', smb_data['path_alt'])
    assert COMSHARE.assert_share_description('smb', smb_data['description_alt'])
    assert COMSHARE.is_share_enabled('smb', smb_data['name_alt'])

    # Environment Teardown
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    COMSHARE.delete_share_by_api('smb', smb_data['name_alt'])
    DATASET.delete_dataset_by_api(smb_data['path_alt'])
    NAV.navigate_to_dashboard()
