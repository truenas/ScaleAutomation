import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.replication import Replication as REP


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Local")
@pytest.mark.random_order(disabled=True)
@pytest.mark.parametrize('rep', get_data_list('replication')[:1], scope='class')
class Test_Create_Replicate_Task_Local:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, rep) -> None:
        """
        This method cleans the environment in preparation for running tests
        """
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["source"]}', True)
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["destination"]}', True)

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, rep) -> None:
        """
        This method cleans the environment after running tests
        """
        yield
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["source"]}', True)
        API_DELETE.delete_dataset(f'{rep["pool"]}/{rep["destination"]}', True)

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

        # Create Periodic Task
        response = API_POST.create_snapshot(f'{rep["pool"]}/{rep["source"]}', "rep-%Y-%m-%d_%H-%M").json()
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert DP.is_snapshot_visible(f'{rep["pool"]}/{rep["source"]}', response['snapshot_name']) is True
        assert COM.is_text_visible(f'{rep["pool"]}/{rep["destination"]}') is False

        # Create Replication Task
        NAV.navigate_to_data_protection()
        DP.click_add_replication_button()
        REP.set_source_location_on_same_box(f'{rep["pool"]}/{rep["source"]}')
        REP.set_destination_location_on_same_box(f'{rep["pool"]}/{rep["destination"]}')
        REP.set_custom_snapshots()
        COM.set_input_field('naming-schema', "rep-%Y-%m-%d_%H-%M")
        REP.set_task_name(rep['task-name'])
        COM.click_next_button()

        REP.set_run_once_button()
        REP.unset_read_only_destination_checkbox()
        REP.click_save_button_and_resolve_dialogs()

        # Verify Replication Task successful
        NAV.navigate_to_data_protection()
        assert REP.is_replication_task_visible(rep['task-name']) is True
        assert REP.get_replication_status(rep['task-name']) == rep['status']
        DP.click_snapshots_button()
        assert DP.is_snapshot_visible(f'{rep["pool"]}/{rep["destination"]}', response['snapshot_name']) is True
        assert COM.assert_file_exists('rep_one.txt', f'{rep["pool"]}/{rep["destination"]}') is True

    @allure.tag("Create")
    @allure.story("Create and Run Replication Task to Local Box")
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

        # Create Periodic Task
        response = API_POST.create_snapshot(f'{rep["pool"]}/{rep["source"]}', "rep-%Y-%m-%d_%H-%M").json()
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert DP.is_snapshot_visible(f'{rep["pool"]}/{rep["source"]}', response['snapshot_name']) is True
        assert COM.is_text_visible(f'secondary/{rep["destination"]}') is False

        # Create Replication Task
        NAV.navigate_to_data_protection()
        DP.click_add_replication_button()
        REP.set_source_location_on_same_box(f'{rep["pool"]}/{rep["source"]}')
        REP.set_destination_location_on_same_box(f'secondary/{rep["destination"]}')
        REP.set_custom_snapshots()
        COM.set_input_field('naming-schema', "rep-%Y-%m-%d_%H-%M")
        REP.set_task_name(rep['task-name'])
        COM.click_next_button()

        REP.set_run_once_button()
        REP.unset_read_only_destination_checkbox()
        REP.click_save_button_and_resolve_dialogs()

        # Verify Replication Task successful
        NAV.navigate_to_data_protection()
        assert REP.is_replication_task_visible(rep['task-name']) is True
        assert REP.get_replication_status(rep['task-name']) == rep['status']
        DP.click_snapshots_button()
        assert DP.is_snapshot_visible(f'secondary/{rep["destination"]}', response['snapshot_name']) is True
        assert COM.assert_file_exists('rep_one.txt', f'secondary/{rep["destination"]}') is True

        API_POST.export_pool('secondary', True)
