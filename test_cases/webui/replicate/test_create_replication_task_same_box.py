import pytest

from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.replication import Replication as REP


@pytest.mark.parametrize('rep', get_data_list('replication')[:2], scope='class')
class Test_Create_Replicate_Task_Same_Box():

    @staticmethod
    def test_setup_replicate_task(rep) -> None:
        """
        This test verifies a replicate task can be setup
        """
        DP.click_add_replication_button()
        REP.set_source_location_on_same_box(rep['source'])
        REP.set_destination_location_on_same_box(rep['destination'])
        REP.set_custom_snapshots()
        REP.set_task_name(rep['task-name'])
        COM.click_next_button()

        REP.set_run_once_button()
        REP.unset_read_only_destination_checkbox()
        COM.click_save_button()

        if REP.is_destination_snapshots_dialog_visible() is True:
            COM.assert_confirm_dialog()
        if REP.is_task_started_dialog_visible() is True:
            REP.click_close_task_started_button()
        if REP.is_run_now_dialog_visible() is True:
            COM.cancel_confirm_dialog()
        assert REP.is_replication_task_visible(rep['task-name']) is True

    @staticmethod
    def verify_run_replicate_task(rep) -> None:
        """
        This test verifies the replicate task can be executed successfully
        """
        REP.click_run_now_replication_task_by_name(rep['task-name'])
        assert REP.get_replication_status(rep['task-name']) == rep['status']

    @staticmethod
    def verify_teardown(rep) -> None:
        """
        This test removes the replicate task
        """
        # reset the change
        DP.delete_all_periodic_snapshot_tasks()
        DP.delete_all_snapshots()
        NAV.navigate_to_data_protection()
        REP.delete_replication_task_by_name(rep['task-name'])
