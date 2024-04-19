import allure
import pytest

from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.local_groups import Local_Groups as LG
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('groups', get_data_list('local_groups'), scope='class')
@allure.tag("Local_Groups")
@allure.epic("Credentials")
@allure.feature("Local Groups")
class Test_Local_Groups:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, groups) -> None:
        """
        This method sets up each test to start with builtin groups not shown
        """
        API_DELETE.delete_group(groups['alt-group-name'], groups['group-privileges'])
        API_DELETE.delete_group(groups['group-name'], groups['group-privileges'])
        NAV.navigate_to_local_groups()
        LG.unset_show_builtin_groups_toggle()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, groups):
        """
        This method clears any test groups after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_group(groups['group-name'], groups['group-privileges'])
        API_DELETE.delete_group(groups['alt-group-name'], groups['group-privileges'])

    @allure.tag("Update")
    @allure.story("Add Member to Local Groups")
    def test_add_member_to_new_group(self, groups) -> None:
        """
        Summary: This test verifies adding a member to a new local group

        Test Steps:
        1. Expand and Edit group
        2. Add User to Group Members list
        3. Verify User in Group Members list, and NOT in User list
        4. Remove User from Group Members list
        5. Verify User in User list, and NOT in Group Members list
        """
        # Environment setup
        if LG.is_group_visible(groups['group-name']) is False:
            API_POST.create_group(groups['group-name'])
            assert LG.is_group_visible(groups['group-name']) is True

        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_members_button(groups['group-name'])
        LG.click_user_account_by_name(groups['username'])
        LG.click_add_to_list_button()
        assert LG.is_user_in_group_list(groups['username']) is True
        assert LG.is_user_in_users_list(groups['username']) is False
        COM.click_save_button_and_wait_for_right_panel()
        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_members_button(groups['group-name'])
        assert LG.is_user_in_group_list(groups['username']) is True
        assert LG.is_user_in_users_list(groups['username']) is False
        COM.click_cancel_button()

    @allure.tag("Create")
    @allure.story("Create New Local Groups")
    def test_create_new_local_group(self, groups) -> None:
        """
        Summary: This test verifies a new local group can be created

        Test Steps:
        1. Click Add Group button
        2. Set Group values (gid, name, privileges, allow sudo, allow sudo no pswd)
        3. Verify sudo commands disabled
        4. Click Save button
        5. Verify Group exists and is visible
        """
        LG.click_add_group_button()
        LG.set_group_gid(groups['gid'])
        LG.set_group_name(groups['group-name'])
        LG.select_group_privileges(groups['group-privileges'])
        LG.add_group_allowed_sudo_command(groups['sudo-commands-1'])
        LG.add_group_allowed_sudo_command_no_password(groups['sudo-commands-2'])
        LG.set_group_allow_all_sudo_commands_checkbox()
        assert LG.assert_sudo_commands_is_disabled() is True
        LG.unset_group_allow_all_sudo_commands_checkbox()
        assert LG.assert_sudo_commands_is_disabled() is False
        LG.set_group_allow_all_sudo_commands_no_password_checkbox()
        assert LG.assert_sudo_commands_no_password_is_disabled() is True
        LG.unset_group_allow_all_sudo_commands_no_password_checkbox()
        assert LG.assert_sudo_commands_no_password_is_disabled() is False
        LG.set_samba_authentication()
        LG.set_allow_duplicate_gids()
        COM.click_save_button_and_wait_for_right_panel()
        assert LG.is_group_visible(groups['group-name']) is True

    @allure.tag("Create")
    @allure.story("Create New Local Groups with Duplicate GID")
    def test_create_new_local_group_with_duplicate_gid(self, groups) -> None:
        """
        Summary: This test verifies a new local group with duplicate ID can be created

        Test Steps:
        1. Click Add Group button
        2. Set Group values (duplicate gid, name)
        3. Click Save button
        4. Verify duplicate Group exists and has duplicate GID is visible
        """
        # Environment setup
        if LG.is_group_visible(groups['group-name']) is False:
            LG.click_add_group_button()
            LG.set_group_gid(groups['dup-gid'])
            LG.set_group_name(groups['group-name'])
            COM.click_save_button_and_wait_for_right_panel()
            assert LG.is_group_visible(groups['group-name']) is True
            assert LG.assert_group_gid(groups['group-name'], groups['dup-gid']) is True

        LG.click_add_group_button()
        LG.set_allow_duplicate_gids()
        LG.set_group_gid(groups['dup-gid'])
        LG.set_group_name(groups['alt-group-name'])
        COM.click_save_button_and_wait_for_right_panel()
        assert LG.is_group_visible(groups['alt-group-name']) is True
        assert LG.assert_group_gid(groups['alt-group-name'], groups['dup-gid']) is True
        LG.expand_group_by_name(groups['alt-group-name'])
        LG.click_group_edit_button_by_name(groups['alt-group-name'])
        assert COM.assert_right_panel_header('Edit Group') is True
        assert LG.assert_gid_field_is_disabled() is True
        COM.close_right_panel()
        LG.delete_group_by_api(groups['group-name'], groups['group-privileges'])
        LG.delete_group_by_api(groups['alt-group-name'], groups['group-privileges'])

    @allure.tag("Delete")
    @allure.story("Delete Member from Local Groups")
    def test_delete_member_from_new_group(self, groups) -> None:
        """
        Summary: This test verifies deleting a member from a new local group

        Test Steps:
        1. Expand and Edit Group
        2. Remove User from Group Members list
        3. Click Save button
        4. Expand and Edit Group
        5. Verify user NOT in Group Member list
        """
        # Environment setup
        if LG.is_group_visible(groups['group-name']) is False:
            API_DELETE.delete_group(groups['group-name'], groups['group-privileges'])
            API_POST.create_group(groups['group-name'])
            assert LG.is_group_visible(groups['group-name']) is True
            LG.expand_group_by_name(groups['group-name'])
            LG.click_group_members_button(groups['group-name'])
            LG.click_user_account_by_name(groups['username'])
            LG.click_add_to_list_button()
            assert LG.is_user_in_group_list(groups['username']) is True
            assert LG.is_user_in_users_list(groups['username']) is False
            COM.click_save_button_and_wait_for_right_panel()
            assert LG.is_group_visible(groups['group-name']) is True

        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_members_button(groups['group-name'])
        LG.click_group_members_by_name(groups['username'])
        LG.click_remove_from_list_button()
        assert LG.is_user_in_group_list(groups['username']) is False
        assert LG.is_user_in_users_list(groups['username']) is True
        COM.click_save_button_and_wait_for_right_panel()
        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_members_button(groups['group-name'])
        assert LG.is_user_in_group_list(groups['username']) is False
        assert LG.is_user_in_users_list(groups['username']) is True
        COM.click_cancel_button()

    @allure.tag("Delete")
    @allure.story("Delete Local Groups")
    def test_delete_new_local_group(self, groups) -> None:
        """
        Summary: This test verifies a new local group can be deleted

        Test Steps:
        1. Expand Group
        2. Click Delete Group button
        3. Verify Group deleted and is NOT visible
        """
        # Environment setup
        if LG.is_group_visible(groups['group-name']) is False:
            API_POST.create_group(groups['group-name'])
            assert LG.is_group_visible(groups['group-name']) is True

        LG.delete_group_by_name(groups['group-name'])
        assert LG.is_group_visible(groups['group-name']) is False

    @allure.tag("Update")
    @allure.story("Edit Local Groups")
    def test_edit_local_group(self, groups) -> None:
        """
        Summary: This test verifies a local group can be edited

        Test Steps:
        1. Expand and Edit Group
        2. Edit Group values (name, privileges, Allow sudo commands, samba auth)
        3. Click Save button
        4. Verify old Group is not visible and new group is visible
        5. Expand and Edit Group
        6. Edit Group values (name, privileges, Allow sudo commands, samba auth)
        7. Click Save button
        8. Verify old Group is visible
        """
        if LG.is_group_visible(groups['group-name']) is False:
            API_POST.create_group(groups['group-name'])
            assert LG.is_group_visible(groups['group-name']) is True

        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_edit_button_by_name(groups['group-name'])
        LG.set_group_name(groups['alt-group-name'])
        LG.select_group_privileges(groups['group-privileges'])

        assert LG.assert_gid_field_is_disabled() is True
        LG.delete_group_allowed_sudo_command(groups['sudo-commands-1'])
        LG.delete_group_allowed_sudo_command_no_password(groups['sudo-commands-2'])

        LG.unset_samba_authentication()
        COM.click_save_button_and_wait_for_right_panel()
        assert LG.is_group_visible(groups['group-name']) is False
        assert LG.is_group_visible(groups['alt-group-name']) is True
        LG.expand_group_by_name(groups['alt-group-name'])
        LG.click_group_edit_button_by_name(groups['alt-group-name'])
        LG.set_group_name(groups['group-name'])
        LG.add_group_allowed_sudo_command(groups['sudo-commands-2'])
        LG.add_group_allowed_sudo_command_no_password(groups['sudo-commands-1'])
        LG.set_group_allow_all_sudo_commands_checkbox()
        assert LG.assert_group_allowed_sudo_commands_is_disabled() is True
        LG.set_group_allow_all_sudo_commands_no_password_checkbox()
        assert LG.assert_group_allowed_sudo_commands_no_password_is_disabled() is True
        LG.set_samba_authentication()
        COM.click_save_button_and_wait_for_right_panel()
        assert LG.is_group_visible(groups['group-name']) is True
        assert LG.is_group_visible(groups['alt-group-name']) is False
        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_edit_button_by_name(groups['group-name'])
        LG.unset_group_allow_all_sudo_commands_checkbox()
        LG.unset_group_allow_all_sudo_commands_no_password_checkbox()
        LG.add_group_allowed_sudo_command(groups['sudo-commands-1'])
        LG.add_group_allowed_sudo_command(groups['sudo-commands-2'])
        LG.add_group_allowed_sudo_command_no_password(groups['sudo-commands-1'])
        LG.add_group_allowed_sudo_command_no_password(groups['sudo-commands-2'])
        COM.click_save_button_and_wait_for_right_panel()
        assert LG.is_group_visible(groups['group-name']) is True
        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_edit_button_by_name(groups['group-name'])
        LG.delete_all_group_allowed_sudo_commands()
        LG.delete_all_group_allowed_sudo_commands_no_password()
        COM.click_save_button_and_wait_for_right_panel()
        assert LG.is_group_visible(groups['group-name']) is True
