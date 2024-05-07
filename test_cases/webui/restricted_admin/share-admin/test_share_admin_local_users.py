import allure
import pytest

import xpaths.common_xpaths
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Share Admin', 'Local Users', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Share Admin')
class Test_Share_Admin_Local_Users:
    """
    This test class tests share admin Local Users
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self):
        """
        This setup fixture create the dataset and share admin for all test cases.
        """
        NAV.navigate_to_local_users()

    @allure.tag("Read")
    @allure.story("Share Admin Can See The Local Users")
    def test_share_admin_can_see_the_local_users(self):
        """
        Summary: This test verifies the share admin is able to see Local Users.

        Test Steps:
        1. Verify the share admin is able to see Local Users
        2. Expand Local Users
        3. Verify Local Users edit button
        4. Verify Local Users delete button
        5. Verify Local Users logs button
        """
        assert COM.is_visible(xpaths.common_xpaths.any_data_test("row-user-sha")) is True
        LU.expand_user("sha")
        assert COM.is_visible(xpaths.common_xpaths.button_field("edit-sha")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("delete-sha")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("logs-sha")) is True

    @allure.tag("Read")
    @allure.story("Share Admin Can View the configured Local Users")
    def test_share_admin_can_view_the_configured_local_users(self):
        """
        Summary: This test verifies the share admin is able to view the configured local users.

        Test Steps:
        1. Expand Local Users
        2. Click Local User edit button
        3. Verify Edit User right panel
        4. Verify Local Users fields (fullname, username, email, etc)
        5. Verify sub-sections (Identification, User ID and Groups, Directories and Permissions, Authentication)
        6. Close right panel
        """
        LU.expand_user("sha")
        LU.click_user_edit_button()
        assert COM.assert_right_panel_header("Edit User") is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("full-name")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("username")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("email")) is True
        assert COM.is_visible(xpaths.common_xpaths.toggle_field("password-disabled")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("password")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("password-conf")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("uid")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("groups")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("group")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("home")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("user-read")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("user-write")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("user-execute")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("group-read")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("group-write")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("group-execute")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("other-read")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("other-write")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("other-execute")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("home-create")) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field("sshpubkey")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("ssh-password-enabled")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("shell")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("locked")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("sudo-commands")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("sudo-commands-all")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("sudo-commands-nopasswd")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("sudo-commands-nopasswd-all")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("smb")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True

        # Verify Sub-sections
        assert COM.is_visible(xpaths.common_xpaths.any_text("Identification")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("User ID and Groups")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Directories and Permissions")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Authentication")) is True
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to add a Local Users")
    def test_share_admin_can_not_add_local_users(self):
        """
        Summary: This test verifies the share admin is not able to add a Local Users.

        Test Steps:
        1. Verify the add Local Users button is locked and not clickable
        """
        assert LU.assert_add_local_user_button_is_locked_and_not_clickable() is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to delete a Local Users")
    def test_share_admin_can_not_delete_local_users(self):
        """
        Summary: This test verifies the share admin is not able to delete a Local Users.

        Test Steps:
        1. Expand Local Users
        2. Verify the delete Local Users button is locked and not clickable
        """
        LU.expand_user("sha")
        assert LU.assert_delete_local_user_button_is_locked_and_not_clickable('sha') is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to modify a Local Users")
    def test_share_admin_can_not_modify_local_users(self):
        """
        Summary: This test verifies the share admin is not able to modify a Local Users.

        Test Steps:
        1. Expand Local Users
        2. Click Local Users edit button
        3. Verify the save Local Users button is locked and not clickable
        4. Close right panel
        """
        LU.expand_user("sha")
        LU.click_user_edit_button()
        assert COM.assert_button_is_locked_and_not_clickable('save') is True
        COM.close_right_panel()
