import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.ssh.common import Common_SSH as SSH
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.services import Services as SERVICE
from keywords.webui.nfs import NFS


@pytest.mark.parametrize('user_data', get_data_list('user'))
@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs_acl'))
def test_connect_to_new_nfs_share(user_data, nfs_data) -> None:
    # Environment setup
    COMSHARE.delete_share_by_api('nfs', nfs_data['sharename'])
    COM.create_non_admin_user_by_api(nfs_data['user'], nfs_data['user'] + ' Full', 'testing', 'True')
    NFS.create_non_admin_share_host_user()
    DATASET.delete_dataset_by_api(nfs_data['path'])
    DATASET.create_dataset_by_api(nfs_data['path'], 'nfs')
    COMSHARE.create_share_by_api('nfs', nfs_data['name'], nfs_data['path'])
    payload = DATASET.set_dataset_acl_user_and_group_payload('FULL_CONTROL', 'FULL_CONTROL')
    DATASET.set_dataset_acl_by_api('/mnt/' + nfs_data['path'], 'NFS4', payload)

    # user should be nobody and group should be nogroup
    DATASET.set_dataset_permissions_user_and_group_by_api(nfs_data['path'], nfs_data['user'], nfs_data['group'])
    SERVICE.start_service_by_api('nfs')
    SERVICE.start_service_by_api('ssh')

    # Verify share unmounted
    # NFS.unmount_NFS_Share('sudo umount /home/jodraj/nfsshares')
    NFS.unmount_nfs_share(nfs_data['path'])

    # Mount share
    # NFS.verify_NFS_Share_Mount(nfs_data['path'])'sudo mount -t nfs 10.234.27.212:/mnt/tank/NFSShare /home/jodraj/nfsshares')
    assert NFS.verify_nfs_share_mounted(nfs_data['path'])

    # Verify base share access
    assert NFS.verify_share_read_access(nfs_data['user'])
    assert NFS.verify_share_write_permission(nfs_data['user'], nfs_data['write'])
    assert NFS.verify_share_exec_permission(nfs_data['user'], nfs_data['execute'])
    assert NFS.verify_share_delete_permission(nfs_data['user'], nfs_data['delete'])

    # Cleanup
    NFS.unmount_nfs_share(nfs_data['path'])
    COMSHARE.delete_share_by_api('nfs', nfs_data['sharename'])
    DATASET.delete_dataset_by_api(nfs_data['path'])
    COM.delete_user_by_api(nfs_data['user'])
# String response = .'ssh.common_SSH.run_Command_And_Get_Output'('sudo umount /home/jodraj/shares')
# 
# // Verify Connect to Share
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo mount -t  10.234.27.212:/mnt/tank/NFSShare /home/jodraj/nfsshares')
# response = .'ssh.common_SSH.run_Command_And_Get_Output'('ls -al /home/jodraj')
# // Verify mount successful
# assert response.contains('nfsshares')
# 
# // Create Directory
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo mkdir /home/jodraj/nfsshares/new-folder')
# response = .'ssh.common_SSH.run_Command_And_Get_Output'('ls -al /home/jodraj/nfsshares')
# assert response.contains('new-folder')
# 
# // Create File
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo touch /home/jodraj/nfsshares/new-folder/newfile.sh')
# response = .'ssh.common_SSH.run_Command_And_Get_Output'('ls -al /home/jodraj/nfsshares/new-folder')
# assert response.contains('newfile.sh')
# 
# // Make file executable
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo chmod 777 /home/jodraj/nfsshares/new-folder/newfile.sh')
# response = .'ssh.common_SSH.run_Command_And_Get_Output'('ls -al /home/jodraj/nfsshares/new-folder')
# assert response.contains('newfile.sh')
# 
# // Execute file
# .'ssh.common_SSH.run_Command_And_Get_Output'("sudo echo 'touch testfile2.txt' >> /home/jodraj/nfsshares/new-folder/newfile.sh")
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo tail /home/jodraj/nfsshares/new-folder/newfile.sh')
# .'ssh.common_SSH.run_Command_And_Get_Output'('cd /home/jodraj/nfsshares/new-folder; sudo ./newfile.sh')
# response = .'ssh.common_SSH.run_Command_And_Get_Output'('ls -al /home/jodraj/nfsshares/new-folder')
# assert response.contains('testfile2.txt')
# 
# // clean up
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo rm /home/jodraj/nfsshares/new-folder/newfile.sh')
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo rm /home/jodraj/nfsshares/new-folder/testfile2.txt')
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo rmdir /home/jodraj/nfsshares/new-folder')
# response = .'ssh.common_SSH.run_Command_And_Get_Output'('ls -al /home/jodraj/nfsshares')
# assert !response.contains('new-folder')
# 
# .'ssh.common_SSH.run_Command_And_Get_Output'('sudo umount /home/jodraj/nfsshares')
# response = .'ssh.common_SSH.run_Command_And_Get_Output'('mount')
# assert !response.contains('nfsshares')
# 
# api_DELETE.delete_NFSShare'(strSharename)
# api_DELETE.delete_Dataset'(strDataset)
#
