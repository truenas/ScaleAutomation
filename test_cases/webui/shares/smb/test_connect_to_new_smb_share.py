import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.ssh.common import Common_SSH as SSH
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.system_services import System_Services as SERVICE
from keywords.webui.smb import SMB


@pytest.mark.parametrize('smb_data', get_data_list('shares/smb_acl'))
def test_connect_to_new_smb_share(smb_data) -> None:
    # Environment setup
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
    assert SSH.verify_smb_share_read_permission(smb_data['user'], smb_data['read'])
    assert SSH.verify_smb_share_write_permission(smb_data['user'], smb_data['write'])
    assert SSH.verify_smb_share_exec_permission(smb_data['user'], smb_data['execute'])
    assert SSH.verify_smb_share_delete_permission(smb_data['user'], smb_data['delete'])

    # # Environment Teardown
    SSH.delete_smb_test_files(smb_data['user'])
    assert SSH.assert_file_not_exist(smb_data['user'], 'putfile')
    COMSHARE.delete_share_by_api('smb', smb_data['name'])
    DATASET.delete_dataset_by_api(smb_data['path'])
