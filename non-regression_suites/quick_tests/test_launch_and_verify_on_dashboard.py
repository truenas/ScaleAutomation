import pytest
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation as NAV
from helper.data_config import get_data_list


class test_launch_and_verify_on_dashboard:

    @staticmethod
    def verify_we_are_on_the_dashboard(user_data):
        NAV.navigate_to_dashboard()
        assert Common.assert_page_header('Dashboard')
