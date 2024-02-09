import pytest

from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.local_groups import Local_Groups as LG


@pytest.mark.parametrize('groups', get_data_list('local_groups'), scope='class')
class Test_Local_Groups:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, groups) -> None:
        """
        This method sets up each test to start with builtin groups not shown
        """
        LG.unset_show_builtin_groups_toggle()
        API_DELETE.delete_group(groups['group-name'], groups['group-privileges'])
        API_DELETE.delete_group(groups['alt-group-name'], groups['group-privileges'])

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, groups):
        """
        This method clears any test groups after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_group(groups['group-name'], groups['group-privileges'])
        API_DELETE.delete_group(groups['alt-group-name'], groups['group-privileges'])

    @staticmethod
    def test_add_member_to_new_group(groups) -> None:
        """
        This test verifies adding a member to a new local group
        """
        # Environment setup
        print("@@@ ADD MEMBER TEST:")
        if LG.is_group_visible(groups['group-name']) is False:
            API_POST.create_group(groups['group-name'])
            assert LG.is_group_visible(groups['group-name']) is True

        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_members_button(groups['group-name'])
        LG.click_user_account_by_name(groups['username'])
        LG.click_add_to_list_button()
        assert LG.is_user_in_group_list(groups['username']) is True
        assert LG.is_user_in_users_list(groups['username']) is False
        COM.click_save_button()
        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_members_button(groups['group-name'])
        assert LG.is_user_in_group_list(groups['username']) is True
        assert LG.is_user_in_users_list(groups['username']) is False
        COM.click_cancel_button()

    @staticmethod
    def test_create_new_local_group(groups) -> None:
        """
        This test verifies a new local group can be created
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
        COM.click_save_button()
        assert LG.is_group_visible(groups['group-name']) is True

    @staticmethod
    def test_create_new_local_group_with_duplicate_gid(groups) -> None:
        """
        This test verifies a new local group with duplicate ID can be created
        """
        # Environment setup
        if LG.is_group_visible(groups['group-name']) is False:
            LG.click_add_group_button()
            LG.set_group_gid(groups['dup-gid'])
            LG.set_group_name(groups['group-name'])
            COM.click_save_button()
            assert LG.is_group_visible(groups['group-name']) is True
            assert LG.assert_group_gid(groups['group-name'], groups['dup-gid']) is True

        LG.click_add_group_button()
        LG.set_allow_duplicate_gids()
        LG.set_group_gid(groups['dup-gid'])
        LG.set_group_name(groups['alt-group-name'])
        COM.click_save_button()
        assert LG.is_group_visible(groups['alt-group-name']) is True
        assert LG.assert_group_gid(groups['alt-group-name'], groups['dup-gid']) is True
        LG.expand_group_by_name(groups['alt-group-name'])
        LG.click_group_edit_button_by_name(groups['alt-group-name'])
        assert LG.assert_gid_field_is_disabled() is True
        COM.click_save_button()
        LG.delete_group_by_api(groups['group-name'], groups['group-privileges'])
        LG.delete_group_by_api(groups['alt-group-name'], groups['group-privileges'])

    @staticmethod
    def test_delete_member_from_new_group(groups) -> None:
        """
        This test verifies deleting a member from a new local group
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
            COM.click_save_button()
            assert LG.is_group_visible(groups['group-name']) is True

        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_members_button(groups['group-name'])
        LG.click_user_account_by_name(groups['username'])
        LG.click_remove_from_list_button()
        assert LG.is_user_in_group_list(groups['username']) is False
        assert LG.is_user_in_users_list(groups['username']) is True
        COM.click_save_button()
        LG.expand_group_by_name(groups['group-name'])
        LG.click_group_members_button(groups['group-name'])
        assert LG.is_user_in_group_list(groups['username']) is False
        assert LG.is_user_in_users_list(groups['username']) is True
        COM.click_cancel_button()
