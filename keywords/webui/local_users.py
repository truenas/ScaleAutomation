import xpaths
from helper.webui import WebUI
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common as COM


class Local_Users:

    @classmethod
    def click_add_user_button(cls):
        """
        This method clicks the add user button

        Example
         - Local_Users.click_add_user_button()
        """
        COM.click_button('add-user')

    @classmethod
    def click_user_delete_button(cls, username: str) -> None:
        """
        This method clicks the user delete button of the given user

        :param username: is the name of the user

        Example
         - Local_Users.click_user_delete_button('username')
        """
        name = COM.convert_to_tag_format(username)
        COM.click_button('delete-' + name)

    @classmethod
    def confirm_delete_user_and_primary_group_by_full_name(cls, fullname: str) -> None:
        """
        This method confirms the user delete dialog and checks the delete primary group checkbox

        :param fullname: is the fullname of the user

        Example
         - Local_Users.click_user_delete_button('Full Name')
        """
        cls.confirm_delete_user_by_full_name(fullname, True)

    @classmethod
    def confirm_delete_user_by_full_name(cls, fullname: str, primary_group: bool = False) -> None:
        """
        This method confirms the user delete dialog and checks the delete primary group checkbox

        :param fullname: is the fullname of the user
        :param primary_group: is whether to delete the primary group as well

        Example
         - Local_Users.confirm_delete_user_by_full_name('Full Name')
         - Local_Users.confirm_delete_user_by_full_name('Full Name', True)
        """
        if COM.is_visible(xpaths.common_xpaths.any_text(fullname)):
            cls.expand_user_by_full_name(fullname)
            cls.click_user_delete_button(cls.get_username_from_full_name(fullname))
            if primary_group:
                if COM.is_visible(xpaths.common_xpaths.checkbox_field('delete-primary-group')):
                    WebUI.xpath(xpaths.common_xpaths.checkbox_field('delete-primary-group')).click()
            COM.click_button('delete')
            COM.assert_page_header('Delete User')

    @classmethod
    def delete_user_by_api(cls, username):
        """
        This method deletes the given user by API call

        :param username: is the name of the user to delete

        Example
         - Local_Users.delete_user_by_api('username')
        """
        API_DELETE.delete_user(username)

    @classmethod
    def expand_user_by_full_name(cls, fullname: str) -> None:
        """
        This method expands the given user section

        :param fullname: is the fullname of the user to expand

        Example
         - Local_Users.expand_user_by_full_name('Full Name')
        """
        name = cls.get_username_from_full_name(fullname)
        name = COM.convert_to_tag_format(name)
        if COM.is_visible(xpaths.common_xpaths.button_field('edit-' + name)) is False:
            WebUI.xpath(xpaths.common_xpaths.any_text(fullname)).click()

    @classmethod
    def get_username_from_full_name(cls, fullname: str) -> str:
        """
        This method returns the username from the given fullname

        :param fullname: is the fullname of the user to expand

        Example
         - Local_Users.get_username_from_full_name('Full Name')
        """
        name = WebUI.xpath(xpaths.common_xpaths.any_text(fullname)).text
        if name.__contains__(' fullname'):
            name = name.replace(' fullname', '')
        return name

    @classmethod
    def is_user_visible(cls, username: str) -> bool:
        """
        This method unsets the show built-in users toggle

        :param username: is the name of the user

        Example
         - Local_Users.unset_show_builtin_users_toggle()
        """
        WebUI.refresh()
        name = COM.convert_to_tag_format(username)
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@data-test="row-{name}"]'))

    @classmethod
    def set_show_builtin_users_toggle(cls):
        """
        This method sets the show built-in users toggle

        Example
         - Local_Users.set_show_builtin_users_toggle()
        """
        COM.set_toggle('show-built-in-users')

    @classmethod
    def set_user_email(cls, email):
        """
        This method sets the email of the user

        :param email: is the email of the user

        Example
         - Local_Users.set_user_email('email@nowhere.com')
        """
        COM.set_input_field('email', email)

    @classmethod
    def set_user_fullname(cls, fullname):
        """
        This method sets the fullname of the user

        :param fullname: is the fullname of the user

        Example
         - Local_Users.set_user_fullname('user fullname')
        """
        COM.set_input_field('full-name', fullname)

    @classmethod
    def set_user_password(cls, password):
        """
        This method sets the password of the user

        :param password: is the password of the user

        Example
         - Local_Users.set_user_password('password')
        """
        COM.set_input_field('password', password)

    @classmethod
    def set_user_password_confirm(cls, password):
        """
        This method sets the confirmation password of the user

        :param password: is the password of the user

        Example
         - Local_Users.set_user_password_confirm('password')
        """
        COM.set_input_field('password-conf', password)

    @classmethod
    def set_user_username(cls, username):
        """
        This method sets the name of the user

        :param username: is the name of the user

        Example
         - Local_Users.set_user_username('username')
        """
        COM.set_input_field('username', username)

    @classmethod
    def unset_show_builtin_users_toggle(cls):
        """
        This method unsets the show built-in users toggle

        Example
         - Local_Users.unset_show_builtin_users_toggle()
        """
        COM.unset_toggle('show-built-in-users')
