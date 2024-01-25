import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU


@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
class Test_Delete_Replicate_Task_Different_Box():

    @staticmethod
    def test_delete_new_user(users) -> None:
        """
        This test verifies a new user can be deleted
        """
        COM.create_non_admin_user_by_api(users['username'], users['fullname'], users['password'])
        assert LU.is_user_visible(users['username']) is True

        LU.unset_show_builtin_users_toggle()
        LU.confirm_delete_user_and_primary_group_by_full_name(users['fullname'])

        assert LU.is_user_visible(users['username']) is False

    @staticmethod
    def verify_teardown(users) -> None:
        """
        This test removes the new user
        """
        # reset the change
        # LU.delete_user_by_api(users['username'])
