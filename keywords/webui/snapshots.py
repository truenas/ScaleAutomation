from selenium.common import ElementClickInterceptedException

import xpaths
from helper.webui import WebUI

from keywords.webui.common import Common


class Snapshots:

    @classmethod
    def assert_clone_to_new_snapshot_button_is_restricted(cls, snapshots_name) -> bool:
        """
        This method asserts that the Clone to New Snapshot button is locked and not clickable

        :param snapshots_name: The name of the snapshot
        :return: True if the Clone to New Snapshot button is locked and not clickable, otherwise it returns False.

        Example:
            - Snapshots.assert_clone_to_new_snapshot_button_is_restricted('test-snapshot')
        """
        return Common.assert_button_is_restricted(f'clone-{snapshots_name}')

    @classmethod
    def assert_dataset_snapshot_page_header(cls, dataset) -> bool:
        """
        This method asserts that the Dataset Snapshot page header is visible

        :param dataset: The name of the dataset including the pool
        :return: True if the page header is visible, otherwise it returns False.

        Example:
            - Snapshots.assert_dataset_snapshot_page_header('pool/dataset')
        """
        return Common.assert_page_header(f'Snapshots: {dataset}')

    @classmethod
    def assert_delete_button_is_restricted(cls, snapshots_name: str) -> bool:
        """
        This method asserts that the Delete Snapshot button is locked and not clickable

        :param snapshots_name: The name of the snapshot
        :return: True if the Delete Snapshot button is locked and not clickable, otherwise it returns False.

        Example:
            - Snapshots.assert_delete_snapshot_button_is_restricted('test-snapshot')
        """
        return Common.assert_button_is_restricted(f'delete-{snapshots_name}')

    @classmethod
    def assert_hold_checkbox_is_restricted(cls, snapshots_name: str) -> bool:
        """
        This method asserts that the Hold checkbox is locked and not clickable

        :param snapshots_name: The name of the snapshot
        :return: True if the Hold checkbox is locked and not clickable, otherwise it returns False.

        Example:
            - Snapshots.assert_hold_checkbox_is_restricted('test-snapshot')
        """
        assert WebUI.wait_until_visible(xpaths.datasets.checkbox_locked_snapshot_hold(snapshots_name)) is True
        WebUI.delay(0.2)
        try:
            Common.click_on_element(xpaths.common_xpaths.any_xpath("//*[@data-test='checkbox']"))
        except ElementClickInterceptedException:
            return True
        return False

    @classmethod
    def assert_rollback_button_is_restricted(cls, snapshots_name: str) -> bool:
        """
        This method asserts that the Rollback Snapshot button is locked and not clickable

        :param snapshots_name: The name of the snapshot
        :return: True if the Rollback Snapshot button is locked and not clickable, otherwise it returns False.

        Example:
            - Snapshots.assert_rollback_snapshot_button_is_restricted('test-snapshot')
        """
        return Common.assert_button_is_restricted(f'rollback-{snapshots_name}')

    @classmethod
    def assert_snapshot_is_visible(cls, snapshot_name: str) -> bool:
        """
        This method asserts that the snapshot is visible

        :param snapshot_name: The name of the snapshot
        :return: True if the snapshot is visible, otherwise it returns False.

        Example:
            - Snapshots.assert_snapshot_is_visible('test-snapshot')
        """
        return Common.assert_text_is_visible(snapshot_name)

    @classmethod
    def assert_snapshots_page_header(cls) -> bool:
        """
        This method asserts that the Snapshots page is visible

        Example:
            - Snapshots.assert_snapshots_page_header()
        """
        return Common.assert_page_header('Snapshots')

    @classmethod
    def click_add_snapshot_button(cls) -> None:
        """
        This method clicks the Add snapshot button

        Example:
            - Data_Protection.click_add_snapshot_button()
        """
        Common.click_button('add-snapshot')
        assert Common.assert_right_panel_header('Add Snapshot') is True
        assert Common.assert_progress_bar_not_visible() is True

    @classmethod
    def click_rollback_button(cls) -> None:
        """
        This method clicks the Rollback Snapshot button

        Example:
            - Snapshots.click_rollback_button()
        """
        return Common.click_on_element('//*[starts-with(@data-test,"button-rollback")]')

    @classmethod
    def confirm_rollback_snapshot_dialog(cls) -> None:
        """
        This method confirms the Rollback Snapshot dialog

        Example:
            - Snapshots.confirm_rollback_snapshot_dialog()
        """
        Common.set_checkbox('force')
        Common.click_button('rollback')

    @classmethod
    def expand_snapshot_by_name(cls, snapshot_name: str) -> None:
        """
        This method expands the given snapshot

        :param snapshot_name: The name of the snapshot to expand

        Example:
            - Snapshots.expand_snapshot('test-snapshot')
        """
        Common.click_on_element(xpaths.common_xpaths.any_text(snapshot_name))

    @classmethod
    def select_schedule_preset(cls, option: str) -> None:
        """
        This method selects the schedule preset option

        :param option: is the option to select [custom/daily/hourly/monthly/weekly]

        Example:
            - Replication.select_schedule_preset('monthly')
        """
        Common.select_option('schedule-presets', f'schedule-presets-{Common.convert_to_tag_format(option)}')
        if option == 'custom':
            WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Presets', 4))

    @classmethod
    def select_snapshot_dataset(cls, path: str):
        """
        This method selects the Snapshot dataset

        :param path: is the path of the dataset to snapshot

        Example:
            - Snapshots.select_snapshot_dataset('pool/dataset/path')
        """
        Common.select_option('dataset', f'dataset-{Common.convert_to_tag_format(path)}')
