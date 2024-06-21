import pytest

from helper.global_config import private_config
from keywords.api.post import API_POST
from keywords.api.put import API_PUT


@pytest.fixture(scope='class', autouse=True)
def setup_class():
    """
    This method creates all ssh connections needed for replication
    """
    API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
    API_PUT.enable_user_ssh_password(private_config['USERNAME'])
    private_config['API_IP'] = private_config['REP_DEST_IP']
    API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
    API_PUT.enable_user_ssh_password(private_config['USERNAME'])
    private_config['API_IP'] = private_config['IP']
    API_POST.start_service('ssh')
