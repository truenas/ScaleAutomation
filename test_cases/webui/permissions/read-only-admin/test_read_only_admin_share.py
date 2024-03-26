import allure
import pytest
from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.iscsi import API_ISCSI
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.common_shares import Common_Shares
from keywords.webui.iscsi import iSCSI
from keywords.webui.navigation import Navigation
from keywords.webui.nfs import NFS


@allure.tag('Read Only Admin', 'Shares', 'Permissions')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
@pytest.mark.parametrize('data', get_data_list('read_only_admin_shares'), scope='class')
class Test_Read_Only_Admin_Share:
    """
    This test class tests read-only admin share.
    """

    @pytest.fixture(scope='function', autouse=True)
    def navigate_to_shares(self):
        """
        This fixture navigates to shares page before each test starts.
        """
        Navigation.navigate_to_shares()

    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self, data):
        # API_POST.create_read_only_admin(data['username'], data['fullname'], data['password'])
        # API_ISCSI.create_iscsi_share(data['iscsi_name'], data['pool_name'], int(data['lunid']))
        API_POST.start_service('iscsitarget')
        # API_POST.create_dataset(f'{data["pool_name"]}/{data["nfs_name"]}', 'NFS')
        # API_POST.create_share('nfs', data['nfs_name'], data['nfs_path'],
        #                       comment=data['nfs_description'])
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

    @allure.tag('Read', 'iSCSI')
    @allure.story("Read Only Admin Is Able To View Pre-Configured iSCSI Shares On The iSCSI Card")
    def test_read_only_admin_is_able_to_view_pre_configured_iscsi_shares_on_the_iscsi_card(self, data):
        """
        This test verifies the read-only admin can view pre-configured iSCSI shares on the iSCSI card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin can view pre-configured iSCSI shares
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        assert Common_Shares.assert_iscsi_target_is_visible(data['iscsi_name_xpath']) is True

    @allure.tag('Update', 'iSCSI')
    @allure.story("Read Only Admin Is Not Able To Enable Or Disable The iSCSI Service On The iSCSI Card")
    def test_read_only_is_not_able_enable_or_disable_iscsi_service_on_the_iscsi_card(self, data):
        """
        This test verifies the read-only admin is not able to enable or disable the NFS service on the iSCSI card.
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

    @allure.tag('Create', 'iSCSI')
    @allure.story("Read Only Admin Is Not Able To Create An iSCSI Share On The iSCSI Card")
    def test_read_only_admin_is_not_able_to_create_an_iscsi_shares_on_the_iscsi_card(self, data):
        """
        This test verifies the read-only admin is not able to create and modify an iSCSI share on the iSCSI card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        assert Common_Shares.assert_share_card_displays('iscsi') is True

        # Verify the read-only admin is not able to create an iSCSI share
        assert Common_Shares.assert_card_iscsi_configure_button_is_locked_and_not_clickable() is True
        assert Common_Shares.assert_card_iscsi_wizard_button_is_locked_and_not_clickable() is True

    @allure.tag('Update', 'iSCSI')
    @allure.story("Read Only Admin Is Not Able To Modify An iSCSI Share On The iSCSI Card")
    def test_read_only_admin_is_not_able_to_modify_an_iscsi_share_on_the_iscsi_card(self, data):
        """
        This test verifies the read-only admin is not able to modify an iSCSI share on the iSCSI card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        assert Common_Shares.assert_share_card_displays('iscsi') is True
        # Verify the read-only admin is not able to modify an iSCSI share
        Common_Shares.click_edit_iscsi_target(data['iscsi_name_xpath'])
        assert iSCSI.assert_edit_iscsi_target_panel_header() is True
        assert Common.assert_header_readonly_badge() is True

        iSCSI.set_target_alias_input(data['target_alias'])
        assert Common.assert_save_button_is_locked_and_not_clickable() is True

        Common.close_right_panel()

    @allure.tag('Delete', 'iSCSI')
    @allure.story("Read Only Admin Is Not Able To Delete An iSCSI Share On The iSCSI Card")
    def test_read_only_admin_is_not_able_to_delete_an_iscsi_share_on_the_iscsi_card(self, data):
        """
        This test verifies the read-only admin is not able to delete an iSCSI share on the iSCSI card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        assert Common_Shares.assert_share_card_displays('iscsi') is True

        # Verify the read-only admin is not able to delete an iSCSI share
        assert Common_Shares.assert_card_iscsi_delete_button_is_locked_and_not_clickable(data['iscsi_name_xpath']) is True

    @allure.tag('Read', 'NFS')
    @allure.story("Read Only Admin Is Able To View Pre-Configured NFS Shares On The NFS Card")
    def test_read_only_admin_is_able_to_view_pre_configured_nfs_shares_on_the_nfs_card(self, data):
        """
        This test verifies the read-only admin can view pre-configured NFS shares on the NFS card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin can view pre-configured iSCSI shares
        assert Common_Shares.assert_share_card_displays('nfs') is True
        assert Common_Shares.assert_share_name('nfs', data['nfs_path']) is True
        assert Common_Shares.assert_share_description('nfs', data['nfs_description']) is True

    @allure.tag('Update', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Enable Or Disable The NFS Service On The NFS Card")
    def test_read_only_is_not_able_enable_or_disable_nfs_service_on_the_nfs_card(self, data):
        """
        This test verifies the read-only admin is not able to enable or disable the NFS service on the NFS card.
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

    @allure.tag('Create', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Create An NFS Share On The NFS Card")
    def test_read_only_admin_is_not_able_to_create_an_nfs_shares_on_the_nfs_card(self, data):
        """
        This test verifies the read-only admin is not able to create an NFS share on the NFS card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to create an iSCSI share
        assert Common_Shares.assert_share_card_displays('nfs') is True
        assert Common_Shares.assert_card_add_share_button_is_locked_and_not_clickable('nfs') is True

    @allure.tag('Update', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Modify An NFS Share On The NFS Card")
    def test_read_only_admin_is_not_able_to_modify_an_iscsi_share_on_the_nfs_card(self, data):
        """
        This test verifies the read-only admin is not able to modify an NFS share on the NFS card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to modify an iSCSI share
        assert Common_Shares.assert_share_card_displays('nfs') is True
        Common_Shares.click_edit_share('nfs', data['nfs_xpath'])
        assert NFS.assert_edit_nfs_panel_header() is True
        assert Common.assert_header_readonly_badge() is True

        Common_Shares.set_share_description('This is a new description')
        assert Common.assert_save_button_is_locked_and_not_clickable() is True

        Common.close_right_panel()

    @allure.tag('Update', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Disable Or Enable An NFS Share On The NFS Card")
    def test_read_only_admin_is_not_able_to_disable_or_enable_an_nfs_shares_on_the_nfs_card(self, data):
        """
        This test verifies the read-only admin is not able to disable and enable an NFS share on the NFS card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to disable and enable an NFS share
        assert Common_Shares.assert_share_card_displays('nfs') is True
        assert Common_Shares.assert_card_share_enabled_toggle_is_locked_and_disabled('nfs', data['nfs_xpath']) is True

    @allure.tag('Delete', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Delete An NFS Share On The NFS Card")
    def test_read_only_admin_is_not_able_to_delete_an_nfs_shares_on_the_nfs_card(self, data):
        """
        This test verifies the read-only admin is not able to delete an NFS share on the NFS card.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to delete an NFS share
        assert Common_Shares.assert_share_card_displays('nfs') is True
        assert Common_Shares.assert_card_share_delete_button_is_locked_and_not_clickable('nfs', data['nfs_xpath']) is True

    @allure.tag('Create', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Create An NFS Share On The Sharing NFS Page")
    def test_read_only_admin_is_not_able_to_create_an_nfs_shares_on_the_sharing_nfs_page(self, data):
        """
        This test verifies the read-only admin is not able to create an NFS share on the Sharing NFS page.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to create an NFS share on the Sharing NFS page
        assert Common_Shares.assert_share_card_displays('nfs') is True
        Common_Shares.click_share_card_header_link('nfs')
        assert NFS.assert_sharing_nfs_page_header() is True
        assert NFS.assert_add_button_is_locked_and_not_clickable_on_nfs_page() is True

    @allure.tag('Update', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Modify An NFS Share On The Sharing NFS Page")
    def test_read_only_admin_is_not_able_to_modify_an_nfs_shares_on_the_sharing_nfs_page(self, data):
        """
        This test verifies the read-only admin is not able to modify an NFS share on the Sharing NFS page.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to modify an NFS share on the Sharing NFS page
        assert Common_Shares.assert_share_card_displays('nfs') is True
        Common_Shares.click_share_card_header_link('nfs')
        assert NFS.assert_sharing_nfs_page_header() is True
        NFS.click_nfs_share_edit_button(data['nfs_xpath'])
        assert NFS.assert_edit_nfs_panel_header() is True
        assert Common.assert_header_readonly_badge() is True

        Common_Shares.set_share_description('This is a new description')
        assert Common.assert_save_button_is_locked_and_not_clickable() is True

        Common.close_right_panel()

    @allure.tag('Delete', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Delete An NFS Share On The Sharing NFS Page")
    def test_read_only_admin_is_not_able_to_delete_an_nfs_shares_on_the_sharing_nfs_page(self, data):
        """
        This test verifies the read-only admin is not able to delete an NFS share on the Sharing NFS page.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to delete an NFS share on the Sharing NFS page
        assert Common_Shares.assert_share_card_displays('nfs') is True
        Common_Shares.click_share_card_header_link('nfs')
        assert NFS.assert_sharing_nfs_page_header() is True
        assert NFS.assert_share_delete_button_is_locked_and_not_clickable_on_nfs_page(data['nfs_xpath']) is True

    @allure.tag('updated', 'NFS')
    @allure.story("Read Only Admin Is Not Able To Disable Or Enable An NFS Share On The Sharing NFS Page")
    def test_read_only_admin_is_not_able_to_disable_or_enable_an_nfs_shares_on_the_sharing_nfs_page(self, data):
        """
        This test verifies the read-only admin is not able to disable and enable an NFS share on the Sharing NFS page.
        """
        # Navigate to the Sharing page
        Navigation.navigate_to_shares()

        # Verify the read-only admin is not able to disable and enable an NFS share on the Sharing NFS page
        assert Common_Shares.assert_share_card_displays('nfs') is True
        Common_Shares.click_share_card_header_link('nfs')
        assert NFS.assert_sharing_nfs_page_header() is True
        assert NFS.assert_share_enabled_toggle_is_locked_and_not_clickable_on_nfs_page(data['nfs_xpath']) is True