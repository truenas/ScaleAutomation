import allure
import pytest

from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.permissions import Permissions as PERM
from keywords.webui.smb import SMB


@allure.tag("SMB", "Guest")
@allure.epic("Shares")
@allure.feature("SMB-Guest")
class Test_SMB_Guest_User:

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
        API_POST.create_non_admin_user('smbguest', 'smbguest Full', 'testing', 'True')
        NAV.navigate_to_shares()
        SMB.click_edit_share_filesystem_acl('SMBGUEST')
        PERM.select_ace_who('user')
        PERM.select_ace_user('nobody')
        PERM.set_ace_permissions('FULL CONTROL')
        PERM.click_save_acl_button()
        API_POST.start_service('cifs')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self) -> None:
        """
        This method removes datasets and shares after test is run for a clean environment
        """
        # Environment Teardown
        yield
        API_DELETE.delete_share('smb', "SMBGUEST")
        API_DELETE.delete_dataset("tank/SMBGUEST")
        API_DELETE.delete_user('smbguest')

    @allure.tag("Read")
    @allure.story("Verify SMB Guest can access Share")
    def test_guest_user_can_connect_to_new_smb_share(self) -> None:

        # Verify SMB Guest can access Share
        assert SMB.assert_guest_access('SMBGUEST') is True

    @allure.tag("Delete")
    @allure.story("Verify SMB Guest can delete file")
    def test_guest_user_can_delete_file(self) -> None:

        # Verify SMB Guest can delete file
        assert SMB.assert_guest_put_file('putfile', 'SMBGUEST') is True
        assert SMB.assert_guest_delete_file('putfile', 'SMBGUEST') is True

    @allure.tag("Create")
    @allure.story("Verify SMB Guest can edit file")
    def test_guest_user_can_edit_file(self) -> None:

        # Verify SMB Guest can edit file
        assert SMB.assert_guest_put_file('putfile', 'SMBGUEST') is True

    @allure.tag("Read")
    @allure.story("Verify SMB Guest denied edit file with read permissions")
    def test_guest_user_denied_edit_file_with_read_permissions(self) -> None:

        # Verify SMB Guest denied edit file with read permissions
        NAV.navigate_to_shares()
        SMB.click_edit_share_filesystem_acl('SMBGUEST')
        PERM.select_ace_who('user')
        PERM.select_ace_user('nobody')
        PERM.set_ace_permissions('READ')
        PERM.click_save_acl_button()
        assert SMB.assert_guest_put_file('putfile', 'SMBGUEST') is False
