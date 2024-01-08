import pytest
from helper.global_config import private_config
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation


def pytest_sessionstart(session):
    Common.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard():
    # Ensure we are on the dashboard.
    Navigation.navigate_to_dashboard()
