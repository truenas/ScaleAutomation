import allure
import pytest

from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.common_shares import Common_Shares as SHARE
from keywords.webui.iscsi import iSCSI as ISCSI
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
        API_POST.create_share('smb', smb_data['name'], f'/mnt/{smb_data["path"]}')
        API_POST.start_service('cifs')
        API_PUT.enable_service_at_boot('cifs')

        # Setup NFS Share
        API_DELETE.delete_share('nfs', nfs_data['dataset_name'])
        API_DELETE.delete_dataset(nfs_data['api_path'])
        API_POST.create_dataset(nfs_data['api_path'], 'NFS')
        API_POST.create_share('nfs', nfs_data['dataset_name'], f'/mnt/{nfs_data["api_path"]}')
        API_POST.start_service('nfs')
        API_PUT.enable_service_at_boot('nfs')

        # Setup ISCSI Share
        NAV.navigate_to_shares()
        SHARE.delete_all_shares_by_share_type("iscsi-target")
        API_DELETE.delete_dataset("tank/iscsi-share", True, True)
        API_POST.create_dataset("tank/iscsi-share")
        COM.click_button("iscsi-share-wizard")
        assert COM.assert_right_panel_header("iSCSI Wizard") is True
        SHARE.set_share_name("iscsi-share", True)
        COM.select_option("disk", "disk-create-new")
        SHARE.set_share_dataset_path("/mnt/tank/iscsi-share")
        SHARE.set_share_volsize("10")
        COM.select_option("target", "target-create-new")
        COM.click_next_button()
        # Wait that the Portal step is open to avoid a race condition
        assert COM.assert_step_header_is_open("Portal") is True
        COM.select_option("portal", "portal-create-new")
        COM.click_button("add-item-ip-address")
        ISCSI.set_ip_address("0.0.0.0")
        ISCSI.click_wizard_portal_next_button()
        # Wait that the Initiator step is open to avoid a race condition
        assert COM.assert_step_header_is_open("Initiator") is True
        ISCSI.click_wizard_save_button()
        COM.assert_progress_bar_not_visible()
        COM.click_button('do-not-start')

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
        ISCSI.delete_all_iscsi_portals()
        ISCSI.delete_all_iscsi_initiators()
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
        assert SHARE.assert_share_card_displays("smb") is True
        assert SHARE.assert_share_card_displays("nfs") is True
        assert SHARE.assert_share_card_displays("iscsi") is True

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
        assert SHARE.assert_share_configuration_field_visible("smb", "path") is True
        assert SHARE.assert_share_configuration_field_visible("smb", "name") is True
        assert SHARE.assert_share_configuration_field_visible("smb", "purpose") is True
        assert SHARE.assert_share_configuration_field_visible("smb", "description") is True
        assert SHARE.assert_share_configuration_field_visible("smb", "enabled") is True
        assert SHARE.assert_share_configuration_field_visible("smb", "save") is True
        assert SHARE.assert_share_configuration_field_visible("smb", "advanced options") is True
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
        assert SMB.assert_share_acl_configuration_field_visible("add") is True
        assert SMB.assert_share_acl_configuration_field_visible("who") is True
        assert SMB.assert_share_acl_configuration_field_visible("permission") is True
        assert SMB.assert_share_acl_configuration_field_visible("type") is True
        assert SMB.assert_share_acl_configuration_field_visible("save") is True
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
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("owner") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("owner group") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("apply owner") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("apply group") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("add item") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("save acl") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("strip acl") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("use preset") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("save as preset") is True
        assert SMB.assert_share_filesystem_acl_configuration_field_visible("Access Control Entry") is True
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
        assert SHARE.assert_share_row_name('smb', smb_data['name']) is True
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is True
        SHARE.unset_share_enabled_toggle("smb", smb_data['name'])
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is False
        SHARE.click_edit_share("smb", smb_data['name'])
        assert COM.assert_right_panel_header("Edit SMB") is True
        assert COM.is_checked("enabled") is False
        COM.close_right_panel()
        assert SHARE.assert_share_row_name('smb', smb_data['name']) is True
        SHARE.set_share_enabled_toggle("smb", smb_data['name'])
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is True
        SHARE.click_edit_share("smb", smb_data['name'])
        assert COM.assert_right_panel_header("Edit SMB") is True
        assert COM.is_checked("enabled") is True
        COM.close_right_panel()
        SHARE.click_edit_share("smb", smb_data['name'])
        COM.unset_checkbox("enabled")
        COM.click_save_button()
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("smb", smb_data['name']) is False
        SHARE.click_edit_share("smb", smb_data['name'])
        COM.set_checkbox("enabled")
        COM.click_save_button()
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
        SHARE.set_share_configuration_field("path", "/mnt/tank/smb-create")
        COM.click_save_button()
        COM.click_button('do-not-restart')
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
        SHARE.set_share_configuration_field("name", "smb-modify")
        COM.click_save_button()
        assert SHARE.assert_share_row_name("smb", "smb-modify") is True

        # Clean Up
        SHARE.click_edit_share("smb", "smb-modify")
        SHARE.set_share_configuration_field("name", smb_data['name'])
        COM.click_save_button()
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
        assert SHARE.assert_card_share_has_no_shares("smb")

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
        SHARE.click_edit_share("nfs", f'/mnt/{nfs_data["api_path"]}')
        assert SHARE.assert_share_configuration_field_visible("nfs", "path") is True
        assert SHARE.assert_share_configuration_field_visible("nfs", "description") is True
        assert SHARE.assert_share_configuration_field_visible("nfs", "enabled") is True
        assert SHARE.assert_share_configuration_field_visible("nfs", "add network") is True
        assert SHARE.assert_share_configuration_field_visible("nfs", "add hosts") is True
        assert SHARE.assert_share_configuration_field_visible("nfs", "save") is True
        assert SHARE.assert_share_configuration_field_visible("nfs", "advanced options") is True
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
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", f'mnt/{nfs_data["api_path"]}') is True
        SHARE.unset_share_enabled_toggle("nfs", f'/mnt/{nfs_data["api_path"]}')
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", f'mnt/{nfs_data["api_path"]}') is False
        SHARE.click_edit_share("nfs", f'mnt/{nfs_data["api_path"]}')
        assert COM.is_checked("enabled") is False
        COM.close_right_panel()
        SHARE.set_share_enabled_toggle("nfs", f'/mnt/{nfs_data["api_path"]}')
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", f'mnt/{nfs_data["api_path"]}') is True
        SHARE.click_edit_share("nfs", f'mnt/{nfs_data["api_path"]}')
        assert COM.is_checked("enabled") is True
        COM.close_right_panel()
        SHARE.click_edit_share("nfs", f'mnt/{nfs_data["api_path"]}')
        COM.unset_checkbox("enabled")
        COM.click_save_button()
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", f'mnt/{nfs_data["api_path"]}') is False
        SHARE.click_edit_share("nfs", f'mnt/{nfs_data["api_path"]}')
        COM.set_checkbox("enabled")
        COM.click_save_button()
        assert SHARE.assert_card_share_enabled_toggle_is_enabled("nfs", f'mnt/{nfs_data["api_path"]}') is True

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
        SHARE.set_share_configuration_field("path", "/mnt/tank/nfs-create")
        COM.click_save_button()
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

        SHARE.click_edit_share("nfs", f'mnt/{nfs_data["api_path"]}')
        assert COM.assert_right_panel_header("Edit NFS Share") is True
        SHARE.set_share_configuration_field("path", "/mnt/tank/nfs-modify")
        COM.click_save_button()
        assert SHARE.assert_share_row_name("nfs", "/mnt/tank/nfs-modify") is True

        # Clean Up
        SHARE.click_edit_share("nfs", "/mnt/tank/nfs-modify")
        SHARE.set_share_configuration_field("path", f'/mnt/{nfs_data["api_path"]}')
        COM.click_save_button()
        assert SHARE.assert_share_row_name("nfs", f'/mnt/{nfs_data["api_path"]}') is True
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
        assert SHARE.assert_share_row_name("nfs", f'/mnt/{nfs_data["api_path"]}') is True
        SHARE.delete_all_shares_by_share_type("nfs")
        assert SHARE.assert_card_share_has_no_shares("nfs")

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
        assert SHARE.assert_share_configuration_field_visible("iscsi", "target name") is True
        assert SHARE.assert_share_configuration_field_visible("iscsi", "target alias") is True
        assert SHARE.assert_share_configuration_field_visible("iscsi", "add networks") is True
        assert SHARE.assert_share_configuration_field_visible("iscsi", "add groups") is True
        assert SHARE.assert_share_configuration_field_visible("iscsi", "portal") is True
        assert SHARE.assert_share_configuration_field_visible("iscsi", "initiator") is True
        assert SHARE.assert_share_configuration_field_visible("iscsi", "authentication method") is True
        assert SHARE.assert_share_configuration_field_visible("iscsi", "authentication group") is True
        assert SHARE.assert_share_configuration_field_visible("iscsi", "save") is True
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
        SHARE.set_share_configuration_field("name", "iscsi-create")
        SHARE.set_share_configuration_field("disk", "disk-create-new")
        SHARE.set_share_configuration_field("dataset", "/mnt/tank/iscsi-share")
        SHARE.set_share_configuration_field("volsize", "10 MiB")
        SHARE.set_share_configuration_field("target", "target-create-new")
        COM.click_button("next")
        # Wait that the Portal step is open to avoid a race condition
        assert COM.assert_step_header_is_open("Portal") is True
        SHARE.set_share_configuration_field("portal", "portal-1-0-0-0-0")
        ISCSI.click_wizard_portal_next_button()
        ISCSI.click_wizard_save_button()
        COM.assert_progress_bar_not_visible()
        COM.click_button('do-not-start')
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
        SHARE.set_share_configuration_field("name", "iscsi-modify")
        SHARE.set_share_configuration_field("disk", "disk-create-new")
        SHARE.set_share_configuration_field("dataset", "/mnt/tank/iscsi-share")
        SHARE.set_share_configuration_field("volsize", "10 MiB")
        SHARE.set_share_configuration_field("target", "target-create-new")
        COM.click_button("next")
        # Wait that the Portal step is open to avoid a race condition
        assert COM.assert_step_header_is_open("Portal") is True
        SHARE.set_share_configuration_field("portal", "portal-1-0-0-0-0")
        ISCSI.click_wizard_portal_next_button()
        # Wait that the Initiator step is open to avoid a race condition
        assert COM.assert_step_header_is_open("Initiator") is True
        ISCSI.click_wizard_save_button()
        COM.assert_progress_bar_not_visible()
        COM.click_button('do-not-start')
        assert SHARE.assert_share_row_name("iscsi", "iscsi-modify") is True

        SHARE.click_edit_iscsi_target("iscsi-modify")
        assert COM.assert_right_panel_header("Edit ISCSI Target") is True
        SHARE.set_share_configuration_field("name", "iscsi-update")
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
        assert SHARE.assert_card_share_has_no_shares("iscsi")
