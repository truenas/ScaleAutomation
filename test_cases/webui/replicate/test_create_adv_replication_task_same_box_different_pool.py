import allure
import pytest

from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.pool_creation_wizard import Pool_Creation_Wizard as PCW
from keywords.webui.replication import Replication as REP
from keywords.ssh.common import Common_SSH as SSHCOM
from keywords.webui.storage import Storage as STORE


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Local")
@pytest.mark.random_order(disabled=True)
@pytest.mark.parametrize('rep', get_data_list('replication')[:2], scope='class')
class Test_Create_Adv_Replicate_Task_Other_Pool_Same_Box:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method sets up each test to start with test replication tasks deleted
        """
        API_POST.create_dataset('tank/replicate')
        NAV.navigate_to_storage()
        STORE.click_create_pool_button()
        PCW.set_name_entry('two')
        PCW.click_next_button('general')

        assert COM.assert_step_header_is_open('Data')
        PCW.select_layout_option('data', 'Mirror')
        PCW.select_disk_size_option('data', '20 GiB (HDD)')
        PCW.select_width_option('data', 2)
        PCW.select_number_of_vdevs_option('data', 1)
        PCW.click_save_and_go_to_review_button('data')

        PCW.click_create_pool_button()
        PCW.click_confirm_waring_dialog()
        assert PCW.assert_create_pool_dialog_not_visible() is True

        API_POST.create_dataset('two/advrep')
        API_POST.create_snapshot_task('two/advrep')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self) -> None:
        """
        This test removes the replicate task
        """
        yield
        # reset the change
        NAV.navigate_to_data_protection()
        DP.delete_all_periodic_snapshot_tasks()
        REP.delete_replication_task_by_name('other_pool')
        API_POST.delete_all_dataset_snapshots('two/advrep')
        API_POST.export_pool('two', True)

    @allure.tag("Create", "NAS-T1671")
    @allure.story("Create Advanced Replication Task to anther Pool on Local Box")
    def test_create_advanced_replicate_task_to_other_pool(self) -> None:
        """
        Summary: This test verifies a local replicate task to another pool can be created, "Run Now", and is successful

        Test Steps:
        1. Add test file to Source (local)
        2. Create Advanced Replication Task (Destination = different pool)
        3. Trigger Task with "Run Now" button
        4. Verify Replication Task is successful (Status = FINISHED)
        5. Verify file exists in Destination (different pool)
        """
        SSHCOM.add_test_file('rep_one.txt', 'tank/replicate')
        assert COM.assert_file_exists('rep_one.txt', 'tank/replicate') is True

        NAV.navigate_to_data_protection()
        DP.click_add_replication_button()
        REP.set_source_location_on_same_box('tank/replicate')
        REP.set_destination_location_on_same_box('two/advrep')
        REP.set_custom_snapshots()
        REP.set_task_name('other_pool')
        COM.click_next_button()

        REP.set_run_once_button()
        REP.unset_read_only_destination_checkbox()
        REP.click_save_button_and_resolve_dialogs()
        assert REP.is_replication_task_visible('other_pool') is True

        REP.click_run_now_replication_task_by_name('other_pool')
        assert REP.get_replication_status('other_pool') == 'FINISHED'

        DP.click_snapshots_button()
        assert COM.assert_text_is_visible('two/advrep') is True
        assert COM.assert_file_exists('rep_one.txt', 'two/advrep') is True
