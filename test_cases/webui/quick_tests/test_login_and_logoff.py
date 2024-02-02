import pytest
from keywords.webui.common import Common
from helper.data_config import get_data_list


@pytest.mark.parametrize('user_data', get_data_list('user'), scope='class')
class test_launch_and_verify_on_dashboard:

    @staticmethod
    def verify_we_are_on_the_dashboard(user_data):
        assert Common.assert_page_header('Dashboard')
