import pytest
from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard():
    # Ensure we are on the dashboard.
    Navigation.navigate_to_dashboard()
    assert Dashboard.assert_dashboard_page_header_is_visible()
