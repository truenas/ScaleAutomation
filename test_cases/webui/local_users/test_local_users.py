import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.local_users import Local_Users as LU
from keywords.webui.navigation import Navigation as NAV


@allure.tag("Local Users")
@allure.epic("Credentials")
@allure.feature("Local Users")
@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
class Test_Local_Users:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, users) -> None:
        """
        This method sets up each test to start with builtin users not shown
        """
        API_DELETE.delete_user(users['username'])
        API_DELETE.delete_user(users['username'] + '-edt')
        API_POST.create_non_admin_user(users['username'], users['fullname'], users['password'], 'False')
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_local_users()
        LU.unset_show_builtin_users_toggle()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, users):
        """
        This method clears any test users after test is run for a clean environment
        """
        yield
        # Clean up environment.
        API_DELETE.delete_user(users['username'])
        API_DELETE.delete_user(users['username'] + '-edt')
        COM.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])

    @allure.tag("Create", 'Percy')
    @allure.story("Add New Local Users")
    def test_add_new_user(self, users) -> None:
        """
        Summary: This test verifies a new user can be created

        Test Steps:
        1. Click Add User button
        2. Edit User values (username, fullname, password, confirm password, email)
        3. Click Save button
        4. Verify User is visible
        """
        API_DELETE.delete_user(users['username'])
        assert LU.is_user_not_visible(users['username']) is True
        LU.click_add_user_button()

        LU.set_user_fullname(users['fullname'])
        LU.set_user_username(users['username'])
        LU.set_user_password(users['password'])
        LU.set_user_password_confirm(users['password'])
        LU.set_user_email(users['email'])
        WebUI.take_percy_snapshot('Add User UI', scope='//*[contains(@class,"ix-slide-in-body")]')
        COM.click_save_button_and_wait_for_progress_bar()
        LU.unset_show_builtin_users_toggle()
        LU.refresh_local_user_page('100')

        assert LU.is_user_visible(users['username']) is True
        WebUI.take_percy_snapshot('Users UI with New User')

    @allure.tag("Delete")
    @allure.story("Delete Local Users")
    def test_delete_new_user(self, users) -> None:
        """
        Summary: This test verifies a new user can be deleted

        Test Steps:
        1. Verify User is visible
        2. Expand User then Delete User and confirm
        3. Verify User is Not visible
        """
        assert LU.is_user_visible(users['username'])

        LU.unset_show_builtin_users_toggle()
        LU.confirm_delete_user_and_primary_group_by_full_name(users['fullname'])

        assert LU.is_user_not_visible(users['username'])

    @allure.tag("Update")
    @allure.story("Edit Local Users - Authentication Fields")
    def test_edit_user_authentication_fields(self, users) -> None:
        """
        Summary: This test verifies user authentication fields can be edited

        Test Steps:
        1. Verify User is visible
        2. Edit User Authentication fields
        3. Click Save button
        4. Verify User Authentication fields are set
        """
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
        COM.click_error_dialog_close_button()

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
        COM.click_save_button_and_wait_for_progress_bar()
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
        COM.click_save_button_and_wait_for_progress_bar()
        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        assert LU.assert_user_allowed_sudo_commands_disabled() is True
        assert LU.assert_user_allow_all_sudo_commands() is True

        assert LU.assert_user_allowed_sudo_commands_no_password_disabled() is True
        assert LU.assert_user_allow_all_sudo_commands_no_password() is True

        COM.close_right_panel()

    @allure.tag("Update")
    @allure.story("Edit Local Users - Directory Permissions")
    def test_edit_user_directory_permissions(self, users) -> None:
        """
        Summary: This test verifies user directory permission fields can be edited

        Test Steps:
        1. Verify User is visible
        2. Edit User directory permission fields
        3. Click Save button
        4. Verify User directory permission fields are set
        """
        assert LU.is_user_visible(users['username']) is True

        LU.unset_show_builtin_users_toggle()
        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        LU.set_user_home_directory(users['home-dir'])
        LU.set_user_create_home_directory_checkbox()

        # Home Directory requires User Read. Verify Error message, then set User Read permission
        LU.unset_user_home_directory_permission_user_read_checkbox()
        COM.click_save_button()
        assert LU.assert_error_user_home_directory_requires_read() is True
        COM.click_error_dialog_close_button()
        LU.set_user_home_directory_permission_user_read_checkbox()

        LU.unset_user_home_directory_permission_user_write_checkbox()

        # Home Directory requires User Execution. Verify Error message, then set User Execute permission
        LU.unset_user_home_directory_permission_user_execute_checkbox()
        COM.click_save_button()
        assert LU.assert_error_user_home_directory_requires_execute() is True
        COM.click_error_dialog_close_button()
        LU.set_user_home_directory_permission_user_execute_checkbox()

        LU.unset_user_home_directory_permission_group_read_checkbox()
        LU.unset_user_home_directory_permission_group_write_checkbox()
        LU.unset_user_home_directory_permission_group_execute_checkbox()

        LU.unset_user_home_directory_permission_other_read_checkbox()
        LU.unset_user_home_directory_permission_other_write_checkbox()
        LU.unset_user_home_directory_permission_other_execute_checkbox()

        COM.click_save_button_and_wait_for_progress_bar()

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

    @allure.tag("Update")
    @allure.story("Edit Local Users - Identification Fields")
    def test_edit_user_identification_fields(self, users) -> None:
        """
        Summary: This test verifies user identification fields can be edited

        Test Steps:
        1. Verify User is visible
        2. Edit User identification fields
        3. Click Save button
        4. Verify User identification fields are set
        """
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
        COM.click_save_button_and_wait_for_progress_bar()

        LU.expand_user_by_full_name(users['fullname'] + '-edt')
        LU.click_user_edit_button()
        LU.assert_user_username(users['username'] + '-edt')
        LU.assert_user_fullname(users['fullname'] + '-edt')
        LU.assert_user_email(users['email'] + '-edt')
        # Password fields are blank - need to log out and login to verify passwords were set
        LU.assert_user_password('')
        LU.assert_user_password_confirm('')

        COM.close_right_panel()

    @allure.tag("Update")
    @allure.story("Edit Local Users - User ID and Group Fields")
    def test_edit_user_user_id_and_group_fields(self, users) -> None:
        """
        Summary: This test verifies user id and group fields can be edited

        Test Steps:
        1. Verify User is visible
        2. Edit user id and group fields
        3. Click Save button
        4. Verify user id and group fields are set
        """
        assert LU.is_user_visible(users['username']) is True

        LU.unset_show_builtin_users_toggle()
        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        LU.add_user_auxiliary_group(users['aux-group'])
        LU.set_user_primary_group(users['primary-group'])
        COM.click_save_button_and_wait_for_progress_bar()

        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()

        assert LU.assert_user_auxiliary_group(users['aux-group'])
        assert LU.assert_user_primary_group(users['primary-group'])

        COM.close_right_panel()

    @allure.tag("Update")
    @allure.story("Edit Local Users - Login with New User")
    def verify_user_login_after_edit(self, users) -> None:
        """
        Summary: This test verifies user can log in after identification fields edited

        Test Steps:
        1. Verify User is visible
        2. Edit User identification fields
        3. Click Save button
        4. Log off
        4. Verify User can log in
        """
        assert LU.is_user_visible(users['username']) is True

        LU.expand_user_by_full_name(users['fullname'])
        LU.click_user_edit_button()
        LU.add_user_auxiliary_group(users['aux-group'])
        COM.click_save_button_and_wait_for_progress_bar()
        NAV.navigate_to_dashboard()
        COM.logoff_truenas()
        COM.set_login_form(users['username'], users['password'])
        NAV.navigate_to_local_users()
        assert COM.assert_page_header('Users')

        # Log in with default user
        COM.logoff_truenas()
        COM.set_login_form(private_config['USERNAME'], private_config['PASSWORD'])
