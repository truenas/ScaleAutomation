import allure
import pytest

from helper.data_config import get_data_list
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
@pytest.mark.parametrize('rep', get_data_list('replication')[:2], scope='class')
class Test_Create_Replicate_Task_Same_Box:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, rep) -> None:
        """
        This method sets up each test to start with test replication tasks deleted
        """
        API_POST.create_dataset(rep['source'])
        API_POST.create_dataset(rep['destination'])
        API_POST.delete_all_dataset_snapshots(rep['source'])
        API_POST.delete_all_dataset_snapshots(rep['destination'])
        NAV.navigate_to_data_protection()
        if REP.is_replication_task_visible(rep['task-name']) is True:
            REP.delete_replication_task_by_name(rep['task-name'])

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, rep) -> None:
        """
        This test removes the replicate task
        """
        yield
        # reset the change
        NAV.navigate_to_data_protection()
        DP.delete_all_periodic_snapshot_tasks()
        REP.delete_replication_task_by_name(rep['task-name'])
        API_POST.delete_all_dataset_snapshots(rep['source'])
        API_POST.delete_all_dataset_snapshots(rep['destination'])
        API_DELETE.delete_dataset(rep['source'])
        API_DELETE.delete_dataset(rep['destination'])

    @allure.tag("Create")
    @allure.story("Setup and Run Replication Task to Local Box")
    def test_setup_and_run_replicate_task(self, rep) -> None:
        """
        Summary: This test verifies a local replicate task can be created, "Run Now", and task is successful

        Test Steps:
        1. Create Replication Task (Source and Destination = local)
        2. Trigger Task with "Run Now" button
        3. Verify Replication Task is successful (Status = FINISHED)
        """
        DP.click_add_replication_button()
        REP.set_source_location_on_same_box(rep['source'])
        REP.set_destination_location_on_same_box(rep['destination'])
        REP.set_custom_snapshots()
        REP.set_task_name(rep['task-name'])
        COM.click_next_button()

        REP.set_run_once_button()
        REP.unset_read_only_destination_checkbox()
        REP.click_save_button_and_resolve_dialogs()
        assert REP.is_replication_task_visible(rep['task-name']) is True

        REP.click_run_now_replication_task_by_name(rep['task-name'])
        assert REP.get_replication_status(rep['task-name']) == rep['status']
