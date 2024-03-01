from helper.webui import WebUI
import xpaths
from keywords.webui.common import Common as COM


class Login_Invalid_Credentials:

    @classmethod
    def set_login_form_with_invalid_credentials(cls, user: str, password: str):
        """
        This method enters the invalid credentials and asserts that the relevant error message displays

        :param user: the username to enter
        :param password: the password to enter
        """
        if COM.is_visible(xpaths.common_xpaths.any_header('Dashboard', 1)):
            COM.logoff_truenas()
        COM.set_input_field('username', user, True)
        COM.set_input_field('password', password, True)
        COM.click_button('log-in')
        if user == "":
            assert COM.is_visible(xpaths.common_xpaths.any_text('Either "username" or "uid" must be specified')) is False
        # else:
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Wrong username or password. Please try again.')) is True
        WebUI.refresh()
