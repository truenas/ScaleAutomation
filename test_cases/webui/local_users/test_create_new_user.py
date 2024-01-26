import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU


@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
class Test_Create_Replicate_Task_Different_Box():

    @staticmethod
    def test_add_new_user(users) -> None:
        """
        This test verifies a new user can be created
        """
        LU.click_add_user_button()

        LU.set_user_fullname(users['fullname'])
        LU.set_user_username(users['username'])
        LU.set_user_password(users['password'])
        LU.set_user_password_confirm(users['password'])
        LU.set_user_email(users['email'])

        COM.click_save_button()
        LU.unset_show_builtin_users_toggle()
        COM.set_100_items_per_page()

        assert LU.is_user_visible(users['username']) is True

    @staticmethod
    def verify_teardown(users) -> None:
        """
        This test removes the new user
        """
        # reset the change
        LU.delete_user_by_api(users['username'])