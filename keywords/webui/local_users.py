import xpaths
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
    def delete_user_by_api(cls, username):
        """
        This method deletes the given user by API call

        :param username: is the name of the user to delete

        Example
         - Local_Users.delete_user_by_api('username')
        """
        API_DELETE.delete_user(username)

    @classmethod
    def is_user_visible(cls, username: str) -> bool:
        """
        This method unsets the show built-in users toggle

        :param username: is the name of the user

        Example
         - Local_Users.unset_show_builtin_users_toggle()
        """
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
