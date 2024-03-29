import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.common_shares import Common_Shares
from keywords.webui.navigation import Navigation
from keywords.webui.smb import SMB


@allure.tag('Read Only Admin', 'Shares', 'Permissions', 'SMB')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
@pytest.mark.parametrize('data', get_data_list('read_only_admin_shares'), scope='class')
class Test_Read_Only_Admin_SMB_Share:
    """
    This test class tests read-only admin SMB share permissions.
    """

    @pytest.fixture(scope='function', autouse=True)
    def navigate_to_shares(self):
        """
        This fixture navigates to shares page before each test starts.
        """
        Navigation.navigate_to_shares()

    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self, data):
        API_POST.create_read_only_admin(data['username'], data['fullname'], data['password'])
        API_POST.create_dataset(f'{data["pool_name"]}/{data["smb_name"]}', 'SMB')
        API_POST.create_share('smb', data['smb_name'], f'/mnt/{data["pool_name"]}/{data["smb_name"]}',
                              comment=data['smb_description'])
        API_POST.start_service('cifs')

        Common.logoff_truenas()
        Common.login_to_truenas(data['username'], data['password'])

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_test(self, data):
        yield
        API_DELETE.delete_share('nfs', f"{data['smb_name']}")
        API_DELETE.delete_dataset(f"{data['pool_name']}/{data['smb_name']}", force=True)

        Common.logoff_truenas()
        Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
        API_DELETE.delete_user(data['username'])

    @allure.tag('Read')
    @allure.story("Read Only Admin Is Able To View Pre-Configured SMB Shares On The SMB Card")
    def test_read_only_admin_is_able_to_view_pre_configured_smb_shares_on_the_smb_card(self, data):
        """
        This test verifies the read-only admin is able to view pre-configured SMB shares on the SMB card.
        """
        assert Common_Shares.assert_share_card_displays('smb') is True
        assert Common_Shares.assert_share_name('smb', data['smb_name']) is True
        assert Common_Shares.assert_share_description('smb', data['smb_description']) is True

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Enable Or Disable NFS Service On The SMB Card")
    def test_read_only_is_not_able_enable_or_disable_nfs_service_on_the_smb_card(self, data):
        # Verify the read-only admin is not able to enable or disable the NFS service
        assert Common_Shares.assert_share_card_displays('smb') is True
        assert Common_Shares.assert_disable_share_service_is_locked_and_not_clickable('smb') is True
        assert Common_Shares.is_share_service_running('smb') is True

        API_POST.stop_service('cifs')
        assert Common_Shares.assert_share_card_displays('smb') is True
        assert Common_Shares.assert_enable_share_service_is_locked_and_not_clickable('smb') is True
        assert Common_Shares.is_share_service_stopped('smb') is True

    @allure.tag('Create')
    @allure.story("Read Only Admin Is Not Able To Create An SMB Share On The SMB Card")
    def test_read_only_admin_is_not_able_to_create_an_smb_share_on_the_smb_card(self, data):
        """
        This test verifies the read-only admin is not able to create an SMB share on the SMB card.
        """
        # Verify the read-only admin is not able to create an SMB share
        assert Common_Shares.assert_share_card_displays('smb') is True
        assert Common_Shares.assert_card_add_share_button_is_locked_and_not_clickable('smb') is True

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Disable Or Enable An SMB Share On The SMB Card")
    def test_read_only_admin_is_not_able_to_disable_or_enable_an_smb_shares_on_the_smb_card(self, data):
        """
        This test verifies the read-only admin is not able to disable and enable an SMB share on the SMB card.
        """
        # Verify the read-only admin is not able to disable and enable an SMB share
        assert Common_Shares.assert_share_card_displays('smb') is True
        assert Common_Shares.assert_card_share_enabled_toggle_is_locked_and_disabled('smb', data['smb_xpath']) is True

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Modify An SMB Share On The SMB Card")
    def test_read_only_admin_is_not_able_to_modify_an_smb_share_on_the_smb_card(self, data):
        """
        This test verifies the read-only admin is not able to modify an SMB share on the SMB card.
        """

        # Verify the read-only admin is not able to modify an iSCSI share
        assert Common_Shares.assert_share_card_displays('smb') is True
        Common_Shares.click_edit_share('smb', data['smb_xpath'])
        assert SMB.assert_edit_smb_panel_header() is True
        assert Common.assert_header_readonly_badge() is True

        Common_Shares.set_share_description('This is a new description')
        assert Common.assert_save_button_is_locked_and_not_clickable() is True

        Common.close_right_panel()

    @allure.tag('Delete')
    @allure.story("Read Only Admin Is Not Able To Delete An SMB Share On The SMB Card")
    def test_read_only_admin_is_not_able_to_delete_an_smb_share_on_the_smb_card(self, data):
        """
        This test verifies the read-only admin is not able to delete an SMB share on the SMB card.
        """
        # Verify the read-only admin is not able to delete an SMB share
        assert Common_Shares.assert_share_card_displays('smb') is True
        assert Common_Shares.assert_card_share_delete_button_is_locked_and_not_clickable('smb', data['smb_xpath']) is True

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Edit The SMB Filesystem ACL Permissions On The SMB Card")
    def test_read_only_admin_is_not_able_to_edit_the_smb_filesystem_acl_permissions_on_the_smb_card(self, data):
        """
        This test verifies the read-only admin is not able to edit the SMB filesystem ACL permissions on the SMB card.
        """
        assert Common_Shares.assert_share_card_displays('smb') is True
        assert Common_Shares.assert_card_edit_filesystem_acl_permissions_button_is_locked_and_not_clickable(data['smb_xpath']) is True

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Edit The SMB Share ACL Permissions On The SMB Card")
    def test_read_only_admin_is_not_able_to_edit_the_smb_share_acl_permissions_on_the_smb_card(self, data):
        """
        This test verifies the read-only admin is not able to edit the SMB share ACL permissions on the SMB card.
        """
        assert Common_Shares.assert_share_card_displays('smb') is True
        assert Common_Shares.assert_card_edit_share_acl_permissions_button_is_locked_and_not_clickable(data['smb_xpath']) is True