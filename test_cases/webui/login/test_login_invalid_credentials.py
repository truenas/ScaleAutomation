import pytest
from keywords.webui.common import Common as COM
from keywords.webui.login_Invalid_credentials import Login_Invalid_Credentials as LIC
from helper.data_config import get_data_list
from helper.global_config import private_config


@pytest.mark.parametrize('user_data', get_data_list('invalid_creds'))
def test_login_invalid_credentials(user_data):
    COM.navigate_to_login_screen(private_config['IP'])
    LIC.set_login_form_with_invalid_credentials(user_data['username'], user_data['password'])
