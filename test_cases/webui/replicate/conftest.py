import pytest

import xpaths
from helper.data_config import get_data_list
from helper.global_config import private_config
from helper.webui import WebUI
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation
from keywords.webui.replication import Replication
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


@pytest.fixture(scope='class', autouse=True)
def navigate_to_():
    """
    This method starts all tests to navigate to the Data Protection page
    """
    # Ensure we are on the Data Protection page.
    Navigation.navigate_to_data_protection()


@pytest.fixture(scope='class', autouse=True)
@pytest.mark.parametrize('rep', get_data_list('replication'), scope='class')
def setup_class(rep):
    """
    This method creates all ssh connections needed for replication
    """
    # Setup Datasets.
    DATASET.create_dataset_by_api(rep['source'])
    DATASET.create_dataset_by_api(rep['destination'])
    DATASET.create_remote_dataset_by_api(rep['source'])
    DATASET.create_remote_dataset_by_api(rep['destination'])

    # Setup SSH connections.
    Navigation.navigate_to_backup_credentials()
    SSHCON.assert_ssh_connection_exists(rep['connection-name'])

    # Remove Snapshots if exists
    DP.delete_all_periodic_snapshot_tasks()
    DP.delete_all_snapshots()
    Navigation.navigate_to_data_protection()


@pytest.fixture(scope='class', autouse=True)
def teardown_class():
    yield
    WebUI.switch_to_window_index(0)
    if COM.is_visible(xpaths.common_xpaths.button_field('log-in')):
        COM.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
