import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM


class Boot:

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
        return WebUI.wait_until_visible(f'//*[@data-test="row-{be_xpath}"]')

    @classmethod
    def assert_boot_pool_status(cls, status: str) -> bool:
        """
        This method returns True if the boot pool status is active.

        :param status: The status of the boot pool.
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
        COM.click_on_element(xpaths.boot.bootenv_actions_button(be_xpath))
        result = COM.assert_link_is_restricted(f'{be_xpath}-activate')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_attach_disk_is_restricted(cls, boot_disk):
        """
        This method returns True or False whether the Attach Disk button is locked and not clickable.

        :return: True if the Attach Disk button is locked and not clickable otherwise it returns False.

        Example:
            - Boot.assert_attach_disk_is_restricted()
        """
        xpath_disk = COM.convert_to_tag_format(boot_disk)
        COM.click_button(f'{xpath_disk}-actions')
        result = COM.assert_button_is_restricted('attach')
        WebUI.send_key('esc')
        return result

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
        COM.click_on_element(xpaths.boot.bootenv_actions_button(be_xpath))
        result = COM.assert_link_is_restricted(f'{be_xpath}-clone')
        WebUI.send_key('esc')
        return result

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
        COM.click_on_element(xpaths.boot.bootenv_actions_button(be_xpath))
        result = COM.assert_link_is_restricted(f'{be_xpath}-delete')
        WebUI.send_key('esc')
        return result

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
        COM.click_on_element(xpaths.boot.bootenv_actions_button(be_xpath))
        result = COM.assert_link_is_restricted(f'{be_xpath}-toggle-keep')
        WebUI.send_key('esc')
        return result

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
        COM.click_on_element(xpaths.boot.bootenv_actions_button(be_xpath))
        result = COM.assert_link_is_restricted(f'{be_xpath}-rename')
        WebUI.send_key('esc')
        return result

    @classmethod
    def assert_replace_disk_is_restricted(cls, boot_disk):
        """
        """
        xpath_disk = COM.convert_to_tag_format(boot_disk)
        COM.click_button(f'{xpath_disk}-actions')
        result = COM.assert_button_is_restricted('replace')
        WebUI.send_key('esc')
        return result

    @classmethod
    def asser_scrub_boot_environment_button_is_restricted(cls) -> bool:
        """
        This method returns True or False whether the Scrub Boot Environment button is locked and not clickable.

        :return: True if the Scrub Boot Environment button is locked and not clickable otherwise it returns False.

        Example:
            - Boot.asser_scrub_boot_environment_button_is_restricted()
        """
        return COM.assert_button_is_restricted('bootenv-scrub')

    @classmethod
    def asser_stats_settings_button_is_not_restricted(cls) -> bool:
        """
        This method returns True or False whether the Scrub Boot Environment button is not locked and clickable.

        :return: True if the Scrub Boot Environment button is not locked and clickable otherwise it returns False.

        Example:
            - Boot.asser_scrub_boot_environment_button_is_not_restricted()
        """
        return COM.assert_button_is_restricted('bootenv-stats')

    @classmethod
    def click_boot_pool_status_button(cls) -> None:
        """
        This method clicks on the Boot Pool Status button.

        Example:
            - Boot.click_boot_pool_status_button()
        """
        COM.click_button('bootenv-status')