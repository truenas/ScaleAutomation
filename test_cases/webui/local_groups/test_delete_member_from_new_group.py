import pytest

from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.local_groups import Local_Groups as LG


@pytest.mark.parametrize('groups', get_data_list('local_groups'), scope='class')
class Test_Delete_Member_From_New_Group:

    @staticmethod
    def test_delete_member_from_new_group(groups) -> None:
        """
        This test verifies deleting a member from a new local group
        """
        # Environment setup
        if LG.is_group_visible(groups['group-name']) is False:
            API_DELETE.delete_group(groups['group-name'])
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

        # Environment clean up
        LG.delete_group_by_api(groups['group-name'], groups['group-privileges'])
