import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
class Test_Edit_User_Directory_Permissions:

    @staticmethod
    def test_edit_user_directory_permissions(users) -> None:
        """
        This test verifies the user directory permissions can be edited
        """
        COM.create_non_admin_user_by_api(users['username'], users['fullname'], users['password'])
        assert LU.is_user_visible(users['username']) is True

        LU.unset_show_builtin_users_toggle()
        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        LU.set_user_home_directory(users['home-dir'])
        LU.set_user_create_home_directory_checkbox()

        LU.unset_user_home_directory_permission_user_read_checkbox()
        LU.unset_user_home_directory_permission_user_write_checkbox()
        LU.unset_user_home_directory_permission_user_execute_checkbox()

        LU.unset_user_home_directory_permission_group_read_checkbox()
        LU.unset_user_home_directory_permission_group_write_checkbox()
        LU.unset_user_home_directory_permission_group_execute_checkbox()

        LU.unset_user_home_directory_permission_other_read_checkbox()
        LU.unset_user_home_directory_permission_other_write_checkbox()
        LU.unset_user_home_directory_permission_other_execute_checkbox()

        COM.click_save_button()

        # Home Directory requires User Execution. Verify Error message, then set User Execute permission
        assert LU.assert_error_user_home_directory_requires_execute() is True

        LU.set_user_home_directory_permission_user_execute_checkbox()

        COM.click_save_button()

        # Home Directory requires User Read. Verify Error message, then set User Read permission
        assert LU.assert_error_user_home_directory_requires_read() is True

        LU.set_user_home_directory_permission_user_read_checkbox()

        COM.click_save_button()

        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        assert LU.assert_user_home_directory(users['home-dir'] + "/" + users['username']) is True
        assert LU.assert_user_home_directory_permission_user_read_checkbox() is True
        assert LU.assert_user_home_directory_permission_user_write_checkbox() is False
        assert LU.assert_user_home_directory_permission_user_execute_checkbox() is True

        assert LU.assert_user_home_directory_permission_group_read_checkbox() is False
        assert LU.assert_user_home_directory_permission_group_write_checkbox() is False
        assert LU.assert_user_home_directory_permission_group_execute_checkbox() is False

        assert LU.assert_user_home_directory_permission_other_read_checkbox() is False
        assert LU.assert_user_home_directory_permission_other_write_checkbox() is False
        assert LU.assert_user_home_directory_permission_other_execute_checkbox() is False

        COM.close_right_panel()

    @staticmethod
    def verify_teardown(users) -> None:
        """
        This test removes the new user
        """
        # reset the change
        LU.delete_user_by_api(users['username'])
        NAV.navigate_to_dashboard()
