import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.directory_services import Directory_Services as DS
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.permissions import Permissions as PERM
from keywords.ssh.smb import SSH_SMB as SSHSMB
from keywords.webui.smb import SMB


@allure.tag("SMB", "AD")
@allure.epic("Shares")
@allure.feature("SMB-AD")
@pytest.mark.parametrize('ad_data', get_data_list('ad_credentials'), scope='class')
class Test_SMB_AD_User:

    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self, ad_data) -> None:
        """
        This method sets up each test to start with datasets and shares to execute SMB Guest functionality
        """
        # Environment setup
        NAV.navigate_to_directory_services()
        DS.remove_ldap()
        API_DELETE.delete_share('smb', 'SMBADUSER')
        API_DELETE.delete_dataset('tank/SMBADUSER')
        API_PUT.set_nameservers(ad_data['nameserver'])
        API_PUT.join_active_directory(ad_data['username'], ad_data['password'], ad_data['domain'])
        API_POST.create_dataset('tank/SMBADUSER', 'SMB')
        API_POST.create_share('smb', 'SMBADUSER', '/mnt/tank/SMBADUSER')
        API_POST.start_service('cifs')
        API_POST.start_service('ssh')

    @pytest.fixture(scope='class', autouse=True)
    def teardown_test(self, ad_data) -> None:
        """
        This method removes datasets and shares after test is run for a clean environment
        """
        # Environment Teardown
        yield
        results = API_POST.leave_active_directory(ad_data['username'], ad_data['password'])
        assert results['state'] == 'SUCCESS', results['results']
        API_DELETE.delete_share('smb', "SMBADUSER")
        API_DELETE.delete_dataset("tank/SMBADUSER")

    @allure.tag("Read")
    @allure.story("Verify SMB AD user can access Share")
    def test_ad_user_can_connect_to_new_smb_share(self, ad_data) -> None:

        # Verify SMB AD user can access Share
        assert SMB.assert_user_can_access('SMBADUSER', ad_data['username'], ad_data['password']) is True

    @allure.tag("Delete")
    @allure.story("Verify SMB AD user can access after reboot")
    def test_ad_user_can_access_after_reboot(self, ad_data) -> None:

        # Verify SMB AD user can access after reboot
        assert SSHSMB.assert_user_can_put_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True
        assert SSHSMB.assert_user_can_delete_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True
        assert SSHSMB.assert_user_can_put_directory('Documents', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True
        assert SSHSMB.assert_user_can_delete_directory('Documents', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True
        API_POST.reboot_system()
        COM.set_login_form(private_config['USERNAME'], private_config['PASSWORD'])
        assert SSHSMB.assert_user_can_put_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True
        assert SSHSMB.assert_user_can_delete_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True
        assert SSHSMB.assert_user_can_put_directory('Documents', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True
        assert SSHSMB.assert_user_can_delete_directory('Documents', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True

    @allure.tag("Delete")
    @allure.story("Verify SMB AD user can delete file")
    def test_ad_user_can_delete_file(self, ad_data) -> None:

        # Verify SMB AD user can delete file
        SSHSMB.assert_user_can_put_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True)
        assert SSHSMB.assert_user_can_delete_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True

    @allure.tag("Create")
    @allure.story("Verify SMB AD user can edit file")
    def test_ad_user_can_edit_file(self, ad_data) -> None:

        # Verify SMB Guest can edit file
        assert SSHSMB.assert_user_can_put_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True

    @allure.tag("Read")
    @allure.story("Verify SMB AD user denied edit file with read permissions")
    def test_ad_user_denied_edit_file_with_read_permissions(self, ad_data) -> None:

        # Verify SMB Guest denied edit file with read permissions
        assert SSHSMB.assert_user_can_delete_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is True
        NAV.navigate_to_shares()
        SMB.click_edit_share_filesystem_acl('SMBADUSER')
        COM.click_on_element('//*[contains(text(),"domain users")]/ancestor::ix-permissions-item/following-sibling::*/ix-icon')
        COM.click_on_element('//*[contains(text(),"domain admins")]/ancestor::ix-permissions-item/following-sibling::*/ix-icon')
        PERM.select_ace_who('user')
        PERM.select_ace_user(f'AD03\\{ad_data["username"].lower()}')
        PERM.set_ace_permissions('READ')
        PERM.click_save_acl_button()
        assert SSHSMB.assert_user_can_put_file('putfile', 'SMBADUSER', ad_data['username'], ad_data['password'], True) is False
