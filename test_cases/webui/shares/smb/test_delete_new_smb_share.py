import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'))
def test_delete_new_smb_share(smb_data) -> None:
    # Environment setup
    API_DELETE.delete_share('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    API_POST.create_dataset(smb_data['path'], 'SMB')
    API_POST.create_share('smb', smb_data['name'], "/mnt/"+smb_data['path'])

    NAV.navigate_to_shares()
    assert COMSHARE.assert_share_card_displays('smb')
    COMSHARE.assert_share_name('smb', smb_data['name'])

    COMSHARE.click_delete_share('smb', smb_data['name'])
    COM.assert_confirm_dialog()

    assert not COMSHARE.is_share_visible('smb', smb_data['name'])

    # Environment Teardown
    DATASET.delete_dataset_by_api(smb_data['path'])
    NAV.navigate_to_dashboard()
