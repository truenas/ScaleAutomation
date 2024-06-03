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
        xpath_disk = COM.convert_to_tag_format(boot_disk)
        COM.click_button(f'{xpath_disk}-actions')
        result = COM.assert_button_is_restricted(action)
        WebUI.send_key('esc')
        return result

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

    @classmethod
    def assert_activate_boot_environment_is_restricted(cls, be_name: str) -> bool:
        """
        This method returns True or False whether the Activate button is locked and not clickable.

        :param be_name: The name of the boot environment.
        :return: True if the Activate button is locked and not clickable otherwise it returns False.

        Example:
            - Boot.assert_activate_boot_environment_is_restricted('test-bootenv')
        """
        be_xpath = COM.convert_to_tag_format(be_name)
        return COM.assert_button_is_restricted(f'bootenv-{be_xpath}-mdi-check-decagram-row-action')

    @classmethod
    def assert_clone_boot_environment_is_restricted(cls, be_name: str) -> bool:
        """
        This method returns True or False whether the Clone button is locked and not clickable.

        :param be_name: The name of the boot environment.
        :return: True if the Clone button is locked and not clickable otherwise it returns False.

        Example:
            - Boot.assert_clone_boot_environment_is_restricted('test-bootenv')
        """
        be_xpath = COM.convert_to_tag_format(be_name)
        return COM.assert_button_is_restricted(f'bootenv-{be_xpath}-mdi-content-copy-row-action')

    @classmethod
    def assert_delete_boot_environment_is_restricted(cls, be_name: str) -> bool:
        """
        This method returns True or False whether the Delete button is locked and not clickable.

        :param be_name: The name of the boot environment.
        :return: True if the Delete button is locked and not clickable otherwise it returns False.

        Example:
            - Boot.assert_delete_boot_environment_is_restricted('test-bootenv')
        """
        be_xpath = COM.convert_to_tag_format(be_name)
        return COM.assert_button_is_restricted(f'bootenv-{be_xpath}-mdi-delete-row-action')

    @classmethod
    def assert_keep_boot_environment_is_restricted(cls, be_name: str) -> bool:
        """
        This method returns True or False whether the Keep button is locked and not clickable.

        :param be_name: The name of the boot environment.
        :return: True if the Keep button is locked and not clickable otherwise it returns False.

        Example:
            - Boot.assert_keep_boot_environment_is_restricted('test-bootenv')
        """
        be_xpath = COM.convert_to_tag_format(be_name)
        return COM.assert_button_is_restricted(f'bootenv-{be_xpath}-bookmark-row-action')

    @classmethod
    def assert_rename_boot_environment_is_restricted(cls, be_name: str) -> bool:
        """
        This method returns True or False whether the Rename button is locked and not clickable.

        :param be_name: The name of the boot environment.
        :return: True if the Rename button is locked and not clickable otherwise it returns False.

        Example:
            - Boot.assert_rename_boot_environment_is_restricted('test-bootenv')
        """
        be_xpath = COM.convert_to_tag_format(be_name)
        return COM.assert_button_is_restricted(f'bootenv-{be_xpath}-mdi-rename-box-row-action')
