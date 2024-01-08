from keywords.webui.dashboard import Dashboard
from helper.webui import WebUI


class Test_Verify_A_Dashboard_Card_Can_Be_Reorder:
    @classmethod
    def teardown_class(cls):
        # reset the change
        WebUI.refresh()
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', Dashboard.get_dashboard_widget_name_by_position(1))
        Dashboard.click_the_save_reorder_button()

    @staticmethod
    def on_the_dashboard_move_the_system_information_card_to_truenas_help_card_position():
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_card_position(1, 'sysinfo')
        assert Dashboard.assert_card_position(2, 'help')
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', 'help')
        Dashboard.click_the_save_reorder_button()

    @staticmethod
    def verify_the_system_information_card_position():
        assert Dashboard.assert_card_position(2, 'sysinfo')
