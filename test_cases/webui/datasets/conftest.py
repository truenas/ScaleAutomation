import pytest
from helper.global_config import private_config
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.ssh.common import Common_SSH
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard():
    # Ensure we are on the dashboard.
    Navigation.navigate_to_dashboard()
    assert Dashboard.assert_dashboard_page_header_is_visible()
