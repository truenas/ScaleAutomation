import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
class Test_Edit_User_Authentication_Fields:

    @staticmethod
    def test_edit_user_authentication_fields(users) -> None:
        """
        This test verifies a new user can be created
        """
        COM.create_non_admin_user_by_api(users['username'], users['fullname'], users['password'])
        LU.refresh_local_user_page()
        assert LU.is_user_visible(users['username']) is True

        LU.unset_show_builtin_users_toggle()
        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        # Home Directory must be set to set Authorized Key
        LU.set_user_home_directory('/nonexistent')
        LU.set_user_authorized_keys(users['key'])
        COM.click_save_button()
        # Warning dialog
        LU.confirm_home_warning_dialog()
        assert LU.assert_error_user_home_directory_not_writable() is True

        LU.set_user_home_directory(users['home-dir'])
        LU.set_user_create_home_directory_checkbox()
        LU.set_user_authorized_keys(users['key'])
        LU.set_user_ssh_password_login_enabled_checkbox()
        LU.select_user_shell(users['shell'])
        LU.set_user_lock_user_checkbox()
        LU.set_user_allowed_sudo_commands(users['sudo-commands'])
        LU.set_user_allowed_sudo_commands_no_password(users['no-password-sudo-commands'])
        LU.set_user_samba_authentication_checkbox()
        COM.click_save_button()
        assert LU.assert_error_user_samba_change_password() is True

        LU.set_user_password(users['password'])
        LU.set_user_password_confirm(users['password'])
        COM.click_save_button()

        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        assert LU.assert_user_authorized_keys(users['key']) is True
        assert LU.assert_user_ssh_password_login_enabled() is True
        assert LU.assert_user_shell(users['shell']) is True
        assert LU.assert_user_lock_user() is True
        assert LU.assert_user_allowed_sudo_commands(users['sudo-commands']) is True
        assert LU.assert_user_allowed_sudo_commands_no_password(users['no-password-sudo-commands']) is True
        assert LU.assert_user_samba_authentication() is True

        LU.set_user_allow_all_sudo_commands_checkbox()
        LU.set_user_allow_all_sudo_commands_no_password_checkbox()
        COM.click_save_button()

        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        assert LU.assert_user_allowed_sudo_commands_disabled() is True
        assert LU.assert_user_allow_all_sudo_commands() is True

        assert LU.assert_user_allowed_sudo_commands_no_password_disabled() is True
        assert LU.assert_user_allow_all_sudo_commands_no_password() is True

        COM.close_right_panel()

    @staticmethod
    def verify_teardown(users) -> None:
        """
        This test removes the new user and resets to the dashboard
        """
        # reset the change
        LU.delete_user_by_api(users['username'])
        NAV.navigate_to_dashboard()
