import pytest
from keywords.webui.login_Invalid_credentials import Login_Invalid_Credentials as LIC
from helper.data_config import get_data_list


@pytest.mark.parametrize('user_data', get_data_list('invalid_creds'))
class Test_Login_Invalid_Credentials:
    @staticmethod
    def test_login_invalid_credentials(user_data):
        LIC.set_login_form_with_invalid_credentials(user_data['username'], user_data['password'])
