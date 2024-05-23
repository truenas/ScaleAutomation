import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.api.post import API_POST
from keywords.ssh.common import Common_SSH as SSHCOM
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.datasets import Datasets as DATASET
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.replication import Replication as REP
from keywords.webui.snapshots import Snapshots as SNAP
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Remote")
@pytest.mark.parametrize('rep', get_data_list('replication')[2:], scope='class')
class Test_Create_Replicate_Task_Different_Box:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, rep, clean_remote_box) -> None:
        """
        This method sets up each test to start with test replication tasks deleted
        """
        API_POST.create_dataset(rep['source'])
        API_POST.create_dataset(rep['destination'])
        API_POST.delete_all_dataset_snapshots(rep['source'])
        API_POST.delete_all_dataset_snapshots(rep['destination'])
        API_POST.create_remote_dataset(rep['source'])
        API_POST.create_remote_dataset(rep['destination'])
        API_POST.delete_all_remote_dataset_snapshots(rep['source'])
        API_POST.delete_all_remote_dataset_snapshots(rep['destination'])
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])
        NAV.navigate_to_data_protection()
        if REP.is_replication_task_visible(rep['task-name']) is True:
            REP.delete_replication_task_by_name(rep['task-name'])

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, clean_remote_box) -> None:
        """
        This method removes the replicate task, snapshots, and cleans up the system
        """
        # reset the change
        yield
        # clean source box
        NAV.navigate_to_datasets()
        DATASET.delete_dataset("tank", "receive")
        DATASET.delete_dataset("tank", "replicate")

    @pytest.fixture(scope='function')
    def clean_remote_box(self) -> None:
        """
        This method cleans up the remote system
        """
        # clean destination box
        REP.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_datasets()
        DATASET.delete_dataset("tank", "receive")
        DATASET.delete_dataset("tank", "replicate")
        REP.close_destination_box()

    @allure.tag("Create")
    @allure.story("Setup and Run Replication Task to Remote Box")
    def test_setup_and_run_replicate_task(self, rep) -> None:
        """
        Summary: This test verifies a replicate task can be created, "Run Now", and snapshot on Destination is created

        Test Steps:
        1. Create Replication Task
        2. Trigger Task with "Run Now" button
        3. Verify Replication Task is successful (Status = FINISHED)
        4. Verify snapshot exists on Destination (remote)
       """
        DP.click_add_replication_button()
        REP.set_source_location_on_same_box(rep['source'])
        REP.set_destination_location_on_different_box(rep['destination'], rep['connection-name'])
        REP.set_custom_snapshots()
        REP.set_task_name(rep['task-name'])
        COM.click_next_button()

        REP.set_run_once_button()
        REP.unset_read_only_destination_checkbox()
        REP.click_save_button_and_resolve_dialogs()
        assert REP.is_replication_task_visible(rep['task-name']) is True

        REP.click_run_now_replication_task_by_name(rep['task-name'])
        assert REP.get_replication_status(rep['task-name']) == rep['status']

        # log onto destination box and verify Snapshot exists
        REP.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert COM.assert_text_is_visible(rep['destination']) is True
        REP.close_destination_box()

    @allure.tag("Create", "NAS-T1154")
    @allure.story("System Trigger Replication Task to Remote Box")
    def test_system_trigger_replicate_task_push(self, rep) -> None:
        """
        Summary: This test verifies a push replicate task can be triggered by the system and files transferred

        Test Steps:
        1. Add test file to Source (local)
        2. Create Replication Task and set to trigger 1 min in future then wait for system time to catch up
        3. Verify Replication Task is successful (Status = FINISHED)
        4. Verify file exists on Destination (remote)
        5. Add new test file to Source (local)
        6. Update Replication Task to trigger 1 min in future then wait for system time to catch up
        7. Verify Replication Task is successful (Status = FINISHED)
        8. Verify file exists on Destination (remote)
        """
        # create replication task
        SSHCOM.add_test_file('rep_one.txt', rep['source'])
        assert COM.assert_file_exists('rep_one.txt', rep['source']) is True

        DP.click_add_replication_button()
        REP.set_source_location_on_same_box(rep['source'])
        REP.set_destination_location_on_different_box(rep['destination'], rep['connection-name'])
        REP.set_custom_snapshots()
        REP.set_task_name(rep['task-name'])
        COM.click_next_button()

        REP.select_schedule_preset('custom')
        current_minute = COM.get_current_minute()
        REP.set_preset_custom_time(minutes=str(current_minute + 1))
        COM.click_button('done')
        REP.click_save_button_and_resolve_dialogs()
        assert REP.is_replication_task_visible(rep['task-name']) is True

        # Set replication destination to not read only
        DP.click_edit_replication_task_by_name(rep['task-name'])
        REP.select_destination_read_only('ignore')

        COM.set_checkbox('schedule')
        REP.select_schedule_preset('custom')
        current_minute = COM.get_current_minute()
        REP.set_preset_custom_time(minutes=str(current_minute + 1))
        COM.click_button('done')
        COM.click_save_button()

        COM.wait_for_system_time('minute', current_minute + 1)
        assert REP.get_replication_status(rep['task-name']) == rep['status']

        # Verify file on destination
        assert COM.assert_file_exists('rep_one.txt', rep['destination'], private_config['REP_DEST_IP']) is True

        SSHCOM.add_test_file('rep_trigger.txt', rep['source'])
        assert COM.assert_file_exists('rep_trigger.txt', rep['source']) is True

        # Take new snapshot
        DP.click_edit_snapshot_task_by_name(rep['source'])
        SNAP.select_schedule_preset('custom')
        current_hour = COM.get_current_hour()
        current_minute = COM.get_current_minute()
        REP.set_preset_custom_time(minutes=str(current_minute + 1))
        COM.click_button('done')
        COM.click_save_button_and_wait_for_right_panel()
        COM.wait_for_system_time('minute', current_minute + 1)
        DP.click_snapshots_button()
        DP.assert_snapshot_by_hour_and_minute(current_hour, current_minute)
        # WebUI.delay(3)
        NAV.navigate_to_data_protection()

        DP.click_edit_replication_task_by_name(rep['task-name'])
        REP.select_schedule_preset('custom')
        current_hour = COM.get_current_hour()
        current_minute = COM.get_current_minute()
        REP.set_preset_custom_time(minutes=str(current_minute + 1))
        COM.click_button('done')
        COM.click_save_button()

        COM.wait_for_system_time('minute', current_minute + 1)
        assert REP.get_replication_status(rep['task-name']) == rep['status']
        DP.click_snapshots_button()
        DP.assert_snapshot_by_hour_and_minute(current_hour, current_minute)

        # log onto destination box and verify Snapshot exists
        REP.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert COM.assert_file_exists('rep_trigger.txt', rep['destination'], private_config['REP_DEST_IP']) is True

        # Clean Destination box
        NAV.navigate_to_datasets()
        DATASET.delete_dataset("tank", "receive")
        REP.close_destination_box()

    @allure.tag("Create", "NAS-T1269")
    @allure.story("System Trigger Replication Task to Local Box")
    def test_system_trigger_replicate_task_pull(self, rep) -> None:
        """
        Summary: This test verifies a pull replicate task can be triggered by the system and files transferred

        Test Steps:
        1. Add test file to Source (remote)
        2. Create Replication Task and set to trigger 1 min in future then wait for system time to catch up
        3. Verify Replication Task is successful (Status = FINISHED)
        4. Verify file exists on Destination (local)
        5. Add new test file to Source (remote)
        6. Update Replication Task to trigger 1 min in future then wait for system time to catch up
        7. Verify Replication Task is successful (Status = FINISHED)
        8. Verify file exists on Destination (local)
        """
        # create replication task
        SSHCOM.add_test_file('rep_one.txt', rep['source'], private_config['REP_DEST_IP'])
        assert COM.assert_file_exists('rep_one.txt', rep['source'], private_config['REP_DEST_IP']) is True
        API_POST.create_remote_snapshot_with_naming_schema(rep['source'])

        DP.click_add_replication_button()
        REP.set_source_location_on_different_box(rep['source'], rep['connection-name'])
        REP.set_destination_location_on_same_box(rep['destination'])
        REP.set_task_name(rep['task-name'])
        COM.click_next_button()

        REP.select_schedule_preset('custom')
        current_minute = COM.get_current_minute()
        REP.set_preset_custom_time(minutes=str(current_minute + 1))
        COM.click_button('done')
        REP.click_save_button_and_resolve_dialogs()
        assert REP.is_replication_task_visible(rep['task-name']) is True

        # Set replication destination to not read only
        DP.click_edit_replication_task_by_name(rep['task-name'])
        REP.select_destination_read_only('ignore')

        COM.set_checkbox('schedule')
        REP.select_schedule_preset('custom')
        current_minute = COM.get_current_minute()
        REP.set_preset_custom_time(minutes=str(current_minute + 1))
        COM.click_button('done')
        COM.click_save_button()

        COM.wait_for_system_time('minute', current_minute + 1)
        assert REP.get_replication_status(rep['task-name']) == rep['status']

        # Verify file on destination
        assert COM.assert_file_exists('rep_one.txt', rep['destination']) is True

        SSHCOM.add_test_file('rep_trigger.txt', rep['source'], private_config['REP_DEST_IP'])
        assert COM.assert_file_exists('rep_trigger.txt', rep['source'], private_config['REP_DEST_IP']) is True

        # Take new snapshot
        API_POST.create_remote_snapshot_with_naming_schema(rep['source'])

        DP.click_edit_replication_task_by_name(rep['task-name'])
        REP.select_schedule_preset('custom')
        current_hour = COM.get_current_hour()
        current_minute = COM.get_current_minute()
        REP.set_preset_custom_time(minutes=str(current_minute + 1))
        COM.click_button('done')
        COM.click_save_button()

        COM.wait_for_system_time('minute', current_minute + 1)
        assert REP.get_replication_status(rep['task-name']) == rep['status']

        # Verify Snapshot exists
        DP.click_snapshots_button()
        DP.assert_snapshot_by_hour_and_minute(current_hour, current_minute)
        assert COM.assert_file_exists('rep_trigger.txt', rep['destination']) is True
