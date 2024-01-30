import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
class Test_Edit_User_Identification_Fields:

    @staticmethod
    def test_edit_user_identification_fields(users) -> None:
        """
        This test verifies the user identification fields can be edited
        """
        LU.delete_user_by_api(users['username'] + '-edt')
        COM.create_non_admin_user_by_api(users['username'], users['fullname'], users['password'])
        assert LU.is_user_visible(users['username']) is True

        LU.unset_show_builtin_users_toggle()
        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        # Edit user identification fields
        LU.unset_user_disable_password_toggle()
        LU.set_user_fullname(users['fullname'] + '-edt')
        LU.set_user_username(users['username'] + '-edt')
        LU.set_user_password(users['password'] + '-edt')
        LU.set_user_password_confirm(users['password'] + '-edt')
        LU.set_user_email(users['email'] + '-edt')
        COM.click_save_button()

        LU.expand_user_by_full_name(users['fullname'] + '-edt')
        LU.click_user_edit_button()
        LU.assert_user_username(users['username'] + '-edt')
        LU.assert_user_fullname(users['fullname'] + '-edt')
        LU.assert_user_email(users['email'] + '-edt')
        # Password fields are blank - need to log out and login to verify passwords were set
        LU.assert_user_password('')
        LU.assert_user_password_confirm('')

        COM.close_right_panel()

    @staticmethod
    def verify_user_login_after_edit(users) -> None:
        """
        This test verifies the user can login after identification fields edited
        """
        LU.expand_user_by_full_name(users['fullname'] + '-edt')
        LU.click_user_edit_button()
        LU.add_user_auxiliary_group(users['aux-group'])
        COM.click_save_button()
        COM.logoff_truenas()
        COM.set_login_form(users['username'] + '-edt', users['password'] + '-edt')
        NAV.navigate_to_local_users()
        assert COM.assert_page_header('Users')

    @staticmethod
    def verify_teardown(users) -> None:
        """
        This test removes the new user
        """
        # reset the change
        NAV.navigate_to_dashboard()
        COM.logoff_truenas()
        COM.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
        LU.delete_user_by_api(users['username'] + '-edt')
        LU.delete_user_by_api(users['username'])
