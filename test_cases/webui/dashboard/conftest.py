import pytest
from helper.webui import WebUI
from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard_and_refresh_browser():
    """
    Ensure the browser is refreshed after each test in case the test fails
    in a state where it will affect other tests.
    """
    yield
    Navigation.navigate_to_dashboard()
    WebUI.refresh()
    Dashboard.assert_dashboard_page_header_is_visible()
