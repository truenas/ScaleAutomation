from keywords.webui.navigation import Navigation
import pytest


@pytest.fixture(scope='class', autouse=True)
def navigate_to_apps():
    """
    This method starts all tests to navigate to the Apps page
    """
    # Ensure we are on the apps page.
    Navigation.navigate_to_apps()
