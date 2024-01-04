import pytest
from keywords.webui.common import Common
from helper.data_config import get_data_list


@pytest.mark.parametrize('user_data', get_data_list('user'), scope='class')
class Test_Login_And_Logoff:
    @staticmethod
    def go_to_truenas_login_and_login(user_data):
        Common.login_to_truenas(user_data['username'], user_data['password'])

    @staticmethod
    def verify_we_are_on_the_dashboard(user_data):
        assert Common.assert_page_header('Dashboard')

    @staticmethod
    def verify_logoff_truenas_works(user_data):
        Common.logoff_truenas()
