import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
@pytest.mark.parametrize('builtin_users', get_data_list('builtin_users'), scope='class')
class Test_Built_In_Users:

    @staticmethod
    def test_built_in_users(builtin_users) -> None:
        """
        This test verifies a built-in user in the list of users
        """
        NAV.navigate_to_local_users()
        COM.set_100_items_per_page()
        LU.set_show_builtin_users_toggle()

        assert LU.is_user_visible(builtin_users['username']) is True
        assert LU.get_users_list_uid(builtin_users['username']) == builtin_users['uid']
        assert LU.get_users_list_builtin(builtin_users['username']) is True
        assert LU.get_users_list_full_name(builtin_users['username']) == builtin_users['full-name']

        LU.unset_show_builtin_users_toggle()
        NAV.navigate_to_dashboard()
