import xpaths
from helper.global_config import private_config, shared_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


class Replication:
    @classmethod
    def click_close_task_started_button(cls):
        """
        This method clicks the close button on the Task Started dialog

        Example:
            - Replication.click_close_task_started_button()
        """
        COM.click_dialog_close_button()

    @classmethod
    def click_run_now_replication_task_by_name(cls, name):
        """
        This method clicks the run now button for the given replication task

        :param name: the name of the given replication task

        Example:
            - Replication.click_run_now_replication_task_by_name('myRepTask')
        """
        WebUI.refresh()
        name = COM.convert_to_tag_format(name)
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field(f'replication-task-{name}-play-arrow-row-action')) is True
        COM.click_button(f'replication-task-{name}-play-arrow-row-action')
        COM.assert_confirm_dialog()
        assert WebUI.wait_until_visible(
            f'//*[@data-test="button-state-replication-task-{name}-row-state" and contains(@class,"fn-theme-green")]', shared_config['LONG_WAIT']) is True

    @classmethod
    def click_save_button_and_resolve_dialogs(cls):
        """
        This method clicks the save button and resolves subsequent dialogs

        Example:
            - Replication.click_save_button_and_resolve_dialogs()
        """
        COM.click_save_button()

        if cls.is_destination_snapshots_dialog_visible() is True:
            COM.assert_confirm_dialog()
        if cls.is_sudo_enabled_dialog_visible() is True:
            COM.assert_confirm_dialog()
        if cls.is_task_started_dialog_visible() is True:
            cls.click_close_task_started_button()
        if cls.is_run_now_dialog_visible() is True:
            COM.cancel_confirm_dialog()
        assert COM.assert_progress_bar_not_visible(shared_config['EXTRA_LONG_WAIT']) is True
        return WebUI.wait_until_not_visible(xpaths.common_xpaths.close_right_panel())

    @classmethod
    def close_destination_box(cls) -> None:
        """
        This method closes the destination box browser window and switches to the source box browser window

        Example:
            - Replication.close_destination_box()
        """
        if WebUI.web_driver.current_url.__contains__(private_config['REP_DEST_IP']):
            COM.logoff_truenas()
            WebUI.close_window()
        cls.switch_to_source_box()

    @classmethod
    def delete_replication_task_by_name(cls, name: str) -> None:
        """
        This method deletes the given replication task if exists

        :param name: is the name of the given replication task

        Example:
            - Replication.delete_replication_task_by_name('myRepTask')
        """
        if cls.is_replication_task_visible(name):
            xpath = xpaths.common_xpaths.any_child_parent_target(
                    f'//*[contains(text(),"{name}")]',
                    'tr',
                    f'button[contains(@data-test,"-delete")]')
            COM.click_on_element(xpath)
            COM.assert_confirm_dialog()

    @classmethod
    def get_replication_status(cls, name: str) -> str:
        """
        This method returns the status for the given replication task.

        :param name: is the name of the given replication task
        :return: the status for the given replication task.

        Example:
            - Replication.get_replication_status('myRepTask')
    """
        NAV.navigate_to_data_protection()
        return COM.get_element_property(xpaths.common_xpaths.button_field(f'state-replication-task-{COM.convert_to_tag_format(name)}-row-state'), 'innerText').strip(' ')

    @classmethod
    def is_destination_snapshots_dialog_visible(cls) -> bool:
        """
        This method returns True if the Destination Snapshots dialog is visible.

        :return: True if the Destination Snapshots dialog is visible.

        Example:
            - Replication.is_destination_snapshots_dialog_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Destination Snapshots Are Not Related to Replicated Snapshots'), shared_config['SHORT_WAIT'])

    @classmethod
    def is_replication_task_visible(cls, name: str) -> bool:
        """
        This method returns True if the given replication task is visible, otherwise False

        :param name: is the name of the given replication task
        :return: True if the given replication task is visible, otherwise False

        Example:
            - Replication.is_replication_task_visible('myRepTask')
        """
        return COM.is_visible(xpaths.common_xpaths.any_child_parent_target(
                    f'//*[contains(text(),"{name}")]',
                    'tr',
                    f'button[contains(@data-test,"-delete")]'))

    @classmethod
    def is_run_now_dialog_visible(cls) -> bool:
        """
        This method returns True if the Run Now dialog is visible.

        :return: True if the Run Now dialog is visible.

        Example:
            - Replication.is_run_now_dialog_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Run Now'), shared_config['SHORT_WAIT'])

    @classmethod
    def is_sudo_enabled_dialog_visible(cls) -> bool:
        """
        This method returns True if the Sudo Enabled dialog is visible, otherwise False.

        :return: True if the Sudo Enabled dialog is visible, otherwise False.

        Example:
            - Replication.is_sudo_enabled_dialog_visible()
        """
        return COM.is_visible(xpaths.common_xpaths.any_text('Sudo Enabled'))

    @classmethod
    def is_task_started_dialog_visible(cls) -> bool:
        """
        This method returns True if the Task started dialog is visible.

        :return: True if the Task started dialog is visible.

        Example:
            - Replication.is_task_started_dialog_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Task started'), shared_config['SHORT_WAIT'])

    @classmethod
    def login_to_destination_box(cls, username, password):
        """
        This method opens a new browser window to the destination box and logs in with the given credentials.

        :param username: is the username to log in with
        :param password: is the password of the username

        Example:
            - Replication.login_to_destination_box('user', 'password')
        """
        WebUI.execute_script('window.open();', [])
        WebUI.switch_to_window_index(1)
        WebUI.get(f'http://{private_config["REP_DEST_IP"]}/ui/sessions/signin')
        COM.set_login_form(username, password)
        if COM.assert_page_header('Dashboard') is False:
            NAV.navigate_to_dashboard()
        assert COM.assert_page_header('Dashboard')

    @classmethod
    def select_custom_preset(cls, option: str) -> None:
        """
        This method selects the custom preset option

        :param option: is the option to select [daily/hourly/monthly/weekly]

        Example:
            - Replication.select_custom_preset('monthly')
        """
        COM.select_option('presets', f'presets-{COM.convert_to_tag_format(option)}')

    @classmethod
    def select_destination_read_only(cls, option: str) -> None:
        """
        This method selects the destination read only option

        :param option: is the option to select [ignore/require/set]

        Example:
            - Replication.select_destination_read_only('require')
        """
        COM.select_option('readonly', f'readonly-{COM.convert_to_tag_format(option)}')

    @classmethod
    def select_schedule_preset(cls, option: str) -> None:
        """
        This method selects the schedule preset option

        :param option: is the option to select [custom/daily/hourly/monthly/weekly]

        Example:
            - Replication.select_schedule_preset('monthly')
        """
        COM.select_option('schedule-picker-presets', f'schedule-picker-presets-{COM.convert_to_tag_format(option)}')
        if option == 'custom':
            WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Presets', 4))

    @classmethod
    def set_custom_snapshots(cls) -> None:
        """
        This method sets the custom snapshot checkbox

        Example:
            - Replication.set_custom_snapshots()
        """
        COM.set_checkbox('custom-snapshots')

    @classmethod
    def set_destination_location(cls, path: str) -> None:
        """
        This method sets the given destination path

        :param path: is the path of the destination

        Example:
            - Replication.set_destination_location('tank/replicate')
        """
        COM.set_input_field('target-dataset', path)

    @classmethod
    def set_destination_location_on_different_box(cls, path: str, connection: str) -> None:
        """
        This method sets the given destination path on a different box

        :param path: is the path of the given destination
        :param connection: is the SSh connection to use (blank = no need for one, local)

        Example:
            - Replication.set_destination_location_on_different_box('tank/receive', 'myConnection')
        """
        cls.set_location('target-dataset', 'different', connection, path)

    @classmethod
    def set_destination_location_on_same_box(cls, path: str) -> None:
        """
        This method sets the given destination path on the same box

        :param path: is the path of the given destination

        Example:
            - Replication.set_destination_location_on_same_box('tank/receive')
        """
        cls.set_location('target-dataset', 'this', '', path)

    @classmethod
    def set_location(cls, obj: str, system: str, connection: str, path) -> None:
        """
        This method sets the given source path on the same box

        :param obj: is the name of the obj to assign the path ['source-datasets'/'target-dataset']
        :param system: is the source or destination ['this'/'different']
        :param connection: is the SSh connection to use (blank = no need for one, local)
        :param path: is the path of the given source or destination

        Example:
            - Replication.set_location("source-datasets", "this", "", "tank/replicate")
            - Replication.set_location('target-dataset', 'different', 'mySSHConnection', 'tank/receive')
        """
        prefix = '-on-' if system == 'this' else '-on-a-'
        system = obj + '-from' + prefix + system + '-system'
        if COM.get_element_property(xpaths.common_xpaths.select_field(obj + '-from'), "ariaDisabled") == 'false':
            COM.select_option(obj + '-from', system)
        src = 'source'
        if obj.startswith('target'):
            src = 'target'
        if connection != "":
            cls.set_ssh_connection(src, connection)
            if COM.is_visible(xpaths.common_xpaths.button_field('dialog-confirm')) is True:
                COM.click_button('dialog-confirm')
        COM.set_input_field(obj, path)

    @classmethod
    def set_preset_custom_day_of_week(cls, day: str, state: bool = False) -> None:
        """
        This method sets the given day of the week to the given state (True = on, False = off)

        :param day: is the day of the week [sun/mon/tue/wed/thu/fri/sat]
        :param state: whether to set te day of the week or not [True/False]

        Example:
            - Replication.set_preset_custom_day_of_week('sun')
            - Replication.set_preset_custom_day_of_week('mon', True)
        """
        COM.set_checkbox_by_state(COM.convert_to_tag_format(day), state)

    @classmethod
    def set_preset_custom_month_of_year(cls, month: str, state: bool = False) -> None:
        """
        This method sets the given month of the month to the given state (True = on, False = off)

        :param month: is the month of the month [jan/feb/mar/apr/may/jun/jul/aug/sep/oct/nov/dec]
        :param state: whether to set te month of the month or not [True/False]

        Example:
            - Replication.set_preset_custom_month_of_year('jan')
            - Replication.set_preset_custom_month_of_year('feb', True)
        """
        COM.set_checkbox_by_state(COM.convert_to_tag_format(month), state)

    @classmethod
    def set_preset_custom_time(cls, minutes: str = '*', hours: str = '*', days: str = '*') -> None:
        """
        This method selects the custom preset option

        :param minutes: is the minute of the hour when to trigger the replication task [*/0-59]
        :param hours: is the hour of the day when to trigger the replication task [*/0-23]
        :param days: is the numerical day of the month when to trigger the replication task [*/1-31]

        Example:
            - Replication.set_preset_custom_time('30')
            - Replication.set_preset_custom_time('0', '18')
            - Replication.set_preset_custom_time('*', '*', '5')
        """
        minutes = str(int(minutes) % 60) if minutes != '*' else minutes
        hours = str(int(hours) % 24) if hours != '*' else hours
        days = str(int(days) % 31) if days != '*' else days
        COM.set_input_field('minutes', minutes)
        COM.set_input_field('hours', hours)
        COM.set_input_field('days', days)

    @classmethod
    def set_run_once_button(cls):
        """
        This method sets the run once checkbox

        Example:
            - Replication.set_run_once_button()
        """
        if not COM.get_element_property(xpaths.common_xpaths.radio_button_field_attribute('schedule-method-run-once'), 'checked'):
            COM.click_radio_button('schedule-method-run-once')
            WebUI.delay(0.2)
        assert COM.get_element_property(xpaths.common_xpaths.radio_button_field_attribute('schedule-method-run-once'), 'checked')

    @classmethod
    def set_source_location(cls, path: str) -> None:
        """
        This method sets the given source path

        :param path: is the path of the source

        Example:
            - Replication.set_source_location('tank/replicate')
        """
        COM.set_input_field('source-datasets', path)

    @classmethod
    def set_source_location_on_different_box(cls, path: str, connection: str) -> None:
        """
        This method sets the given source path on a different box

        :param path: is the path of the source
        :param connection: is the SSh connection to use (blank = no need for one, local)

        Example:
            - Replication.set_source_location_on_different_box('tank/replicate')
        """
        cls.set_location('source-datasets', 'different', connection, path)

    @classmethod
    def set_source_location_on_same_box(cls, path: str) -> None:
        """
        This method sets the given source path on the same box

        :param path: is the path of the source

        Example:
            - Replication.set_source_location_on_same_box('tank/replicate')
        """
        cls.set_location('source-datasets', 'this', '', path)

    @classmethod
    def set_ssh_connection(cls, source: str, connection: str) -> None:
        """
        This method sets the given ssh connection to the given source

        :param source: is the type of source ['source'/'target']
        :param connection: is the SSh connection to use (blank = no need for one, local)

        Example:
            - Replication.set_ssh_connection('source', 'mySSHConnection')
            - Replication.set_ssh_connection('target', 'mySSHConnection')
        """
        source = 'ssh-credentials-' + source
        COM.select_option(source, source + '-' + connection)

    @classmethod
    def set_ssh_connection_advanced(cls, connection: str) -> None:
        """
        This method sets the given ssh connection to the given source

        :param connection: is the SSh connection to use (blank = no need for one, local)

        Example:
            - Replication.set_ssh_connection_advanced('mySSHConnection')
        """
        COM.select_option('ssh-credentials', 'ssh-credentials-' + COM.convert_to_tag_format(connection))

    @classmethod
    def set_task_name(cls, name: str) -> None:
        """
        This method sets the replication task name to the given name

        :param name: is the path of the source

        Example:
            - Replication.set_task_name('myRepTask')
        """
        COM.set_input_field('name', name, True)

    @classmethod
    def switch_to_destination_box(cls) -> None:
        """
        This method switches to the destination box browser window

        Example:
            - Replication.switch_to_destination_box()
        """
        WebUI.switch_to_window_index(1)

    @classmethod
    def switch_to_source_box(cls) -> None:
        """
        This method switches to the source box browser window

        Example:
            - Replication.switch_to_source_box()
        """
        WebUI.switch_to_window_index(0)

    @classmethod
    def unset_read_only_destination_checkbox(cls):
        """
        This method unsets the read only destination checkbox

        Example:
            - Replication.unset_read_only_destination_checkbox()
        """
        COM.unset_checkbox('readonly')

    @classmethod
    def wait_for_task_to_stop_running(cls, name: str) -> None:
        """
        This method waits until the given task is no longer running

        :param name: is the name of the task

        Example:
            - Replication.wait_for_task_to_stop_running('myRepTask')
        """
        while COM.get_element_property(xpaths.common_xpaths.button_field(f'state-replication-task-{name}-row-state'), 'innerText') == 'RUNNING':
            WebUI.delay(1)
