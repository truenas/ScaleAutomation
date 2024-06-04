import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM


class Boot:

    @classmethod
    def assert_boot_disk_actions_is_restricted(cls, boot_disk: str, action: str) -> bool:
        """
        This method returns True or False whether the Boot disk actions button is locked and not clickable.

        :param boot_disk: The name of the data disks
        :param action: The name of the action. Options [attach, detach, replace].
        :return: True if the Boot disk actions button is locked and not clickable otherwise it returns False.


        Example:
            - Boot.assert_boot_disk_actions_is_restricted('sda3')
        """
        COM.click_button(f'{COM.convert_to_tag_format(boot_disk)}-actions')
        result = COM.assert_button_is_restricted(action)
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_boot_environment_element_restricted(cls, be_name: str, action: str) -> bool:
        """
        This method returns True or False whether the link is restricted or not.

        :param be_name: The name of the boot environment.
        :param action: The name of the action link on the boot environment.
            Options: [activate, clone, delete, keep, rename]
        :return: True if the link is restricted and not clickable otherwise it returns False.

        Example:
            - Boot.assert_boot_environment_element_restricted('test-bootenv', 'activate')
        """
        be_xpath = COM.convert_to_tag_format(be_name)
        match action:
            case('activate'):
                action_xpath = 'mdi-check-decagram'
            case('clone'):
                action_xpath = 'mdi-content-copy'
            case('delete'):
                action_xpath = 'mdi-delete'
            case('keep'):
                action_xpath = 'bookmark'
            case('rename'):
                action_xpath = 'mdi-rename-box'
            case _:
                assert False, f'Invalid action: {action}'
        return COM.assert_button_is_restricted(f'bootenv-{be_xpath}-{action_xpath}-row-action')

    @classmethod
    def assert_boot_environment_row_exist(cls, be_name: str) -> bool:
        """
        This method returns True or False whether the boot environment exists in the list.

        :param be_name: The name of the boot environment.
        :return: True if the boot environment exists in the list otherwise it returns False.

        Example:
            - Boot.assert_boot_environment_row_exist('test-bootenv')
        """
        be_xpath = COM.convert_to_tag_format(be_name)
        return WebUI.wait_until_visible(f'//*[@data-test="row-bootenv-{be_xpath}"]')

    @classmethod
    def assert_boot_pool_status(cls, status: str) -> bool:
        """
        This method returns True if the boot pool status is active.

        :param status: The status of the boot pool options [ACTIVE/OFFLINE/ONLINE]
        :return: True if the boot pool status is active otherwise it returns False.

        Example:
            - Boot.assert_boot_pool_status('active')
        """
        return WebUI.wait_until_visible(xpaths.boot.boot_pool_status(status))
