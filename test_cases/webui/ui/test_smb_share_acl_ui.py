import allure
import pytest

import xpaths
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as COMSHARE
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.smb import SMB


@allure.tag("SMB", "UI")
@allure.epic("Shares")
@allure.feature("SMB-ACL-UI")
@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'), scope='class')
@pytest.mark.parametrize('ad_data', get_data_list('ad_credentials'), scope='class')
class Test_SMB_ACL_UI:
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self, smb_data, ad_data) -> None:
        """
        This method sets up each test to start with datasets and shares to execute SMB Shadow Copy functionality
        """
        # Environment setup
        API_PUT.set_nameservers(ad_data['nameserver'])
        API_PUT.join_active_directory(ad_data['username'], ad_data['password'], ad_data['domain'])
        API_DELETE.delete_share('smb', smb_data['name'])
        API_DELETE.delete_dataset(smb_data['path'])
        API_POST.create_dataset(smb_data['path'], 'SMB')
        API_POST.create_share('smb', smb_data['name'], '/mnt/'+smb_data['path'])
        NAV.navigate_to_shares()
        assert COMSHARE.assert_share_card_displays('smb')
        SMB.click_edit_share_acl(smb_data['name'])

    @pytest.fixture(autouse=True, scope='class')
    def teardown_test(self, smb_data, ad_data) -> None:
        """
        This method removes datasets and shares after test is run for a clean environment
        """
        # Environment Teardown
        yield
        API_POST.leave_active_directory(ad_data['username'], ad_data['password'])
        API_DELETE.delete_share('smb', smb_data['name'])
        API_DELETE.delete_dataset(smb_data['path'])

    @allure.tag("Read")
    @allure.story("Verify SMB ACL Default UI")
    def test_smb_share_acl_default_ui(self, smb_data) -> None:
        """
        This test verifies the SMB Card UI
        """
        # Verify SMB ACL Elements
        assert COM.assert_right_panel_header(f'Share ACL for {smb_data["name"]}') is True
        assert COM.is_visible(xpaths.common_xpaths.close_right_panel()) is True
        assert COM.assert_text_is_visible('The SMB share ACL defines access rights for users of this SMB share up to, but not beyond, the access granted by filesystem ACLs.')
        assert COM.assert_text_is_visible('ACL Entries') is True
        assert COM.assert_add_item_button('add-entry') is True
        assert COM.assert_text_is_visible('SID: S-1-1-0') is True
        assert COM.assert_removed_item_button_by_row() is True
        assert SMB.assert_smb_acl_who('everyone@') is True
        assert SMB.assert_smb_acl_permission('FULL') is True
        assert SMB.assert_smb_acl_type('ALLOWED') is True

    @allure.tag("Read")
    @allure.story("Verify SMB ACL Dropdown UI")
    def test_smb_share_acl_dropdown_ui(self) -> None:
        """
        This test verifies the SMB Share ACL dropdown UI
        """
        # Verify the who, permission and type dropdown values
        assert SMB.assert_smb_acl_who_dropdown_values() is True
        assert SMB.assert_smb_acl_permission_dropdown_values() is True
        assert SMB.assert_smb_acl_type_dropdown_values() is True

    @allure.tag("Read")
    @allure.story("Verify SMB ACL AD Who User Dropdown UI")
    def test_smb_share_acl_ad_who_user_dropdown_ui(self) -> None:
        """
        This test verifies the SMB Share ACL AD Who User dropdown UI
        """
        # Verify the ad who-user dropdown values
        COM.select_option('ae-who', 'ae-who-user')
        assert SMB.assert_smb_acl_ad_who_user_dropdown_values() is True

    @allure.tag("Read")
    @allure.story("Verify SMB ACL AD Who Group Dropdown UI")
    def test_smb_share_acl_ad_who_group_dropdown_ui(self) -> None:
        """
        This test verifies the SMB Share ACL AD Who Group dropdown UI
        """
        # Verify the who-group dropdown values
        COM.select_option('ae-who', 'ae-who-group')
        assert SMB.assert_smb_acl_ad_who_group_dropdown_values() is True
