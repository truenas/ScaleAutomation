import pytest

from helper.global_config import private_config
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


@pytest.fixture(scope='class', autouse=True)
def setup_class(rep):
    """
    This method creates all ssh connections needed for replication
    """

    # Setup SSH connections.
    Navigation.navigate_to_backup_credentials()
    SSHCON.assert_ssh_connection_exists(rep['connection-name'])
    API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
    API_PUT.enable_user_ssh_password(private_config['USERNAME'])
    API_POST.start_service('ssh')
    private_config['API_IP'] = private_config['REP_DEST_IP']
    API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
    API_PUT.enable_user_ssh_password(private_config['USERNAME'])
    API_POST.start_service('ssh')
    private_config['API_IP'] = private_config['IP']

    # Remove Snapshots if exists
    Navigation.navigate_to_data_protection()
    DP.delete_all_replication_tasks()
    DP.delete_all_periodic_snapshot_tasks()
