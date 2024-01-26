import pytest
from keywords.webui.common import Common as COM
from keywords.webui.login_Invalid_credentials import Login_Invalid_Credentials as LIC
from helper.data_config import get_data_list
from helper.global_config import private_config


@pytest.mark.parametrize('user_data', get_data_list('invalid_creds'))
class Test_Login_Invalid_Credentials:
    @classmethod
    def setup_class(cls):
        COM.logoff_truenas()

    @classmethod
    def teardown_class(cls):
        COM.set_login_form(private_config['USERNAME'], private_config['PASSWORD'])

    @staticmethod
    def test_login_invalid_credentials(user_data):
        LIC.set_login_form_with_invalid_credentials(user_data['username'], user_data['password'])
