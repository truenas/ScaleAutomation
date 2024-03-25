import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.iscsi import API_ISCSI
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.common_shares import Common_Shares
from keywords.webui.iscsi import iSCSI
from keywords.webui.navigation import Navigation


@allure.tag('Read Only Admin', 'Shares', 'Permissions')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
@pytest.mark.parametrize('data', get_data_list('read_only_admin_shares'), scope='class')
class Test_Read_Only_Admin_Share:
    """
    This test class tests read-only admin share
    """

    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self, data):
        API_POST.create_read_only_admin(data['username'], data['fullname'], data['password'])
        API_ISCSI.create_iscsi_share(data['iscsi_name'], data['pool_name'], int(data['lunid']))
        API_POST.start_service('iscsitarget')
        API_POST.create_dataset(f'{data["pool_name"]}/{data["nfs_name"]}', 'NFS')
        API_POST.create_share('nfs', data['nfs_name'], f"/mnt/{data['pool_name']}/{data['nfs_name']}",
                              comment=data['nfs_description'])
        API_POST.start_service('nfs')

        Common.logoff_truenas()
        Common.login_to_truenas(data['username'], data['password'])

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_test(self, data):
        yield
        API_ISCSI.delete_iscsi_share(data['iscsi_name'], data['pool_name'], int(data['lunid']))
        API_DELETE.delete_share('nfs', f"{data['pool_name']}/{data['nfs_name']}")
        API_DELETE.delete_dataset(f"{data['pool_name']}/{data['nfs_name']}", force=True)

        Common.logoff_truenas()
        Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
        API_DELETE.delete_user(data['username'])

    @allure.tag("Read", 'iSCSI')
    @allure.story("Read Only Admin Is Able To View Pre-Configured iSCSI Shares")
    def test_read_only_admin_is_able_to_view_pre_configured_iscsi_shares(self, data):
        """
        This test verifies the read-only admin can view pre-configured iSCSI shares.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin can view pre-configured iSCSI shares
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        assert Common_Shares.assert_iscsi_target_is_visible(data['iscsi_name_xpath']) is True

    def test_read_only_is_not_able_enable_or_disable_iscsi_service(self, data):
        """
        This test verifies the read-only admin is not able to enable or disable the NFS service.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to disable the NFS service
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        assert Common_Shares.assert_disable_share_service_is_locked_and_not_clickable('iscsi') is True
        assert Common_Shares.is_share_service_running('iscsitarget') is True

        # Verify the read-only admin is not able to enable the NFS service
        API_POST.stop_service('iscsitarget')
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        assert Common_Shares.assert_enable_share_service_is_locked_and_not_clickable('iscsi') is True
        assert Common_Shares.is_share_service_stopped('iscsitarget') is True

    @allure.tag("Update", 'iSCSI')
    @allure.story("Read Only Admin Is Not Able To Create And Modify An iSCSI Share")
    def test_read_only_admin_is_not_able_to_create_and_modify_an_iscsi_shares(self, data):
        """
        This test verifies the read-only admin is not able to create and modify an iSCSI share.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        assert Common_Shares.assert_share_card_displays('iscsi') is True

        # Verify the read-only admin is not able to create an iSCSI share
        assert Common_Shares.assert_iscsi_configure_button_is_locked_and_not_clickable() is True
        assert Common_Shares.assert_iscsi_wizard_button_is_locked_and_not_clickable() is True

        # Verify the read-only admin is not able to modify an iSCSI share
        Common_Shares.click_edit_iscsi_target(data['iscsi_name_xpath'])
        assert iSCSI.assert_edit_iscsi_target_panel_header() is True
        assert Common.assert_header_readonly_badge() is True

        iSCSI.set_target_alias_input(data['target_alias'])
        assert Common.assert_save_button_is_locked_and_not_clickable() is True

        Common.close_right_panel()

    @allure.tag("Delete", 'iSCSI')
    @allure.story("Read Only Admin Is Not Able To Delete An iSCSI Share")
    def test_read_only_admin_is_not_able_to_delete_an_iscsi_share(self, data):
        """
        This test verifies the read-only admin is not able to delete an iSCSI share.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        assert Common_Shares.assert_share_card_displays('iscsi') is True

        # Verify the read-only admin is not able to delete an iSCSI share
        assert Common_Shares.assert_iscsi_delete_button_is_locked_and_not_clickable(data['iscsi_name_xpath']) is True

    def test_read_only_admin_is_able_to_view_pre_configured_nfs_shares(self, data):
        """
        This test verifies the read-only admin can view pre-configured NFS shares.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin can view pre-configured iSCSI shares
        assert Common_Shares.assert_share_card_displays('nfs') is True
        assert Common_Shares.assert_share_name('nfs', data['nfs_name']) is True
        assert Common_Shares.assert_share_description('nfs', data['nfs_description']) is True

    def test_read_only_is_not_able_enable_or_disable_nfs_service(self, data):
        """
        This test verifies the read-only admin is not able to enable or disable the NFS service.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to enable or disable the NFS service
        assert Common_Shares.assert_share_card_displays('nfs') is True
        assert Common_Shares.assert_disable_share_service_is_locked_and_not_clickable('nfs') is True
        assert Common_Shares.is_share_service_running('nfs') is True

        API_POST.stop_service('nfs')
        assert Common_Shares.assert_share_card_displays('nfs') is True
        assert Common_Shares.assert_enable_share_service_is_locked_and_not_clickable('nfs') is True
        assert Common_Shares.is_share_service_stopped('nfs') is True



