import xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV

class Rsync:

    @classmethod
    def click_run_now_rsync_task_by_path(cls, path):
        """
        This method clicks the run now button for the given rsync path

        :param path: the path of the given rsync path

        Example:
            - Rsync.click_run_now_rsync_task_by_name('/my/Rsync/Path')
        """
        # WebUI.refresh()
        # Soft page refresh
        NAV.navigate_to_datasets()
        NAV.navigate_to_data_protection()
        COM.click_button(f'card-rsync-task{COM.convert_to_tag_format(path)}-null-play-arrow-row-action')
        COM.assert_confirm_dialog()
        if COM.assert_dialog_visible('FAILED', shared_config['SHORT_WAIT']):
            print("@@@ FAILED RSYNC: ")
            COM.click_error_dialog_close_button()
        # WebUI.refresh()
        # Soft page refresh
        NAV.navigate_to_datasets()
        NAV.navigate_to_data_protection()

    @classmethod
    def delete_rsync_task_by_path(cls, path: str) -> None:
        """
        This method deletes the given rsync task if exists

        :param path: is the path of the given rsync task

        Example:
            - Rsync.delete_rsync_task_by_path('/my/Rep/Path')
        """
        if cls.is_rsync_task_visible(path):
            COM.click_button(f'card-rsync-task{COM.convert_to_tag_format(path)}-null-delete-row-action')
            COM.assert_confirm_dialog()

    @classmethod
    def get_rsync_status(cls, path: str) -> str:
        """
        This method returns the status for the given rsync task.

        :param path: is the name of the given rsync task
        :return: the status for the given rsync task.

        Example:
            - Rsync.get_rsync_status('/my/Rep/Pat')
    """
        WebUI.refresh()
        return COM.get_element_property(xpaths.common_xpaths.button_field(f'state-card-rsync-task{COM.convert_to_tag_format(path)}-null-row-state'), 'innerText').strip(' ')

    @classmethod
    def is_rsync_task_visible(cls, path: str) -> bool:
        """
        This method returns True if the given rsync path is visible, otherwise False

        :param path: is the name of the given rsync path
        :return: True if the given rsync task is visible, otherwise False

        Example:
            - Rsync.is_rsync_task_visible('/my/Rep/Path')
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(
            f'//*[@data-test="button-card-rsync-task{COM.convert_to_tag_format(path)}-null-delete-row-action"]'))

    @classmethod
    def set_connect_using(cls, mode: str) -> None:
        """
        This method sets the rsync connection

        :param mode: is the connection

        Example:
            - Rsync.set_connect_using('connection-from-the-keychain')
        """
        COM.select_option('sshconnectmode', 'sshconnectmode-ssh-' + COM.convert_to_tag_format(mode))

    @classmethod
    def set_connect_using_home_directory(cls) -> None:
        """
        This method sets the rsync connection to use SSH Key from user home directory

       Example:
            - Rsync.set_connect_using_home_directory()
        """
        cls.set_connect_using('private-key-stored-in-users-home-directory')

    @classmethod
    def set_connect_using_keychain(cls) -> None:
        """
        This method sets the rsync connection to use Keychain

       Example:
            - Rsync.set_connect_using_keychain()
        """
        cls.set_connect_using('connection-from-the-keychain')

    @classmethod
    def set_description(cls, desc: str) -> None:
        """
        This method sets the rsync description

        :param desc: is the description

        Example:
            - Rsync.set_description('Rsync Description')
        """
        COM.set_input_field('desc', desc, True)

    @classmethod
    def set_path(cls, path: str) -> None:
        """
        This method sets the rsync path name to the given name

        :param path: is the path of the source

        Example:
            - Rsync.set_path('myRepTask')
        """
        COM.set_input_field('path', path, True)

    @classmethod
    def set_remote_path(cls, path: str) -> None:
        """
        This method sets the rsync remote path

        :param path: is the remote path

        Example:
            - Rsync.set_remote_path('/mnt/tank/rsync')
        """
        COM.set_input_field('remotepath', path, True)

    @classmethod
    def set_rsync_mode(cls, mode: str) -> None:
        """
        This method sets the rsync mode

        :param mode: is the mode [Module/SSH]

        Example:
            - Rsync.set_rsync_mode('Module')
        """
        COM.select_option('mode', 'mode-' + COM.convert_to_tag_format(mode))

    @classmethod
    def set_rsync_mode_module(cls) -> None:
        """
        This method sets the rsync mode to Module

        Example:
            - Rsync.set_rsync_mode_module('Module')
        """
        cls.set_rsync_mode('Module')

    @classmethod
    def set_rsync_mode_ssh(cls) -> None:
        """
        This method sets the rsync mode to SSH

        Example:
            - Rsync.set_rsync_mode_ssh('SSH')
        """
        cls.set_rsync_mode('SSH')

    @classmethod
    def set_schedule(cls, schedule: str) -> None:
        """
        This method sets the rsync remote schedule

        :param schedule: is the schedule [hourly/daily/weekly/monthly/custom]

        Example:
            - Rsync.set_schedule('weekly')
        """
        COM.select_option('schedule-presets', 'schedule-presets-' + COM.convert_to_tag_format(schedule))

    @classmethod
    def set_schedule_custom(cls) -> None:
        """
        This method sets the rsync schedule to custom

        Example:
            - Rsync.set_schedule_custom()
        """
        cls.set_schedule('custom')

    @classmethod
    def set_schedule_daily(cls) -> None:
        """
        This method sets the rsync schedule to daily

        Example:
            - Rsync.set_schedule_daily()
        """
        cls.set_schedule('daily')

    @classmethod
    def set_schedule_hourly(cls) -> None:
        """
        This method sets the rsync schedule to hourly

        Example:
            - Rsync.set_schedule_hourly()
        """
        cls.set_schedule('hourly')

    @classmethod
    def set_schedule_monthly(cls) -> None:
        """
        This method sets the rsync schedule to monthly

        Example:
            - Rsync.set_schedule_monthly()
        """
        cls.set_schedule('monthly')

    @classmethod
    def set_schedule_weekly(cls) -> None:
        """
        This method sets the rsync schedule to weekly

        Example:
            - Rsync.set_schedule_weekly()
        """
        cls.set_schedule('weekly')

    @classmethod
    def set_ssh_connection(cls, connection: str) -> None:
        """
        This method sets the rsync connection

        :param connection: is the connection

        Example:
            - Rsync.set_ssh_connection('myConnection')
        """
        COM.select_option('ssh-credentials', 'ssh-credentials-' + COM.convert_to_tag_format(connection))

    @classmethod
    def set_user(cls, name: str) -> None:
        """
        This method sets the rsync user to the given name

        :param name: is the name of the user

        Example:
            - Rsync.set_user('username')
        """
        COM.set_input_field('user', name, True)
