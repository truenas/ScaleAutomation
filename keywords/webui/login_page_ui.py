from helper.webui import WebUI
from keywords.webui.common import Common as COM
from helper.global_config import private_config
import xpaths


class Login_Page_Ui:

    @classmethod
    def assert_background_image_displays(cls) -> bool:
        """
        This method verifies that the background image displays on the login page

        :return: true if background image displays
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath('//img[@src="assets/images/stars-sky-1200w.jpg"]'))

    @classmethod
    def assert_error_password_requirement_displays_after_deselection(cls) -> bool:
        """
        This method verifies that the password is required error message displays on the login page when field is
        set to blank

        :return: true if password error displays after deselection
        """
        return cls.assert_requirement_error_displays_with_empty_field('Password')

    @classmethod
    def assert_error_password_requirement_doesnt_display(cls, password: str) -> bool:
        """
        This method verifies that the password is required error message doesn't display on the login page when
        field is set

        :param password: password to use in the password field
        :return: true if password error doesn't display when required field is not empty
        """
        return cls.set_textfield_and_assert_error_message_not_present('Password', password)

    @classmethod
    def assert_error_password_requirement_doesnt_display_on_page_load(cls) -> bool:
        """
        This method verifies that the password is required error message doesn't display on the login page when
        page refresh

        :return: true if password error doesn't display on page load  (or is None - doesn't exist)
        """
        WebUI.refresh()
        return not COM.is_visible(xpaths.common_xpaths.any_text('Password is required'))

    @classmethod
    def assert_error_username_requirement_after_login_attempt_displays_after_reselection(cls) -> bool:
        """
        This method verifies that the username is required error message displays on the login page when
        field is reselected

        :return: true if username error does not display after re-selecting an empty username login attempt
        """
        WebUI.refresh()
        COM.select_then_deselect_input_field('username')
        WebUI.xpath(xpaths.common_xpaths.button_field('log-in')).click()
        WebUI.delay(1)
        return COM.is_visible(xpaths.common_xpaths.any_text('Either "username" or "uid" must be specified'))

    @classmethod
    def assert_error_username_requirement_displays_after_deselection(cls) -> bool:
        """
        This method verifies that the username is required error message displays on the login page when field is
        set to blank

        :return: true if username error displays after deselection
        """
        return cls.assert_requirement_error_displays_with_empty_field('Username')

    @classmethod
    def assert_error_username_requirement_displays_after_login_attempt(cls) -> bool:
        """
        This method verifies that the username is required error message displays on the login page when field is
        set to blank and attempt to log in

        :return: true if username error displays after empty username login attempt
        """
        WebUI.refresh()
        COM.select_then_deselect_input_field('username')
        WebUI.xpath(xpaths.common_xpaths.button_field('log-in')).click()
        WebUI.delay(1)
        return COM.is_visible(xpaths.common_xpaths.any_text('Either "username" or "uid" must be specified'))

    @classmethod
    def assert_error_username_requirement_doesnt_display(cls, username: str) -> bool:
        """
        This method verifies that the username is required error message doesn't display on the login page when
        field is set

        :param username: username to use in the username field
        :return: true if username error doesn't display when required field is not empty
        """
        return cls.set_textfield_and_assert_error_message_not_present('Username', username)

    @classmethod
    def assert_error_username_requirement_doesnt_display_on_page_load(cls) -> bool:
        """
        This method verifies that the username is required error message doesn't display on the login page when
        page refreshed

        :return: true if username error doesn't display on page load  (or is None - doesn't exist)
        """
        WebUI.refresh()
        return not COM.is_visible(xpaths.common_xpaths.any_text('Username is Required'))

    @classmethod
    def assert_ixsystems_icon_displays(cls) -> bool:
        """
        This method verifies that the iXSystems icon displays on the login page

        :return: true if iXSystem icon displays
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath('//img[@src="assets/images/ix_logo_full.png"]'))

    @classmethod
    def assert_ixsystems_link_is_correct(cls) -> bool:
        """
        This method verifies that the iXSystems link opens new tab and the url is correct

        :return: true if iXSystem link is correct
        """
        assert WebUI.current_url() == 'http://'+private_config["IP"]+'/ui/sessions/signin'
        WebUI.xpath(xpaths.common_xpaths.any_xpath('//img[@src="assets/images/ix_logo_full.png"]')).click()

        # verify still on current page
        assert WebUI.current_url() == 'http://'+private_config["IP"]+'/ui/sessions/signin'

        # switch to new tab and verify url
        WebUI.switch_to_window_index(1)
        result = WebUI.current_url() == 'https://www.ixsystems.com/'

        # close tab and switch to original tab
        WebUI.close_window()
        WebUI.switch_to_window_index(0)

        return result

    @classmethod
    def assert_password_visibility_button_toggles_off_to_on(cls) -> bool:
        """
        This method verifies that the password visibility button on the login page can toggle from off to on

        :return: true if password visibility state is on
        """
        return cls.click_and_assert_password_visibility_button("visibility_off", "visibility")

    @classmethod
    def assert_password_visibility_button_toggles_on_to_off(cls) -> bool:
        """
        This method verifies that the password visibility button on the login page can toggle from on to off

        :return: true if password visibility state is off
        """
        return cls.click_and_assert_password_visibility_button("visibility", "visibility_off")

    @classmethod
    def assert_requirement_error_displays_with_empty_field(cls, name: str) -> bool:
        """
        This method verifies that the given name field [username/password] is required error message displays
        on the login page when field is set to blank

        :param name: name of the textfield
        :return: true if error displays when required field is empty  (or is None - doesn't exist)
        """
        WebUI.refresh()
        COM.select_then_deselect_input_field(name.lower())
        return COM.is_visible(xpaths.common_xpaths.any_text(name+' is Required'))

    @classmethod
    def assert_text_doesnt_affect_password_visibility_button(cls) -> bool:
        """
        This method verifies that entering values into the password field doesn't affect the password visibility button

        :return: true if text doesn't affect password visibility toggle
        """
        WebUI.xpath(xpaths.common_xpaths.input_field('password')).send_keys('words')
        assert WebUI.xpath(xpaths.common_xpaths.input_field('password')).get_attribute('value') == 'words'
        cls.click_and_assert_password_visibility_button("visibility_off", "visibility")
        assert WebUI.xpath(xpaths.common_xpaths.input_field('password')).get_attribute('value') == 'words'
        cls.click_and_assert_password_visibility_button("visibility", "visibility_off")
        WebUI.xpath(xpaths.common_xpaths.input_field('password')).clear()
        WebUI.xpath(xpaths.common_xpaths.input_field('password')).send_keys('words part two electric boogaloo')
        assert WebUI.xpath(xpaths.common_xpaths.input_field('password')).get_attribute('value') == 'words part two electric boogaloo'
        WebUI.xpath(xpaths.common_xpaths.input_field('password')).clear()
        return WebUI.xpath(xpaths.common_xpaths.input_field('password')).get_attribute('value') == ''

    @classmethod
    def assert_truenas_icon_displays(cls) -> bool:
        """
        This method verifies that the TrueNAS icon displays on the login page

        :return: true if TrueNAS icon displays
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath('//ix-icon[@name="ix:logo_truenas_scale_full"]'))

    @classmethod
    def click_and_assert_password_visibility_button(cls, initial_state: str, after_state: str) -> bool:
        """
        This method verifies that the password visibility button is in the correct state when clicked

        :param initial_state: initial state of password field
        :param after_state: state of password field after toggle
        :return: true if password state equals after_state
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('toggle-password-password')) is True
        if WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f"//*[@fonticon='{initial_state}']")):
            WebUI.xpath(xpaths.common_xpaths.button_field('toggle-password-password')).click()
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f"//*[@fonticon='{after_state}']")) is True

    @classmethod
    def set_textfield_and_assert_error_message_not_present(cls, name: str, entry: str) -> bool:
        """
        This method verifies that the given name field [username/password] is required error message doesn't display
        on the login page when field is set

        :param name: name of the textfield
        :param entry: value to enter into the textfield
        :return: true if username error doesn't display when required field is not empty
        """
        WebUI.xpath(xpaths.common_xpaths.input_field(name.lower())).clear()
        WebUI.xpath(xpaths.common_xpaths.input_field(name.lower())).send_keys(entry)
        return not COM.is_visible(xpaths.common_xpaths.any_text(name+' is required'))
