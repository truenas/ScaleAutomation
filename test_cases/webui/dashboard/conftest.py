import pytest
from keywords.webui.navigation import Navigation


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard():
    """
    Navigate to the dashboard
    """
    yield
    Navigation.navigate_to_dashboard()

