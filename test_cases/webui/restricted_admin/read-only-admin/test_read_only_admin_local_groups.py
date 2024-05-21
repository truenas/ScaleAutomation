import allure
import pytest

import xpaths.common_xpaths
from keywords.webui.common import Common as COM
from keywords.webui.local_groups import Local_Groups as LG
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Read Only Admin', 'Local Groups', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_Local_Groups:
    """
    This test class tests read-only admin Local Groups
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self):
        """
        This setup fixture create the dataset and read-only admin for all test cases.
        """
        NAV.navigate_to_local_groups()

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See The Local Groups")
    def test_read_only_admin_can_see_the_local_groups(self):
        """
        Summary: This test verifies the read-only admin is able to see Local Groups.

        Test Steps:
        1. Verify the read-only admin is able to see Local Groups
        2. Expand Local Groups
        3. Verify Local Groups members button
        4. Verify Local Groups edit button
        5. Verify Local Groups delete button
        """
        assert COM.is_visible(xpaths.common_xpaths.any_data_test("row-group-roa")) is True
        LG.expand_group_by_name("roa")
        assert COM.is_visible(xpaths.common_xpaths.button_field("roa-members")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("roa-edit")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("roa-delete")) is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Can View the Local Groups Members")
    def test_read_only_admin_can_view_the_local_groups_members(self):
        """
        Summary: This test verifies the read-only admin is able to view the local groups members.

        Test Steps:
        1. Expand Local Groups
        2. Click Local Groups members button
        3. Verify Update Members page
        4. Verify save button
        5. Navigate to Local Groups page
        """
        LG.expand_group_by_name("roa")
        LG.click_group_members_button("roa")
        assert COM.assert_page_header("Update Members") is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True
        NAV.navigate_to_local_groups()

    @allure.tag("Read")
    @allure.story("Read Only Admin Can View the configured Local Group")
    def test_read_only_admin_can_view_the_configured_local_group(self):
        """
        Summary: This test verifies the read-only admin is able to view the configured local group.

        Test Steps:
        1. Expand Local Groups
        2. Click Local Groups edit button
        3. Verify Edit Group right panel
        4. Verify Local Group fields (gid, name, privileges, etc)
        5. Close right panel
        """
        LG.expand_group_by_name("roa")
        LG.click_group_edit_button_by_name("roa")
        assert COM.assert_right_panel_header("Edit Group") is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("gid")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("name")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("privileges")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("sudo-commands")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("sudo-commands-all")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("sudo-commands-nopasswd")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("sudo-commands-nopasswd-all")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("smb")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to add a Local Groups")
    def test_read_only_admin_can_not_add_local_group(self):
        """
        Summary: This test verifies the read-only admin is not able to add a Local Groups.

        Test Steps:
        1. Verify the add Local Groups button is locked and not clickable
        """
        assert LG.assert_add_local_group_button_is_restricted() is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to delete a Local Groups")
    def test_read_only_admin_can_not_delete_local_group(self):
        """
        Summary: This test verifies the read-only admin is not able to delete a Local Groups.

        Test Steps:
        1. Expand Local Groups
        2. Verify the delete Local Groups button is locked and not clickable
        """
        LG.expand_group_by_name("roa")
        assert LG.assert_delete_local_group_button_is_restricted('roa') is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to modify a Local Groups")
    def test_read_only_admin_can_not_modify_local_group(self):
        """
        Summary: This test verifies the read-only admin is not able to modify a Local Groups.

        Test Steps:
        1. Expand Local Groups
        2. Click Local Groups edit button
        3. Verify the save Local Groups button is locked and not clickable
        4. Close right panel
        """
        LG.expand_group_by_name("roa")
        LG.click_group_edit_button_by_name("roa")
        assert COM.assert_button_is_restricted('save') is True
        COM.close_right_panel()
