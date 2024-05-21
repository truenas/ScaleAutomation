import xpaths
from helper.global_config import shared_config, private_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


class Data_Protection:

    @classmethod
    def assert_add_cloud_sync_task_button_is_restricted(cls) -> bool:
        """
        This method returns True if the add cloud sync task button is locked and not clickable.

        :return: True if the add cloud sync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_add_cloud_sync_task_button_is_restricted()
        """
        return COM.assert_button_is_restricted('cloudsync-task-add')

    @classmethod
    def assert_add_periodic_snapshot_task_button_is_restricted(cls) -> bool:
        """
        This method returns True if the add periodic snapshot task button is locked and not clickable.

        :return: True if the add periodic snapshot task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_add_periodic_snapshot_task_button_is_restricted()
        """
        return COM.assert_button_is_restricted('snapshot-task-add')

    @classmethod
    def assert_add_rsync_task_button_is_restricted(cls) -> bool:
        """
        This method returns if the add rsync task button is locked and not clickable.

        :return: True if the add rsync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_add_rsync_task_button_is_restricted()
        """
        return COM.assert_button_is_restricted('rsync-task-add')

    @classmethod
    def assert_add_scrub_task_button_is_restricted(cls) -> bool:
        """
        This method returns True if the add scrub task button is locked and not clickable.

        :return: True if the add scrub task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_add_scrub_task_button_is_restricted()
        """
        return COM.assert_button_is_restricted('scrub-task-add')

    @classmethod
    def assert_add_smart_test_button_is_restricted(cls) -> bool:
        """
        This method returns True if the add smart test button is locked and not clickable.

        :return: True if the add smart test button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_add_smart_test_button_is_restricted()
        """
        return COM.assert_button_is_restricted('smart-task-add')

    @classmethod
    def assert_add_vm_periodic_snapshot_button_is_restricted(cls) -> bool:
        """
        This method returns True if the add vm periodic snapshot button is locked and not clickable.

        :return: True if the add vm periodic snapshot button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_add_vm_periodic_snapshot_button_is_restricted()
        """
        return COM.assert_button_is_restricted('add-vmware-snapshot')

    @classmethod
    def assert_cloud_sync_task_description(cls, description: str) -> bool:
        """
        This method returns True if the given cloud sync task description is visible, otherwise returns False.

        :param description: description of the cloud sync task
        :return: True if the given cloud sync task description is visible, otherwise returns False.

        Example:
            - Data_Protection.assert_cloud_sync_task_description("description")
        """
        description = COM.convert_to_tag_format(description)
        return COM.is_visible(xpaths.data_protection.cloud_sync_task_description(description))

    @classmethod
    def assert_delete_cloud_sync_task_button_is_restricted(cls, description: str) -> bool:
        """
        This method returns True if the delete cloud sync task button is locked and not clickable.

        :param description: description of the cloud sync task
        :return: True if the delete cloud sync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_delete_cloud_sync_task_button_is_restricted('description')
        """
        description = COM.convert_to_tag_format(description)
        return COM.assert_element_is_restricted(xpaths.data_protection.cloud_sync_task_delete_button(description))

    @classmethod
    def assert_delete_periodic_snapshot_task_button_is_restricted(cls, path: str) -> bool:
        """
        This method returns True if the delete periodic snapshot task button is locked and not clickable.

        :param path: path of the periodic snapshot task
        :return: True if the delete periodic snapshot task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_delete_periodic_snapshot_task_button_is_restricted('tank/dataset')
        """
        path = COM.convert_to_tag_format(path)
        return COM.assert_element_is_restricted(xpaths.data_protection.periodic_snapshot_task_delete_button(path))

    @classmethod
    def assert_delete_rsync_task_button_is_restricted(cls, path: str) -> bool:
        """
        This method returns if the delete rsync task button is locked and not clickable.

        :param path: path of the rsync task
        :return: True if the delete rsync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_delete_rsync_task_button_is_restricted('/my/Rep/Path')
        """
        xpath_ip = COM.convert_to_tag_format(private_config['REP_DEST_IP'])
        xpath_path = COM.convert_to_tag_format(path)
        xpath = f'card-rsync-task{xpath_path}-{xpath_ip}-delete-row-action'
        return COM.assert_button_is_restricted(xpath)

    @classmethod
    def assert_delete_scrub_task_button_is_restricted(cls, description: str) -> bool:
        """
        This method returns if the delete scrub task button is locked and not clickable.

        :param description: description of the scrub task
        :return: True if the delete scrub task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_delete_scrub_task_button_is_restricted('description')
        """
        description = COM.convert_to_tag_format(description)
        return COM.assert_element_is_restricted(xpaths.data_protection.scrub_task_delete_button(description))

    @classmethod
    def assert_delete_smart_test_button_is_restricted(cls, description: str) -> bool:
        """
        This method returns if the delete smart test button is locked and not clickable.

        :param description: description of the smart test
        :return: True if the delete smart test button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_delete_smart_test_button_is_restricted('description')
        """
        return COM.assert_element_is_restricted(xpaths.data_protection.smart_test_delete_button(description))

    @classmethod
    def assert_delete_vm_periodic_snapshot_task_button_is_restricted(cls, path: str) -> bool:
        """
        This method returns if the delete vm periodic snapshot task button is locked and not clickable.

        :param path: path of the periodic snapshot task
        :return: True if the delete vm periodic snapshot task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_delete_vm_periodic_snapshot_task_button_is_restricted('tank/dataset')
        """
        path = COM.convert_to_tag_format(path)
        return COM.assert_element_is_restricted(xpaths.data_protection.vm_periodic_snapshot_task_delete_button(path))

    @classmethod
    def assert_dry_run_cloud_sync_task_button_is_restricted(cls, description: str) -> bool:
        """
        This method returns Rrue if the dry run cloud sync task button is locked and not clickable.

        :param description: description of the cloud sync task
        :return: True if the dry run cloud sync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_dry_run_cloud_sync_task_button_is_restricted('description')
        """
        description = COM.convert_to_tag_format(description)
        return COM.assert_element_is_restricted(xpaths.data_protection.cloud_sync_task_dry_run_button(description))

    @classmethod
    def assert_enable_cloud_sync_task_toggle_is_restricted(cls, description: str) -> bool:
        """
        This method asserts if the enable cloud sync task toggle is locked and not clickable.

        :param description: description of the cloud sync task
        :return: True if the enable cloud sync task toggle is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_enable_cloud_sync_task_toggle_is_restricted('description')
        """
        description = COM.convert_to_tag_format(description)
        return COM.assert_element_is_restricted(xpaths.data_protection.cloud_sync_task_enable_toggle(description))

    @classmethod
    def assert_enable_periodic_snapshot_task_toggle_is_restricted(cls, path: str) -> bool:
        """
        This method asserts if the enable periodic snapshot task toggle is locked and not clickable.

        :param path: path of the cloud sync task
        :return: True if the enable periodic snapshot task toggle is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_enable_periodic_snapshot_task_toggle_is_restricted('tank/dataset')
        """
        path = COM.convert_to_tag_format(path)
        return COM.assert_element_is_restricted(xpaths.data_protection.periodic_snapshot_task_enable_toggle(path))

    @classmethod
    def assert_enable_rsync_task_toggle_is_restricted(cls, path: str) -> bool:
        """
        This method asserts if the enable rsync task toggle is locked and not clickable.

        :param path: path of the rsync task
        :return: True if the enable rsync task toggle is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_enable_rsync_task_toggle_is_restricted('/my/Rep/Path')
        """
        xpath_ip = COM.convert_to_tag_format(private_config['REP_DEST_IP'])
        xpath_path = COM.convert_to_tag_format(path)
        xpath = f'enabled-card-rsync-task{xpath_path}-{xpath_ip}-row-toggle'
        return COM.assert_toggle_is_restricted(xpath)

    @classmethod
    def assert_enable_scrub_task_toggle_is_restricted(cls, description: str) -> bool:
        """
        This method returns if the enable scrub task toggle is locked and not clickable.

        :param description: description of the scrub task
        :return: True if the enable scrub task toggle is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_enable_scrub_task_toggle_is_restricted('description')
        """
        description = COM.convert_to_tag_format(description)
        return COM.assert_element_is_restricted(xpaths.data_protection.scrub_task_enable_toggle(description))

    @classmethod
    def assert_periodic_snapshot_task_dataset(cls, path: str) -> bool:
        """
        This method returns True if the given periodic snapshot task path is visible, otherwise returns False.

        :param path: path of the periodic snapshot task
        :return: True if the given periodic snapshot task path is visible, otherwise returns False.

        Example:
            - Data_Protection.assert_periodic_snapshot_task_dataset("tank/dataset")
        """
        path = COM.convert_to_tag_format(path)
        return COM.is_visible(xpaths.data_protection.periodic_snapshot_task_path(path))

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
    def assert_restore_cloud_sync_task_button_is_restricted(cls, description: str) -> bool:
        """
        This method returns if the restore cloud sync task button is locked and not clickable.

        :param description: description of the cloud sync task
        :return: True if the restore cloud sync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_restore_cloud_sync_task_button_is_restricted('description')
        """
        description = COM.convert_to_tag_format(description)
        return COM.assert_element_is_restricted(xpaths.data_protection.cloud_sync_task_restore_button(description))

    @classmethod
    def assert_run_cloud_sync_task_button_is_restricted(cls, description: str) -> bool:
        """
        This method returns if the run now cloud sync task button is locked and not clickable.

        :param description: description of the cloud sync task
        :return: True if the run now cloud sync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_run_cloud_sync_task_button_is_restricted('description')
        """
        description = COM.convert_to_tag_format(description)
        return COM.assert_element_is_restricted(xpaths.data_protection.cloud_sync_task_run_now_button(description))

    @classmethod
    def assert_run_rsync_task_button_is_restricted(cls, path: str) -> bool:
        """
        This returns if the run now rsync task button is locked and not clickable.

        :param path: path of the rsync task
        :return: True if the run now rsync task button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_run_rsync_task_button_is_restricted('/my/Rep/Path')
        """
        xpath_ip = COM.convert_to_tag_format(private_config['REP_DEST_IP'])
        xpath_path = COM.convert_to_tag_format(path)
        xpath = f'card-rsync-task{xpath_path}-{xpath_ip}-play-arrow-row-action'
        return COM.assert_button_is_restricted(xpath)

    @classmethod
    def assert_rsync_task_card_header_is_visible(cls) -> bool:
        """
        This method returns if the rsync task card header is visible.

        :return: True if the rsync task card header is visible, otherwise False.

        Example:
            - Data_Protection.assert_rsync_task_card_header_is_visible()
        """
        return COM.is_card_visible('Rsync Task')

    @classmethod
    def assert_rsync_task_is_visible_on_card(cls, path: str) -> bool:
        """
        This method returns True if the given rsync task is visible, otherwise False.

        :param path: is the name of the given rsync path.
        :return: True if the given rsync task is visible, otherwise False.

        Example:
            - Data_Protection.assert_rsync_task_is_visible('/my/Rep/Path')
        """
        xpath_ip = COM.convert_to_tag_format(private_config['REP_DEST_IP'])
        xpath_path = COM.convert_to_tag_format(path)
        task_xpath = f'//*[@data-test="text-path-card-rsync-task{xpath_path}-{xpath_ip}-row-text"]'
        return WebUI.wait_until_visible(task_xpath, shared_config['MEDIUM_WAIT'])

    @classmethod
    def assert_scrub_task_description(cls, description: str) -> bool:
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
    def assert_smart_page_add_smart_test_button_is_restricted(cls) -> bool:
        """
        This method returns True if the add smart test button is locked and not clickable.

        :return: True if the add smart test button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_smart_page_add_smart_test_button_is_restricted()
        """
        return COM.assert_button_is_restricted('periodic-s-m-a-r-t-tests-add')

    @classmethod
    def assert_smart_page_delete_smart_test_button_is_restricted(cls) -> bool:
        """
        This method returns True if the delete smart test button is locked and not clickable.

        :return: True if the delete smart test button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_smart_page_delete_smart_test_button_is_restricted()
        """
        return COM.assert_button_is_restricted('periodic-s-m-a-r-t-tests-options-delete')

    @classmethod
    def assert_smart_page_save_smart_test_button_is_restricted(cls) -> bool:
        """
        This method returns True if the save smart test button is locked and not clickable.

        :return: True if the save smart test button is locked and not clickable, otherwise it returns False.

        Example:
            - Data_Protection.assert_smart_page_save_smart_test_button_is_restricted()
        """
        return COM.assert_button_is_restricted('save')

    @classmethod
    def assert_smart_page_smart_test_description(cls, description: str) -> bool:
        """
        This method returns True if the given smart test description is visible, otherwise returns False.

        :param description: description of the smart test
        :return: True if the given smart test description is visible, otherwise returns False.

        Example:
            - Data_Protection.assert_smart_page_smart_test_description("SMART test Description")
        """
        return COM.is_visible(xpaths.common_xpaths.any_xpath(f'//*[contains(text(),"{description}")]'))

    @classmethod
    def assert_smart_test_description(cls, description: str) -> bool:
        """
        This method returns True if the given smart test description is visible, otherwise returns False.

        :param description: description of the smart test
        :return: True if the given smart test description is visible, otherwise returns False.

        Example:
            - Data_Protection.assert_smart_test_description("SMART test Description")
        """
        return COM.is_visible(xpaths.data_protection.smart_test_description(description))

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
    def click_card_page_link(cls, title: str) -> None:
        """
        This method clicks the card page link for the given card title

        :param title: the title of the given card

        Example:
            - Data_Protection.click_card_page_link('myRepTask')
        """
        COM.click_on_element(f'//h3[contains(text(),"{title}")]')
        COM.assert_page_header(title)

    @classmethod
    def click_edit_cloud_sync_task(cls, description: str) -> None:
        """
        This method clicks the edit button for the given cloud sync task

        :param description: the description of the given cloud sync task

        Example:
            - Data_Protection.click_edit_cloud_sync_task('description')
        """
        description = COM.convert_to_tag_format(description)
        COM.click_on_element(xpaths.data_protection.cloud_sync_task_edit_button(description))
        # TODO: Fix when NAS-128725 is addressed
        COM.cancel_confirm_dialog()
        assert COM.assert_right_panel_header('Edit Cloud Sync Task') is True

    @classmethod
    def click_edit_periodic_snapshot_task(cls, path: str) -> None:
        """
        This method clicks the edit button for the given periodic snapshot task

        :param path: the path of the given periodic snapshot task

        Example:
            - Data_Protection.click_edit_periodic_snapshot_task('tank/dataset')
        """
        path = COM.convert_to_tag_format(path)
        COM.click_on_element(xpaths.data_protection.periodic_snapshot_task_edit_button(path))
        COM.assert_right_panel_header('Edit Periodic Snapshot Task')

    @classmethod
    def click_edit_replication_task_by_name(cls, name: str) -> None:
        """
        This method clicks the edit button for the given replication task

        :param name: the name of the given replication task

        Example:
            - Data_Protection.click_edit_replication_task_by_name('myRepTask')
        """
        COM.click_button(f'replication-task-{COM.convert_to_tag_format(name)}-edit-row-action')
        COM.assert_right_panel_header('Edit Replication Task')

    @classmethod
    def click_edit_rsync_task_by_path(cls, path: str) -> None:
        """
        This method clicks the edit button for the given rsync task

        :param path: the path of the given rsync task

        Example:
            - Data_Protection.click_edit_rsync_task_by_dataset('/mnt/tank/dataset')
        """
        xpath_ip = COM.convert_to_tag_format(private_config['REP_DEST_IP'])
        xpath_path = COM.convert_to_tag_format(path)
        COM.click_button(f'card-rsync-task{xpath_path}-{xpath_ip}-edit-row-action')

    @classmethod
    def click_edit_scrub_task(cls, description: str) -> None:
        """
        This method clicks the edit button for the given scrub task

        :param description: the description of the given scrub task

        Example:
            - Data_Protection.click_edit_scrub_task('description')
        """
        description = COM.convert_to_tag_format(description)
        COM.click_on_element(xpaths.data_protection.scrub_task_edit_button(description))
        assert COM.assert_right_panel_header('Edit Scrub Task') is True

    @classmethod
    def click_edit_smart_test(cls, description: str) -> None:
        """
        This method clicks the edit button for the given smart test

        :param description: the description of the given smart test

        Example:
            - Data_Protection.click_edit_smart_test('description')
        """
        COM.click_on_element(xpaths.data_protection.smart_test_edit_button(description))
        assert COM.assert_right_panel_header('Edit S.M.A.R.T. Test') is True

    @classmethod
    def click_edit_snapshot_task_by_name(cls, name: str) -> None:
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
    def click_edit_vm_periodic_snapshot_task(cls, path: str) -> None:
        """
        This method clicks the edit button for the given vm periodic snapshot task

        :param path: the path of the given periodic snapshot task

        Example:
            - Data_Protection.click_edit_vm_periodic_snapshot_task('tank/dataset')
        """
        path = COM.convert_to_tag_format(path)
        COM.click_on_element(xpaths.data_protection.vm_periodic_snapshot_task_edit_button(path))
        COM.assert_right_panel_header('Edit VM Periodic Snapshot Task')

    @classmethod
    def click_the_rsync_task_header_link(cls):
        """
        This method clicks the rsync task card title link.

        Example:
            - Rsync_Task.click_the_rsync_task_title_link()
        """
        COM.click_link("rsync-task-open-in-new")

    @classmethod
    def click_snapshots_button(cls) -> None:
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
    def delete_all_snapshots(cls) -> None:
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
        COM.select_option(
            'schedule-presets',
            f'schedule-presets-{COM.convert_to_tag_format(schedule)}',
        )
