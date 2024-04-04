import allure
import pytest

from helper.data_config import get_data_list
from helper.global_config import private_config
from keywords.webui.common_replication import Common_Replication as COMREP
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.replication import Replication as REP


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Remote")
@pytest.mark.parametrize('rep', get_data_list('replication')[2:], scope='class')
class Test_Create_Replicate_Task_Different_Box:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self, rep) -> None:
        """
        This method sets up each test to start with test replication tasks deleted
        """
        NAV.navigate_to_data_protection()
        if REP.is_replication_task_visible(rep['task-name']) is True:
            REP.delete_replication_task_by_name(rep['task-name'])

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self, rep) -> None:
        """
        This test removes the replicate task
        """
        # reset the change
        yield
        # clean destination box
        DP.delete_all_snapshots()
        COM.delete_all_test_files(rep['destination'], private_config['REP_DEST_IP'])

        # clean source box
        REP.close_destination_box()
        NAV.navigate_to_data_protection()
        DP.delete_all_replication_tasks()
        DP.delete_all_periodic_snapshot_tasks()
        DP.delete_all_snapshots()
        NAV.navigate_to_data_protection()
        # REP.delete_replication_task_by_name(rep['task-name'])
        COM.delete_all_test_files(rep['source'])

    @allure.tag("Create")
    @allure.story("Setup and Run Replication Task to Remote Box")
    def test_setup_and_run_replicate_task(self, rep) -> None:
        """
        This test verifies a replicate task can be setup
        """
        DP.click_add_replication_button()
        REP.set_source_location_on_same_box(rep['source'])
        REP.set_destination_location_on_different_box(rep['destination'], rep['connection-name'])
        REP.set_custom_snapshots()
        REP.set_task_name(rep['task-name'])
        COM.click_next_button()

        REP.set_run_once_button()
        REP.unset_read_only_destination_checkbox()
        COM.click_save_button()

        if REP.is_destination_snapshots_dialog_visible() is True:
            COM.assert_confirm_dialog()
        if REP.is_sudo_enabled_dialog_visible() is True:
            COM.assert_confirm_dialog()
        if REP.is_task_started_dialog_visible() is True:
            REP.click_close_task_started_button()
        if REP.is_run_now_dialog_visible() is True:
            COM.cancel_confirm_dialog()
        assert REP.is_replication_task_visible(rep['task-name']) is True

        REP.click_run_now_replication_task_by_name(rep['task-name'])
        assert REP.get_replication_status(rep['task-name']) == rep['status']

        # log onto destination box and verify Snapshot exists
        REP.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert COM.assert_text_is_visible(rep['destination']) is True

    @allure.tag("Create")
    @allure.story("System Trigger Replication Task to Remote Box")
    def test_system_trigger_replicate_task(self, rep) -> None:
        """
        This test verifies a replicate task can be triggered by the system
        """
        COM.add_test_file('rep_one.txt', rep['source'])
        assert COM.assert_file_exists('rep_one.txt', rep['source']) is True
        DP.click_add_replication_button()
        COM.click_button('advanced')
        COMREP.set_direction_push()
        REP.set_ssh_connection_advanced(rep['connection-name'])
        COM.assert_confirm_dialog()
        # REP.set_source_location_on_same_box(rep['source'])
        REP.set_source_location(rep['source'])
        # REP.set_destination_location_on_different_box(rep['destination'], rep['connection-name'])
        REP.set_destination_location(rep['destination'])
        REP.set_task_name(rep['task-name'])
        # COM.click_next_button()

        # REP.set_run_once_button()
        # REP.unset_read_only_destination_checkbox()
        REP.select_destination_read_only('ignore')
        COM.set_input_field('also-include-naming-schema', 'auto-%Y-%m-%d_%H-%M')
        COM.set_checkbox('schedule')

        # COM.click_radio_button('schedule-method-run-on-a-schedule')
        REP.select_schedule_preset('custom')
        current_minute = COM.get_current_minute()
        REP.set_preset_custom_time(minutes=str(current_minute + 1))
        COM.click_button('done')
        COM.click_save_button()

        if REP.is_destination_snapshots_dialog_visible() is True:
            COM.assert_confirm_dialog()
        if REP.is_sudo_enabled_dialog_visible() is True:
            COM.assert_confirm_dialog()
        if REP.is_task_started_dialog_visible() is True:
            REP.click_close_task_started_button()
        if REP.is_run_now_dialog_visible() is True:
            COM.cancel_confirm_dialog()
        assert REP.is_replication_task_visible(rep['task-name']) is True

        # REP.click_run_now_replication_task_by_name(rep['task-name'])
        COM.wait_for_system_time('minute', current_minute + 1)
        NAV.navigate_to_datasets()
        NAV.navigate_to_data_protection()
        assert REP.get_replication_status(rep['task-name']) == rep['status']

        # log onto destination box and verify Snapshot exists
        REP.login_to_destination_box(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_data_protection()
        DP.click_snapshots_button()
        assert COM.assert_text_is_visible(rep['destination']) is True
        assert COM.assert_file_exists('rep_one.txt', rep['destination'], private_config['REP_DEST_IP']) is True
