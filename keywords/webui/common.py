from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from helper.webui import WebUI
from helper.global_config import private_config
from helper.global_config import shared_config
from keywords.api.common import API_Common
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
import xpaths


class Common:
    @classmethod
    def assert_confirm_dialog(cls):
        """
        This method confirms and dismisses a confirmation dialog popup

        """
        if cls.is_visible(xpaths.common_xpaths.checkbox_field('confirm')):
            WebUI.xpath(xpaths.common_xpaths.checkbox_field('confirm')).click()
        WebUI.xpath(xpaths.common_xpaths.button_field('dialog-confirm')).click()
        WebUI.delay(1)

    @classmethod
    def assert_copyright_text_is_correct(cls) -> bool:
        """
        This method verifies that the iX copyright text displayed.

        :return: True if copyright text displays correctly otherwise it returns False.
        """
        return cls.assert_text_is_visible('TrueNAS SCALE ® © 2024')

    @classmethod
    def assert_right_panel_header(cls, header_text):
        """
        This method return True if the right panel header text is visible before timeout otherwise it returns False.

        :param header_text: is the text of the right panel header.
        :return: True if the right panel header text is visible before timeout otherwise it returns False.
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header(header_text, 3))

    @classmethod
    def assert_right_panel_header_is_not_visible(cls, header_text):
        """
        This method return True if the right panel header text is not visible before timeout otherwise it returns False.

        :param header_text: is the text of the right panel header.
        :return: True if the right panel header text is not visible before timeout otherwise it returns False.
        """
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header(header_text, 3))

    @classmethod
    def assert_text_is_visible(cls, text):
        """
        This method return True if the given text is visible before timeout otherwise it returns False.

        :param text: is the text to verify it is visible.
        :return: True if the given text is visible otherwise it returns False.
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_text(text))

    @classmethod
    def assert_page_header(cls, header_text: str, timeout: int = shared_config['WAIT']):
        """
        This method return True if the page header text is visible before timeout otherwise it returns False.

        :param header_text: is the text of the page to assert.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: True if the page header text is visible before timeout otherwise it returns False.
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header(header_text, 1), timeout)

    @classmethod
    def cancel_confirm_dialog(cls) -> None:
        """
        This method cancels the confirmation popup dialog [no/cancel]
        """
        assert cls.is_visible(xpaths.common_xpaths.button_field('dialog-cancel'))
        WebUI.xpath(xpaths.common_xpaths.button_field('dialog-cancel')).click()
        WebUI.delay(1)

    @classmethod
    def click_on_element(cls, xpath: str) -> None:
        """
        This method wait and click on the given xpath element.

        :param xpath: is the xpath text to click on.
        """
        find = WebUI.wait_until_clickable(xpath, shared_config['MEDIUM_WAIT'])
        find.click()

    @classmethod
    def click_button(cls, name: str) -> None:
        """
        This method clicks the given button.

        :param name: is the name of the button to click.
        """
        cls.click_on_element(xpaths.common_xpaths.button_field(name))

    @classmethod
    def click_link(cls, name: str) -> None:
        """
        This method clicks the given link.

        :param name: is the name of the link to click.
        """
        cls.click_on_element(xpaths.common_xpaths.link_field(name))

    @classmethod
    def click_save_button(cls) -> None:
        """
        This method clicks the save button
        """
        WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('save'), shared_config['MEDIUM_WAIT']).click()
        WebUI.delay(2)

    @classmethod
    def close_right_panel(cls) -> None:
        """
        This method clicks the close right panel button
        """
        WebUI.wait_until_clickable(xpaths.common_xpaths.close_right_panel(), shared_config['MEDIUM_WAIT']).click()

    @classmethod
    def convert_to_tag_format(cls, name: str) -> str:
        """
        This method converts the given name to standard TAG format

        :param name: is the name to convert to TAG format.
        """
        if name.__contains__('AD03\\'):
            name = name.replace('AD03\\', 'AD-03-')
        name = name.replace('/', '-')
        name = name.replace('_', '-')
        name = name.replace(' ', '-')
        return name.lower()

    @classmethod
    def create_non_admin_user_by_api(cls, name: str, fullname: str, password: str, smb_auth: str = 'false') -> None:
        """
        This method creates a non admin user

        :param name: is the name of the user.
        :param fullname: is the fullname of the user.
        :param password: is the password of the user.
        :param smb_auth: is whether the user needs SMB authorization access.
        """
        API_POST.create_non_admin_user(name, fullname, password, smb_auth)

    @classmethod
    def delete_user_by_api(cls, name: str) -> None:
        """
        This method creates a non admin user

        :param name: is the name of the user.
        """
        API_DELETE.delete_user(name)

    @classmethod
    def get_user_id_by_api(cls, username: str) -> int:
        """
        This method return the ID of the specified username.

        :param username: is the username of the user to get the ID from.
        :return: the ID of the specified username.
        """
        return API_Common.get_user_id(username)

    @classmethod
    def get_user_uid_by_api(cls, username: str) -> int:
        """
        This method return the UID of the specified username.

        :param username: is the username of the user to get the UID from.
        :return: the UID of the specified username.
        """
        return API_Common.get_user_uid(username)

    @classmethod
    def is_card_visible(cls, card_title: str):
        """
        This method return True if the card is visible, otherwise it returns False.

        :param card_title: The name of the title of the card
        :return: True if the card is visible, otherwise it returns False.
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.card_title(card_title))

    @classmethod
    def is_checked(cls, name: str) -> bool:
        """
        This method return True if the given checkbox is checked otherwise it returns False.

        :param name: name of the checkbox.
        :return: True if the checkbox is checked, otherwise it returns False.
        """
        state = False
        if bool(WebUI.xpath(xpaths.common_xpaths.checkbox_field_attribute(name)).get_property('checked')):
            state = True
        return state

    @classmethod
    def is_clickable(cls, xpath: str, timeout: int = shared_config['WAIT']) -> bool:
        """
        This method return True if the xpath element is clickable before timeout otherwise it returns False.

        :param xpath: is the xpath to wait to be clickable.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: True if the xpath element is clickable before timeout otherwise it returns False.
        """
        try:
            WebUI.wait_until_clickable(xpath, timeout)
        except TimeoutException:
            print("TimeoutException occurred trying to find object: " + xpath)
            return False
        else:
            return True

    @classmethod
    def is_service_running(cls, xpath: str) -> bool:
        """
        This method return True if the xpath element is clickable before timeout otherwise it returns False.

        :param xpath: is the service xpath.
        :return: True if the service is running, otherwise it returns False.
        """
        state = False
        text = WebUI.xpath(xpaths.common_xpaths.button_field(xpath)).get_property('innerText')
        if text == 'RUNNING':
            state = True
        return state

    @classmethod
    def is_visible(cls, xpath: str):
        """
        This method verifies if the object identified by the given xpath is visible

        :param xpath: the xpath of the object to find
        :return: true if the object is visible
        """
        obj = None
        try:
            obj = WebUI.xpath(xpath)
        except NoSuchElementException:
            print("NoSuchElementException occurred trying to find object: " + xpath)
            if obj is None:
                return False
        return obj.is_displayed()

    @classmethod
    def login_to_truenas(cls, user: str, password: str):
        """
        This method navigates to the login page and logs in with given user and password

        :param user: the username used to log in TrueNAS
        :param password: the password of the user used to log in
        """
        ip = private_config['IP']
        cls.navigate_to_login_screen(ip)
        cls.set_login_form(user, password)

    @classmethod
    def logoff_truenas(cls):
        """
        This method click the power menu and click logout.
        """
        cls.click_button('power-menu')
        cls.click_button('log-out')
        assert cls.is_clickable(xpaths.common_xpaths.input_field('username'))

    @classmethod
    def navigate_to_login_screen(cls, ip: str):
        """
        This method navigates to the login page of the given IP

        :param ip: IP address of the TrueNAS login page
        """
        WebUI.get(f'http://{ip}/ui/sessions/signin')

    @classmethod
    def select_then_deselect_input_field(cls, name: str):
        """
        This method clears the given field and then TABs out

        :param name: name of the field to deselect
        """
        cls.set_input_field(name, Keys.TAB)

    @classmethod
    def set_checkbox(cls, name: str) -> None:
        """
        This method sets the given checkbox

        :param name: name of the checkbox to set
        """
        cls.set_checkbox_by_state(name, True)

    @classmethod
    def set_checkbox_by_state(cls, name: str, state: bool) -> None:
        """
        This method sets the given checkbox to the given state and asserts is set correctly

        :param name: name of the checkbox to set
        :param state: state to set the checkbox to
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.checkbox_field(name))
        if WebUI.xpath(xpaths.common_xpaths.checkbox_field_attribute(name)).get_property('checked') != state:
            WebUI.xpath(xpaths.common_xpaths.checkbox_field(name)).click()
        assert WebUI.xpath(xpaths.common_xpaths.checkbox_field_attribute(name)).get_property('checked') == state

    @classmethod
    def set_input_field(cls, name: str, value: str, tab: bool = False) -> None:
        """
        This method sets the given field with the given value

        :param name: name of the field to set
        :param value: value to set the field to
        :param tab: whether to tab out of the field or not
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.input_field(name))
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).clear()
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(value)
        if tab:
            WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.TAB)

    @classmethod
    def set_login_form(cls, username: str, password: str):
        """
        This method fills out the login page form [username/password] and clicks the login button

        :param username: username to enter into the username field
        :param password: password to enter into the password field
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.input_field('username'))
        WebUI.xpath(xpaths.common_xpaths.input_field('username')).send_keys(username)
        WebUI.wait_until_visible(xpaths.common_xpaths.input_field('password'))
        WebUI.xpath(xpaths.common_xpaths.input_field('password')).send_keys(password)
        WebUI.xpath(xpaths.common_xpaths.button_field('log-in')).click()
        WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Dashboard', 1))
        WebUI.delay(2)

    @classmethod
    def set_toggle(cls, name: str):
        """
        This method unsets the given toggle.

        :param name: is the name of the toggle to set.
        """
        cls.set_toggle_by_state(name, True)

    @classmethod
    def set_toggle_by_state(cls, name: str, state: bool):
        """
        This method sets the given toggle to the given state and asserts is set correctly

        :param name: is the name of the toggle to set
        :param state: state to set the toggle to
        """
        WebUI.scroll_to_element(xpaths.common_xpaths.toggle_field(name))
        toggle = WebUI.xpath(xpaths.common_xpaths.toggle_field(name))
        if bool(toggle.get_attribute('ariaChecked')) != state:
            toggle.click()
        # in headless sometime the assert fails a .1 delay stop the failing.
        WebUI.delay(0.1)
        toggle = WebUI.xpath(xpaths.common_xpaths.toggle_field(name))
        assert bool(toggle.get_attribute('ariaChecked')) == state

    @classmethod
    def unset_checkbox(cls, name: str) -> None:
        """
        This method unsets the given checkbox

        :param name: name of the checkbox to unset
        """
        cls.set_checkbox_by_state(name, False)

    @classmethod
    def unset_toggle(cls, name: str):
        """
        This method unsets the given toggle.

        :param name: is the name of the toggle.
        """
        cls.set_toggle_by_state(name, False)
