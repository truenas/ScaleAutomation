import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_groups import Local_Groups as LG
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('groups', get_data_list('local_groups'), scope='class')
class Test_Create_New_Local_Group:

    @staticmethod
    def test_add_new_local_group(groups) -> None:
        """
        This test verifies a new local group can be created
        """
        # NAV.navigate_to_local_groups()
        LG.unset_show_builtin_groups_toggle()
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
        NAV.navigate_to_dashboard()
        LG.delete_group_by_api(groups['group-name'], groups['group-privileges'])
