import pytest
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('user_data', get_data_list('user'))
@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'))
def test_delete_new_smb_share(user_data, smb_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    DATASET.create_dataset_by_api(smb_data['path'], 'SMB')
    COMSHARE.create_share_by_api('smb', smb_data['name'], smb_data['path'])

    COM.login_to_truenas(user_data['username'], user_data['password'])
    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('smb')
    COMSHARE.assert_share_name('smb', smb_data['name'])

    COMSHARE.click_delete_share('smb', smb_data['name'])
    COM.assert_confirm_dialog()

    assert not COMSHARE.is_share_visible('smb', smb_data['name'])

    # Environment Teardown
    DATASET.delete_dataset_by_api(smb_data['path'])
    NAV.navigate_to_dashboard()
