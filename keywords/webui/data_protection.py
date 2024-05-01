import xpaths
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


class Data_Protection:

    @classmethod
    def assert_add_scrub_task_button_is_locked_and_not_clickable(cls):
        """
        This method verifies if the delete dataset permissions button is locked and not clickable.

        :return: True if the delete dataset permissions button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_add_scrub_task_button_is_locked_and_not_clickable()
        """
        return COM.assert_button_is_locked_and_not_clickable('scrub-task-add')

    @classmethod
    def assert_delete_scrub_task_button_is_locked_and_not_clickable(cls, description: str):
        """
        This method verifies if the delete dataset permissions button is locked and not clickable.

        :param description: description of the scrub task
        :return: True if the delete dataset permissions button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_delete_scrub_task_button_is_locked_and_not_clickable('description')
        """
        description = COM.convert_to_tag_format(description)
        return COM.assert_element_is_locked_and_not_clickable(xpaths.data_protection.scrub_task_delete_button(description))

    @classmethod
    def assert_enable_scrub_task_toggle_is_locked_and_not_clickable(cls, description: str):
        """
        This method verifies if the delete dataset permissions button is locked and not clickable.

        :param description: description of the scrub task
        :return: True if the delete dataset permissions button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_enable_scrub_task_toggle_is_locked_and_not_clickable('description')
        """
        description = COM.convert_to_tag_format(description)
        print("@@@ TOGGLE: "+xpaths.data_protection.scrub_task_enable_toggle(description))
        return COM.assert_element_is_locked_and_not_clickable(xpaths.data_protection.scrub_task_enable_toggle(description))

    @classmethod
    def assert_preset_dialog_visible(cls) -> bool:
        """
        This method returns True if the dialog is visible, otherwise it returns False.

        :return: True if the Presets dialog is visible, otherwise it returns False.

        Example:
            - Data_Protection.assert_preset_dialog_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header("Presets", 4))

    @classmethod
    def assert_scrub_task_description(cls, description) -> bool:
        """
        This method returns True if the given scrub task description is visible, otherwise returns False.

        :param description: description of the scrub task
        :return: True if the given scrub task description is visible, otherwise returns False.

        Example:
            - Data_Protection.assert_scrub_task_description("Scrub Task Description")
        """
        description = COM.convert_to_tag_format(description)
        return COM.is_visible(xpaths.data_protection.scrub_task_description(description))

    @classmethod
    def click_add_replication_button(cls) -> None:
        """
        This method clicks the Add Replication task button

        Example:
            - Data_Protection.click_add_replication_button()
        """
        COM.click_button('replication-task-add')

    @classmethod
    def click_add_rsync_button(cls) -> None:
        """
        This method clicks the Add Rsync task button

        Example:
            - Data_Protection.click_add_rsync_button()
        """
        COM.click_button('rsync-task-add')

    @classmethod
    def click_edit_replication_task_by_name(cls, name):
        """
        This method clicks the edit button for the given replication task

        :param name: the name of the given replication task

        Example:
            - Data_Protection.click_edit_replication_task_by_name('myRepTask')
        """
        COM.click_button(f'replication-task-{COM.convert_to_tag_format(name)}-edit-row-action')
        COM.assert_right_panel_header('Edit Replication Task')

    @classmethod
    def click_edit_scrub_task(cls, description):
        """
        This method clicks the edit button for the given replication task

        :param description: the description of the given scrub task

        Example:
            - Data_Protection.click_edit_scrub_task('description')
        """
        description = COM.convert_to_tag_format(description)
        COM.click_on_element(xpaths.data_protection.scrub_task_edit_button(description))
        assert COM.assert_right_panel_header('Edit Scrub Task') is True

    @classmethod
    def click_edit_snapshot_task_by_name(cls, name):
        """
        This method clicks the edit button for the given replication task

        :param name: the name of the given replication task

        Example:
            - Data_Protection.click_edit_replication_task_by_name('myRepTask')
        """
        status = cls.get_task_status(name, 'snapshot')
        COM.click_button(f'snapshot-task-{COM.convert_to_tag_format(name)}-{COM.convert_to_tag_format(status)}-edit-row-action')
        COM.assert_right_panel_header('Edit Periodic Snapshot Task')

    @classmethod
    def click_snapshots_button(cls):
        """
        This method clicks the Snapshots button

        Example:
            - Data_Protection.click_snapshots_button()
        """
        COM.click_link('snapshot-task-snapshots')

    @classmethod
    def delete_all_periodic_snapshot_tasks(cls) -> None:
        """
        This method deletes all the Periodic Snapshot tasks

        Example:
            - Data_Protection.delete_all_periodic_snapshot_tasks()
        """
        while COM.is_visible('//*[starts-with(@data-test,"button-snapshot") and contains(@data-test,"-delete-row-action")]'):
            COM.click_on_element('//*[starts-with(@data-test,"button-snapshot") and contains(@data-test,"-delete-row-action")]')
            COM.assert_confirm_dialog()
        assert COM.is_visible('//*[starts-with(@data-test,"button-snapshot") and contains(@data-test,"-delete-row-action")]') is False

    @classmethod
    def delete_all_replication_tasks(cls) -> None:
        """
        This method deletes all the Replication tasks

        Example:
            - Data_Protection.delete_all_replication_tasks()
        """
        while COM.is_visible('//*[starts-with(@data-test,"button-replication") and contains(@data-test,"-delete-row-action")]'):
            COM.click_on_element('//*[starts-with(@data-test,"button-replication") and contains(@data-test,"-delete-row-action")]')
            COM.assert_confirm_dialog()
        assert COM.is_visible('//*[starts-with(@data-test,"button-replication") and contains(@data-test,"-delete-row-action")]') is False

    @classmethod
    def delete_all_snapshots(cls):
        """
        This method deletes all the Snapshots

        Example:
            - Data_Protection.delete_all_snapshots()
        """
        if COM.assert_page_header('Snapshots') is False:
            NAV.navigate_to_periodic_snapshots()
        if COM.assert_text_is_visible('No records have been added yet') is False:
            COM.set_checkbox('column-select-all')
            if COM.is_clickable(xpaths.common_xpaths.button_field('delete-selected')) is True:
                COM.click_button('delete-selected')
                COM.set_checkbox('confirm')
                COM.click_button('delete')
                # delay to allow 'delete' to complete
                assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('close')) is True
                COM.click_button('close')
                COM.assert_text_is_visible('No records have been added yet')
            assert COM.assert_text_is_visible('No records have been added yet')

    @classmethod
    def get_task_status(cls, name: str, task_type: str) -> str:
        """
        This method returns the status for the given task.

        :param name: is the name of the given replication task
        :param task_type: is the type of the given task [replication/snapshot]
        :return: the status for the given task.

        Example:
            - Data_Protection.get_task_status('myRepTask', 'replication')
            - Data_Protection.get_task_status('mySnapshotTask', 'snapshot')
    """
        task_type = COM.convert_to_tag_format(task_type)
        name = COM.convert_to_tag_format(name)
        return COM.get_element_property(xpaths.common_xpaths.any_xpath(f'//*[contains(@data-test,"state-{task_type}-task-{name}")]'), 'innerText')

    @classmethod
    def set_schedule(cls, schedule: str) -> None:
        """
        This method sets the schedule to the given schedule

        :param schedule: is the schedule [hourly/daily/weekly/monthly/custom]

        Example:
            - Data_Protection.set_schedule('weekly')
        """
        COM.select_option('schedule-presets', 'schedule-presets-' + COM.convert_to_tag_format(schedule))
