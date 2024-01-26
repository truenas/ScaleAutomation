import pytest

from helper.global_config import private_config
from keywords.webui.common import Common


def pytest_sessionfinish():
    Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    """

    """
    Common.logoff_truenas()
