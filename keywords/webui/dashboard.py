import xpaths
from helper.global_config import shared_config
from helper.webui import WebUI
from keywords.webui.common import Common


class Dashboard:
    @classmethod
    def assert_card_position(cls, position: int, field: str) -> bool:
        card_name = cls.get_dashboard_widget_name_by_position(position)
        print(card_name)
        return True if field == card_name else False

    @classmethod
    def assert_dashboard_configure_panel_is_visible(cls):
        """
        This method returns True if the dashboard configure panel is visible otherwise it returns False.

        :return: True if the dashboard configure panel is visible otherwise it returns False.
        """
        return Common.assert_right_panel_header('Dashboard Configure')

    @classmethod
    def assert_dashboard_page_header_is_visible(cls):
        """
        This method returns True if the dashboard page header is visible otherwise it returns False.

        :return: True if the dashboard page header is visible otherwise it returns False.
        """
        return Common.assert_page_header('Dashboard')

    @classmethod
    def assert_new_tab_url(cls, link: str):
        """
        This method returns True or False whether the new tab opened to the right link.

        :param link: is the url link to click on.
        :return: True if the new tab opened to the right link, otherwise it returns False.
        """
        initial_tab = WebUI.current_window_handle()
        if link == "https://www.truenas.com/community/":
            Common.click_on_element(xpaths.dashboard.truenas_help_card_link("https://www.ixsystems.com/community/"))
        else:
            Common.click_on_element(xpaths.dashboard.truenas_help_card_link(link))
        WebUI.wait_until_number_of_windows_to_be(2)

        initial_index = WebUI.window_handles().index(initial_tab)
        next_tab = initial_index + 1

        WebUI.switch_to_window_index(next_tab)

        url_exists = True if WebUI.current_url() == link else False

        WebUI.close_window()
        WebUI.switch_to_window_index(initial_index)
        WebUI.wait_until_number_of_windows_to_be(1)

        return url_exists

    @classmethod
    def assert_the_truenas_help_documentation_link(cls):
        """
        This method returns True or False whether TrueNAS Help documentation link opened to the right link.

        :return: True if the documentation link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://www.truenas.com/docs/')

    @classmethod
    def assert_the_truenas_help_ixsystems_inc_link(cls):
        """
        This method returns True or False whether TrueNAS Help iXsystems inc link opened to the right link.

        :return: True if the iXsystems inc link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://www.ixsystems.com/')

    @classmethod
    def assert_the_truenas_help_open_source_link(cls):
        """
        This method returns True or False whether TrueNAS Help open source link opened to the right link.

        :return: True if the open source link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://github.com/truenas/')

    @classmethod
    def assert_the_truenas_help_truenas_community_forums_link(cls):
        """
        This method returns True or False whether TrueNAS Help community forums link opened to the right link.

        :return: True if the community forums link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://www.truenas.com/community/')

    @classmethod
    def assert_the_truenas_help_truenas_newsletter_link(cls):
        """
        This method returns True or False whether TrueNAS Help TrueNAS newsletter link opened to the right link.

        :return: True if the TrueNAS newsletter link opened to the right link, otherwise it returns False.
        """
        return cls.assert_new_tab_url('https://www.truenas.com/newsletter/')

    @classmethod
    def click_check_update_button(cls):
        """
        This method click on the system information Check Updates or Updates Available button.
        """
        Common.click_button('widget-sysinfo-update')

    @classmethod
    def click_the_cancel_reorder_button(cls):
        """
        This method click on the cancel reorder button.
        """
        Common.click_button('cancel-reorder')

    @classmethod
    def click_the_configure_button(cls):
        """
        This method click on the Configure button on the dashboard.
        """
        Common.click_button('configure-dashboard')

    @classmethod
    def click_the_cpu_report_button(cls):
        """
        This method click on CPU report button.
        """
        Common.click_link('cpu-reports')

    @classmethod
    def click_the_memory_report_button(cls):
        """
        This method click on memory report button.
        """
        Common.click_button('memory-go-to-reports')

    @classmethod
    def click_the_network_report_button(cls):
        """
        This method click on Network report button.
        """
        Common.click_link('network-reports')

    @classmethod
    def click_the_reorder_button(cls):
        """
        This method click on the Dashboard Reorder button.
        """
        Common.click_button('start-reorder')

    @classmethod
    def click_the_save_reorder_button(cls):
        """
        This method click on the save reorder button.
        """
        Common.click_button('save-new-order')

    @classmethod
    def click_the_storage_report_button(cls):
        """
        This method click on storage report button.
        """
        Common.click_link('storage-reports')

    @classmethod
    def disable_card(cls, card: str):
        """
        This method disable the given card.

        :param card: is the card toggle name.
        """
        cls.set_dashboard_card_by_state(card, False)

    @classmethod
    def enable_card(cls, card: str):
        """
        This method enable the given card:

        :param card: is the card toggle name
        """
        cls.set_dashboard_card_by_state(card, True)

    @classmethod
    def set_dashboard_card_by_state(cls, card: str, state: bool):
        """
        This method set the card toggle by the given state.

        :param card: is the card toggle name.
        :param state: is True to enable the toggle and False to disable it.
        """
        cls.click_the_configure_button()
        assert cls.assert_dashboard_configure_panel_is_visible() is True
        if state:
            Common.set_toggle(card)
        else:
            Common.unset_toggle(card)
        Common.click_save_button()

    @classmethod
    def is_cpu_card_visible(cls):
        """
        This method returns True if the cpu card is visible otherwise it returns False.

        :return: True if the cpu card is visible otherwise it returns False.
        """
        return Common.is_card_visible('CPU')

    @classmethod
    def is_memory_card_visible(cls):
        """
        This method returns True if the memory card is visible otherwise it returns False.

        :return: True if the memory card is visible otherwise it returns False.
        """
        return Common.is_card_visible('Memory')

    @classmethod
    def is_network_card_visible(cls):
        """
        This method returns True if the network card is visible otherwise it returns False.

        :return: True if the network card is visible otherwise it returns False.
        """
        return Common.is_card_visible('Network')

    @classmethod
    def is_storage_card_visible(cls):
        """
        This method returns True if the storage card is visible otherwise it returns False.

        :return: True if the storage card is visible otherwise it returns False.
        """
        return Common.is_card_visible('Storage')

    @classmethod
    def is_system_information_card_visible(cls):
        """
        This method returns True if the system information card is visible otherwise it returns False.

        :return: True if the system information card is visible otherwise it returns False.
        """
        return Common.is_card_visible('System Information')

    @classmethod
    def is_truenas_help_card_visible(cls):
        """
        This method returns True if the truenas help card is visible otherwise it returns False.

        :return: True if the truenas help card is visible otherwise it returns False.
        """
        return Common.is_card_visible('TrueNAS Help')

    @classmethod
    def get_dashboard_widget_name_by_position(cls, position: int) -> str:
        card_header = WebUI.get_text(xpaths.common_xpaths.any_xpath(f'(//mat-card)[{position}]//h3'))
        return shared_config['DASHBOARD_CARDS'][card_header]

    @classmethod
    def move_card_a_to_card_b_position_by_state(cls, card_a: str, card_b: str):
        if card_a != card_b:
            WebUI.drag_and_drop(xpaths.dashboard.drag_card(card_a), xpaths.dashboard.drop_card(card_b))
            WebUI.delay(0.4)
        else:
            print("card_a can't match card_b")

    @classmethod
    def move_card_a_to_card_b_position(cls, card_a: str, card_b: str):
        cls.move_card_a_to_card_b_position_by_state(card_a, card_b)

    @classmethod
    def set_all_cards_visible(cls):
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
