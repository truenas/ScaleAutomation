import allure
import pytest
from helper.data_config import get_data_list
from keywords.api.iscsi import API_ISCSI
from keywords.api.post import API_POST
from keywords.webui.common import Common
from keywords.webui.common_shares import Common_Shares
from keywords.webui.iscsi import iSCSI
from keywords.webui.navigation import Navigation


@allure.tag('Read Only Admin', 'Shares', 'Permissions', 'iSCSI')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
@pytest.mark.parametrize('data', get_data_list('read_only_admin_shares'), scope='class')
class Test_Read_Only_Admin_iSCSI_Share:
    """
    This test class tests read-only admin iSCSI share permissions.
    """

    @pytest.fixture(scope='function', autouse=True)
    def navigate_to_shares(self):
        """
        This fixture navigates to shares page before each test starts.
        """
        Navigation.navigate_to_shares()

    @pytest.fixture(scope='class', autouse=True)
    def setup_test(self, data):
        API_ISCSI.create_iscsi_share(data['iscsi_name'], data['pool_name'], int(data['lunid']))
        API_POST.start_service('iscsitarget')

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_test(self, data):
        yield
        API_ISCSI.delete_iscsi_share(data['iscsi_name'], data['pool_name'], int(data['lunid']))

    @allure.tag('Read')
    @allure.story("Read Only Admin Is Able To View Pre-Configured iSCSI Shares On The iSCSI Card")
    def test_read_only_admin_is_able_to_view_pre_configured_iscsi_shares_on_the_iscsi_card(self, data):
        """
        This test verifies the read-only admin can view pre-configured iSCSI shares on the iSCSI card.
        """

        # Verify the read-only admin can view pre-configured iSCSI shares
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        assert Common_Shares.assert_iscsi_target_is_visible(data['iscsi_name_xpath']) is True

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Enable Or Disable The iSCSI Service On The iSCSI Card")
    def test_read_only_is_not_able_enable_or_disable_iscsi_service_on_the_iscsi_card(self):
        """
        This test verifies the read-only admin is not able to enable or disable the NFS service on the iSCSI card.
        """

        # Verify the read-only admin is not able to disable the NFS service
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        assert Common_Shares.assert_disable_share_service_is_restricted('iscsi') is True
        assert Common_Shares.is_share_service_running('iscsitarget') is True

        # Verify the read-only admin is not able to enable the NFS service
        API_POST.stop_service('iscsitarget')
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        assert Common_Shares.assert_enable_share_service_is_restricted('iscsi') is True
        assert Common_Shares.is_share_service_stopped('iscsitarget') is True

    @allure.tag('Create')
    @allure.story("Read Only Admin Is Not Able To Create An iSCSI Share On The iSCSI Card")
    def test_read_only_admin_is_not_able_to_create_an_iscsi_shares_on_the_iscsi_card(self):
        """
        This test verifies the read-only admin is not able to create and modify an iSCSI share on the iSCSI card.
        """

        assert Common_Shares.assert_share_card_displays('iscsi') is True

        # Verify the read-only admin is not able to create an iSCSI share
        assert Common_Shares.assert_card_iscsi_configure_button_is_restricted() is True
        assert Common_Shares.assert_card_iscsi_wizard_button_is_restricted() is True

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Modify An iSCSI Share On The iSCSI Card")
    def test_read_only_admin_is_not_able_to_modify_an_iscsi_share_on_the_iscsi_card(self, data):
        """
        This test verifies the read-only admin is not able to modify an iSCSI share on the iSCSI card.
        """

        assert Common_Shares.assert_share_card_displays('iscsi') is True
        # Verify the read-only admin is not able to modify an iSCSI share
        Common_Shares.click_edit_iscsi_target(data['iscsi_name_xpath'])
        assert iSCSI.assert_edit_iscsi_target_panel_header() is True
        assert Common.assert_header_readonly_badge() is True

        iSCSI.set_target_alias_input(data['target_alias'])
        assert Common.assert_save_button_is_restricted() is True

        Common.close_right_panel()

    @allure.tag('Delete')
    @allure.story("Read Only Admin Is Not Able To Delete An iSCSI Share On The iSCSI Card")
    def test_read_only_admin_is_not_able_to_delete_an_iscsi_share_on_the_iscsi_card(self, data):
        """
        This test verifies the read-only admin is not able to delete an iSCSI share on the iSCSI card.
        """

        assert Common_Shares.assert_share_card_displays('iscsi') is True
        # Verify the read-only admin is not able to delete an iSCSI share
        assert Common_Shares.assert_card_iscsi_delete_button_is_restricted(data['iscsi_name_xpath']) is True

    @allure.tag('Read')
    @allure.story("Read Only Admin Is Able To View Pre-Configured iSCSI Shares On The iSCSI Page")
    def test_read_only_admin_is_able_to_view_pre_configured_iscsi_target_on_the_iscsi_page(self, data):
        """
        This test verifies the read-only admin can view pre-configured iSCSI targets on the iSCSI page.
        """
        # Navigate to the iSCSI page
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        Common_Shares.click_share_card_header_link('iscsi')
        assert iSCSI.assert_sharing_iscsi_page_header() is True

        # Verify the read-only admin can view pre-configured iSCSI shares
        assert iSCSI.assert_iscsi_tab_header_is_visible('Targets') is True
        assert iSCSI.assert_iscsi_target_name_exists(data['iscsi_name_xpath']) is True

    @allure.tag('Create')
    @allure.story("Read Only Admin Is Not Able To Use The iSCSI Wizard On The Sharing iSCSI Page")
    def test_read_only_admin_is_not_able_to_use_the_iscsi_wizard_on_the_sharing_iscsi_page(self):
        """
        This test verifies the read-only admin is not able to use the iSCSI wizard on the Sharing iSCSI page.
        """

        # Verify the read-only admin is not able to use the iSCSI wizard
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        Common_Shares.click_share_card_header_link('iscsi')
        assert iSCSI.assert_sharing_iscsi_page_header() is True
        assert iSCSI.assert_iscsi_wizard_button_is_restricted() is True

    @allure.tag('Create')
    @allure.story("Read Only Admin Is Not Able To Use The Add Button On a Tab Of The Sharing iSCSI Page")
    @pytest.mark.parametrize('tab', ['Portals', 'Initiators Groups',  'Authorized Access', 'Targets', 'Extents', 'Associated Targets'])
    def test_read_only_admin_is_not_able_to_click_add_on_a_tab_of_the_sharing_iscsi_page(self, tab):
        """
        This test verifies a read-only admin is not able to click add on a tab of the Sharing iSCSI page.
        """

        # Verify the read-only admin is not able to create an iSCSI share
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        Common_Shares.click_share_card_header_link('iscsi')
        assert iSCSI.assert_sharing_iscsi_page_header() is True
        iSCSI.click_on_iscsi_tab(tab)
        assert iSCSI.assert_iscsi_tab_header_is_visible(tab) is True
        assert iSCSI.assert_tab_add_button_is_restricted(tab) is True

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Modify An Item On A Tab Of The Sharing iSCSI Page")
    @pytest.mark.parametrize('tab', ['Portals', 'Targets', 'Extents'])
    def test_read_only_admin_is_not_able_to_modify_an_item_on_a_tab_of_sharing_iscsi_page(self, data, tab):
        """
        This test verifies a read-only admin is not able to modify an item on a tab of the Sharing iSCSI page.
        """

        # Navigate to the tab on the iSCSI page
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        Common_Shares.click_share_card_header_link('iscsi')
        assert iSCSI.assert_sharing_iscsi_page_header() is True
        iSCSI.click_on_iscsi_tab(tab)
        assert iSCSI.assert_iscsi_tab_header_is_visible(tab) is True

        # Verify the read-only admin is not able to modify an iSCSI target
        iSCSI.click_on_the_tab_row_item_edit_button(tab, data['iscsi_name_xpath'])
        assert iSCSI.assert_edit_panel_header_is_visible_opened_from_iscsi_tab(tab) is True
        assert Common.assert_header_readonly_badge() is True

        assert Common.assert_save_button_is_restricted() is True

        Common.close_right_panel()

    @allure.tag('Delete')
    @allure.story("Read Only Admin Is Not Able To Delete An Item On A Tab Of The Sharing iSCSI Page")
    @pytest.mark.parametrize('tab', ['Portals', 'Targets', 'Extents'])
    def test_read_only_admin_is_not_able_to_delete_an_item_on_a_tab_of_the_sharing_iscsi_page(self, data, tab):
        """
        This test verifies a read-only admin is not able to delete an item on a tab of the Sharing iSCSI page.
        """

        # Navigate to the tab on the iSCSI page
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        Common_Shares.click_share_card_header_link('iscsi')
        assert iSCSI.assert_sharing_iscsi_page_header() is True

        iSCSI.click_on_iscsi_tab(tab)
        assert iSCSI.assert_iscsi_tab_header_is_visible(tab) is True
        # Verify the read-only admin is not able to delete an iSCSI target
        iSCSI.assert_tab_row_item_delete_button_is_restricted(tab, data['iscsi_name_xpath'])

    @allure.tag('Update')
    @allure.story("Read Only Admin Is Not Able To Save A Target Global Configuration On The Sharing iSCSI Page")
    def test_read_only_admin_is_not_able_to_save_a_target_global_configuration_on_the_sharing_iscsi_page(self):
        """
        This test verifies a read-only admin is not able to save a Target Global Configuration on the Sharing iSCSI page.
        """

        # Navigate to Target Global Configuration tab on the iSCSI page
        assert Common_Shares.assert_share_card_displays('iscsi') is True
        Common_Shares.click_share_card_header_link('iscsi')
        assert iSCSI.assert_sharing_iscsi_page_header() is True

        # Verify the read-only admin is not able to save a Target Global Configuration
        iSCSI.click_on_iscsi_tab('Target Global Configuration')
        assert iSCSI.assert_global_configuration_tab_is_visible() is True
        assert Common.assert_save_button_is_restricted() is True
