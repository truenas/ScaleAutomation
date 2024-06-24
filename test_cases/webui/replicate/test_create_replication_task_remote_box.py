import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.replication import Replication as REP
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Remote")
@pytest.mark.random_order(disabled=True)
@pytest.mark.parametrize('rep', get_data_list('replication')[2:4], scope='class')
class Test_Create_Replicate_Task_Remote:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, rep) -> None:
        """
        This method cleans the environment in preparation for running tests
        """
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["source"]}', True)
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["destination"]}', True)
        API_DELETE.delete_remote_dataset(f'{rep["pool"]}/{rep["source"]}', True)
        API_DELETE.delete_remote_dataset(f'{rep["pool"]}/{rep["destination"]}', True)

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, rep) -> None:
        """
        This method cleans the environment after running tests
        """
        yield
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["source"]}', True)
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["destination"]}', True)
        API_DELETE.delete_remote_dataset(f'{rep["pool"]}/{rep["source"]}', True)
        API_DELETE.delete_remote_dataset(f'{rep["pool"]}/{rep["destination"]}', True)
        API_DELETE.delete_ssh_connection(rep['connection-name'])
        API_DELETE.delete_ssh_keypairs(rep['connection-name'])

    @allure.tag("Create")
    @allure.story("Create and Run Replication Task to Remote Box")
    def test_create_and_run_replicate_task_remote_push(self, rep) -> None:
        """
        Summary: This test verifies a remote replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create Datasets Task (Source = local and Destination = remote)
        2. Verify SSH Connection exists, if not create it
        3. Add data for replication
        4. Create Periodic Snapshot
        5. Create Replication Task (Source = local and Destination = remote)
        6. Trigger Replication Task by Run Once and save
        7. Verify Replication Task is successful (Status = FINISHED, files replicated)
        """
        # Create Datasets
        API_POST.create_dataset(f'{rep["pool"]}/{rep["source"]}', box='LOCAL')
        API_POST.create_dataset(f'{rep["pool"]}/{rep["destination"]}', box='REMOTE')

        # Verify SSH Connection
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])

        # Add data
        COM.add_test_file('rep_one.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["destination"]}', private_config['REP_DEST_IP']) is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M')

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'{rep["pool"]}/{rep["destination"]}',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'LOCAL',
                                    'REMOTE')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_one.txt',
                                                          'REMOTE') is True

    @allure.tag("Create")
    @allure.story("Create and Run Replication Task to Remote Box")
    def test_create_and_run_replicate_task_remote_pull(self, rep) -> None:
        """
        Summary: This test verifies a remote replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create Datasets Task (Source = remote and Destination = local)
        2. Verify SSH Connection exists, if not create it
        3. Add data for replication
        4. Create Periodic Snapshot
        5. Create Replication Task (Source = remote and Destination = local)
        6. Trigger Replication Task by Run Once and save
        7. Verify Replication Task is successful (Status = FINISHED, files replicated)
        """
        # Create Datasets
        API_POST.create_dataset(f'{rep["pool"]}/{rep["source"]}', box='REMOTE')
        API_POST.create_dataset(f'{rep["pool"]}/{rep["destination"]}', box='LOCAL')

        # Verify SSH Connection
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])

        # Add data
        COM.add_test_file('rep_one.txt', f'{rep["pool"]}/{rep["source"]}', private_config['REP_DEST_IP'])
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["source"]}', private_config['REP_DEST_IP']) is True
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["destination"]}') is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'REMOTE',
                                                     'LOCAL')

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'{rep["pool"]}/{rep["destination"]}',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'REMOTE',
                                    'LOCAL')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_one.txt',
                                                          'LOCAL') is True

    @allure.tag("Create")
    @allure.story("Second Run Replication Task to Remote Box")
    def test_second_run_replicate_task_remote_push(self, rep) -> None:
        """
        Summary: This test verifies a remote replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create Datasets Task (Source = local and Destination = remote)
        2. Verify SSH Connection exists, if not create it
        3. Add data for replication
        4. Create Periodic Snapshot and Replication Task (Source = local and Destination = remote)
        5. Trigger Replication Task by Run Once and save
        6. Verify Replication Task is successful (Status = FINISHED, files replicated)
        7. Add Data and Trigger 2nd Replication Task by Run now
        8. Verify Replication Task is successful (Status = FINISHED, files replicated)
        """
        # Create Datasets
        API_POST.create_dataset(f'{rep["pool"]}/{rep["source"]}', box='LOCAL')
        API_POST.create_dataset(f'{rep["pool"]}/{rep["destination"]}', box='REMOTE')

        # Verify SSH Connection
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])

        # Add data
        COM.add_test_file('rep_one.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["destination"]}', private_config['REP_DEST_IP']) is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M')

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'{rep["pool"]}/{rep["destination"]}',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'LOCAL',
                                    'REMOTE')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_one.txt',
                                                          'REMOTE') is True

        # Add second data
        COM.add_test_file('rep_two.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_two.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_two.txt', f'{rep["pool"]}/{rep["destination"]}', private_config['REP_DEST_IP']) is False

        # Create second Periodic Task
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M')

        # Verify Replication Task successful
        NAV.navigate_to_data_protection()
        REP.click_run_now_replication_task_by_name(rep['task-name'])
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_two.txt',
                                                          'REMOTE') is True

    @allure.tag("Create")
    @allure.story("Second Run Replication Task to Remote Box")
    def test_second_run_replicate_task_remote_pull(self, rep) -> None:
        """
        Summary: This test verifies a remote replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create Datasets Task (Source = remote and Destination = local)
        2. Verify SSH Connection exists, if not create it
        3. Add data for replication
        4. Create Periodic Snapshot and Replication Task (Source = remote and Destination = local)
        5. Trigger Replication Task by Run Once and save
        6. Verify Replication Task is successful (Status = FINISHED, files replicated)
        7. Add Data and Trigger 2nd Replication Task by Run now
        8. Verify Replication Task is successful (Status = FINISHED, files replicated)
        """
        # Create Datasets
        API_POST.create_dataset(f'{rep["pool"]}/{rep["source"]}', box='REMOTE')
        API_POST.create_dataset(f'{rep["pool"]}/{rep["destination"]}', box='LOCAL')

        # Verify SSH Connection
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])

        # Add data
        COM.add_test_file('rep_one.txt', f'{rep["pool"]}/{rep["source"]}', private_config['REP_DEST_IP'])
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["source"]}', private_config['REP_DEST_IP']) is True
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["destination"]}') is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'REMOTE',
                                                     'LOCAL')

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'{rep["pool"]}/{rep["destination"]}',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'REMOTE',
                                    'LOCAL')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_one.txt',
                                                          'LOCAL') is True

        # Add second data
        COM.add_test_file('rep_two.txt', f'{rep["pool"]}/{rep["source"]}', private_config['REP_DEST_IP'])
        assert COM.assert_file_exists('rep_two.txt', f'{rep["pool"]}/{rep["source"]}', private_config['REP_DEST_IP']) is True
        assert COM.assert_file_exists('rep_two.txt', f'{rep["pool"]}/{rep["destination"]}') is False

        # Create second Periodic Task
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'REMOTE',
                                                     'LOCAL')

        # Verify Replication Task successful
        NAV.navigate_to_data_protection()
        REP.click_run_now_replication_task_by_name(rep['task-name'])
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_two.txt',
                                                          'LOCAL') is True
