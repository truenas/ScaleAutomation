import allure
import pytest

from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.replication import Replication as REP


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Local")
@pytest.mark.random_order(disabled=True)
@pytest.mark.parametrize('rep', get_data_list('replication')[:2], scope='class')
class Test_Create_Replicate_Task_Local:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, rep) -> None:
        """
        This method cleans the environment in preparation for running tests
        """
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["source"]}', True)
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["destination"]}', True)
        API_POST.export_pool('secondary', True)

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, rep) -> None:
        """
        This method cleans the environment after running tests
        """
        yield
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["source"]}', True)
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["destination"]}', True)
        API_POST.export_pool('secondary', True)

    @allure.tag("Create")
    @allure.story("Create and Run Replication Task to Local Box")
    def test_create_and_run_replicate_task_local(self, rep) -> None:
        """
        Summary: This test verifies a local replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create Datasets Task (Source and Destination = local)
        2. Add data for replication
        3. Create Periodic Snapshot
        4. Create Replication Task (Source and Destination = local)
        5. Trigger Replication Task by Run Once and save
        6. Verify Replication Task is successful (Status = FINISHED, files replicated)
        """
        # Create Datasets
        API_POST.create_dataset(f'{rep["pool"]}/{rep["source"]}', box='LOCAL')
        API_POST.create_dataset(f'{rep["pool"]}/{rep["destination"]}', box='LOCAL')

        # Add data
        COM.add_test_file('rep_one.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["destination"]}') is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'LOCAL',
                                                     'LOCAL')

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'{rep["pool"]}/{rep["destination"]}',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'LOCAL',
                                    'LOCAL')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_one.txt',
                                                          'LOCAL') is True

    @allure.tag("Create")
    @allure.story("Create and Run Replication Task to Different Pool on Local Box")
    def test_create_and_run_replicate_task_different_pool_local(self, rep) -> None:
        """
        Summary: This test verifies a local replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create secondary pool (local)
        2. Create Datasets Task (Source = tank and Destination = secondary)
        3. Add data for replication
        4. Create Periodic Snapshot
        5. Create Replication Task (Source and Destination = local)
        6. Trigger Replication Task by Run Once and save
        7. Verify Replication Task is successful (Status = FINISHED, files replicated)
        """
        # Create Datasets
        disks = API_POST.get_unused_disks()
        print(f'@@@ DISKS: {disks}')
        API_POST.create_pool('secondary', 'MIRROR', disks[:2])

        # Create Datasets
        API_POST.create_dataset(f'{rep["pool"]}/{rep["source"]}', box='LOCAL')
        API_POST.create_dataset(f'secondary/{rep["destination"]}', box='LOCAL')

        # Add data
        COM.add_test_file('rep_one.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_one.txt', f'secondary/{rep["destination"]}') is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'secondary/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'LOCAL',
                                                     'LOCAL')

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'secondary/{rep["destination"]}',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'LOCAL',
                                    'LOCAL')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'secondary/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_one.txt',
                                                          'LOCAL') is True

    @allure.tag("Create")
    @allure.story("Second Run Replication Task to Local Box")
    def test_second_run_replicate_task_local(self, rep) -> None:
        """
        Summary: This test verifies a local replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create Datasets Task (Source and Destination = local)
        2. Add data for replication
        3. Create Periodic Snapshot and Replication Task (Source and Destination = local)
        4. Trigger Replication Task by Run Once and save
        5. Verify Replication Task is successful (Status = FINISHED, files replicated)
        6. Add Data and Trigger 2nd Replication Task by Run now
        7. Verify Replication Task is successful (Status = FINISHED, files replicated)
        """
        # Create Datasets
        API_POST.create_dataset(f'{rep["pool"]}/{rep["source"]}', box='LOCAL')
        API_POST.create_dataset(f'{rep["pool"]}/{rep["destination"]}', box='LOCAL')

        # Add data
        COM.add_test_file('rep_one.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["destination"]}') is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'LOCAL',
                                                     'LOCAL')

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'{rep["pool"]}/{rep["destination"]}',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'LOCAL',
                                    'LOCAL')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_one.txt',
                                                          'LOCAL') is True

        # Add data
        COM.add_test_file('rep_two.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_two.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_two.txt', f'{rep["pool"]}/{rep["destination"]}') is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'{rep["pool"]}/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'LOCAL',
                                                     'LOCAL')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'{rep["pool"]}/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_two.txt',
                                                          'LOCAL') is True

    @allure.tag("Create")
    @allure.story("Second Run Replication Task to Different Pool on Local Box")
    def test_second_run_replicate_task_different_pool_local(self, rep) -> None:
        """
        Summary: This test verifies a local replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create secondary pool (local)
        2. Create Datasets Task (Source = tank and Destination = secondary)
        3. Add data for replication
        4. Create Periodic Snapshot and Replication Task (Source and Destination = local)
        5. Trigger Replication Task by Run Once and save
        6. Verify Replication Task is successful (Status = FINISHED, files replicated)
        7. Add Data and Trigger 2nd Replication Task by Run now
        8. Verify Replication Task is successful (Status = FINISHED, files replicated)
        """
        # Create Datasets
        disks = API_POST.get_unused_disks()
        print(f'@@@ DISKS: {disks}')
        API_POST.create_pool('secondary', 'MIRROR', disks[:2])

        # Create Datasets
        API_POST.create_dataset(f'{rep["pool"]}/{rep["source"]}', box='LOCAL')
        API_POST.create_dataset(f'secondary/{rep["destination"]}', box='LOCAL')

        # Add data
        COM.add_test_file('rep_one.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_one.txt', f'secondary/{rep["destination"]}') is False

        # Create Periodic Snapshot
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'secondary/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'LOCAL',
                                                     'LOCAL')

        # Create Replication Task
        REP.create_replication_task(f'{rep["pool"]}/{rep["source"]}',
                                    f'secondary/{rep["destination"]}',
                                    rep['connection-name'],
                                    'rep-%Y-%m-%d_%H-%M',
                                    rep['task-name'],
                                    'LOCAL',
                                    'LOCAL')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'secondary/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_one.txt',
                                                          'LOCAL') is True

        # Add data
        COM.add_test_file('rep_two.txt', f'{rep["pool"]}/{rep["source"]}')
        assert COM.assert_file_exists('rep_two.txt', f'{rep["pool"]}/{rep["source"]}') is True
        assert COM.assert_file_exists('rep_two.txt', f'secondary/{rep["destination"]}') is False

        # Create Periodic Task
        snapshot_name = REP.create_periodic_snapshot(f'{rep["pool"]}/{rep["source"]}',
                                                     f'secondary/{rep["destination"]}',
                                                     'rep-%Y-%m-%d_%H-%M',
                                                     'LOCAL',
                                                     'LOCAL')

        # Verify Replication Task successful
        assert REP.is_destination_snapshot_and_file_exist(rep['task-name'],
                                                          f'secondary/{rep["destination"]}',
                                                          snapshot_name,
                                                          'rep_two.txt',
                                                          'LOCAL') is True
