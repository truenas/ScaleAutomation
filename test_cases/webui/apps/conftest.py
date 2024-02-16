from keywords.webui.navigation import Navigation as NAV
from keywords.webui.apps import Apps
import pytest


@pytest.fixture(scope='class', autouse=True)
def navigate_to_apps():
    """
    This method navigates to the apps page and configures the apps pool if not configured.
    """
    # Ensure we are on the apps page.
    NAV.navigate_to_apps()
    Apps.configure_apps_pool()
    Apps.refresh_charts()
