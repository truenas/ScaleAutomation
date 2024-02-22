from pathlib import Path

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

from helper.reporting import take_screenshot
from helper.webui import WebUI
from helper.global_config import private_config
from helper.global_config import shared_config
from keywords.api.common import API_Common
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
import xpaths


class Common:
    @classmethod
    def assert_confirm_dialog(cls) -> None:
        """
        This method confirms and dismisses a confirmation dialog popup


        Example:
            - Common.assert_confirm_dialog()
        """
        if cls.is_clickable(xpaths.common_xpaths.checkbox_field('confirm'), shared_config['SHORT_WAIT']):
            WebUI.xpath(xpaths.common_xpaths.checkbox_field('confirm')).click()
        WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('dialog-confirm'))
        WebUI.xpath(xpaths.common_xpaths.button_field('dialog-confirm')).click()
        WebUI.delay(1)

    @classmethod
    def assert_copyright_text_is_correct(cls) -> bool:
        """
        This method verifies that the iX copyright text displayed.

        :return: True if copyright text displays correctly otherwise it returns False.

        Example:
            - Common.assert_copyright_text_is_correct()
        """
        return cls.assert_text_is_visible('TrueNAS SCALE ® © 2024')

    @classmethod
    def assert_dialog_visible(cls, dialog_title: str, wait: int = shared_config['WAIT']) -> bool:
        """
        This method returns true or false weather the dialog is visible before timeout.

        :param dialog_title: The name of the title of the dialog
        :param wait: The number of seconds to wait before timeout
        :return: True if the dialog is visible before timeout otherwise it returns False.

        Example:
            - Common.assert_dialog_visible('Create Pool')
            - Common.assert_dialog_visible('Create Pool', shared_config['MEDIUM_WAIT'])
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header(dialog_title, 1), wait)

    @classmethod
    def assert_dialog_not_visible(cls, dialog_title: str, wait: int = shared_config['WAIT']) -> bool:
        """
        This method returns True or False weather the dialog is not visible before timeout.

        :param dialog_title: The name of the title of the dialog
        :param wait: The number of seconds to wait before timeout
        :return: True if the dialog is not visible before timeout otherwise it returns False.

        Example:
            - Common.assert_dialog_not_visible('Create Pool')
            - Common.assert_dialog_not_visible('Create Pool', shared_config['MEDIUM_WAIT'])
        """
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header(dialog_title, 1), wait)

    @classmethod
    def assert_label_and_value_exist(cls, label: str, value: str) -> bool:
        """
        This method returns True or False weather the given label and value is visible.

        :param label: The name of the label
        :param value: The value of the label
        :return: True if the given label and value is visible otherwise it returns False.

        Example:
            - Common.assert_label_and_value_exist('Pool Status', 'Online')
        """
        return WebUI.wait_until_visible(xpaths.xpaths.common_xpaths.label_and_value(label, value),
                                        shared_config['SHORT_WAIT'])

    @classmethod
    def assert_please_wait_not_visible(cls, wait: int = shared_config['LONG_WAIT']) -> bool:
        """
        This method returns True or False weather the please wait is not visible before timeout.

        :param wait: The number of seconds to wait before timeout
        :return: True if the please wait is not visible before timeout otherwise it returns False.

        Example:
            - Common.assert_please_wait_Not_visible()
            - Common.assert_please_wait_Not_visible(shared_config['MEDIUM_WAIT'])
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Please wait', 1), shared_config['SHORT_WAIT'])
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Please wait', 1), wait)

    @classmethod
    def assert_progress_bar_not_visible(cls, wait: int = shared_config['LONG_WAIT']) -> bool:
        """
        This method returns True or False weather the progress bar is not visible before timeout.

        :param wait: The number of seconds to wait before timeout
        :return: True if the progress bar is not visible before timeout otherwise it returns False.

        Example:
            - Common.assert_progress_bar_not_visible()
            - Common.assert_progress_bar_not_visible(shared_config['MEDIUM_WAIT'])
        """
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.progress_bar, wait)

    @classmethod
    def assert_progress_spinner_not_visible(cls, wait: int = shared_config['LONG_WAIT']) -> bool:
        """
        This method returns True or False weather the progress spinner is not visible before timeout.

        :param wait: The number of seconds to wait before timeout
        :return: True if the progress spinner is not visible before timeout otherwise it returns False.

        Example:
            - Common.assert_progress_spinner_not_visible()
            - Common.assert_progress_spinner_not_visible(shared_config['MEDIUM_WAIT'])
        """
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.progress_spinner, wait)

    @classmethod
    def assert_page_header(cls, header_text: str, timeout: int = shared_config['WAIT']) -> bool:
        """
        This method return True if the page header text is visible before timeout otherwise it returns False.

        :param header_text: is the text of the page to assert.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: True if the page header text is visible before timeout otherwise it returns False.

        Example:
            - Common.assert_page_header('Header Title')
            - Common.assert_page_header('Header Title', shared_config['SHORT_WAIT'])
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header(header_text, 1), timeout)

    @classmethod
    def assert_right_panel_header(cls, header_text) -> bool:
        """
        This method return True if the right panel header text is visible before timeout otherwise it returns False.

        :param header_text: is the text of the right panel header.
        :return: True if the right panel header text is visible before timeout otherwise it returns False.

        Example:
            - Common.assert_right_panel_header('Header text')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header(header_text, 3))

    @classmethod
    def assert_right_panel_header_is_not_visible(cls, header_text) -> bool:
        """
        This method return True if the right panel header text is not visible before timeout otherwise it returns False.

        :param header_text: is the text of the right panel header.
        :return: True if the right panel header text is not visible before timeout otherwise it returns False.

        Example:
            - Common.assert_right_panel_header_is_not_visible('Header text')
        """
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header(header_text, 3))

    @classmethod
    def assert_step_header_is_open(cls, step_header: str) -> bool:
        """
        This method verifies if the given step is visible and open.

        :param step_header: The name of the step
        :return: True if the given step is visible and open otherwise it returns False.

        Example:
            - Common.assert_step_is_visible_and_open('Identifier and Type')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.step_header_is_open(step_header),
                                        shared_config['SHORT_WAIT'])

    @classmethod
    def assert_text_is_visible(cls, text) -> bool:
        """
        This method return True if the given text is visible before timeout otherwise it returns False.

        :param text: is the text to verify it is visible.
        :return: True if the given text is visible otherwise it returns False.

        Example:
            - Common.assert_text_is_visible('any Text')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_text(text))

    @classmethod
    def assert_tree_is_expanded(cls, name: str) -> bool:
        """
        This method expands the tree if it is not expanded.
        :param name: The name of the tree
        :return: True if the tree is expanded otherwise it returns False.
        """
        expanded = False
        to = xpaths.common_xpaths.any_xpath(f'//*[contains(@data-test,"-row-{name}")]')
        if WebUI.wait_until_visible(to, shared_config['SHORT_WAIT']):
            if WebUI.get_attribute(to, 'outerText') != 'expand_more':
                cls.click_on_element(to)
            expanded = WebUI.get_attribute(to, 'outerText') == 'expand_more'
        return expanded

    @classmethod
    def cancel_confirm_dialog(cls) -> None:
        """
        This method cancels the confirmation popup dialog [no/cancel]

        Example:
            - Common.cancel_confirm_dialog()
        """
        assert WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('dialog-cancel'))
        WebUI.xpath(xpaths.common_xpaths.button_field('dialog-cancel')).click()
        WebUI.delay(1)

    @classmethod
    def clear_input_field(cls, name: str, tab: bool = False) -> None:
        """
        This method highlights the text in the given field then deletes it

        :param name: name of the field to clear
        :param tab: whether to tab out of input field

        Example:
            - Common.clear_input_field('myInput')
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.input_field(name))
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.CONTROL + 'a')
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.DELETE)
        if tab:
            WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.TAB)

    @classmethod
    def click_advanced_options_button(cls):
        """
        This method clicks the Advanced Options button.

        Example:
            - Common.click_advanced_options_button()
        """
        Common.click_button('toggle-advanced')

    @classmethod
    def click_button(cls, name: str) -> None:
        """
        This method clicks the given button.

        :param name: is the name of the button to click.

        Example:
            - Common.click_button('myButton')
        """
        cls.click_on_element(xpaths.common_xpaths.button_field(name))

    @classmethod
    def click_cancel_button(cls) -> None:
        """
        This method clicks the cancel button

        Example:
            - Common.click_cancel_button()
        """
        WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('cancel'), shared_config['SHORT_WAIT']).click()

    @classmethod
    def click_link(cls, name: str) -> None:
        """
        This method clicks the given link.

        :param name: is the name of the link to click.

        Example:
            - Common.click_link('myLink')
        """
        cls.click_on_element(xpaths.common_xpaths.link_field(name))

    @classmethod
    def click_on_element(cls, xpath: str) -> None:
        """
        This method wait and click on the given xpath element.

        :param xpath: is the xpath text to click on.

        Example:
            - Common.click_on_element('xpath')
        """
        find = WebUI.wait_until_clickable(xpath, shared_config['MEDIUM_WAIT'])
        find.click()

    @classmethod
    def click_radio_button(cls, name: str) -> None:
        """
        This method clicks the given radio button.

        :param name: is the name of the radio button to click.

        Example:
            - Common.click_radio_button('myRadio')
        """
        cls.click_on_element(xpaths.common_xpaths.radio_button_field(name))

    @classmethod
    def click_next_button(cls) -> None:
        """
        This method clicks the next button

        Example:
            - Common.click_next_button()
        """
        WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('next'), shared_config['MEDIUM_WAIT'])
        WebUI.xpath(xpaths.common_xpaths.button_field('next')).click()
        WebUI.wait_until_visible(xpaths.common_xpaths.button_field('save'), shared_config['MEDIUM_WAIT'])
        assert cls.assert_text_is_visible('What and Where')

    @classmethod
    def click_save_button(cls) -> None:
        """
        This method clicks the save button

        Example:
            - Common.click_save_button()
        """
        WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('save'), shared_config['MEDIUM_WAIT']).click()
        WebUI.delay(2)

    @classmethod
    def click_save_button_and_wait_for_progress_bar(cls) -> bool:
        """
        This method clicks the save button and waits for the progress bar to disappear

        Example:
            - Common.click_save_button_and_wait_for_progress_bar_to_disappear()
        """
        cls.click_save_button()
        return cls.assert_progress_bar_not_visible()

    @classmethod
    def close_right_panel(cls) -> None:
        """
        This method clicks the close right panel button

        Example:
            - Common.close_right_panel()
        """
        WebUI.wait_until_clickable(xpaths.common_xpaths.close_right_panel(), shared_config['MEDIUM_WAIT']).click()

    @classmethod
    def convert_to_tag_format(cls, name: str) -> str:
        """
        This method converts the given name to standard TAG format

        :param name: is the name to convert to TAG format.

        Example:
            - Common.convert_to_tag_format('Element Name')
        """
        if name.__contains__('AD03\\'):
            name = name.replace('AD03\\', 'AD-03-')
        if name.__contains__('iperf3'):
            name = name.replace('iperf3', 'iperf-3')
        if name.startswith('_'):
            name = name.replace('_', '', 1)
        name = name.replace('/', '-')
        name = name.replace('_', '-')
        name = name.replace(' ', '-')
        return name.lower()

    @classmethod
    def create_non_admin_user_by_api(cls, name: str, fullname: str, password: str, smb_auth: str = 'False') -> None:
        """
        This method creates a non admin user

        :param name: is the name of the user.
        :param fullname: is the fullname of the user.
        :param password: is the password of the user.
        :param smb_auth: is whether the user needs SMB authorization access.

        Example:
            - Common.create_non_admin_user_by_api('name', 'full name', 'password')
            - Common.create_non_admin_user_by_api('name', 'full name', 'password', True)
        """
        response = API_POST.create_non_admin_user(name, fullname, password, smb_auth)
        print(f'Response code: {response.status_code}\n\nResponse text: {response.text}')

    @classmethod
    def delete_file(cls, path: str, filename: str) -> None:
        """
        This method deletes the given file if it exists in the given directory

        :param path: the username used to log in to TrueNAS.
        :param filename: the password of the user used to log in.

        Example:
            - Common.is_file_downloaded('C:/path', 'myfile.txt')
        """
        file = Path(path + '/' + filename)
        file.unlink(True)

    @classmethod
    def delete_pill(cls, xpath: str) -> None:
        """
        This method deletes the given pill

        :param xpath: is the xpath of the pill.

        Example:
            - Common.delete_pill('xpath')
        """
        WebUI.xpath(xpaths.common_xpaths.any_xpath(xpath)).send_keys(Keys.DELETE)

    @classmethod
    def delete_user_by_api(cls, name: str) -> None:
        """
        This method creates a non admin user

        :param name: is the name of the user.

        Example:
            - Common.delete_user_by_api('user')
        """
        response = API_DELETE.delete_user(name)
        print(f'Response code: {response.status_code}\n\nResponse text: {response.text}')

    @classmethod
    def get_element_property(cls, xpath: str, prop: str = 'value') -> str | bool:
        """
        This method gets the value of the given property of the given element

        :param xpath: xpath of the element
        :param prop: name of the property to get
        :return: value of the element property

        Example:
            - Common.get_element_property('//myButton', 'disabled')
            - Common.get_element_property('//myCheckbox', 'checked')
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(xpath))
        return WebUI.xpath(xpaths.common_xpaths.any_xpath(xpath)).get_property(prop)

    @classmethod
    def get_input_property(cls, name: str, prop: str = 'value') -> str | bool:
        """
        This method gets the value of the given property of the given element

        :param name: name of the element
        :param prop: name of the property to get
        :return: value of the element property

        Example:
            - Common.get_input_property('myElement', 'disabled')
            - Common.get_input_property('myCheckbox', 'checked')
        """
        return cls.get_element_property(xpaths.common_xpaths.input_field(name), prop)

    @classmethod
    def get_label_value(cls, label: str) -> str:
        """
        This method returns the value of the given label

        :param label: the label to find the value of

        Example:
            - Common.get_label_value('Label')
        """
        return cls.get_element_property(xpaths.common_xpaths.any_xpath(f'//*[contains(text(),"{label}")]/following-sibling::*'), 'textContent')

    @classmethod
    def get_user_id_by_api(cls, username: str) -> int:
        """
        This method return the ID of the specified username.

        :param username: is the username of the user to get the ID from.
        :return: the ID of the specified username.

        Example:
            - Common.get_user_id_by_api('username')
        """
        return API_Common.get_user_id(username)

    @classmethod
    def get_user_uid_by_api(cls, username: str) -> int:
        """
        This method return the UID of the specified username.

        :param username: is the username of the user to get the UID from.
        :return: the UID of the specified username.

        Example:
            - Common.get_user_uid_by_api('username')
        """
        return API_Common.get_user_uid(username)

    @classmethod
    def is_card_not_visible(cls, card_title: str) -> bool:
        """
        This method return True if the card is not visible, otherwise it returns False.

        :param card_title: The name of the title of the card
        :return: True if the card is not visible, otherwise it returns False.

        Example:
            - Common.is_card_not_visible('myCard')
        """
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.card_title(card_title))

    @classmethod
    def is_card_visible(cls, card_title: str) -> bool:
        """
        This method return True if the card is visible, otherwise it returns False.

        :param card_title: The name of the title of the card
        :return: True if the card is visible, otherwise it returns False.

        Example:
            - Common.is_card_visible('myCard')
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.card_title(card_title))

    @classmethod
    def is_checked(cls, name: str) -> bool:
        """
        This method return True if the given checkbox is checked otherwise it returns False.

        :param name: name of the checkbox.
        :return: True if the checkbox is checked, otherwise it returns False.

        Example:
            - Common.is_checked('myCheckbox')
        """
        return cls.get_element_property(xpaths.common_xpaths.checkbox_field_attribute(name), 'checked')

    @classmethod
    def is_clickable(cls, xpath: str, timeout: int = shared_config['WAIT']) -> bool:
        """
        This method return True if the xpath element is clickable before timeout otherwise it returns False.

        :param xpath: is the xpath to wait to be clickable.
        :param timeout: is optional and is the number of second to wait before timeout, it is defaulted to
        shared_config['WAIT'].
        :return: True if the xpath element is clickable before timeout otherwise it returns False.

        Example:
            - Common.is_clickable('myXpath')
            - Common.is_clickable('myXpath', shared_config['SHORT_WAIT'])
        """
        try:
            WebUI.wait_until_clickable(xpath, timeout)
        except TimeoutException:
            print("TimeoutException occurred trying to find object: " + xpath)
            return False
        else:
            return True

    @classmethod
    def is_checkbox_disabled(cls, name: str) -> bool:
        """
        This method returns if the checkbox is disabled, otherwise it returns False.

        :param name: The name of the checkbox
        :return: True if the checkbox is disabled, otherwise it returns False.

        Example:
            - Common.is_checkbox_disabled('my-checkbox')
        """
        return cls.get_element_property(xpaths.common_xpaths.checkbox_field_attribute(name), 'disabled')

    @classmethod
    def is_dialog_visible(cls, dialog_title: str, level: int) -> bool:
        """
        This method return True if the dialog is visible, otherwise it returns False.

        :param dialog_title: The name of the title of the dialog
        :param level: The level of the title of the dialog [1/3]
        :return: True if the dialog is visible, otherwise it returns False.

        Example:
            - Common.is_dialog_visible('Dialog Title', 1)
            - Common.is_dialog_visible('Dialog Title', 3)
        """
        return cls.is_visible(xpaths.common_xpaths.any_header(dialog_title, level))

    @classmethod
    def is_file_downloaded(cls, download_path: str, filename: str) -> bool:
        """
        This method returns True if the given file exists in the given download directory, otherwise returns False

        :param download_path: the username used to log in to TrueNAS.
        :param filename: the password of the user used to log in.

        Example:
            - Common.is_file_downloaded('C:/path', 'myfile.txt')
        """
        print("@@@ PATH: " + download_path)
        file = Path(download_path + '/' + filename)
        print("@@@ FILE: " + str(file))
        return file.is_file()

    @classmethod
    def is_save_button_disabled(cls) -> bool:
        """
        This method returns True if the Save button is disabled, otherwise it returns False.

        :return: returns True if the Save button is disabled, otherwise it returns False.

        Example:
            - Common.is_save_button_disabled()
        """
        return cls.get_element_property(xpaths.common_xpaths.button_field('save'), 'disabled')

    @classmethod
    def is_toggle_enabled(cls, name: str) -> bool:
        """
        This method return True if the given toggle is enabled (uses ariaChecked attr) otherwise it returns False.

        :param name: name of the toggle field.
        :return: True if the toggle is enabled, otherwise it returns False.

        Example:
            - Common.is_toggle_enabled('ftp-service')
        """
        return eval(cls.get_element_property(xpaths.common_xpaths.toggle_field(name), 'ariaChecked').capitalize())

    @classmethod
    def is_visible(cls, xpath: str) -> bool:
        """
        This method verifies if the object identified by the given xpath is visible

        :param xpath: the xpath of the object to find
        :return: true if the object is visible

        Example:
            - Common.is_visible('myXpath')
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
    def login_to_truenas(cls, user: str, password: str) -> None:
        """
        This method navigates to the login page and logs in with given user and password

        :param user: the username used to log in TrueNAS
        :param password: the password of the user used to log in

        Example:
            - Common.login_to_truenas('user', 'password')
        """
        ip = private_config['IP']
        cls.navigate_to_login_screen(ip)
        cls.set_login_form(user, password)

    @classmethod
    def logoff_truenas(cls) -> None:
        """
        This method click the power menu and click logout.

        Example:
            - Common.logoff_truenas()
        """
        cls.click_button('power-menu')
        cls.click_button('log-out')
        assert WebUI.wait_until_not_visible(xpaths.common_xpaths.button_field('power-menu'))
        assert WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('log-in'))

    @classmethod
    def navigate_to_login_screen(cls, ip: str) -> None:
        """
        This method navigates to the login page of the given IP

        :param ip: IP address of the TrueNAS login page

        Example:
            - Common.navigate_to_login_screen('10.0.0.1')
        """
        WebUI.get(f'http://{ip}/ui/sessions/signin')
        WebUI.wait_until_visible(xpaths.common_xpaths.button_field('log-in'))

    @classmethod
    def print_defect_and_screenshot(cls, ticketnumber: str) -> None:
        """
        This method prints the NAS ticket number and screenshots.

        :param ticketnumber: The ticket number to display with the failure.

        Example:
            - Common.print_defect_and_screenshot('NAS-999999')
        """
        print(f'##### This test has an associated NAS ticket number: | {ticketnumber} | #####')
        take_screenshot(ticketnumber)
        # TODO: Refactor into webui to be a list that gets added to each time it is called.
        #  Then add to global conftest to print at the end.

    @classmethod
    def reboot_system(cls) -> None:
        """
        This method reboots the system

        Example:
            - Common.reboot_system()
        """
        cls.click_button('power-menu')
        cls.click_button('restart')
        cls.assert_confirm_dialog()
        WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Connecting to TrueNAS'),
                                 shared_config['EXTRA_LONG_WAIT'])
        WebUI.wait_until_not_visible(
            xpaths.common_xpaths.any_xpath('//ix-disconnected-message//*[contains(text(), "Connecting to TrueNAS")]'),
            shared_config['EXTRA_LONG_WAIT'])
        WebUI.wait_until_visible(xpaths.common_xpaths.input_field('username'), shared_config['EXTRA_LONG_WAIT'])
        assert WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('log-in'))

    @classmethod
    def select_then_deselect_input_field(cls, name: str) -> None:
        """
        This method clears the given field and then TABs out

        :param name: name of the field to deselect

        Example:
            - Common.select_then_deselect_input_field('myInput')
        """
        cls.set_input_field(name, '', True)

    @classmethod
    def select_option(cls, name: str, option: str) -> None:
        """
        This method selects the given option from the given select field

        :param name: name of the select field to select from
        :param option: name of the option to select

        Example:
            - Common.select_option('mySelect', 'myOption')
        """
        WebUI.wait_until_clickable(xpaths.common_xpaths.select_field(name), shared_config['MEDIUM_WAIT']).click()
        WebUI.wait_until_clickable(xpaths.common_xpaths.option_field(option), shared_config['SHORT_WAIT']).click()
        WebUI.xpath(xpaths.common_xpaths.select_field(name)).send_keys(Keys.TAB)

    @classmethod
    def select_option_by_row(cls, name: str, row: int, option: str) -> None:
        """
        This method selects the given option from the given select field row

        :param name: The name of the select field to select from.
        :param row: The row number of the select field.
        :param option: The name of the option to select.

        Example:
            - Common.select_option_text('size-and-type-data', 1, '20-gi-b-hdd')
        """
        cls.click_on_element(xpaths.common_xpaths.select_field_by_row(name, row))
        cls.click_on_element(xpaths.common_xpaths.option_field(option))

    @classmethod
    def select_option_text(cls, name: str, option: str) -> None:
        """
        This method selects the given option text from the given select field.

        :param name: The name of the select field to select from.
        :param option: The name of the option to select.

        Example:
            - Common.select_option_text('size-and-type-data', '20 GiB (HDD)')
        """
        cls.click_on_element(xpaths.common_xpaths.select_field(name))
        cls.click_on_element(f'//mat-option[contains(.,"{option}")]')

    @classmethod
    def set_10_items_per_page(cls) -> None:
        """
        This method sets the items per page to 10

        Example:
            - Common.set_10_items_per_page()
        """
        cls.set_items_per_page('10')

    @classmethod
    def set_20_items_per_page(cls) -> None:
        """
        This method sets the items per page to 20

        Example:
            - Common.set_20_items_per_page()
        """
        cls.set_items_per_page('20')

    @classmethod
    def set_50_items_per_page(cls) -> None:
        """
        This method sets the items per page to 50

        Example:
            - Common.set_50_items_per_page()
        """
        cls.set_items_per_page('50')

    @classmethod
    def set_100_items_per_page(cls) -> None:
        """
        This method sets the items per page to 100

        Example:
            - Common.set_100_items_per_page()
        """
        cls.set_items_per_page('100')

    @classmethod
    def set_checkbox(cls, name: str) -> None:
        """
        This method sets the given checkbox

        :param name: name of the checkbox to set

        Example:
            - Common.set_checkbox('myCheckbox')
        """
        cls.set_checkbox_by_state(name, True)

    @classmethod
    def set_checkbox_by_row(cls, name: str, row: int) -> None:
        """
        This method sets the given checkbox name by the given row
        :param name: The name of the checkbox.
        :param row: The row of the checkbox.

        Example:
            - Common.set_checkbox_by_row('enabled', 1)
        """
        cls.set_checkbox_by_row_and_state(name, row, True)

    @classmethod
    def set_checkbox_by_row_and_state(cls, name: str, row: int, state: bool) -> None:
        """
        This method sets the given checkbox name by the given row and state
        :param name: The name of the checkbox.
        :param row: The row of the checkbox.
        :param state: The state to set the checkbox: True to set and False to unset

        Example:
            - Common.set_checkbox_by_row_and_state('enabled', 1, True)
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.checkbox_field_by_row(name, row)) is True
        if cls.get_element_property(xpaths.common_xpaths.checkbox_field_by_row_attribute(name, row), 'checked') is not state:
            WebUI.xpath(xpaths.common_xpaths.checkbox_field_by_row(name, row)).click()
        assert cls.get_element_property(xpaths.common_xpaths.checkbox_field_by_row_attribute(name, row), 'checked') is state

    @classmethod
    def set_checkbox_by_state(cls, name: str, state: bool) -> None:
        """
        This method sets the given checkbox to the given state and asserts is set correctly

        :param name: The name of the checkbox to set
        :param state: The state to set the checkbox: True to set and False to unset

        Example:
            - Common.set_checkbox_by_state('myCheckbox', False)
            - Common.set_checkbox_by_state('myCheckbox', True)
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.checkbox_field(name)) is True
        if cls.get_element_property(xpaths.common_xpaths.checkbox_field_attribute(name), 'checked') is not state:
            WebUI.xpath(xpaths.common_xpaths.checkbox_field(name)).click()
        assert cls.get_element_property(xpaths.common_xpaths.checkbox_field_attribute(name), 'checked') is state

    @classmethod
    def set_input_field(cls, name: str, value: str, tab: bool = False, pill: bool = False) -> None:
        """
        This method sets the given field with the given value

        :param name: name of the field to set
        :param value: value to set the field to
        :param tab: whether to tab out of the field or not
        :param pill: whether a pill is created or not

        Example:
            - Common.set_input_field('myInput', 'text')
            - Common.set_input_field('myInput', 'text', True)
            - Common.set_input_field('myInput', 'text', '', True)
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.input_field(name))
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).clear()
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(value)
        if tab:
            WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.TAB)
        if pill:
            assert WebUI.get_attribute(xpaths.common_xpaths.any_pill(name, value), 'textContent').strip() == value
        else:
            assert WebUI.get_attribute(xpaths.common_xpaths.input_field(name), 'value') == value

    @classmethod
    def set_items_per_page(cls, count: str) -> None:
        """
        This method sets the items per page to the given count [10/20/50/100]

        :param count: the items per page count

        Example:
            - Common.set_items_per_page('10')
        """
        if WebUI.get_attribute(xpaths.common_xpaths.any_xpath('//mat-select'), 'innerText') != count:
            cls.select_option('page-size', f'page-size-option-{count}')

    @classmethod
    def set_login_form(cls, username: str, password: str) -> None:
        """
        This method fills out the login page form [username/password] and clicks the login button

        :param username: username to enter into the username field
        :param password: password to enter into the password field

        Example:
            - Common.set_login_form('user', 'password')
        """
        assert WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('log-in'))
        WebUI.xpath(xpaths.common_xpaths.input_field('username')).send_keys(username)
        WebUI.xpath(xpaths.common_xpaths.input_field('password')).send_keys(password)
        WebUI.xpath(xpaths.common_xpaths.button_field('log-in')).click()
        WebUI.wait_until_not_visible(xpaths.common_xpaths.button_field('log-in'))
        WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('power-menu'))

    @classmethod
    def set_search_field(cls, text: str) -> None:
        """
        This method sets the search field with the given text.

        :param text: is the text to set the search field to.

        Example:
            - Common.set_search_field('search text')
        """
        field = xpaths.common_xpaths.search_field()
        # TODO: Get this fixed (create Ticket)
        if cls.assert_page_header('Discover', shared_config['MEDIUM_WAIT']):
            field = '//*[@data-test="input"]'
        WebUI.wait_until_visible(field)
        WebUI.xpath(field).clear()
        WebUI.xpath(field).send_keys(text)

    @classmethod
    def set_textarea_field(cls, name: str, value: str, tab: bool = False) -> None:
        """
        This method sets the given textarea field with the given value.
        :param name: The name of the textarea field.
        :param value: The value to set the textarea field to.
        :param tab: Is optional, True if the user wants to tab out of the field.

        Example:
            - Common.set_textarea_field('name', 'text')
        """
        WebUI.wait_until_visible(xpaths.common_xpaths.textarea_field(name))
        WebUI.xpath(xpaths.common_xpaths.textarea_field(name)).clear()
        WebUI.xpath(xpaths.common_xpaths.textarea_field(name)).send_keys(value)
        if tab:
            WebUI.xpath(xpaths.common_xpaths.textarea_field(name)).send_keys(Keys.TAB)
        assert WebUI.get_attribute(xpaths.common_xpaths.textarea_field(name), 'value') == value

    @classmethod
    def set_toggle(cls, name: str) -> None:
        """
        This method unsets the given toggle.

        :param name: is the name of the toggle to set.

        Example:
            - Common.set_toggle('myToggle')
        """
        cls.set_toggle_by_state(name, True)

    @classmethod
    def set_toggle_by_state(cls, name: str, state: bool) -> None:
        """
        This method sets the given toggle to the given state and asserts is set correctly

        :param name: is the name of the toggle to set
        :param state: state to set the toggle to

        Example:
            - Common.set_toggle_by_state('myToggle', True)
            - Common.set_toggle_by_state('myToggle', False)
        """
        WebUI.scroll_to_element(xpaths.common_xpaths.toggle_field(name))
        toggle = WebUI.xpath(xpaths.common_xpaths.toggle_field(name))
        if eval(toggle.get_attribute('ariaChecked').title()) != state:
            toggle.click()
        # in headless sometime the assert fails a .1 delay stop the failing.
        WebUI.delay(0.5)
        toggle = WebUI.xpath(xpaths.common_xpaths.toggle_field(name))
        assert eval(toggle.get_attribute('ariaChecked').title()) is state

    @classmethod
    def unset_checkbox(cls, name: str) -> None:
        """
        This method unsets the given checkbox

        :param name: name of the checkbox to unset

        Example:
            - Common.unset_checkbox('myCheckbox')
        """
        cls.set_checkbox_by_state(name, False)

    @classmethod
    def unset_checkbox_by_row(cls, name: str, row: int) -> None:
        """
        This method unsets the given checkbox by the given row.
        :param name: The name of the checkbox.
        :param row: The row of the checkbox.

        Example:
            - Common.unset_checkbox_by_row('enabled', 1)
        """
        cls.set_checkbox_by_row_and_state(name, row, False)

    @classmethod
    def unset_toggle(cls, name: str) -> None:
        """
        This method unsets the given toggle.

        :param name: is the name of the toggle.

        Example:
            - Common.unset_toggle('myToggle')
        """
        cls.set_toggle_by_state(name, False)

    @classmethod
    def verify_logged_in_user_correct(cls, user: str, password: str) -> None:
        """
        This method verifies the NAS is logged in as the given user and if not, logs in as the given user.

        :param user: the username used to log in to TrueNAS.
        :param password: the password of the user used to log in.

        Example:
            - Common.verify_logged_in_user_correct('username', 'password')
        """
        if cls.is_visible(xpaths.common_xpaths.button_field('power-menu')):
            if not cls.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@data-test="button-user-menu"]//*[contains(text(), "{user}")]')):
                cls.logoff_truenas()
                cls.set_login_form(user, password)
                assert cls.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@data-test="button-user-menu"]//*[contains(text(), "{user}")]'))
        else:
            cls.set_login_form(user, password)
            assert cls.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@data-test="button-user-menu"]//*[contains(text(), "{user}")]'))
