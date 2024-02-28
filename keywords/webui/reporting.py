from keywords.webui.common import Common


class Reporting:
    @classmethod
    def assert_cpu_reporting_page_header(cls) -> bool:
        """
        This method returns True or False whether the CPU Reporting page header is visible.

        :return: True if the CPU reporting page header is visible, otherwise it returns False.
        """
        return Common.assert_page_header('CPU')

    @classmethod
    def assert_memory_reporting_page_header(cls) -> bool:
        """
        This method returns True or False whether the memory reporting page header is visible.

        :return: True if the memory reporting page header is visible, otherwise it returns False.
        """
        return Common.assert_page_header('Memory')

    @classmethod
    def assert_network_reporting_page_header(cls) -> bool:
        """
        This method returns True or False whether the network reporting page header is visible.

        :return: True if the network reporting page header is visible, otherwise it returns False.
        """
        return Common.assert_page_header('Network')

    @classmethod
    def assert_reporting_page_breadcrumb(cls) -> bool:
        """
        This method returns True or False whether the Reporting page breadcrumb is visible.

        :return: True if the Reporting page breadcrumb is visible, otherwise it returns False.
        """
        return Common.assert_text_is_visible('Reporting')

    @classmethod
    def assert_storage_reporting_page_header(cls) -> bool:
        """
        This method returns True or False whether the storage reporting page header is visible.

        :return: True if the storage reporting page header is visible, otherwise it returns False.
        """
        return Common.assert_page_header('Disk')

    @classmethod
    def is_cpu_usage_card_visible(cls) -> bool:
        """
        This method returns True or False whether the CPU usage card is visible.

        :return: True if the CPU usage card is visible, otherwise it returns False.
        """
        return Common.is_card_visible('CPU Usage')

    @classmethod
    def is_disk_i_o_card_visible(cls, name: str) -> bool:
        """
        This method returns True or False whether the disk card is visible.

        :return: True if the disk card is visible, otherwise it returns False.
        """
        # TODO: This will fail sporadically due to the dynamic/lazy loading of the reporting page.
        #   NAS-127431 has been created for the non-alphabetical portion of the failure but we should
        #   come up with a better solution anyways to actually verify the disks on the system are present.
        return Common.is_card_visible(f'Disk I/O {name}')

    @classmethod
    def is_interface_traffic_card_visible(cls) -> bool:
        """
        This method returns True or False whether the interface traffic card is visible.

        :return: True if the interface traffic card is visible, otherwise it returns False.
        """
        return Common.is_card_visible('Interface Traffic')

    @classmethod
    def is_physical_memory_utilization_card_visible(cls) -> bool:
        """
        This method returns True or False whether the physical memory utilization card is visible.

        :return: True if the physical memory utilization card is visible, otherwise it returns False.
        """
        return Common.is_card_visible('Physical memory utilization')

    @classmethod
    def is_swap_utilization_card_visible(cls) -> bool:
        """
        This method returns True or False whether the swap utilization card is visible.

        :return: True if the swap utilization card is visible, otherwise it returns False.
        """
        return Common.is_card_visible('Swap Utilization')

    @classmethod
    def is_system_load_card_visible(cls) -> bool:
        """
        This method returns True or False whether the system load card is visible.

        :return: True if the system load card is visible, otherwise it returns False.
        """
        return Common.is_card_visible('System Load')
