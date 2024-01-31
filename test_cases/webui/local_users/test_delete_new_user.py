import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
class Test_Delete_New_User:

    @staticmethod
    def test_delete_new_user(users) -> None:
        """
        This test verifies a new user can be deleted
        """
        COM.create_non_admin_user_by_api(users['username'], users['fullname'], users['password'])
        LU.refresh_local_user_page()
        assert LU.is_user_visible(users['username']) is True

        LU.unset_show_builtin_users_toggle()
        LU.confirm_delete_user_and_primary_group_by_full_name(users['fullname'])

        assert LU.is_user_visible(users['username']) is False
        NAV.navigate_to_dashboard()

