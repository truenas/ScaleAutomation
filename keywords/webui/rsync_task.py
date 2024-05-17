import xpaths
from helper.global_config import shared_config, private_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM


class Rsync_Task:
    @classmethod
    def assert_add_rsync_task_button_is_restricted(cls) -> bool:
        """
        This method verifies if the add rsync task button is locked and not clickable.

        :return: True if the add rsync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Rsync_Task.assert_add_rsync_task_button_is_restricted()
        """
        return COM.assert_button_is_restricted('add-task')

    @classmethod
    def assert_delete_rsync_task_button_is_restricted(cls, path: str) -> bool:
        """
        This method verifies if the delete rsync task button is locked and not clickable.

        :param path: path of the rsync task
        :return: True if the delete rsync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_delete_rsync_task_button_is_restricted('/my/Rep/Path')
        """
        xpath_ip = COM.convert_to_tag_format(private_config['REP_DEST_IP'])
        xpath_path = COM.convert_to_tag_format(path)
        xpath = f'rsync-task{xpath_path}-{xpath_ip}-delete-row-action'
        return COM.assert_button_is_restricted(xpath)

    @classmethod
    def assert_edit_rsync_task_panel_header_is_visible(cls) -> bool:
        """
        This method verifies if the edit rsync task panel header is visible.

        :return: True if the edit rsync task panel header is visible, otherwise False.

        Example:
            - Rsync_Task.assert_edit_rsync_task_panel_header_is_visible()
        """
        return COM.assert_right_panel_header('Edit Rsync Task')

    @classmethod
    def assert_rsync_task_is_visible_on_page(cls, path: str) -> bool:
        """
        This method verifies if the given rsync path is visible.

        :param path: is the name of the given rsync path.
        :return: True if the given rsync task is visible, otherwise False.

        Example:
            - Rsync_Task.assert_rsync_task_is_visible('/my/Rep/Path')
        """
        xpath_ip = private_config['REP_DEST_IP'].replace('.', '-')
        xpath_path = COM.convert_to_tag_format(path)
        task_xpath = f'//*[@data-test="text-path-rsync-task{xpath_path}-{xpath_ip}-row-text"]'
        return WebUI.wait_until_visible(task_xpath, shared_config['MEDIUM_WAIT'])

    @classmethod
    def assert_rsync_task_page_header(cls) -> bool:
        """
        This method verifies if the rsync task page header is visible.

        Example:
            - Rsync_Task.assert_rsync_task_page_header()
        """
        return COM.assert_page_header('Rsync Task')

    @classmethod
    def assert_run_rsync_task_button_is_restricted(cls, path: str) -> bool:
        """
        This method verifies if the run now rsync task button is locked and not clickable.

        :param path: path of the rsync task
        :return: True if the run now rsync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_run_rsync_task_button_is_restricted('/my/Rep/Path')
        """
        xpath_ip = COM.convert_to_tag_format(private_config['REP_DEST_IP'])
        xpath_path = COM.convert_to_tag_format(path)
        xpath = f'rsync-task{xpath_path}-{xpath_ip}-play-arrow-row-action'
        return COM.assert_button_is_restricted(xpath)

    @classmethod
    def click_edit_rsync_task_by_path(cls, path: str) -> None:
        """
        This method clicks the edit button for the given rsync path.

        :param path: the path of the given rsync path.

        Example:
            - Rsync_Task.click_edit_rsync_task_by_path('/my/Rsync/Path')
        """
        xpath_ip = COM.convert_to_tag_format(private_config['REP_DEST_IP'])
        xpath_path = COM.convert_to_tag_format(path)
        COM.click_button(f'rsync-task{xpath_path}-{xpath_ip}-edit-row-action')

    @classmethod
    def click_run_now_rsync_task_by_path(cls, path) -> None:
        """
        This method clicks the run now button for the given rsync path.

        :param path: the path of the given rsync path.

        Example:
            - Rsync_Task.click_run_now_rsync_task_by_name('/my/Rsync/Path')
        """
        WebUI.refresh()
        COM.click_button(f'card-rsync-task{COM.convert_to_tag_format(path)}-null-play-arrow-row-action')
        COM.assert_confirm_dialog()
        if COM.assert_dialog_visible('FAILED', shared_config['SHORT_WAIT']):
            print("RSYNC failed correctly")
            COM.click_error_dialog_close_button()
        WebUI.refresh()

    @classmethod
    def delete_rsync_task_by_path(cls, path: str) -> None:
        """
        This method deletes the given rsync task if exists.

        :param path: is the path of the given rsync task.

        Example:
            - Rsync_Task.delete_rsync_task_by_path('/my/Rep/Path')
        """
        if cls.is_rsync_task_visible(path):
            COM.click_button(f'card-rsync-task{COM.convert_to_tag_format(path)}-null-delete-row-action')
            COM.assert_confirm_dialog()

    @classmethod
    def get_rsync_status(cls, path: str) -> str:
        """
        This method returns the status for the given rsync task.

        :param path: is the name of the given rsync task.
        :return: the status for the given rsync task.

        Example:
            - Rsync_Task.get_rsync_status('/my/Rep/Pat')
    """
        WebUI.refresh()
        return COM.get_element_property(xpaths.common_xpaths.button_field(f'state-card-rsync-task{COM.convert_to_tag_format(path)}-null-row-state'), 'innerText').strip(' ')

    @classmethod
    def is_rsync_task_visible(cls, path: str) -> bool:
        """
        This method returns True if the given rsync path is visible, otherwise False.

        :param path: is the name of the given rsync path.
        :return: True if the given rsync task is visible, otherwise False.

        Example:
            - Rsync_Task.is_rsync_task_visible('/my/Rep/Path')
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(
            f'//*[@data-test="button-card-rsync-task{COM.convert_to_tag_format(path)}-null-delete-row-action"]'))

    @classmethod
    def set_connect_using(cls, mode: str) -> None:
        """
        This method sets the rsync connection.

        :param mode: is the connection.

        Example:
            - Rsync_Task.set_connect_using('connection-from-the-keychain')
        """
        COM.select_option(
            'sshconnectmode',
            f'sshconnectmode-ssh-{COM.convert_to_tag_format(mode)}'
        )

    @classmethod
    def set_connect_using_home_directory(cls) -> None:
        """
        This method sets the rsync connection to use SSH Key from user home directory

       Example:
            - Rsync_Task.set_connect_using_home_directory()
        """
        cls.set_connect_using('private-key-stored-in-users-home-directory')

    @classmethod
    def set_connect_using_keychain(cls) -> None:
        """
        This method sets the rsync connection to use Keychain

       Example:
            - Rsync_Task.set_connect_using_keychain()
        """
        cls.set_connect_using('connection-from-the-keychain')

    @classmethod
    def set_description(cls, desc: str) -> None:
        """
        This method sets the rsync description

        :param desc: is the description

        Example:
            - Rsync_Task.set_description('Rsync Description')
        """
        COM.set_input_field('desc', desc, True)

    @classmethod
    def set_path(cls, path: str) -> None:
        """
        This method sets the rsync path name to the given name

        :param path: is the path of the source

        Example:
            - Rsync_Task.set_path('myRepTask')
        """
        COM.set_input_field('path', path, True)

    @classmethod
    def set_remote_path(cls, path: str) -> None:
        """
        This method sets the rsync remote path

        :param path: is the remote path

        Example:
            - Rsync_Task.set_remote_path('/mnt/tank/rsync')
        """
        COM.set_input_field('remotepath', path, True)

    @classmethod
    def set_rsync_mode(cls, mode: str) -> None:
        """
        This method sets the rsync mode

        :param mode: is the mode [Module/SSH]

        Example:
            - Rsync_Task.set_rsync_mode('Module')
        """
        COM.select_option('mode', f'mode-{COM.convert_to_tag_format(mode)}')

    @classmethod
    def set_rsync_mode_module(cls) -> None:
        """
        This method sets the rsync mode to Module

        Example:
            - Rsync_Task.set_rsync_mode_module('Module')
        """
        cls.set_rsync_mode('Module')

    @classmethod
    def set_rsync_mode_ssh(cls) -> None:
        """
        This method sets the rsync mode to SSH

        Example:
            - Rsync_Task.set_rsync_mode_ssh('SSH')
        """
        cls.set_rsync_mode('SSH')

    @classmethod
    def set_schedule(cls, schedule: str) -> None:
        """
        This method sets the rsync remote schedule

        :param schedule: is the schedule [hourly/daily/weekly/monthly/custom]

        Example:
            - Rsync_Task.set_schedule('weekly')
        """
        COM.select_option(
            'schedule-presets',
            f'schedule-presets-{COM.convert_to_tag_format(schedule)}'
        )

    @classmethod
    def set_schedule_custom(cls) -> None:
        """
        This method sets the rsync schedule to custom

        Example:
            - Rsync_Task.set_schedule_custom()
        """
        cls.set_schedule('custom')

    @classmethod
    def set_schedule_daily(cls) -> None:
        """
        This method sets the rsync schedule to daily

        Example:
            - Rsync_Task.set_schedule_daily()
        """
        cls.set_schedule('daily')

    @classmethod
    def set_schedule_hourly(cls) -> None:
        """
        This method sets the rsync schedule to hourly

        Example:
            - Rsync_Task.set_schedule_hourly()
        """
        cls.set_schedule('hourly')

    @classmethod
    def set_schedule_monthly(cls) -> None:
        """
        This method sets the rsync schedule to monthly

        Example:
            - Rsync_Task.set_schedule_monthly()
        """
        cls.set_schedule('monthly')

    @classmethod
    def set_schedule_weekly(cls) -> None:
        """
        This method sets the rsync schedule to weekly

        Example:
            - Rsync_Task.set_schedule_weekly()
        """
        cls.set_schedule('weekly')

    @classmethod
    def set_ssh_connection(cls, connection: str) -> None:
        """
        This method sets the rsync connection

        :param connection: is the connection

        Example:
            - Rsync_Task.set_ssh_connection('myConnection')
        """
        COM.select_option(
            'ssh-credentials',
            f'ssh-credentials-{COM.convert_to_tag_format(connection)}',
        )

    @classmethod
    def set_user(cls, name: str) -> None:
        """
        This method sets the rsync user to the given name

        :param name: is the name of the user

        Example:
            - Rsync_Task.set_user('username')
        """
        COM.set_input_field('user', name, True)
