import xpaths
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


class Replication:
    @classmethod
    def assert_ssh_connection_exists(cls, connection: str) -> bool:
        """
        This method verifies the given connection exists

        :param connection: is the name of the given connection

        Example:
            - Replication.assert_ssh_connection_exists('myConnection')
        """
        if SSHCON.is_ssh_connection_visible(connection) is False:
            COM.click_button('add-ssh-connection')
            COM.set_input_field('connection-name', connection)
            url = private_config['REP_DEST_IP']
            if connection.__contains__('self'):
                url = private_config['IP']
            SSHCON.set_url(url)
            SSHCON.set_admin_credentials(private_config['USERNAME'], private_config['PASSWORD'])
            ssh_username = 'root'
            if ssh_username.__contains__('admin'):
                ssh_username = 'admin'
            SSHCON.set_username(ssh_username)
            SSHCON.set_passwordless_sudo_checkbox()
            SSHCON.click_generate_new_private_key()
            COM.click_save_button()
        return SSHCON.is_ssh_connection_visible(connection)

    @classmethod
    def click_close_task_started_button(cls):
        """
        This method clicks the close button on the Task Started dialog

        Example:
            - Replication.click_close_task_started_button()
        """
        COM.click_button('dialog-close')

    @classmethod
    def click_run_now_replication_task_by_name(cls, name):
        """
        This method unsets the read only destination checkbox

        :param name: the name of the given replication task

        Example:
            - Replication.click_run_now_replication_task_by_name('myRepTask')
        """
        COM.click_button(f'replication-task-{COM.convert_to_tag_format(name)}-play-arrow-row-action')
        COM.assert_confirm_dialog()
        # WebUI.delay(2)
        WebUI.wait_until_visible(
            f'//*[@data-test="button-state-replication-task-{COM.convert_to_tag_format(name)}-row-state" and contains(@class,"fn-theme-green")]')

    @classmethod
    def delete_all_snapshots(cls):
        if COM.assert_page_header('Snapshots') is False:
            NAV.navigate_to_periodic_snapshots()
        COM.set_checkbox('column-select-all')
        if COM.is_visible(xpaths.common_xpaths.button_field('delete-selected')) is True:
            COM.click_button('delete-selected')
            COM.set_checkbox('confirm')
            COM.click_button('delete')
            # delay to allow delete to complete
            assert COM.is_visible(xpaths.common_xpaths.button_field('close')) is True
            COM.click_button('close')
            COM.assert_text_is_visible('No records have been added yet')

    @classmethod
    def delete_replication_task_by_name(cls, name: str) -> None:
        """
        This method deletes the given replication task if exists

        :param name: is the name of the given replication task

        Example:
            - Replication.delete_replication_task_by_name('myRepTask')
        """
        if cls.is_replication_task_visible(name):
            WebUI.xpath(xpaths.common_xpaths.any_child_parent_target(
                    f'//*[contains(text(),"{name}")]',
                    'tr',
                    f'button[contains(@data-test,"-delete")]')).click()
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
        return WebUI.xpath(xpaths.common_xpaths.button_field(f'state-replication-task-{COM.convert_to_tag_format(name)}-row-state')).text

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
    def is_task_started_dialog_visible(cls) -> bool:
        """
        This method returns True if the Task started dialog is visible.

        :return: True if the Task started dialog is visible.

        Example:
            - Replication.is_task_started_dialog_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Task started'))

    @classmethod
    def set_custom_snapshots(cls) -> None:
        """
        This method sets the custom snapshot checkbox

        Example:
            - Replication.set_custom_snapshots()
        """
        COM.set_checkbox('custom-snapshots')

    @classmethod
    def set_destination_location_on_different_box(cls, path: str) -> None:
        """
        This method sets the given destination path on a different box

        :param path: is the path of the given destination

        Example:
            - Replication.set_destination_location_on_different_box('tank/receive')
        """
        cls.set_location('target-dataset', 'different', '', path)

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
            - Replication.set_location('source-datasets', 'this', '', 'tank/replicate)
            - Replication.set_location('target-dataset', 'different', 'mySSHConnection', 'tank/receive)
        """
        prefix = '-on-' if system == 'this' else '-on-a-'
        system = obj + '-from' + prefix + system + '-system'
        COM.select_option(obj + '-from', system)
        src = 'source'
        if obj.startswith('target'):
            src = 'target'
        if connection != "":
            cls.set_ssh_connection(src, connection)
            if src == 'target':
                if COM.is_visible(xpaths.common_xpaths.button_field('dialog-confirm')) is True:
                    COM.click_button('dialog-confirm')
        COM.set_input_field(obj, path)

    @classmethod
    def set_run_once_button(cls):
        """
        This method sets the run once checkbox

        Example:
            - Replication.set_run_once_button()
        """
        COM.click_radio_button('schedule-method-run-once')

    @classmethod
    def set_source_location_on_different_box(cls, path: str) -> None:
        """
        This method sets the given source path on a different box

        :param path: is the path of the source

        Example:
            - Replication.set_source_location_on_different_box('tank/replicate')
        """
        cls.set_location('source-datasets', 'different', '', path)

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
    def set_ssh_connection(cls, source, connection) -> None:
        """
        This method sets the given ssh connection to the given source

        :param source: is the type of source ['source'/'target']
        :param connection: is the SSh connection to use (blank = no need for one, local)

        Example:
            - Replication.set_ssh_connection('source', 'mySSHConnection')
            - Replication.set_ssh_connection('target', 'mySSHConnection')
        """
        source = xpaths.common_xpaths.select_field('ssh-credentials-' + source)
        COM.select_option(source, connection)

    @classmethod
    def set_task_name(cls, name: str) -> None:
        """
        This method sets the replication task name to the given name

        :param name: is the path of the source

        Example:
            - Replication.set_task_name('myRepTask')
        """
        COM.set_input_field('name', name)

    @classmethod
    def unset_read_only_destination_checkbox(cls):
        """
        This method unsets the read only destination checkbox

        Example:
            - Replication.unset_read_only_destination_checkbox()
        """
        COM.set_checkbox('readonly')

    @classmethod
    def is_run_now_dialog_visible(cls) -> bool:
        """
        This method returns True if the Run Now dialog is visible.

        :return: True if the Run Now dialog is visible.

        Example:
            - Replication.is_run_now_dialog_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_text('Run Now'))
