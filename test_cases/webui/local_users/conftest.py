import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation


def pytest_sessionstart(session):
    Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])


@pytest.fixture(scope='class', autouse=True)
def navigate_to_():
    """
    This method starts all tests to navigate to the Data Protection page
    """
    # Ensure we are on the Data Protection page.
    Navigation.navigate_to_local_users()


@pytest.fixture(scope='class', autouse=True)
@pytest.mark.parametrize('users', get_data_list('local_users'), scope='class')
def setup_class(users):
    """
    This method clears any test users before test is run for a clean environment
    """
    # Setup clean environment.
    API_DELETE.delete_user(users['username'])
