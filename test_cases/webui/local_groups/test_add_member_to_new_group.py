import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_groups import Local_Groups as LG


@pytest.mark.parametrize('groups', get_data_list('local_groups'), scope='class')
class Test_Add_Member_To_New_Group:

    @staticmethod
    def test_add_new_local_group_with_duplicate_gid(groups) -> None:
        """
        This test verifies adding a member to a new local group
        """
        # Environment setup
        if LG.is_group_visible(groups['group-name']) is False:
            LG.delete_group_by_api(groups['group-name'], groups['group-privileges'])
            LG.create_group_by_api(groups['group-name'])
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
