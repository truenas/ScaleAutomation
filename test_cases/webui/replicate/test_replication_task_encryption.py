import allure
import pytest

from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATA
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.replication import Replication as REP
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Encryption")
@pytest.mark.random_order(disabled=True)
class Test_Create_Replicate_Task_Encryption:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method cleans the environment in preparation for running tests
        """
        API_DELETE.delete_dataset('tank/source', True)
        API_DELETE.delete_remote_dataset('tank/destination', True)
        # Create Datasets
        API_POST.create_encrypted_dataset('tank/source')
        API_POST.create_dataset('tank/destination', box='REMOTE')

        # Add source test files
        COM.add_test_file('test_file.txt', 'tank/source')
        assert COM.assert_file_exists('test_file.txt', 'tank/source') is True

        # Verify destination test file do not exist
        assert COM.assert_file_exists('test_file.txt', 'tank/destination', private_config['REP_DEST_IP']) is False

        # Verify SSH Connection
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists('admin-other')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self) -> None:
        """
        This method cleans the environment after running tests
        """
        yield
        API_DELETE.delete_dataset('tank/source', True)
        API_DELETE.delete_remote_dataset('tank/destination', True)
        API_DELETE.delete_ssh_connection('admin-other')
        API_DELETE.delete_ssh_keypairs('admin-other')


    @allure.tag("Create")
    @allure.story("Run Replication Task from Encrypted to Unencrypted")
    def test_run_replicate_task_from_encrypted_to_unencrypted_remote(self) -> None:
        """
        Summary: This test verifies a replicate task runs from encrypted dataset to unencrypted dataset

        Test Steps:
        1. Create Periodic Snapshot
        2. Create Replication Task (Include Dataset Properties = False)
        3. Trigger Replication Task
        4. Verify destination dataset file exists
        """

        # Create Periodic Snapshot
        NAV.navigate_to_data_protection()
        REP.create_periodic_snapshot('tank/source',
                                     'tank/destination',
                                     'rep-%Y-%m-%d_%H-%M',
                                     'LOCAL',
                                     'REMOTE')

        # Create Replication Task
        replication_options = {
            "NAME": "rep-enc-non",
            "TRANSPORT": "transport-ssh",
            "SOURCE": "tank/source",
            "INCLUDE_PROPERTIES": False,
            "SSH_CONNECTION": "admin-other",
            "DESTINATION": "tank/destination/enc-non",
            "READ_ONLY_POLICY": "readonly-ignore",
            "MATCHING_SCHEMA": True,
            "NAMING_SCHEMA": "rep-%Y-%m-%d_%H-%M",
            "RUN_AUTOMATICALLY": False,
            }

        REP.create_advanced_replication_task_local(replication_options)
        REP.click_run_now_replication_task_by_name('rep-enc-non')

        # Verify destination dataset file exists
        assert COM.assert_file_exists('test_file.txt', 'tank/destination/enc-non', private_config['REP_DEST_IP']) is True
        REP.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()
        DATA.expand_all_datasets()
        DATA.select_dataset('enc-non')
        assert DATA.is_locked('enc-non') is False
        REP.close_destination_box()
