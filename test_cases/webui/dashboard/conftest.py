import pytest
from helper.global_config import private_config
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard():
    # Ensure we are on the dashboard.
    Navigation.navigate_to_dashboard()


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    # Ensure we are logged in as the correct user.
    Common.verify_logged_in_user_correct(private_config['USERNAME'], private_config['PASSWORD'])
