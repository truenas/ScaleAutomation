import pytest
from helper.global_config import private_config
from keywords.api.put import API_PUT
from keywords.ssh.common import Common_SSH
from keywords.webui.common import Common
from keywords.webui.dashboard import Dashboard
from keywords.webui.navigation import Navigation


def pytest_sessionstart(session):
    # Setup SSH, user groups and sudo commands with no password
    Common_SSH.set_host_ssh_key_and_enable_ssh_on_the_nas(private_config['USERNAME'])
    API_PUT.set_user_groups(private_config['USERNAME'], ['root', 'builtin_administrators'])
    API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])


@pytest.fixture(scope='class', autouse=True)
def navigate_to_dashboard():
    # Ensure we are on the dashboard.
    Navigation.navigate_to_dashboard()
    assert Dashboard.assert_dashboard_page_header_is_visible()
