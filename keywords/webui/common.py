import datetime
import re
import xpaths
from pathlib import Path

from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.keys import Keys

from helper.cli import SSH_Command_Line
from helper.reporting import take_screenshot
from helper.webui import WebUI
from helper.global_config import private_config
from helper.global_config import shared_config
from keywords.api.common import API_Common
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST


class Common:

    @classmethod
    def add_test_file(cls, file: str, path: str, ip: str = private_config['IP'],
                      user: str = private_config['SSH_USERNAME'],
                      password: str = private_config['PASSWORD']) -> None:
        """
        This method adds the files used for testing smb permissions

        :param file: is the name of the file to add
        :param path: is the path of the file
        :param ip: is the ip of the system
        :param user: is the user accessing the system
        :param password: is the password of user accessing the system

        Example:
            - Common.add_test_file('myFile.txt', 'tank/path')
            - Common.add_test_file('myFile.txt', 'tank/path', '10.0.0.1', 'user', 'password')
        """
        SSH_Command_Line(f'sudo touch /mnt/{path}/{file}', ip, user, password)

    @classmethod
    def assert_add_item_button(cls, name: str) -> bool:
        """
        This method returns True if the given add item button is visible, otherwise returns False.

        :param name: name of the add item button
        :return: True if the given add item button is visible, otherwise returns False.

        Example:
            - Common.assert_add_item_button('add entry')
        """
        name = cls.convert_to_tag_format(name)
        return cls.is_visible(xpaths.common_xpaths.button_field(f'add-item-{name}'))

    @classmethod
    def assert_button_is_greyed_and_not_clickable(cls, name: str) -> bool:
        """
        This method asserts that the given button is greyed and not clickable

        :param name: name of the button
        :return: True if the button is greyed and not clickable otherwise it returns False

        Example:
            - Common.assert_button_is_greyed_and_not_clickable('delete')
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field_greyed(name)) is True
        try:
            # At this point the button is visible a Timeout or ElementClickIntercepted exception will be thrown.
            cls.click_button(name, 1)
        except (ElementClickInterceptedException, TimeoutException):
            return True
        return False

    @classmethod
    def assert_button_is_restricted(cls, name: str) -> bool:
        """
        This method asserts that the given button is locked and not clickable

        :param name: name of the button
        :return: True if the button is locked and not clickable otherwise it returns False

        Example:
            - Common.assert_button_is_restricted('delete')
        """
        xpath_name = cls.convert_to_tag_format(name)
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field_locked(xpath_name)) is True
        try:
            # At this point the button is visible a Timeout or ElementClickIntercepted exception will be thrown.
            cls.click_button(xpath_name, 1)
        except (ElementClickInterceptedException, TimeoutException):
            return True
        return False

    @classmethod
    def assert_checkbox_is_restricted(cls, name: str) -> bool:
        """
        This method asserts that the given checkbox is locked and not clickable

        :param name: name of the checkbox
        :return: True if the checkbox is locked and not clickable otherwise it returns False

        Example:
            - Common.assert_checkbox_is_restricted('myCheckbox')
        """
        xpath_name = cls.convert_to_tag_format(name)
        assert WebUI.wait_until_visible(xpaths.common_xpaths.checkbox_field_locked(xpath_name)) is True
        try:
            cls.set_checkbox(xpath_name)
        except ElementClickInterceptedException:
            return True
        return False

    @classmethod
    def assert_confirm_dialog(cls) -> None:
        """
        This method confirms and dismisses a confirmation dialog popup


        Example:
            - Common.assert_confirm_dialog()
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('dialog-confirm')) is True
        if cls.is_visible(xpaths.common_xpaths.checkbox_field('confirm')):
            cls.set_checkbox('confirm')
        cls.click_button('dialog-confirm')
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
        This method returns true or false whether the dialog is visible before timeout.

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
        This method returns True or False whether the dialog is not visible before timeout.

        :param dialog_title: The name of the title of the dialog
        :param wait: The number of seconds to wait before timeout
        :return: True if the dialog is not visible before timeout otherwise it returns False.

        Example:
            - Common.assert_dialog_not_visible('Create Pool')
            - Common.assert_dialog_not_visible('Create Pool', shared_config['MEDIUM_WAIT'])
        """
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header(dialog_title, 1), wait)

    @classmethod
    def assert_element_is_restricted(cls, xpath: str) -> bool:
        """
        This method asserts that the given element is locked and not clickable

        :param xpath: xpath of the element
        :return: True if the element is locked and not clickable otherwise it returns False

        Example:
            - Common.assert_element_is_restricted('delete')
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(xpath)) is True
        try:
            # At this point the element is visible a Timeout or ElementClickIntercepted exception will be thrown.
            cls.click_on_element(xpath, 1)
        except (ElementClickInterceptedException, TimeoutException):
            return True
        return False

    @classmethod
    def assert_file_exists(cls, file: str, path: str, ip: str = private_config['IP'],
                           user: str = private_config['SSH_USERNAME'],
                           password: str = private_config['PASSWORD']) -> bool:
        """
        This method returns True if the given file exists, otherwise it returns False.

        :param file: is the name of the file to find in the response to validate
        :param path: is the path of the file
        :param ip: is the ip of the system
        :param user: is the user accessing the system
        :param password: is the password of user accessing the system
        :return: returns True if the given file exists, otherwise it returns False.

        Example:
            - Common.assert_file_exists('myFile.txt', 'tank/path')
            - Common.assert_file_exists('myFile.txt', 'tank/path', '10.0.0.1', 'user', 'password')
        """
        response = SSH_Command_Line(f'ls -al /mnt/{path}', ip, user, password)
        # print(f'{file} RESPONSE: {response.status}')
        # print(f'{file} SUCCESS RESPONSE: {response.stdout}')
        # print(f'{file} ERROR RESPONSE: {response.stderr}')
        print(f'{file}: ' + str(response.stdout.__contains__(file)))
        return response.stdout.__contains__(file)

    @classmethod
    def assert_header_readonly_badge(cls) -> bool:
        """
        This method verifies the readonly badge on the header exists.

        :return: True if the readonly badge exists otherwise it returns False.

        Example:
            - Common.assert_header_readonly_badge()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.readonly_badge)

    @classmethod
    def assert_label_and_value_exist(cls, label: str, value: str) -> bool:
        """
        This method returns True or False whether the given label and value is visible.

        :param label: The name of the label
        :param value: The value of the label
        :return: True if the given label and value is visible otherwise it returns False.

        Example:
            - Common.assert_label_and_value_exist('Pool Status', 'Online')
        """
        return WebUI.wait_until_visible(xpaths.xpaths.common_xpaths.label_and_value(label, value),
                                        shared_config['SHORT_WAIT'])

    @classmethod
    def assert_link_is_restricted(cls, name: str) -> bool:
        """
        This method returns True or False whether the button is locked and not clickable.

        :param name: name of the link
        :return: True if the button is locked and not clickable otherwise it returns False

        Example:
            - Common.assert_button_is_restricted('delete')
        """
        xpath_name = cls.convert_to_tag_format(name)
        assert WebUI.wait_until_visible(xpaths.common_xpaths.link_field_locked(xpath_name)) is True
        try:
            # At this point the link is visible a Timeout or ElementClickIntercepted exception will be thrown.
            cls.click_link(xpath_name)
        except (ElementClickInterceptedException, TimeoutException):
            return True
        return False

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
    def assert_please_wait_not_visible(cls, wait: int = shared_config['LONG_WAIT']) -> bool:
        """
        This method returns True or False whether the please wait is not visible before timeout.

        :param wait: The number of seconds to wait before timeout
        :return: True if the please wait is not visible before timeout otherwise it returns False.

        Example:
            - Common.assert_please_wait_Not_visible()
            - Common.assert_please_wait_Not_visible(shared_config['MEDIUM_WAIT'])
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Please wait', 6), shared_config['SHORT_WAIT']) is True
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.any_header('Please wait', 1), wait)

    @classmethod
    def assert_progress_bar_not_visible(cls, wait: int = shared_config['LONG_WAIT']) -> bool:
        """
        This method returns True or False whether the progress bar is not visible before timeout.

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
        This method returns True or False whether the progress spinner is not visible before timeout.

        :param wait: The number of seconds to wait before timeout
        :return: True if the progress spinner is not visible before timeout otherwise it returns False.

        Example:
            - Common.assert_progress_spinner_not_visible()
            - Common.assert_progress_spinner_not_visible(shared_config['MEDIUM_WAIT'])
        """
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.progress_spinner, wait)

    @classmethod
    def assert_removed_item_button_by_row(cls, row: int = 1) -> bool:
        """
        This method returns True if the remove item button is visible, otherwise returns False.

        :param row: is the index of the remove item button.
        :return: True if the remove item button is visible, otherwise returns False.

        Example:
            - Common.assert_removed_item_button()
        """
        return cls.is_visible(xpaths.common_xpaths.any_xpath(f'(//*[@data-test="button-remove-from-list"])[{row}]'))

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
    def assert_save_button_is_restricted(cls) -> bool:
        """
        This method returns True or False if the save button is locked and not clickable.

        :return: True if the save button is locked and not clickable, otherwise it returns False.

        Example:
            - Common.assert_save_button_is_restricted()
        """
        return cls.assert_button_is_restricted('save')

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
    def assert_toggle_is_restricted(cls, name) -> bool:
        """
        This method returns True or False if the toggle is locked and not clickable.

        :return: True if the toggle is locked and not clickable, otherwise it returns False.

        Example:
            - Common.assert_toggle_is_restricted()
        """
        xpath_name = cls.convert_to_tag_format(name)
        assert WebUI.wait_until_visible(xpaths.common_xpaths.toggle_field_locked(xpath_name)) is True
        try:
            cls.click_on_element(xpaths.common_xpaths.toggle_field(xpath_name))
        except (ElementClickInterceptedException, TimeoutException):
            return True
        return False

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
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('dialog-cancel')) is True
        cls.click_button('dialog-cancel')
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
        assert WebUI.wait_until_visible(xpaths.common_xpaths.input_field(name)) is True
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.CONTROL + 'a')
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.DELETE)
        if tab:
            WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.TAB)

    @classmethod
    def clear_extra_windows(cls):
        # and switch to initial tab
        initial_tab = WebUI.window_handles()[0]
        current_tab = WebUI.current_window_handle()
        initial_index = WebUI.window_handles().index(initial_tab)
        if initial_tab != current_tab:
            WebUI.close_window()
            WebUI.switch_to_window_index(initial_index)

    @classmethod
    def click_advanced_options_button(cls):
        """
        This method clicks the Advanced Options button.

        Example:
            - Common.click_advanced_options_button()
        """
        Common.click_button('toggle-advanced-options')

    @classmethod
    def click_button(cls, name: str, timeout: int = shared_config['WAIT']) -> None:
        """
        This method clicks the given button.

        :param name: is the name of the button to click.
        :param timeout: optional - is the timeout in seconds.

        Example:
            - Common.click_button('myButton')
        """
        cls.click_on_element(xpaths.common_xpaths.button_field(name), timeout)

    @classmethod
    def click_cancel_button(cls) -> None:
        """
        This method clicks the cancel button

        Example:
            - Common.click_cancel_button()
        """
        cls.click_button('cancel')

    @classmethod
    def click_dialog_close_button(cls) -> None:
        """
        This method clicks the dialog close button

        Example:
            - Common.click_dialog_close_button()
        """
        cls.click_button('dialog-close')

    @classmethod
    def click_error_dialog_close_button(cls) -> None:
        """
        This method clicks the error dialog close button

        Example:
            - Common.click_error_dialog_close_button()
        """
        cls.click_button('close-error-dialog')

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
    def click_on_element(cls, xpath: str, timeout: int = shared_config['WAIT']) -> None:
        """
        This method wait and click on the given xpath element.

        :param xpath: is the xpath text to click on.
        :param timeout: optional - is the timeout in seconds.

        Example:
            - Common.click_on_element('xpath')
            - Common.click_on_element('xpath', 5)
            - Common.click_on_element('xpath', shared_config['MEDIUM_WAIT'])
        """
        find = WebUI.wait_until_clickable(xpath, timeout)
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
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('next'), shared_config['MEDIUM_WAIT']) is True
        cls.click_button('next')
        WebUI.delay(3)

    @classmethod
    def click_save_button(cls) -> None:
        """
        This method clicks the save button

        Example:
            - Common.click_save_button()
        """
        cls.click_button('save')
        WebUI.delay(2)

    @classmethod
    def click_save_button_and_wait_for_progress_bar(cls) -> bool:
        """
        This method clicks the save button and waits for the progress bar to disappear

        Example:
            - Common.click_save_button_and_wait_for_progress_bar()
        """
        cls.click_save_button()
        return cls.assert_progress_bar_not_visible()

    @classmethod
    def click_save_button_and_wait_for_progress_spinner(cls) -> bool:
        """
        This method clicks the save button and waits for the progress spinner to disappear

        Example:
            - Common.click_save_button_and_wait_for_progress_spinner()
        """
        cls.click_save_button()
        return cls.assert_progress_spinner_not_visible()

    @classmethod
    def click_save_button_and_wait_for_right_panel(cls) -> bool:
        """
        This method clicks the save button and waits for the right panel to disappear

        Example:
            - Common.click_save_button_and_wait_for_right_panel()
        """
        cls.click_save_button()
        assert cls.assert_progress_bar_not_visible() is True
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.close_right_panel())

    @classmethod
    def close_right_panel(cls):
        """
        This method clicks the close right panel button

        Example:
            - Common.close_right_panel()
        """
        cls.click_on_element(xpaths.common_xpaths.close_right_panel())
        assert WebUI.wait_until_not_visible(xpaths.common_xpaths.close_right_panel()) is True

    @classmethod
    def convert_to_tag_format(cls, name: str) -> str:
        """
        This method converts the given name to standard TAG format

        :param name: is the name to convert to TAG format.

        Example:
            - Common.convert_to_tag_format('Element Name')
        """
        name = name.lower()
        if name.__contains__('ad03\\'):
            name = name.replace('ad03\\', 'ad-03-')
        elif 's.m.a.r.t.' in name:
            name = name.replace('s.m.a.r.t.', 'smartd')
        else:
            # this split the name with numbers
            name_list = list(filter(None, re.split(r'(\d+)', name)))
            name = '-'.join(name_list)
        if name.startswith('_'):
            name = name.replace('_', '', 1)
        name = name.replace('/', '-')
        name = name.replace('.', '-')
        name = name.replace('_', '-')
        name = name.replace(' ', '-')
        name = name.replace('---', '-')
        name = name.replace('--', '-')
        return name

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
        API_POST.create_non_admin_user(name, fullname, password, smb_auth)

    @classmethod
    def delete_all_test_files(cls, path: str, ip: str = private_config['IP'],
                              user: str = private_config['SSH_USERNAME'],
                              password: str = private_config['SSH_PASSWORD']) -> None:
        """
        This method adds the files used for testing smb permissions

        :param path: is the path of the file
        :param ip: is the ip of the system
        :param user: is the user accessing the system
        :param password: is the password of user accessing the system

        Example:
            - Common.delete_all_test_files('tank/path')
            - Common.delete_all_test_files('tank/path', '10.0.0.1', 'user', 'password')
        """
        SSH_Command_Line(f'sudo rm /mnt/{path}/*', ip, user, password)

    @classmethod
    def delete_file(cls, path: str, filename: str) -> None:
        """
        This method deletes the given file if it exists in the given directory

        :param path: the username used to log in to TrueNAS.
        :param filename: the password of the user used to log in.

        Example:
            - Common.delete_file('C:/path', 'myfile.txt')
        """
        file = Path(f'{path}/{filename}')
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
    def delete_test_file(cls, file: str, path: str, ip: str = private_config['IP'],
                         user: str = private_config['SSH_USERNAME'],
                         password: str = private_config['PASSWORD']) -> None:
        """
        This method adds the files used for testing smb permissions

        :param file: is the name of the file to add
        :param path: is the path of the file
        :param ip: is the ip of the system
        :param user: is the user accessing the system
        :param password: is the password of user accessing the system

        Example:
            - Common.delete_test_file('myFile.txt', 'tank/path')
            - Common.delete_test_file('myFile.txt', 'tank/path', '10.0.0.1', 'user', 'password')
        """
        SSH_Command_Line(f'sudo rm /mnt/{path}/{file}', ip, user, password)

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
    def get_current_day(cls) -> int:
        """
        This method returns the current system day date [1-31]

        :return: returns the current system day date

        Example:
            - Common.get_current_day('23')
        """
        return datetime.datetime.now().day

    @classmethod
    def get_current_hour(cls) -> int:
        """
        This method returns the current system hour [0-23]

        :return: returns the current system hour

        Example:
            - Common.get_current_hour('16')
        """
        return datetime.datetime.now().hour

    @classmethod
    def get_current_minute(cls) -> int:
        """
        This method returns the current system minute [0-59]

        :return: returns the current system minute

        Example:
            - Common.get_current_minute('12')
        """
        return datetime.datetime.now().minute

    @classmethod
    def get_current_time_element(cls, element: str) -> int:
        """
        This method returns the current system element value

        :param element: the element of time to return [day/hour/minute]
        :return: returns the current system given element value

        Example:
            - Common.get_current_time_element('minute')
        """
        match element:
            case 'minute':
                return datetime.datetime.now().minute
            case 'hour':
                return datetime.datetime.now().hour
            case 'day':
                return datetime.datetime.now().day

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
        assert WebUI.wait_until_presence_is_located(xpath) is True
        return WebUI.xpath(xpath).get_property(prop)

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
    def is_button_visible(cls, name) -> bool:
        """
        This method returns True if the given button is visible, otherwise False.

        :param name: name of the button.
        :return: True if the given button is visible, otherwise False.

        Example:
            - Common.is_button_visible('save')
        """
        return cls.is_visible(xpaths.common_xpaths.button_field(cls.convert_to_tag_format(name)))

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
    def is_checkbox_visible(cls, name) -> bool:
        """
        This method returns True if the given checkbox is visible, otherwise False.

        :param name: name of the checkbox.
        :return: True if the given checkbox is visible, otherwise False.

        Example:
            - Common.is_checkbox_visible('enabled')
        """
        return cls.is_visible(xpaths.common_xpaths.checkbox_field(cls.convert_to_tag_format(name)))

    @classmethod
    def is_checked(cls, name: str) -> bool:
        """
        This method return True if the given checkbox is checked otherwise it returns False.

        :param name: name of the checkbox.
        :return: True if the checkbox is checked, otherwise it returns False.

        Example:
            - Common.is_checked('myCheckbox')
        """
        # wait the checkbox to be clickable before looking if checked
        assert cls.is_clickable(xpaths.common_xpaths.checkbox_field(name)) is True
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
            print(f"TimeoutException occurred trying to find object: {xpath}")
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
        print(f"@@@ PATH: {download_path}")
        file = Path(f'{download_path}/{filename}')
        print(f"@@@ FILE: {str(file)}")
        i = 0
        while file.is_file() is False:
            i = i + 1
            WebUI.delay(5)
            if i > 6:
                print("File not found")
                return False
        return file.is_file()

    @classmethod
    def is_input_visible(cls, name: str) -> bool:
        """
        This method returns True if the given input is visible, otherwise False.

        :param name: name of the input.
        :return: True if the given input is visible, otherwise False.

        Example:
            - Common.is_input_visible('save')
        """
        return cls.is_visible(xpaths.common_xpaths.input_field(cls.convert_to_tag_format(name)))

    @classmethod
    def is_link_visible(cls, name: str) -> bool:
        """
        This method returns True if the given link is visible, otherwise False.

        :param name: name of the link.
        :return: True if the given link is visible, otherwise False.

        Example:
            - Common.is_link_visible('save')
        """
        return cls.is_visible(xpaths.common_xpaths.link_field(cls.convert_to_tag_format(name)))

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
    def is_row_visible(cls, name: str) -> bool:
        """
        This method returns True or False whether the given row is visible.

        :param name: name of the row.
        :return: True if the given row is visible, otherwise False.

        Example:
            - Common.is_row_visible('save')
        """
        return cls.is_visible(f'//*[@data-test="row-{cls.convert_to_tag_format(name)}"]')

    @classmethod
    def is_select_visible(cls, name: str) -> bool:
        """
        This method returns True if the given select is visible, otherwise False.

        :param name: name of the select.
        :return: True if the given select is visible, otherwise False.

        Example:
            - Common.is_select_visible('save')
        """
        return cls.is_visible(xpaths.common_xpaths.select_field(cls.convert_to_tag_format(name)))

    @classmethod
    def is_select_by_row_visible(cls, name: str, row: int = 1) -> bool:
        """
        This method returns True if the given select is visible, otherwise False.

        :param name: name of the select.
        :param row: index of the select. default = 1
        :return: True if the given select is visible, otherwise False.

        Example:
            - Common.is_select_by_row_visible('search')
            - Common.is_select_by_row_visible('search', 2)
        """
        return cls.is_visible(xpaths.common_xpaths.select_field_by_row(cls.convert_to_tag_format(name), row))

    @classmethod
    def is_text_visible(cls, text: str) -> bool:
        """
        This method returns True if the given text is visible, otherwise False.

        :param text: the text.
        :return: True if the given text is visible, otherwise False.

        Example:
            - Common.is_text_visible('save')
        """
        return cls.is_visible(xpaths.common_xpaths.any_text(text))

    @classmethod
    def is_textarea_visible(cls, name: str) -> bool:
        """
        This method returns True if the given textarea is visible, otherwise False.

        :param name: name of the textarea.
        :return: True if the given textarea is visible, otherwise False.

        Example:
            - Common.is_textarea_visible('public-key')
        """
        return cls.is_visible(xpaths.common_xpaths.textarea_field(cls.convert_to_tag_format(name)))

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
    def is_toggle_visible(cls, name: str) -> bool:
        """
        This method returns True if the given toggle is visible, otherwise False.

        :param name: name of the toggle.
        :return: True if the given toggle is visible, otherwise False.

        Example:
            - Common.is_toggle_visible('builtin-users')
        """
        return cls.is_visible(xpaths.common_xpaths.toggle_field(cls.convert_to_tag_format(name)))

    @classmethod
    def is_visible(cls, xpath: str, wait: int = shared_config['SHORT_WAIT']) -> bool:
        """
        This method verifies if the object identified by the given xpath is visible

        :param xpath: the xpath of the object to find
        :param wait: the time in seconds to wait for the object to be visible
        :return: true if the object is visible

        Example:
            - Common.is_visible('myXpath')
            - Common.is_visible('myXpath', shared_config['MEDIUM_WAIT'])
        """
        return WebUI.wait_until_visible(xpath, wait)

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
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('log-in'))
        # Let the login page settle
        WebUI.delay(2)

    @classmethod
    def navigate_to_login_screen(cls, ip: str) -> None:
        """
        This method navigates to the login page of the given IP

        :param ip: IP address of the TrueNAS login page

        Example:
            - Common.navigate_to_login_screen('10.0.0.1')
        """
        WebUI.get(f'http://{ip}/ui/sessions/signin')
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('log-in')) is True

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
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Connecting to TrueNAS'),
                                        shared_config['EXTRA_LONG_WAIT']) is True
        assert WebUI.wait_until_not_visible(
            xpaths.common_xpaths.any_xpath('//ix-disconnected-message//*[contains(text(), "Connecting to TrueNAS")]'),
            shared_config['EXTRA_LONG_WAIT']) is True
        assert WebUI.wait_until_visible(xpaths.common_xpaths.input_field('username'), shared_config['EXTRA_LONG_WAIT']) is True
        WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('log-in'))

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
        WebUI.delay(0.1)
        cls.click_on_element(xpaths.common_xpaths.select_field(name))
        WebUI.delay(0.1)
        cls.click_on_element(xpaths.common_xpaths.option_field(option))
        WebUI.xpath(xpaths.common_xpaths.select_field(name)).send_keys(Keys.TAB)
        WebUI.delay(0.1)

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
        WebUI.delay(0.1)
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
        WebUI.delay(0.1)
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
        WebUI.delay(0.1)

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
        WebUI.delay(0.1)

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
            cls.click_on_element(f'(//*[@data-test="checkbox-{name}"])[{row}]')
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
        WebUI.delay(0.2)
        if cls.get_element_property(xpaths.common_xpaths.checkbox_field_attribute(name), 'checked') is not state:
            cls.click_on_element(xpaths.common_xpaths.checkbox_field(name))
            WebUI.delay(0.2)
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
            - Common.set_input_field("myInput", "text", "", True)
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.input_field(name)) is True
        # assert WebUI.wait_until_clickable(xpaths.common_xpaths.input_field(name)) is True
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).clear()
        WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(value)
        WebUI.delay(0.1)
        if tab:
            WebUI.xpath(xpaths.common_xpaths.input_field(name)).send_keys(Keys.TAB)
            WebUI.delay(0.1)
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
        WebUI.wait_until_clickable(xpaths.common_xpaths.button_field('log-in'))
        WebUI.xpath(xpaths.common_xpaths.input_field('username')).send_keys(username)
        WebUI.xpath(xpaths.common_xpaths.input_field('password')).send_keys(password)
        cls.click_button('log-in')
        assert WebUI.wait_until_not_visible(xpaths.common_xpaths.button_field('log-in'), shared_config['LONG_WAIT']) is True
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('power-menu')) is True

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
        if cls.is_visible(xpaths.common_xpaths.any_header('Discover', 1)):
            field = '//*[@data-test="input"]'
        assert WebUI.wait_until_visible(field) is True
        WebUI.xpath(field).clear()
        WebUI.xpath(field).send_keys(text)
        WebUI.delay(1)

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
        assert WebUI.wait_until_visible(xpaths.common_xpaths.textarea_field(name)) is True
        WebUI.xpath(xpaths.common_xpaths.textarea_field(name)).clear()
        WebUI.xpath(xpaths.common_xpaths.textarea_field(name)).send_keys(value)
        if tab:
            WebUI.xpath(xpaths.common_xpaths.textarea_field(name)).send_keys(Keys.TAB)
        assert WebUI.get_attribute(xpaths.common_xpaths.textarea_field(name), 'value') == value

    @classmethod
    def set_toggle(cls, name: str) -> None:
        """
        This method sets the given toggle.

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
            assert cls.assert_progress_spinner_not_visible() is True
        WebUI.wait_until_visible(xpaths.common_xpaths.toggle_field(name))
        toggle = WebUI.xpath(xpaths.common_xpaths.toggle_field(name))
        i = 0
        while eval(toggle.get_attribute('ariaChecked').title()) != state and i > shared_config['WAIT']:
            i += 1
            WebUI.delay(1)
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
                print("Wrong user. Logging off.")
                cls.logoff_truenas()
                print("Logging in as correct user.")
                cls.set_login_form(user, password)
                assert cls.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@data-test="button-user-menu"]//*[contains(text(), "{user}")]'))
            else:
                print("\nLogged in as correct user.")
        else:
            print("Not logged in. Logging in as correct user.")
            cls.set_login_form(user, password)
            assert cls.is_visible(xpaths.common_xpaths.any_xpath(f'//*[@data-test="button-user-menu"]//*[contains(text(), "{user}")]'))

    @classmethod
    def wait_for_system_time(cls, time: str, value: int) -> None:
        """
        This method waits in increments of 1 interval until the given time element is equal to or later than the given value.

        :param time: the time element to check against. ['day'/'hour'/'minute']
        :param value: the vale used to verify against.

        Example:
            - Common.wait_for_system_time('minute', 10)
        """
        pause = 0
        match time:
            case 'minute':
                pause = 60
            case 'hour':
                pause = 3600
            case 'day':
                pause = 86400

        if (value % pause) == 0:
            value = 1

        while cls.get_current_time_element(time) < value:
            print(f"@@@ WAIT FOR: {str(cls.get_current_time_element(time))} to be: {value}")
            WebUI.delay(pause)
