import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
class Test_Edit_User_User_ID_And_Group_Fields:

    @staticmethod
    def test_edit_user_user_id_and_group_fields(users) -> None:
        """
        This test verifies the user id and group fields can be edited
        """
        COM.create_non_admin_user_by_api(users['username'], users['fullname'], users['password'])
        assert LU.is_user_visible(users['username']) is True

        LU.unset_show_builtin_users_toggle()
        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        LU.add_user_auxiliary_group(users['aux-group'])
        LU.set_user_primary_group(users['primary-group'])
        COM.click_save_button()

        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        assert LU.assert_user_auxiliary_group(users['aux-group'])
        assert LU.assert_user_primary_group(users['primary-group'])

        COM.close_right_panel()

    @staticmethod
    def verify_teardown(users) -> None:
        """
        This test removes the new user
        """
        # reset the change
        NAV.navigate_to_dashboard()
