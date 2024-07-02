import xpaths
from helper.global_config import private_config, shared_config
from helper.webui import WebUI
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.datasets import Datasets as DATASET
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
    def click_run_now_button(cls, name):
        """
        This method clicks the run now button for the given replication task

        :param name: the name of the given replication task

        Example:
            - Replication.click_run_now_replication_task_by_name('myRepTask')
        """
        name = COM.convert_to_tag_format(name)
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field(f'replication-task-{name}-play-arrow-row-action')) is True
        COM.click_button(f'replication-task-{name}-play-arrow-row-action')
        COM.assert_confirm_dialog()

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
    def create_advanced_replication_task_local(cls, options: dict) -> None:
        """
        This methode creates a Replication Task with Advanced Options.

        :param options: the dict of the options to set on the replication task

        Example:
            - Replication.create_replication_task({'NAME'= 'rep_task', 'SOURCE'= 'tank/source', 'DESTINATION'= 'tank/destination', 'ENABLED'= True, 'NAMING'= 'rep-%Y-%m-%d_%H-%M'})
        """
        # Create Replication Task
        NAV.navigate_to_data_protection()
        DP.click_add_replication_button()
        assert COM.assert_right_panel_header('Replication Task Wizard') is True
        COM.click_button('advanced')
        assert COM.assert_right_panel_header('Add Replication Task') is True

        # Set Options
        for opt in options:
            match opt:
                case "NAME":
                    COM.set_input_field('name', options[opt], True)
                case "TRANSPORT":
                    COM.select_option('transport', options[opt])
                case "SSH_CONNECTION":
                    COM.click_on_element(xpaths.common_xpaths.select_field('ssh-credentials'))
                    COM.click_on_element(xpaths.common_xpaths.option_field(f'ssh-credentials-{options[opt]}'))
                    COM.assert_confirm_dialog()
                case "DESTINATION":
                    COM.set_input_field('target-dataset', options[opt])
                case "READ_ONLY_POLICY":
                    COM.click_on_element(xpaths.common_xpaths.select_field('readonly'))
                    COM.select_option('readonly', options[opt])
                case "SOURCE":
                    COM.set_input_field('source-datasets', options[opt])
                case "INCLUDE_PROPERTIES":
                    if COM.get_element_property(xpaths.common_xpaths.checkbox_field_attribute('properties'), 'checked') is not options[opt]:
                        # regular set checkbox not work.
                        COM.send_space(xpaths.common_xpaths.checkbox_field_attribute('properties'))
                case "MATCHING_SCHEMA":
                    COM.click_radio_button('schema-or-regex-matching-naming-schema')
                case  "NAMING_SCHEMA":
                    COM.set_input_field('also-include-naming-schema', options[opt])
                case "RUN_AUTOMATICALLY":
                    if COM.get_element_property(xpaths.common_xpaths.checkbox_field_attribute('auto'), 'checked') is not options[opt]:
                        # regular set checkbox not work.
                        COM.send_space(xpaths.common_xpaths.checkbox_field_attribute('auto'))
                case "SCHEDULE":
                    COM.set_checkbox_by_state('schedule', options[opt])
                case "FREQUENCY":
                    COM.select_option('schedule-picker-presets', options[opt])

        cls.click_save_button_and_resolve_dialogs()

    @classmethod
    def create_periodic_snapshot(cls, source_path: str, destination_path: str, naming_schema: str, source_box: str = 'LOCAL', destination_box: str = 'REMOTE') -> str:
        """
        This methode return the name of the created Periodic Snapshot.

        :param source_path: the path of the source
        :param destination_path: the path of the destination
        :param naming_schema: the naming schema to use for snapshot
        :param source_box: the location of the source [LOCAL/REMOTE]
        :param destination_box: the location of the destination [LOCAL/REMOTE]

        Example:
            - Replication.create_periodic_snapshot('tank/source', 'tank/destination', 'snapshot-%Y-%m-%d_%H-%M')
            - Replication.create_periodic_snapshot('tank/source', 'tank/destination', 'snapshot-%Y-%m-%d_%H-%M', 'REMOTE', 'LOCAL')
        """
        # Create Periodic Snapshot
        if source_box.upper() == 'REMOTE':
            private_config['API_IP'] = private_config['REP_DEST_IP']
        response = API_POST.create_snapshot(source_path, naming_schema).json()
        if source_box.upper() == 'REMOTE':
            private_config['API_IP'] = private_config['IP']
            cls.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert DP.is_snapshot_visible(source_path, response['snapshot_name']) is True
        if source_box.upper() == 'REMOTE':
            cls.close_destination_box()

        if destination_box.upper() == 'REMOTE':
            cls.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert DP.is_snapshot_visible(destination_path, response['snapshot_name']) is False
        if destination_box.upper() == 'REMOTE':
            cls.close_destination_box()
        return response['snapshot_name']

    @classmethod
    def create_replication_task(cls, source_path: str, destination_path: str, connection: str, naming_schema: str,
                                task_name: str, source_box: str = 'LOCAL', destination_box: str = 'REMOTE') -> None:
        """
        This methode return the True if the Replication Task was successful,
            the snapshot exists and the file exists, otherwise False.

        :param source_path: the path of the source
        :param destination_path: the path of the destination
        :param connection: the name of the connection
        :param naming_schema: the name of the naming_schema
        :param task_name: the name of the task
        :param source_box: the location of the source [LOCAL/REMOTE]
        :param destination_box: the location of the destination [LOCAL/REMOTE]

        Example:
            - Replication.create_replication_task('tank/source', 'tank/destination', 'connection', 'rep-%Y-%m-%d_%H-%M', 'rep_task')
            - Replication.create_replication_task('tank/source', 'tank/destination', 'connection', 'rep-%Y-%m-%d_%H-%M', 'rep_task', 'REMOTE', 'LOCAL')
        """
        # Create Replication Task
        NAV.navigate_to_data_protection()
        DP.click_add_replication_button()
        if source_box.upper() == 'REMOTE':
            cls.set_source_location_on_different_box(source_path, connection)
        else:
            cls.set_source_location_on_same_box(source_path)

        if destination_box.upper() == 'LOCAL':
            cls.set_destination_location_on_same_box(destination_path)
        else:
            cls.set_destination_location_on_different_box(destination_path, connection)

        if source_box.upper() == 'LOCAL':
            cls.set_custom_snapshots()
        COM.set_input_field('naming-schema', naming_schema)
        cls.set_task_name(task_name)
        # Clicking the "Next" button doesn't seeme to work on the pipeline
        # However, clicking on the "Step 2: When" appears to work
        # If this gets fixed, replace with the 'click_next_button()'
        COM.click_on_element('//*[@class="mat-step-label"]')
        WebUI.delay(0.2)
        # COM.click_next_button()

        cls.set_run_once_button()
        cls.unset_read_only_destination_checkbox()
        cls.click_save_button_and_resolve_dialogs()

    @classmethod
    def delete_dataset_by_box(cls, pool: str, dataset: str, box: str = 'LOCAL') -> None:
        """
        This method deletes the given dataset on the given box.
        :param pool: The name of the pool.
        :param dataset: The name of the dataset.
        :param box: The location of the dataset. [LOCAL/REMOTE]

        Example:
            - Dataset.delete_dataset('test-pool', 'test-dataset')
            - Dataset.delete_dataset('test-pool', 'test-dataset', 'REMOTE')
        """
        if box.upper() == 'REMOTE':
            cls.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])

        NAV.navigate_to_datasets()
        DATASET.expand_all_datasets()
        DATASET.delete_dataset(pool, dataset)

        if box.upper() == 'REMOTE':
            cls.close_destination_box()

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
                    'button[contains(@data-test,"-delete")]')
            COM.click_on_element(xpath)
            COM.assert_confirm_dialog()

    @classmethod
    def get_replication_log(cls, name: str) -> None:
        """
        This method displays the log for the given replication task.

        :param name: is the name of the given replication task

        Example:
            - Replication.get_replication_log('myRepTask')
        """
        COM.click_on_element(xpaths.common_xpaths.button_field(f'state-replication-task-{COM.convert_to_tag_format(name)}-row-state'))

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
    def is_destination_snapshot_and_file_exist(cls, task_name: str, destination_path: str, snapshot_name: str, file_name: str, destination_box: str = 'REMOTE') -> bool:
        """
        This methode return the True if the Replication Task was successful the snapshot exists and the file exists, otherwise False.

        :param task_name: the name of the replication task
        :param destination_path: the path of the destination
        :param snapshot_name: the name of the snapshot
        :param file_name: the name of the file
        :param destination_box: the location of the destination [LOCAL/REMOTE]

        Example:
            - Replication.is_destination_snapshot_and_file_exist('rep_task', 'FINISHED', 'snapshot-2024-01-01_10-01', 'filename.txt')
            - Replication.is_destination_snapshot_and_file_exist('rep_task', 'FINISHED', 'snapshot-2024-01-01_10-01', 'filename.txt', 'LOCAL')
        """
        # Verify Replication Task successful
        NAV.navigate_to_data_protection()
        assert cls.is_replication_task_visible(task_name) is True
        assert cls.get_replication_status(task_name) == 'FINISHED'
        if destination_box.upper() == 'REMOTE':
            cls.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
            NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert DP.is_snapshot_visible(destination_path, snapshot_name) is True
        ip = private_config['API_IP']

        if destination_box.upper() == 'REMOTE':
            cls.close_destination_box()
            ip = private_config['REP_DEST_IP']
        return COM.assert_file_exists(file_name, destination_path, ip) is True

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
                    'button[contains(@data-test,"-delete")]'))

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
