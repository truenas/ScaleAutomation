import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.ssh.common import Common_SSH as SSH
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.services import Services as SERVICE
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.smb import SMB


@pytest.mark.parametrize('user_data', get_data_list('user'))
@pytest.mark.parametrize('smb_data', get_data_list('shares/smb_acl'))
def test_connect_to_new_smb_share(user_data, smb_data) -> None:
    # Environment setup
    COM.create_non_admin_user_by_api(smb_data['user'], smb_data['user']+' Full', 'testing', 'true')
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
    DATASET.create_dataset_by_api(smb_data['path'], 'SMB')
    COMSHARE.create_share_by_api('smb', smb_data['name'], smb_data['path'])
    DATASET.set_dataset_permissions_user_and_group_by_api(smb_data['path'], smb_data['user'], smb_data['user'])
    payload = DATASET.set_dataset_acl_user_and_group_payload('FULL_CONTROL', 'FULL_CONTROL')
    DATASET.set_dataset_acl_by_api('/mnt/'+smb_data['path'], 'NFS4', payload)
    SERVICE.start_service_by_api('cifs')
    SERVICE.start_service_by_api('ssh')

    # Set SMB Share ACL Permissions
    userid = COM.get_user_uid_by_api(smb_data['user'])
    SMB.add_smb_acl_entry_by_api(smb_data['who'], userid, smb_data['perm'], smb_data['permtype'])
    SMB.set_smb_acl_by_api(smb_data['name'])
    SERVICE.restart_service_by_api('cifs')

    # # Add SMB Files
    SSH.add_smb_test_files(smb_data['user'], smb_data['path'], private_config['IP'])
    assert SSH.verify_read_permission(smb_data['user'], smb_data['read'])
    assert SSH.verify_write_permission(smb_data['user'], smb_data['write'])
    assert SSH.verify_exec_permission(smb_data['user'], smb_data['execute'])
    assert SSH.verify_delete_permission(smb_data['user'], smb_data['delete'])

    # SMB.click_add_share_button()
    # COMSHARE.set_share_path(smb_data['path'])
    # COMSHARE.set_share_name(smb_data['name'])
    # SMB.set_share_purpose(smb_data['purpose'])
    # COMSHARE.set_share_description(smb_data['description'])
    # COM.set_checkbox('enabled')
    # COM.click_save_button()
    # SMB.confirm_smb_service_dialog()
    #
    # # Verify Share attached to Dataset
    # NAV.navigate_to_datasets()
    # DATASET.expand_dataset('tank')
    # DATASET.select_dataset(smb_data['name'])
    # assert DATASET.assert_dataset_share_attached(smb_data['name'])
    # assert DATASET.assert_dataset_roles_smb_icon(smb_data['name'])
    #
    # # Verify share on share page
    # NAV.navigate_to_shares()
    # assert COMSHARE.assert_share_name('smb', smb_data['name'])
    # assert COMSHARE.assert_share_path('smb', smb_data['path'])
    # assert COMSHARE.assert_share_description('smb', smb_data['description'])
    # assert COMSHARE.is_share_enabled('smb', smb_data['name'])
    #
    # # Environment Teardown
    # COMSHARE.delete_share_by_api('smb', smb_data['name'])
    # DATASET.delete_dataset_by_api(smb_data['path'])
    # COM.delete_user_by_api('testuser')
    # NAV.navigate_to_dashboard()
