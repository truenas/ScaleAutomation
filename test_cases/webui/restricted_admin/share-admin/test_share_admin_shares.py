import allure
import pytest

import xpaths.common_xpaths
from helper.data_config import get_data_list
from helper.webui import WebUI
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as SHARE
from keywords.webui.smb import SMB as SMB
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Share Admin', 'Shares', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Share Admin')
@pytest.mark.parametrize('smb_data', get_data_list('shares/smb'), scope='class')
@pytest.mark.parametrize('nfs_data', get_data_list('shares/nfs'), scope='class')
class Test_Share_Admin_Shares:
    """
    This test class tests share admin Shares
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_class(self, smb_data, nfs_data):
        """
        This setup fixture create the dataset, shares and share admin for all test cases.
        """
        # Setup SMB Share
        API_POST.create_non_admin_user('smbuser', 'smbuser Full', 'testing', 'True')
        API_DELETE.delete_share('smb', smb_data['name'])
        API_DELETE.delete_dataset(smb_data['path'])
        API_POST.create_dataset(smb_data['path'], 'SMB')
        API_POST.create_share('smb', smb_data['name'], "/mnt/" + smb_data['path'])

        # Setup NFS Share
        API_DELETE.delete_share('nfs', nfs_data['dataset_name'])
        API_DELETE.delete_dataset(nfs_data['api_path'])
        API_POST.create_dataset(nfs_data['api_path'], 'NFS')
        API_POST.create_share('nfs', nfs_data['dataset_name'], "/mnt/" + nfs_data['api_path'])

        # Setup ISCSI Share
        NAV.navigate_to_shares()
        SHARE.delete_all_shares_by_share_type("iscsi-target")
        API_DELETE.delete_dataset("tank/iscsi-share", True, True)
        API_POST.create_dataset("tank/iscsi-share")
        COM.click_button("iscsi-share-wizard")
        assert COM.assert_right_panel_header("iSCSI Wizard") is True
        COM.set_input_field("name", "iscsi-share", True)
        COM.select_option("disk", "disk-create-new")
        COM.set_input_field("dataset", "/mnt/tank/iscsi-share")
        COM.set_input_field("volsize", "10")
        COM.select_option("target", "target-create-new")
        COM.click_button("next")
        WebUI.delay(1)
        # assert COM.assert_step_header_is_open("Portal") is True
        # COM.click_on_element(xpaths.common_xpaths.data_test_field("select-portal")+"/div/div")
        # COM.click_on_element(xpaths.common_xpaths.data_test_field("option-portal-create-new"))
        COM.select_option("portal", "portal-create-new")
        COM.click_button("add-item-ip-address")
        COM.click_on_element(xpaths.common_xpaths.data_test_field("select"))
        COM.click_on_element(xpaths.common_xpaths.data_test_field("option-0-0-0-0"))
        COM.click_on_element('(//*[@data-test="button-next"])[2]')
        COM.click_on_element('(//*[@data-test="button-save"])[2]')
        COM.assert_progress_bar_not_visible()
        COM.click_button("do-not-start")

    @pytest.fixture(autouse=True, scope='class')
    def teardown_class(self, smb_data, nfs_data):
        """
        This teardown fixture delete the dataset, shares and share admin for all test cases.
        """
        yield
        # Teardown SMB Share
        SHARE.delete_all_shares_by_share_type("smb")
        API_DELETE.delete_dataset(smb_data['path'])
        API_DELETE.delete_user('smbuser')

        # Teardown SMB Share
        SHARE.delete_all_shares_by_share_type("nfs")
        API_DELETE.delete_dataset(nfs_data['api_path'])

        # Teardown ISCSI Share
        SHARE.delete_all_shares_by_share_type("iscsi")
        API_DELETE.delete_dataset("tank/iscsi-share", True, True)

    @allure.tag("Read")
    @allure.story("Share Admin Can See The Shares")
    def test_share_admin_can_see_the_shares(self):
        """
        Summary: This test verifies the share admin is able to see Shares.

        Test Steps:
        1. Verify the share admin is able to see Shares (SMB, NFS, iSCSI)
        """
        assert COM.assert_page_header("Sharing") is True
        assert COM.is_visible(xpaths.common_xpaths.any_header("Windows (SMB) Shares", 3)) is True
        assert COM.is_visible(xpaths.common_xpaths.any_header("UNIX (NFS) Shares", 3)) is True
        assert COM.is_visible(xpaths.common_xpaths.any_header("Block (iSCSI) Shares Targets", 3)) is True

    @allure.tag("Read", "SMB")
    @allure.story("Share Admin Can View the Configured SMB Share")
    def test_share_admin_can_view_the_configured_smb_share(self, smb_data):
        """
        Summary: This test verifies the share admin is able to view the configured SMB Share.

        Test Steps:
        1. Click Edit SMB Share
        2. Verify SMB Share fields (path, name, purpose, etc.)
        3. Close right panel
        """
        SHARE.click_edit_share("smb", smb_data['name'])
        assert COM.is_visible(xpaths.common_xpaths.input_field("path")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("name")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("purpose")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("comment")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("enabled")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("toggle-advanced-options")) is True
        COM.close_right_panel()

    @allure.tag("Read", "SMB")
    @allure.story("Share Admin Can View the Configured SMB Share ACL Permissions")
    def test_share_admin_can_view_the_configured_smb_share_acl_permissions(self, smb_data):
        """
        Summary: This test verifies the share admin is able to view the configured SMB Share ACL permissions.

        Test Steps:
        1. Click Edit SMB Share ACL permissions
        2. Verify SMB Share fields (add button, who, permission, etc.)
        3. Close right panel
        """
        SMB.click_edit_share_acl(smb_data['name'])
        assert COM.assert_right_panel_header(f'Share ACL for {smb_data["name"]}')
        assert COM.is_visible(xpaths.common_xpaths.button_field("add-item-add-entry")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("ae-who")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("ae-perm")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("ae-type")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True
        COM.close_right_panel()

    @allure.tag("Read", "SMB")
    @allure.story("Share Admin Can View the Configured SMB Share filesystem Permissions")
    def test_share_admin_can_view_the_configured_smb_share_filesystem_permissions(self, smb_data):
        """
        Summary: This test verifies the share admin is able to view the configured SMB Share filesystem permissions.

        Test Steps:
        1. Click Edit SMB Share filesystem permissions
        2. Verify SMB Share fields (owner, owner group, apply owner, etc.)
        3. Navigate to Shares
        """
        SMB.click_edit_share_filesystem_acl(smb_data['name'])
        assert COM.is_visible(xpaths.common_xpaths.input_field("owner")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("owner-group")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("apply-owner")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("apply-group")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("add-acl-item")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save-acl")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("strip-acl")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("use-preset")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save-as-preset")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Access Control Entry")) is True
        NAV.navigate_to_shares()

    @allure.tag("Read", "SMB")
    @allure.story("Share Admin Is Able to enable and disable SMB Share")
    def test_share_admin_can_enable_and_disable_smb_share(self, smb_data):
        """
        Summary: This test verifies the share admin is able to enable and disable SMB Share.

        Test Steps:
        1. Verify the enabled SMB Share toggle can be set to disabled
        2. Edit SMB Share
        3. Verify enabled checkbox is unchecked
        4. Verify the disabled SMB Share toggle can be set to enabled
        5. Edit SMB Share
        6. Verify enabled checkbox is checked
        """
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is True
        SHARE.unset_share_enabled_toggle("smb", smb_data['name'])
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is False
        SHARE.click_edit_share("smb", smb_data['name'])
        assert COM.assert_right_panel_header("Edit SMB") is True
        assert COM.is_checked("enabled") is False
        COM.close_right_panel()
        SHARE.set_share_enabled_toggle("smb", smb_data['name'])
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is True
        SHARE.click_edit_share("smb", smb_data['name'])
        assert COM.assert_right_panel_header("Edit SMB") is True
        assert COM.is_checked("enabled") is True
        COM.close_right_panel()
        SHARE.click_edit_share("smb", smb_data['name'])
        COM.unset_checkbox("enabled")
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is False
        SHARE.click_edit_share("smb", smb_data['name'])
        COM.set_checkbox("enabled")
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is True

    @allure.tag("Create", "SMB")
    @allure.story("Share Admin Is Able to add a SMB Share")
    def test_share_admin_can_add_smb_share(self):
        """
        Summary: This test verifies the share admin is able to add SMB Share.

        Test Steps:
        1. Click the add SMB Share button
        2. Fill SMB Share fields (path)
        3. Click Save button
        4. Verify SMB Share is visible
        """
        API_POST.create_dataset("tank/smb-create", 'SMB')
        SHARE.click_add_share_button("smb")
        assert COM.assert_right_panel_header("Add SMB") is True
        COM.set_input_field("path", "/mnt/tank/smb-create", True)
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_share_row_name("smb", "smb-create") is True

        API_DELETE.delete_share("smb", "smb-create")
        API_DELETE.delete_dataset("tank/smb-create")

    @allure.tag("Update")
    @allure.story("Share Admin Is Able to modify a SMB Share")
    def test_share_admin_can_modify_smb_share(self, smb_data):
        """
        Summary: This test verifies the share admin is not able to modify SMB Share.

        Test Steps:
        1. Click Edit SMB Share
        2. Update field names (name)
        3. Click Save button
        4. Verify the SMB Share fields are update
        """
        API_POST.create_dataset("tank/smb-modify", 'SMB')

        SHARE.click_edit_share("smb", smb_data['name'])
        assert COM.assert_right_panel_header("Edit SMB") is True
        COM.set_input_field("name", "smb-modify", True)
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_share_row_name("smb", "smb-modify") is True

        # Clean Up
        SHARE.click_edit_share("smb", "smb-modify")
        COM.set_input_field("name", smb_data['name'], True)
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_share_row_name("smb", smb_data['name']) is True
        API_DELETE.delete_dataset("tank/smb-modify")

    @allure.tag("Delete", "SMB")
    @allure.story("Share Admin Is Able to delete a SMB Share")
    def test_share_admin_can_delete_smb_share(self, smb_data):
        """
        Summary: This test verifies the share admin is able to delete SMB Share.

        Test Steps:
        1. Click the delete SMB Share button
        2. Confirm delete dialog
        3. Verify SMB Share is no longer visible
        """
        assert SHARE.assert_share_row_name("smb", smb_data['name']) is True
        SHARE.delete_all_shares_by_share_type("smb")
        assert COM.is_visible(xpaths.common_xpaths.any_xpath('//ix-smb-card//h3[contains(text(),"No records have been added yet")]'))

    @allure.tag("Read", "NFS")
    @allure.story("Share Admin Can View the Configured NFS Share")
    def test_share_admin_can_view_the_configured_nfs_share(self, nfs_data):
        """
        Summary: This test verifies the share admin is able to view the configured NFS Share.

        Test Steps:
        1. Click Edit NFS Share
        2. Verify NFS Share fields (path, comment, enabled, etc.)
        3. Close right panel
        """
        SHARE.click_edit_share("nfs", "mnt/"+nfs_data['api_path'])
        assert COM.is_visible(xpaths.common_xpaths.input_field("path")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("comment")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("enabled")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("add-item-networks")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("add-item-hosts")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("toggle-advanced-options")) is True
        COM.close_right_panel()

    @allure.tag("Read", "NFS")
    @allure.story("Share Admin Is Able to enable and disable NFS Share")
    def test_share_admin_can_enable_and_disable_nfs_share(self, nfs_data):
        """
        Summary: This test verifies the share admin is able to enable and disable NFS Share.

        Test Steps:
        1. Verify the enabled NFS Share toggle can be set to disabled
        2. Edit NFS Share
        3. Verify enabled checkbox is unchecked
        4. Verify the disabled NFS Share toggle can be set to enabled
        5. Edit NFS Share
        6. Verify enabled checkbox is checked
        """
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", "mnt/"+nfs_data['api_path']) is True
        SHARE.unset_share_enabled_toggle("nfs", "mnt/"+nfs_data['api_path'])
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", "mnt/"+nfs_data['api_path']) is False
        SHARE.click_edit_share("nfs", "mnt/"+nfs_data['api_path'])
        assert COM.is_checked("enabled") is False
        COM.close_right_panel()
        SHARE.set_share_enabled_toggle("nfs", "mnt/"+nfs_data['api_path'])
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", "mnt/"+nfs_data['api_path']) is True
        SHARE.click_edit_share("nfs", "mnt/"+nfs_data['api_path'])
        assert COM.is_checked("enabled") is True
        COM.close_right_panel()
        SHARE.click_edit_share("nfs", "mnt/"+nfs_data['api_path'])
        COM.unset_checkbox("enabled")
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", "mnt/"+nfs_data['api_path']) is False
        SHARE.click_edit_share("nfs", "mnt/"+nfs_data['api_path'])
        COM.set_checkbox("enabled")
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", "mnt/"+nfs_data['api_path']) is True

    @allure.tag("Create", "NFS")
    @allure.story("Share Admin Is Able to add a NFS Share")
    def test_share_admin_can_add_nfs_share(self):
        """
        Summary: This test verifies the share admin is able to add a NFS Share.

        Test Steps:
        1. Click the add NFS Share button
        2. Fill NFS Share fields (path)
        3. Click Save button
        4. Verify NFS Share is visible
        """
        API_POST.create_dataset("tank/nfs-create", 'NFS')
        SHARE.click_add_share_button("nfs")
        assert COM.assert_right_panel_header("Add NFS Share") is True
        COM.set_input_field("path", "/mnt/tank/nfs-create", True)
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_share_row_name("nfs", "/mnt/tank/nfs-create") is True

        API_DELETE.delete_share("nfs", "/mnt/tank/nfs-create")
        API_DELETE.delete_dataset("tank/nfs-create")

    @allure.tag("Update")
    @allure.story("Share Admin Is Able to modify a NFS Share")
    def test_share_admin_can_modify_nfs_share(self, nfs_data):
        """
        Summary: This test verifies the share admin is not able to modify a NFS Share.

        Test Steps:
        1. Click Edit NFS Share
        2. Update field names (path)
        3. Click Save button
        4. Verify the NFS Share fields are update
        """
        API_POST.create_dataset("tank/nfs-modify", 'NFS')

        SHARE.click_edit_share("nfs", "/mnt/" + nfs_data['api_path'])
        assert COM.assert_right_panel_header("Edit NFS Share") is True
        COM.set_input_field("path", "/mnt/tank/nfs-modify", True)
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_share_row_name("nfs", "/mnt/tank/nfs-modify") is True

        # Clean Up
        SHARE.click_edit_share("nfs", "/mnt/tank/nfs-modify")
        COM.set_input_field("path", "/mnt/" + nfs_data['api_path'], True)
        COM.click_save_button()
        COM.click_button("do-not-start")
        assert SHARE.assert_share_row_name("nfs", "/mnt/" + nfs_data['api_path']) is True
        API_DELETE.delete_dataset("tank/nfs-modify")

    @allure.tag("Delete", "NFS")
    @allure.story("Share Admin Is Able to delete a NFS Share")
    def test_share_admin_can_delete_nfs_share(self, nfs_data):
        """
        Summary: This test verifies the share admin is able to delete a NFS Share.

        Test Steps:
        1. Click the delete NFS Share button
        2. Confirm delete dialog
        3. Verify NFS Share is no longer visible
        """
        assert SHARE.assert_share_row_name("nfs", "/mnt/" + nfs_data['api_path']) is True
        SHARE.delete_all_shares_by_share_type("nfs")
        assert COM.is_visible(xpaths.common_xpaths.any_xpath('//ix-nfs-card//h3[contains(text(),"No records have been added yet")]'))

    @allure.tag("Read", "iSCSI")
    @allure.story("Share Admin Can View the Configured ISCSI Share")
    def test_share_admin_can_view_the_configured_iscsi_share(self):
        """
        Summary: This test verifies the share admin is able to view the configured ISCSI Share.

        Test Steps:
        1. Click Edit ISCSI Share
        2. Verify ISCSI Share fields (path, comment, enabled, etc.)
        3. Close right panel
        """
        SHARE.click_edit_iscsi_target("iscsi-share")
        assert COM.is_visible(xpaths.common_xpaths.input_field("name")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("alias")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("add-item-authorized-networks")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("add-item-add-groups")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("portal")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("initiator")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("authmethod")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("auth")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True
        COM.close_right_panel()

    @allure.tag("Create", "ISCSI")
    @allure.story("Share Admin Is Able to add a ISCSI Share")
    def test_share_admin_can_add_iscsi_share(self):
        """
        Summary: This test verifies the share admin is able to add a ISCSI Share.

        Test Steps:
        1. Click the ISCSI Share Wizard button
        2. Fill ISCSI Share fields (name, disk, dataset, etc.)
        3. Click Save button
        4. Verify ISCSI Share is visible
        """
        COM.click_button("iscsi-share-wizard")
        assert COM.assert_right_panel_header("iSCSI Wizard") is True
        COM.set_input_field("name", "iscsi-create")
        COM.select_option("disk", "disk-create-new")
        COM.set_input_field("dataset", "/mnt/tank/iscsi-share")
        COM.set_input_field("volsize", "10")
        COM.select_option("target", "target-create-new")
        COM.click_button("next")
        # assert COM.assert_step_header_is_open("Portal") is True
        # COM.click_on_element(xpaths.common_xpaths.data_test_field("select-portal")+"/div/div")
        # COM.click_on_element(xpaths.common_xpaths.data_test_field("option-portal-1-0-0-0-0"))
        COM.select_option("portal", "portal-1-0-0-0-0")
        COM.click_on_element('(//*[@data-test="button-next"])[2]')
        COM.click_on_element('(//*[@data-test="button-save"])[2]')
        COM.assert_progress_bar_not_visible()
        COM.click_button("do-not-start")
        assert SHARE.assert_share_row_name("iscsi", "iscsi-create") is True

    @allure.tag("Update")
    @allure.story("Share Admin Is Able to modify a ISCSI Share")
    def test_share_admin_can_modify_iscsi_share(self):
        """
        Summary: This test verifies the share admin is not able to modify a ISCSI Share.

        Test Steps:
        1. Click Edit ISCSI Share
        2. Update fields (name)
        3. Click Save button
        4. Verify the ISCSI Share fields are update
        """
        COM.click_button("iscsi-share-wizard")
        assert COM.assert_right_panel_header("iSCSI Wizard") is True
        COM.set_input_field("name", "iscsi-modify")
        COM.select_option("disk", "disk-create-new")
        COM.set_input_field("dataset", "/mnt/tank/iscsi-share")
        COM.set_input_field("volsize", "10")
        COM.select_option("target", "target-create-new")
        COM.click_button("next")
        # assert COM.assert_step_header_is_open("Portal") is True
        # COM.click_on_element(xpaths.common_xpaths.data_test_field("select-portal") + "/div/div")
        # COM.click_on_element(xpaths.common_xpaths.data_test_field("option-portal-1-0-0-0-0"))
        COM.select_option("portal", "portal-1-0-0-0-0")
        COM.click_on_element('(//*[@data-test="button-next"])[2]')
        COM.click_on_element('(//*[@data-test="button-save"])[2]')
        COM.assert_progress_bar_not_visible()
        COM.click_button("do-not-start")
        assert SHARE.assert_share_row_name("iscsi", "iscsi-modify") is True

        SHARE.click_edit_iscsi_target("iscsi-modify")
        assert COM.assert_right_panel_header("Edit ISCSI Target") is True
        COM.set_input_field("name", "iscsi-update")
        COM.click_save_button()
        assert SHARE.assert_share_row_name("iscsi", "iscsi-update") is True

    @allure.tag("Delete", "ISCSI")
    @allure.story("Share Admin Is Able to delete a ISCSI Share")
    def test_share_admin_can_delete_iscsi_share(self):
        """
        Summary: This test verifies the share admin is able to delete a ISCSI Share.

        Test Steps:
        1. Click the delete ISCSI Share button
        2. Confirm delete dialog
        3. Verify ISCSI Share is no longer visible
        """
        SHARE.delete_all_shares_by_share_type("iscsi")
        assert COM.is_visible(xpaths.common_xpaths.any_xpath('//ix-iscsi-card//h3[contains(text(),"No records have been added yet")]'))
