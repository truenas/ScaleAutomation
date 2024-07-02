import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import shared_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.replication import Replication as REP
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Options")
@pytest.mark.random_order(disabled=True)
@pytest.mark.parametrize('rep', get_data_list('replication')[2:3], scope='class')
class Test_Replicate_Task_Errors:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method cleans the environment in preparation for running tests
        """
        API_DELETE.delete_dataset('tank/source', True)
        API_DELETE.delete_remote_dataset('tank/destination', True)
        # Create Datasets
        API_POST.create_dataset('tank/source', box='LOCAL')
        API_POST.create_dataset('tank/destination', box='REMOTE')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self) -> None:
        """
        This method cleans the environment after running tests
        """
        yield
        API_DELETE.delete_dataset('tank/source', True)
        API_DELETE.delete_remote_dataset('tank/destination', True)

    @allure.tag("Read")
    @allure.story("Download Replication Task Log")
    def test_replicate_task_error_failed_destination(self, rep) -> None:
        """
        Summary: This test verifies a failed alert of a replicate task can be produced

        Test Steps:
        1. Verify SSH Connection exists, if not create it
        2. Create Replication Task (Source = local and Destination = remote/bad directory)
        3. Verify Replication Task error (Alerts / Replication Task)
        """
        # Verify SSH Connection
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'foo/reptask',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'LOCAL',
                                    'REMOTE')

        # Verify Replication Task Error
        NAV.navigate_to_data_protection()
        REP.click_run_now_button(rep['task-name'])
        assert COM.is_dialog_visible('FAILED', 1, shared_config['LONG_WAIT']) is True
        error_message = "cannot open 'foo': dataset does not exist cannot receive new filesystem stream: unable to restore to destination."
        assert COM.assert_error_dialog_message(error_message) is True
        COM.click_error_dialog_close_button()
        COM.click_button('alerts-indicator')
        assert COM.assert_alert_message(error_message) is True
        COM.click_button('close-panel')
