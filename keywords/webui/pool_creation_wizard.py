import xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common


class Pool_Creation_Wizard:
    @classmethod
    def assert_create_pool_dialog_not_visible(cls):
        """
        This method returns True or False if the create pool dialog is not visible before timeout.

        :return: True if the create pool dialog is not visible before timeout otherwise it returns False.

        Example:
            - Pool_Creation_Wizard.assert_create_pool_dialog_not_visible()
        """
        return Common.assert_dialog_not_visible('Create Pool', shared_config['EXTRA_LONG_WAIT'])

    @classmethod
    def assert_data_value(cls, value: str):
        """
        This method returns True or False if the data value exists.

        :param value: The value of the data
        :return: returns True if the data value exists otherwise it returns False.

        Example:
            - Pool_Creation_Wizard.assert_data_value('100 MB')
        """
        return Common.assert_label_and_value_exist('Data', value)

    @classmethod
    def assert_est_usable_raw_capacity(cls, value: str):
        """
        This method returns True or False if the est. usable raw capacity value exists.

        :param value: The value of the est. usable raw capacity
        :return: returns True if the est. usable raw capacity value exists otherwise it returns False.

        Example:
            - Pool_Creation_Wizard.assert_est_usable_raw_capacity('100 MB')
        """
        return Common.assert_label_and_value_exist('Est. Usable Raw Capacity', value)

    @classmethod
    def assert_pool_creation_wizard_page(cls) -> bool:
        """
        This method returns True or False if the pool creation wizard page is visible.

        :return: True if the pool creation wizard page is visible otherwise it returns False.

        Example:
            - Pool_Creation_Wizard.assert_pool_creation_wizard_page()
        """
        return Common.assert_page_header('Pool Creation Wizard')

    @classmethod
    def assert_pool_name_value(cls, value: str) -> bool:
        """
        This method returns True or False if the pool name value exists.

        :param value: The value of the pool name
        :return: True if the pool name value exists otherwise it returns False.

        Example:
            - Pool_Creation_Wizard.assert_pool_name_value('test_pool')
        """
        return Common.assert_label_and_value_exist('Pool Name', value)

    @classmethod
    def click_back_button(cls, step: str):
        """
        This method click on the Back button of the given step.
        :param step: The name of the step. Available options are: data, log, spare, cache, metadata, dedup or review

        Example:
            - Pool_Creation_Wizard.click_back_button('data')
        """
        Common.click_button(f'back-{step}')

    @classmethod
    def click_confirm_waring_dialog(cls):
        """
        This method click on the confirm button of the warning dialog.

        Example:
            - Pool_Creation_Wizard.click_confirm_waring_dialog()
        """
        assert Common.assert_dialog_visible('Warning') is True
        Common.assert_confirm_dialog()

    @classmethod
    def click_create_pool_button(cls):
        """
        This method click on the Create Pool button on Review step.

        Example:
            - Pool_Creation_Wizard.click_create_pool_button()
        """
        Common.click_button('create-pool')

    @classmethod
    def click_manual_disk_selection_button(cls, step: str):
        """
        This method click on the Manual Disk Selection button of the given step.
        :param step: The name of the step. Available options are: data, log, spare, cache, metadata or dedup.

        Example:
            - Pool_Creation_Wizard.click_manual_disk_selection_button('data')
        """
        Common.click_button(f'manual-{step}')

    @classmethod
    def click_next_button(cls, step: str):
        """
        This method click on the Next button of the given step.
        :param step: The name of the step. Available options are: general, data, log, spare, cache, metadata or dedup.

        Example:
            - Pool_Creation_Wizard.click_next_button('data')
        """
        Common.click_button(f'next-{step}')

    @classmethod
    def click_reset_step_button(cls, step: str):
        """
        This method click on the Reset button of the given step.
        :param step: The name of the step. Available options are: data, log, spare, cache, metadata or dedup.

        Example:
            - Pool_Creation_Wizard.click_reset_step_button('data')
        """
        Common.click_button(f'reset-fields-in-{step}-step')

    @classmethod
    def click_save_and_go_to_review_button(cls, step: str):
        """
        This method click on the Save and Go to Review button of the given step.
        :param step: The name of the step. Available options are: general, data, log, spare, cache, metadata or dedup.

        Example:
            - Pool_Creation_Wizard.click_save_and_go_to_review_button('data')
        """
        Common.click_button(f'save-and-go-to-review-{step}')

    @classmethod
    def click_save_selection_button(cls):
        """
        Clicks the save selection button.

        Example:
            - Pool_Creation_Wizard.click_save_selection_button()
        """
        Common.click_button('save-selection')

    @classmethod
    def click_add_vdevs_button(cls):
        """
        This method click on the Add VDEVS button.

        Example:
            - Pool_Creation_Wizard.click_add_vdevs_button()
        """
        Common.click_button('add')

    @classmethod
    def is_manual_selection_visible(cls) -> bool:
        """
        Check if the Manual Selection element is visible.

        :return: A boolean indicating if the Manual Selection element is visible.

        Example:
            - Pool_Creation_Wizard.is_manual_selection_visible()
        """
        return WebUI.wait_until_visible(xpaths.common_xpaths.any_header('Manual Selection', 3))

    @classmethod
    def select_disk_size_option(cls, step: str, option: str):
        """
        This method selects the given disk size option from the given step.

        :param step: The name of the step. Available options are: data, log, spare, cache, metadata or dedup.
        :param option: The name of the disk size option for example if the option is 20 GiB (HDD)
        then it will look like 20-gi-b-hdd

        Example:
            - Pool_Creation_Wizard.select_disk_size_option('data', '20-gi-b-hdd')
        """
        # TODO: Replace select_option_text with select_option when https://ixsystems.atlassian.net/browse/NAS-126826 is fixed.
        # Common.select_option(f'size-and-type-{step}', f'size-and-type-{option}')
        Common.select_option_text(f'size-and-type-{step}', option)

    @classmethod
    def select_layout_option(cls, step: str, option: str):
        """
        This method selects the given layout option from the given step.

        :param step: The name of the step. Available options are: data, log, metadata or dedup.
        :param option: The name of the layout. Available options are: stripe, mirror, raidz-1' raidz-2, raidz-3,
         d-raid-1, d-raid-2 and d-raid-3.

        Example:
            - Pool_Creation_Wizard.select_layout_option('data', 'raidz-1')
        """
        # TODO: Replace select_option_text with select_option when https://ixsystems.atlassian.net/browse/NAS-126826 is fixed.
        # Common.select_option(f'size-and-type-{step}', f'layout-{option}')
        Common.select_option_text(f'layout-{step}', option)

    @classmethod
    def select_number_of_vdevs_option(cls, step: str, option: int):
        """
        This method selects the given number of vdevs option from the given step.

        :param step: The name of the step. Available options are: data, metadata and dedup.
        :param option: The number of vdevs. Available options are: 1, 2 and 3.

        Example:
            - Pool_Creation_Wizard.select_number_of_vdevs_option('data', 2)
        """
        # TODO: Replace select_option_text with select_option when https://ixsystems.atlassian.net/browse/NAS-126826 is fixed.
        # Common.select_option(f'vdevs-number-{step}', f'vdevs-number-{option})
        Common.select_option_text(f'vdevs-number-{step}', str(option))

    @classmethod
    def select_width_option(cls, step: str, option: int):
        """
        This method selects the given width option from the given step.

        :param step: The name of the step. Available options are: data, log, metadata or dedup.
        :param option: The number of vdevs. Available options are: 1, 2 and 3.

        Example:
            - Pool_Creation_Wizard.select_width_option('data', 2)
        """
        # TODO: Replace select_option_text with select_option when https://ixsystems.atlassian.net/browse/NAS-126826 is fixed.
        # Common.select_option(f'width-{step}', f'width-{option})
        Common.select_option_text(f'width-{step}', str(option))

    @classmethod
    def set_encryption_checkbox(cls):
        """
        This method sets the encryption checkbox.

        Example:
            - Pool_Creation_Wizard.set_encryption_checkbox()
        """
        Common.set_checkbox('encryption')

    @classmethod
    def set_name_entry(cls, pool_name: str):
        """
        This method sets the pool name entry.

        :param pool_name: The name of the pool.

        Example:
            - Pool_Creation_Wizard.set_name_entry('test_pool')
        """
        Common.set_input_field('name', pool_name)

    @classmethod
    def set_search_entry(cls, search):
        """
        This method sets the search entry.

        :param search: The disk name to search.

        Example:
            - Pool_Creation_Wizard.set_search_entry('test_pool')
        """
        Common.set_input_field('search', search)

    @classmethod
    def set_treat_disk_size_as_minimum_checkbox(cls, step: str):
        """
        This method sets the Treat Disk Size as Minimum checkbox.

        :param step: The name of the step. Available options are: data, log, spare, cache, metadata and dedup.

        Example:
            - Pool_Creation_Wizard.set_treat_disk_size_as_minimum_checkbox('data')
        """
        Common.set_checkbox(f'disk-size-as-minimum-{step}')

    @classmethod
    def unset_encryption_checkbox(cls):
        """
        This method unsets the encryption checkbox.

        Example:
            - Pool_Creation_Wizard.unset_encryption_checkbox()
        """
        Common.unset_checkbox('encryption')

    @classmethod
    def unset_treat_disk_size_as_minimum_checkbox(cls, step: str):
        """
        This method unsets the Treat Disk Size as Minimum checkbox.
        :param step: The name of the step. Available options are: data, log, spare, cache, metadata and dedup.

        Example:
            - Pool_Creation_Wizard.unset_treat_disk_size_as_minimum_checkbox('data')
        """
        Common.unset_checkbox(f'disk-size-as-minimum-{step}')
