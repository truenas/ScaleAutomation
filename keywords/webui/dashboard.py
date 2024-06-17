import xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common


class Dashboard:
    @classmethod
    def assert_card_position(cls, position: int, field: str) -> bool:
        """
        This method returns True if the given card is at the given position otherwise it returns False.

        :param position: is the number of the position that the card should be.
        :param field: is the name of the card.
        :return: True if the given card is at the given position otherwise it returns False.
        """
        card_name = cls.get_dashboard_card_name_by_position(position)
        return True if field == card_name else False

    @classmethod
    def assert_cpu_card_load_graph_text(cls) -> bool:
        """
        This method returns True or False whether all cpu load graph text are visible.

        :return: True if all cpu load graph text are visible otherwise it returns False.
        """
        assert WebUI.wait_until_visible('//ix-view-chart-gauge', shared_config['LONG_WAIT']) is True
        assert WebUI.wait_until_visible(xpaths.dashboard.cpu_subtitle) is True
        results_list = [
            "Avg Usage" in WebUI.get_text(xpaths.dashboard.cpu_subtitle),
            "Thread" in WebUI.get_text(xpaths.dashboard.cpu_load_cores(1)),
            "Usage" in WebUI.get_text(xpaths.dashboard.cpu_load_cores(2))
        ]
        return all(results_list)

    @classmethod
    def assert_cpu_card_load_graph_ui(cls) -> bool:
        """
        This method returns True or False whether the cpu load graph ui is visible.

        :return: True if the cpu load graph ui is visible otherwise it returns False.
        """
        # Wait until the cpu cores chart is visible
        return WebUI.wait_until_visible(xpaths.dashboard.cpu_cores_chart)

    @classmethod
    def assert_cpu_card_load_text(cls, index: int, text) -> bool:
        """
        This method returns True or False whether the given cpu load text is visible in the given index.

        :param index: is the number of the item in the list to get the text.
        :param text: is the text to verify that it match with the given index.
        :return: True if the given cpu load text is visible in the given index otherwise it returns False.
        """
        return text in WebUI.get_text(xpaths.dashboard.card_list_item('cpu', index)+'//strong')

    @classmethod
    def assert_dashboard_configure_panel_is_visible(cls) -> bool:
        """
        This method returns True if the dashboard configure panel is visible otherwise it returns False.

        :return: True if the dashboard configure panel is visible otherwise it returns False.
        """
        return Common.assert_right_panel_header('Dashboard Configure')

    @classmethod
    def assert_dashboard_page_header_is_visible(cls) -> bool:
        """
        This method returns True if the dashboard page header is visible otherwise it returns False.

        :return: True if the dashboard page header is visible otherwise it returns False.
        """
        return Common.assert_page_header('Dashboard')

    @classmethod
    def assert_new_tab_url(cls, link: str) -> bool:
        """
        This method returns True or False whether the new tab opened to the right link.

        :param link: is the url link to click on.
        :return: True if the new tab opened to the right link, otherwise it returns False.
        """
        initial_tab = WebUI.current_window_handle()
        Common.click_on_element(xpaths.dashboard.truenas_help_card_link(link))
        WebUI.wait_until_number_of_windows_to_be(2)

        initial_index = WebUI.window_handles().index(initial_tab)
        next_tab = initial_index + 1

        WebUI.switch_to_window_index(next_tab)

        # Let the browser load the new tab
        WebUI.delay(1)
        url_exists = True if WebUI.current_url() == link else False

        WebUI.close_window()
        WebUI.switch_to_window_index(initial_index)
        WebUI.wait_until_number_of_windows_to_be(1)

        return url_exists

    @classmethod
    def assert_system_information_version_clipboard_copy(cls) -> None:
        """
        This method return True or False whether the copied version match the version on the UI.

        :return: True if the copied version match the version on the UI, otherwise it returns False
        """
        xpath = '//*[contains(text(),"Version:")]/ancestor::ix-widget-sysinfo/descendant::span/div'
        version = WebUI.get_text(xpaths.common_xpaths.any_xpath(xpath))
        version = version.replace('Version:', '').replace('assignment', '').strip()
        Common.click_button('copy-to-clipboard')
        clipboard = WebUI.get_clipboard_text()
        return version == clipboard

    @classmethod
    def assert_system_information_ui(cls) -> bool:
        """
        This method returns True or False whether Platform, Version, Hostname, Uptime
        are all found on System Information Card.

        :return: True if Platform, Version, Hostname, Uptime are all found on System
        Information Card, otherwise it returns False.
        """
        list_results = [
            WebUI.get_text(xpaths.dashboard.card_list_item('sysinfo', 1)).startswith('Platform'),
            WebUI.get_text(xpaths.dashboard.card_list_item('sysinfo', 2)).startswith('Version'),
            WebUI.get_text(xpaths.dashboard.card_list_item('sysinfo', 3)).startswith('Hostname'),
            WebUI.get_text(xpaths.dashboard.card_list_item('sysinfo', 4)).startswith('Uptime')
        ]
        # All need to be true or it returns false.
        return all(list_results)

    @classmethod
    def assert_the_truenas_help_documentation_link(cls) -> bool:
        """
        This method returns True or False whether TrueNAS Help documentation link opened to the right link.

        :return: True if the documentation link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://www.truenas.com/docs/')

    @classmethod
    def assert_the_truenas_help_ixsystems_inc_link(cls) -> bool:
        """
        This method returns True or False whether TrueNAS Help iXsystems inc link opened to the right link.

        :return: True if the iXsystems inc link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://www.ixsystems.com/')

    @classmethod
    def assert_the_truenas_help_open_source_link(cls) -> bool:
        """
        This method returns True or False whether TrueNAS Help open source link opened to the right link.

        :return: True if the open source link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://github.com/truenas/')

    @classmethod
    def assert_the_truenas_help_truenas_community_forums_link(cls) -> bool:
        """
        This method returns True or False whether TrueNAS Help community forums link opened to the right link.

        :return: True if the community forums link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://forums.truenas.com/')

    @classmethod
    def assert_the_truenas_help_truenas_newsletter_link(cls) -> bool:
        """
        This method returns True or False whether TrueNAS Help TrueNAS newsletter link opened to the right link.

        :return: True if the TrueNAS newsletter link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://www.truenas.com/newsletter/')

    @classmethod
    def click_check_update_button(cls) -> None:
        """
        This method click on the system information Check Updates or Updates Available button.
        """
        Common.click_button('widget-sysinfo-update')

    @classmethod
    def click_the_cancel_reorder_button(cls) -> None:
        """
        This method click on the cancel reorder button.
        """
        Common.click_button('cancel-reorder')

    @classmethod
    def click_the_configure_button(cls) -> None:
        """
        This method click on the Configure button on the dashboard.
        """
        Common.click_button('configure-dashboard')

    @classmethod
    def click_the_cpu_report_button(cls) -> None:
        """
        This method click on CPU report button.
        """
        Common.click_link('cpu-reports')

    @classmethod
    def click_the_memory_report_button(cls) -> None:
        """
        This method click on memory report button.
        """
        Common.click_button('memory-go-to-reports')

    @classmethod
    def click_the_network_report_button(cls) -> None:
        """
        This method click on Network report button.
        """
        Common.click_link('network-reports')

    @classmethod
    def click_the_reorder_button(cls) -> None:
        """
        This method click on the Dashboard Reorder button.
        """
        Common.click_button('start-reorder')
        WebUI.delay(1)

    @classmethod
    def click_the_save_reorder_button(cls) -> None:
        """
        This method click on the save reorder button.
        """
        Common.click_button('save-new-order')
        WebUI.wait_until_visible(xpaths.common_xpaths.button_field('start-reorder'))

    @classmethod
    def click_the_storage_report_button(cls) -> None:
        """
        This method click on storage report button.
        """
        Common.click_link('storage-reports')

    @classmethod
    def disable_all_cards(cls) -> None:
        """
        This method set all dashboard card to be disabled (invisible).
        """
        cls.click_the_configure_button()
        assert cls.assert_dashboard_configure_panel_is_visible() is True
        Common.unset_toggle('system-information')
        Common.unset_toggle('help')
        Common.unset_toggle('cpu')
        Common.unset_toggle('memory')
        Common.unset_toggle('backup')
        Common.unset_toggle('storage')
        Common.unset_toggle('pool-tank')
        Common.unset_toggle('network')
        Common.unset_toggle('enp-1-s-0')
        Common.click_save_button()

        assert Common.assert_right_panel_header_is_not_visible('Dashboard Configure') is True

    @classmethod
    def disable_card(cls, card: str) -> None:
        """
        This method disable the given card.

        :param card: is the card toggle name.
        """
        cls.set_dashboard_card_by_state(card, False)

    @classmethod
    def enable_card(cls, card: str) -> None:
        """
        This method enable the given card:

        :param card: is the card toggle name
        """
        if card == 'sysinfo':
            card = 'system-information'
        if card == 'pool':
            card = 'pool-tank'
        if card == 'nic':
            card = 'enp-1-s-0'
        cls.set_dashboard_card_by_state(card, True)

    @classmethod
    def get_dashboard_card_name_by_position(cls, position: int) -> str:
        """
        This method returns the name dashboard card by name from given position.

        :param position: in the number of the position of the card.
        :return: the name dashboard card by name
        """
        assert WebUI.wait_until_visible(xpaths.common_xpaths.any_xpath(f'(//mat-card)[{position}]//h3')) is True
        card_header = WebUI.get_text(xpaths.common_xpaths.any_xpath(f'(//mat-card)[{position}]//h3'))
        return shared_config['DASHBOARD_CARDS'][card_header]

    @classmethod
    def get_dashboard_card_position(cls, name: str) -> int:
        """
        This method returns the position of the given dashboard card.

        :param name: name of the card.
        :return: the position of the dashboard card
        """
        pos = 1
        while pos < 10:
            if cls.get_dashboard_card_name_by_position(pos) == name:
                return pos
            else:
                pos += 1
        return 0

    @classmethod
    def get_system_information_uptime(cls) -> str:
        """
        This method get the System Information uptime value and returns it.

        :return: the System Information Uptime value.
        """
        assert WebUI.wait_until_visible(xpaths.dashboard.card_list_item('sysinfo', 4)) is True
        return WebUI.get_text(xpaths.dashboard.card_list_item('sysinfo', 4))

    @classmethod
    def is_cpu_card_visible(cls) -> bool:
        """
        This method returns True if the cpu card is visible otherwise it returns False.

        :return: True if the cpu card is visible otherwise it returns False.
        """
        return Common.is_card_visible('CPU')

    @classmethod
    def is_memory_card_visible(cls) -> bool:
        """
        This method returns True if the memory card is visible otherwise it returns False.

        :return: True if the memory card is visible otherwise it returns False.
        """
        return Common.is_card_visible('Memory')

    @classmethod
    def is_network_card_visible(cls) -> bool:
        """
        This method returns True if the network card is visible otherwise it returns False.

        :return: True if the network card is visible otherwise it returns False.
        """
        return Common.is_card_visible('Network')

    @classmethod
    def is_storage_card_visible(cls) -> bool:
        """
        This method returns True if the storage card is visible otherwise it returns False.

        :return: True if the storage card is visible otherwise it returns False.
        """
        return Common.is_card_visible('Storage')

    @classmethod
    def is_system_information_card_visible(cls) -> bool:
        """
        This method returns True if the system information card is visible otherwise it returns False.

        :return: True if the system information card is visible otherwise it returns False.
        """
        return Common.is_card_visible('System Information')

    @classmethod
    def is_truenas_help_card_visible(cls) -> bool:
        """
        This method returns True if the truenas help card is visible otherwise it returns False.

        :return: True if the truenas help card is visible otherwise it returns False.
        """
        return Common.is_card_visible('TrueNAS Help')

    @classmethod
    def move_card_a_to_card_b_position(cls, card_a: str, card_b: str) -> None:
        """
        This method move given card_a to the card_b position.

        :param card_a: name of the card to move
        :param card_b: name of the card to move card_a to
        """
        a_pos = cls.get_dashboard_card_position(card_a)
        b_pos = cls.get_dashboard_card_position(card_b)
        print(f'BEFORE SWAP: {card_a} - {a_pos} {card_b} - {b_pos}')
        if card_a != card_b:
            # Ensure the drag xpath and drop xpath are visible before moving the card
            assert WebUI.wait_until_visible(xpaths.dashboard.drag_card(card_a)) is True
            assert WebUI.wait_until_visible(xpaths.dashboard.drop_card(card_b)) is True
            WebUI.drag_and_drop(xpaths.dashboard.drag_card(card_a), xpaths.dashboard.drop_card(card_b))
            WebUI.delay(2)
            print(f'AFTER SWAP: {card_a} - {cls.get_dashboard_card_position(card_a)} {card_b} - {cls.get_dashboard_card_position(card_b)}')
        else:
            print("card_a can't match card_b")

    @classmethod
    def set_all_cards_visible(cls) -> None:
        """
        This method set all dashboard card to be visible.
        """
        cls.click_the_configure_button()
        assert cls.assert_dashboard_configure_panel_is_visible() is True
        Common.set_toggle('system-information')
        Common.set_toggle('help')
        Common.set_toggle('cpu')
        Common.set_toggle('memory')
        Common.set_toggle('backup')
        Common.set_toggle('storage')
        Common.set_toggle('pool-tank')
        Common.set_toggle('network')
        Common.set_toggle('enp-1-s-0')
        Common.click_save_button()

        assert Common.assert_right_panel_header_is_not_visible('Dashboard Configure') is True

    @classmethod
    def set_dashboard_card_by_state(cls, card: str, state: bool) -> None:
        """
        This method set the card toggle by the given state.

        :param card: is the card toggle name.
        :param state: is True to enable the toggle and False to disable it.
        """
        cls.click_the_configure_button()
        assert cls.assert_dashboard_configure_panel_is_visible()
        if state:
            Common.set_toggle_by_state(card, True)
        else:
            Common.set_toggle_by_state(card, False)
        assert Common.click_save_button_and_wait_for_right_panel() is True

    @classmethod
    def set_original_card_position(cls, card) -> None:
        """
        This method set all dashboard card to be visible.
        """
        card_order = ['sysinfo', 'help', 'cpu', 'memory', 'backup', 'storage', 'pool', 'network', 'nic']
        pos = card_order.index(card) + 1
        cls.enable_card(card)
        cls.click_the_reorder_button()
        cls.move_card_a_to_card_b_position(card, Dashboard.get_dashboard_card_name_by_position(pos))
        cls.click_the_save_reorder_button()
        assert Dashboard.assert_card_position(pos, card) is True

    @classmethod
    def set_all_cards_original_card_positions(cls) -> None:
        """
        This method set all dashboard card to be visible.
        """
        cls.set_original_card_position('sysinfo')
        cls.set_original_card_position('help')
        cls.set_original_card_position('cpu')
        cls.set_original_card_position('memory')
        cls.set_original_card_position('backup')
        cls.set_original_card_position('storage')
        cls.set_original_card_position('pool')
        cls.set_original_card_position('network')
        cls.set_original_card_position('nic')
