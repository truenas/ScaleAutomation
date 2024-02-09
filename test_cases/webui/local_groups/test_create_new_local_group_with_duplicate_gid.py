import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_groups import Local_Groups as LG
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('groups', get_data_list('local_groups'), scope='class')
class Test_Create_New_Local_Group:

    @staticmethod
    def test_add_new_local_group_with_duplicate_gid(groups) -> None:
        """
        This test verifies a new local group with duplicate ID can be created
        """
        # Environment setup
        NAV.navigate_to_local_groups()
        LG.unset_show_builtin_groups_toggle()
        LG.click_add_group_button()
        LG.set_group_gid(groups['dup-gid'])
        LG.set_group_name(groups['group-name'])
        COM.click_save_button()
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

        # Environment clean up
        NAV.navigate_to_dashboard()
        LG.delete_group_by_api(groups['group-name'], groups['group-privileges'])
        LG.delete_group_by_api(groups['alt-group-name'], groups['group-privileges'])
