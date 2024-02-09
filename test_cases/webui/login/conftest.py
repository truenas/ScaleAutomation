import pytest

from helper.global_config import private_config
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    NAV.navigate_to_dashboard()
    COM.logoff_truenas()


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    yield
    COM.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])