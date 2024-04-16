import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.ssh.common import Common_SSH as SSH
from keywords.ssh.smb import SSH_SMB as SSHSMB
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.system_services import System_Services as SERVICE


@allure.tag("SMB", "Connect")
@allure.epic("Shares")
@allure.feature("SMB-Connect")
@pytest.mark.parametrize('smb_data', get_data_list('shares/smb_acl'))
class Test_SMB_Connect_To_Share:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, smb_data) -> None:
        """
        This method sets up each test to start with datasets and shares to execute SMB Guest functionality
        """
        # Environment setup
        API_DELETE.delete_share('smb', smb_data['name'])
        API_DELETE.delete_dataset(smb_data['path'])
        API_POST.create_dataset(smb_data['path'], 'SMB')
        API_POST.create_share('smb', smb_data['name'], '/mnt/'+smb_data['path'])
        DATASET.set_dataset_permissions_user_and_group_by_api(smb_data['path'], smb_data['user'], smb_data['user'])
        payload = DATASET.set_dataset_acl_user_and_group_payload('FULL_CONTROL', 'FULL_CONTROL')
        DATASET.set_dataset_acl_by_api('/mnt/'+smb_data['path'], 'NFS4', payload)
        SERVICE.start_service_by_api('cifs')
        SERVICE.start_service_by_api('ssh')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, smb_data) -> None:
        """
        This method removes datasets and shares after test is run for a clean environment
        """
        # # Environment Teardown
        yield
        SSHSMB.delete_smb_test_files(smb_data['user'])
        assert SSH.assert_file_exists('putfile', smb_data['path'], private_config['SMB_ACL_IP'], user=smb_data['user'], password='testing') is False
        API_DELETE.delete_share('smb', smb_data['name'])
        API_DELETE.delete_dataset(smb_data['path'])

    @allure.tag("Update")
    @allure.story("Verify SMB user can connect to Share")
    def test_connect_to_new_smb_share(self, smb_data) -> None:
        # Set SMB Share ACL Permissions
        API_POST.add_smb_acl_entry(smb_data['who'], smb_data['id'], smb_data['perm'], smb_data['permtype'])
        API_POST.set_smb_acl(smb_data['name'])
        SERVICE.restart_service_by_api('cifs')

        # # Add SMB Files
        SSHSMB.add_smb_test_files(smb_data['user'], smb_data['path'], private_config['IP'])
        assert SSH.verify_smb_share_read_permission(smb_data['user'], smb_data['read']) is True
        assert SSH.verify_smb_share_write_permission(smb_data['user'], smb_data['write']) is True
        assert SSH.verify_smb_share_exec_permission(smb_data['user'], smb_data['execute']) is True
        assert SSH.verify_smb_share_delete_permission(smb_data['user'], smb_data['delete']) is True

    @allure.tag("Update")
    @allure.story("Verify SMB user can connect to Home Dir Share")
    def test_connect_to_home_directory_smb_share(self, smb_data) -> None:
        # Set user Home Directory
        NAV.navigate_to_local_users()
        LU.expand_user_by_full_name(f'{smb_data["user"]} Full')
        LU.click_user_edit_button()
        LU.set_user_home_directory(f'/mnt/{smb_data["path"]}')
        COM.click_save_button()
        COM.assert_confirm_dialog()

        # Set SMB Share ACL Permissions
        API_POST.add_smb_acl_entry(smb_data['who'], smb_data['id'], smb_data['perm'], smb_data['permtype'])
        API_POST.set_smb_acl(smb_data['name'])
        SERVICE.restart_service_by_api('cifs')

        # # Add SMB Files
        SSHSMB.add_smb_test_files(smb_data['user'], smb_data['path'], private_config['IP'])
        assert SSH.verify_smb_share_read_permission(smb_data['user'], smb_data['read']) is True
        assert SSH.verify_smb_share_write_permission(smb_data['user'], smb_data['write']) is True
        assert SSH.verify_smb_share_exec_permission(smb_data['user'], smb_data['execute']) is True
        assert SSH.verify_smb_share_delete_permission(smb_data['user'], smb_data['delete']) is True
