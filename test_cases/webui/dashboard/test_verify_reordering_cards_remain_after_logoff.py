import allure
import pytest
from helper.data_config import get_data_list
from helper.webui import WebUI
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard


@allure.tag("Dashboard")
@allure.epic("Dashboard")
@allure.feature("Dashboard-Reorder")
class Test_Verify_Reordering_Cards_Remain_After_Logoff:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        WebUI.refresh()
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        Dashboard.set_all_cards_visible()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        yield
        # reset the change
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', Dashboard.get_dashboard_card_name_by_position(1))
        Dashboard.move_card_a_to_card_b_position('help', Dashboard.get_dashboard_card_name_by_position(2))
        Dashboard.move_card_a_to_card_b_position('cpu', Dashboard.get_dashboard_card_name_by_position(3))
        Dashboard.click_the_save_reorder_button()

    @allure.tag("Update")
    @allure.story("Verify Card Reorder Remains After Re-Login")
    @pytest.mark.parametrize('user_data', get_data_list('user'))
    def on_the_dashboard_move_the_sysinfo_card_to_cpu_card_position_and_save(self, user_data):
        assert Dashboard.assert_dashboard_page_header_is_visible() is True
        assert Dashboard.assert_card_position(1, 'sysinfo') is True
        assert Dashboard.assert_card_position(3, 'cpu') is True
        WebUI.refresh()
        Dashboard.click_the_reorder_button()
        Dashboard.move_card_a_to_card_b_position('sysinfo', 'cpu')
        assert Dashboard.assert_card_position(3, 'sysinfo') is True
        assert Dashboard.assert_card_position(2, 'cpu') is True
        Dashboard.click_the_save_reorder_button()

        # logoff and login
        Common.logoff_truenas()
        Common.set_login_form(user_data['username'], user_data['password'])
        assert Dashboard.assert_dashboard_page_header_is_visible() is True

        # verify the system the sysinfo card to cpu card position
        assert Dashboard.assert_card_position(3, 'sysinfo') is True
        assert Dashboard.assert_card_position(2, 'cpu') is True
