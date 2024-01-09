import pytest
from helper.data_config import get_data_list
from helper.webui import WebUI
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard


class Test_Verify_Reordering_Cards_Remain_After_Logoff:
    @classmethod
    def setup_class(cls):
        WebUI.refresh()

    @classmethod
    def teardown_class(cls):
        # reset the change
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', Dashboard.get_dashboard_card_name_by_position(1))
        Dashboard.move_card_a_to_card_b_position('help', Dashboard.get_dashboard_card_name_by_position(2))
        Dashboard.move_card_a_to_card_b_position('cpu', Dashboard.get_dashboard_card_name_by_position(3))
        Dashboard.click_the_save_reorder_button()

    @staticmethod
    def on_the_dashboard_move_the_sysinfo_card_to_cpu_card_position_and_save():
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_card_position(1, 'sysinfo')
        assert Dashboard.assert_card_position(3, 'cpu')
        WebUI.refresh()
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', 'cpu')
        assert Dashboard.assert_card_position(3, 'sysinfo')
        assert Dashboard.assert_card_position(2, 'cpu')
        Dashboard.click_the_save_reorder_button()

    @staticmethod
    @pytest.mark.parametrize('user_data', get_data_list('user'))
    def then_logoff_and_login(user_data):
        Common.logoff_truenas()
        Common.set_login_form(user_data['username'], user_data['password'])
        assert Dashboard.assert_dashboard_page_header_is_visible() is True

    @staticmethod
    def and_verify_the_system_the_sysinfo_card_to_cpu_card_position():
        assert Dashboard.assert_card_position(3, 'sysinfo')
        assert Dashboard.assert_card_position(2, 'cpu')
