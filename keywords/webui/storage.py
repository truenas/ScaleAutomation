import xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common


class Storage:
    # Exporting Pool

    @classmethod
    def assert_export_pool_dialog(cls):
        """
        This method asserts that the export pool dialog is visible.
        """
        pool_name = WebUI.get_text(xpaths.common_xpaths.any_header(' Export/disconnect pool: ', 1))
        pool_name = pool_name.partition(':')[2].strip()
        Common.set_checkbox('destroy')
        Common.set_checkbox('confirm')
        Common.set_input_field('name-input', pool_name)
        Common.click_button('disconnect')
        assert WebUI.wait_until_visible(xpaths.common_xpaths.progress_bar) is True
        assert WebUI.wait_until_not_visible(xpaths.common_xpaths.progress_bar, shared_config['EXTRA_LONG_WAIT']) is True
        assert WebUI.wait_until_visible(xpaths.common_xpaths.button_field('dialog-close')) is True
        assert Common.is_visible(xpaths.common_xpaths.any_text(f'disconnected {pool_name}')) is True
        Common.click_button('dialog-close')

    @classmethod
    def assert_pool_item_value_exist(cls, pool_name: str, item: str, value: str) -> bool:
        """
        This method returns True or False whether the given pool name, item and value is visible.

        :param pool_name: The name of the pool to look at.
        :param item: The item to look at.
        :param value: The value of the item.
        :return: True if the given pool name, item and value is visible otherwise it returns False.
        """
        return Common.is_visible(xpaths.storage.pool_cards_item_value(pool_name, item, value))

    @classmethod
    def assert_pool_data_vdevs_value(cls, pool_name: str, value: str) -> bool:
        """
        This method returns True or False whether the given pool name and vdevs value is visible.

        :param pool_name: The name of the pool to look at.
        :param value: The value of the vdevs.
        :return: returns True if the given pool name and vdevs value is visible otherwise it returns False.
        """
        return cls.assert_pool_item_value_exist(pool_name, 'Data VDEVs', value)

    @classmethod
    def assert_storage_dashboard_page(cls):
        """
        This method returns True or False whether the storage dashboard page is visible.

        :return: returns True if the storage dashboard page is visible otherwise it returns False.
        """
        return Common.assert_page_header('Storage Dashboard')

    @classmethod
    def click_add_disks_to_pool_button(cls):
        """
        This method click on the add disks to pool button.
        """
        Common.click_button('add-to-vdev-vdev-1-1')

    @classmethod
    def click_cancel_pool_button(cls):
        """
        This method click on the cancel pool button.
        """
        Common.click_link('cancel')

    @classmethod
    def click_create_pool_button(cls):
        """
        This method click on the create pool button.
        """
        Common.click_link('create-pool')

    @classmethod
    def click_disks_button(cls):
        """
        This method click on the disks button.
        """
        Common.click_link('disks')

    @classmethod
    def click_export_pool_by_name_button(cls, name: str):
        """
        This method click on the export pool button.

        :param name: The name of the pool to export.
        """
        Common.click_button(f'export-{name}')

    @classmethod
    def click_import_pool_button(cls):
        """
        This method click on the import pool button.
        """
        Common.click_button('import-pool')

    @classmethod
    def click_remove_disks_from_pool_button(cls):
        """
        This method click on the remove disks from pool button.
        """
        Common.click_button('remove-to-vdev-vdev-1-1')

    @classmethod
    def is_pool_name_header_visible(cls, pool_name: str) -> bool:
        """
        This method returns True or False whether the given pool name header is visible.

        :param pool_name: The name of the pool to look at.
        :return: True if the given pool name header is visible otherwise it returns False.
        """
        return WebUI.wait_until_visible(xpaths.storage.pool_name_header(pool_name))

    @classmethod
    def export_all_pools(cls):
        """
        This method export all pools.
        """
        pool_count = len(WebUI.find_xpath(xpaths.common_xpaths.any_start_with_field('button-export')))
        for _ in range(0, pool_count):
            Common.click_on_element(xpaths.common_xpaths.any_start_with_field('button-export'))
            cls.assert_export_pool_dialog()

    @classmethod
    def get_show_disks_count(cls) -> int:
        """
        This method returns the number of disks to show.

        :return: The number of disks to show
        """
        return len(cls.get_show_disks_list())

    @classmethod
    def get_show_disks_list(cls) -> list:
        """
        This method returns the list of disks to show.

        :return: The list of disks to show
        """
        return WebUI.find_xpath(xpaths.common_xpaths.any_start_with_field('checkbox-select-disk'))

    @classmethod
    def set_disk_checkbox(cls, row: int):
        """
        This method sets the given disk checkbox.

        :param row: The row number of the disk name.
        """
        if row <= cls.get_show_disks_count():
            disk_name = WebUI.get_text(xpaths.storage.label_disk_name_by_row(row))
            disk_name = disk_name.partition("(")[0].strip()
            Common.set_checkbox(f'select-disk-{disk_name}')
        if WebUI.wait_until_visible(xpaths.common_xpaths.button_field('dialog-close')) is True:
            Common.click_dialog_close_button()

    @classmethod
    def set_show_disks_checkbox(cls):
        """
        This method sets the show disks checkbox.
        """
        if WebUI.wait_until_visible(xpaths.common_xpaths.checkbox_field('show-disks-with-non-unique-serial-numbers')) is True:
            Common.set_checkbox('show-disks-with-non-unique-serial-numbers')
