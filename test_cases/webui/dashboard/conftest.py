import pytest
from helper.global_config import private_config
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard():
    # Ensure we are on the dashboard.
    Navigation.navigate_to_dashboard()
    Common.assert_progress_spinner_not_visible()