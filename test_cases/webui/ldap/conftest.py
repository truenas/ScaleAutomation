from helper.global_config import private_config
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation
import pytest


def pytest_sessionstart(session):
    Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])


@pytest.fixture(scope='class', autouse=True)
def navigate_to_():
    """
    This method starts all tests to navigate to the Directory Services page
    """
    # Ensure we are on the directory services page.
    Navigation.navigate_to_directory_services()
