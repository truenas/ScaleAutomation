import allure
import pytest
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.permissions import Permissions as PERM
from keywords.webui.system_services import System_Services as SERVICE
from keywords.webui.smb import SMB


@allure.tag("SMB", "Guest")
@allure.epic("Shares")
@allure.feature("SMB-Guest")
class Test_SMB:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method sets up each test to start with datasets and shares to execute SMB Guest functionality
        """
        # Environment setup
        API_DELETE.delete_share('smb', 'SMBGUEST')
        API_DELETE.delete_dataset('tank/SMBGUEST')
        API_POST.create_dataset('tank/SMBGUEST', 'SMB')
        API_POST.create_share('smb', 'SMBGUEST', '/mnt/tank/SMBGUEST', True)
        NAV.navigate_to_shares()
        SMB.click_edit_share_filesystem_acl('SMBGUEST')
        PERM.select_ace_who('user')
        PERM.select_ace_user('smbguest')
        PERM.set_ace_permissions('FULL CONTROL')
        PERM.click_save_acl_button()
        SERVICE.start_service_by_api('cifs')
        SERVICE.start_service_by_api('ssh')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self) -> None:
        """
        This method removes datasets and shares after test is run for a clean environment
        """
        # Environment Teardown
        SSH.delete_smb_test_files('smbuser')
        assert SSH.assert_file_not_exist('smbuser', 'putfile') is True
        COMSHARE.delete_share_by_api('smb', "SMBGUEST")
        DATASET.delete_dataset_by_api("tank/SMBGUEST")

    def test_guest_user_can_connect_to_new_smb_share(self) -> None:

        # Set SMB Share ACL Permissions
        assert SMB.assert_guest_access('SMBGUEST','smbuser', 'testing') is True
