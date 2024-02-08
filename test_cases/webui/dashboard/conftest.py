import pytest
from helper.global_config import private_config
from helper.webui import WebUI


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard():
    # Ensure we are on the dashboard.
    ip = private_config['IP']
    WebUI.get(f'http://{ip}/ui/dashboard')
