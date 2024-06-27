import allure
import pytest

from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common as COM
from keywords.webui.datasets import Datasets as DATA
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.replication import Replication as REP


@allure.tag("Replication")
@allure.epic("Data Protection")
@allure.feature("Replication-Options")
@pytest.mark.random_order(disabled=True)
class Test_Create_Replicate_Task_Options:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method cleans the environment in preparation for running tests
        """
        API_DELETE.delete_dataset('tank/source', True)
        API_DELETE.delete_dataset('tank/destination', True)
        # Create Datasets
        API_POST.create_dataset('tank/source', box='LOCAL')
        API_POST.create_dataset('tank/destination', box='LOCAL')

        # Set dataset Values
        NAV.navigate_to_datasets()
        DATA.expand_all_datasets()
        DATA.select_dataset('source')
        DATA.click_edit_dataset_space_button()
        DATA.set_quota_for_this_dataset('2 GiB')
        DATA.set_quota_for_this_dataset_and_all_children('4 GiB')
        COM.click_save_button_and_wait_for_progress_bar()

        # Verify destination dataset values are not set
        DATA.select_dataset('destination')
        DATA.click_edit_dataset_space_button()
        assert COM.get_input_property('refquota', 'value') == ''
        assert COM.get_input_property('quota', 'value') == ''
        COM.close_right_panel()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self) -> None:
        """
        This method cleans the environment after running tests
        """
        yield
        API_DELETE.delete_dataset('tank/source', True)
        API_DELETE.delete_dataset('tank/destination', True)

    @allure.tag("Create")
    @allure.story("Run Replication Task with Include Dataset Properties enabled")
    def test_run_replicate_task_with_include_dataset_properties_enabled(self) -> None:
        """
        Summary: This test verifies a replicate task copies the dataset properties

        Test Steps:
        1. Create Periodic Snapshot
        2. Create Replication Task (Include Dataset Properties = True)
        3. Trigger Replication Task
        4. Verify destination dataset values are set
        """

        # Create Periodic Snapshot
        NAV.navigate_to_data_protection()
        REP.create_periodic_snapshot('tank/source',
                                     'tank/destination',
                                     'rep-%Y-%m-%d_%H-%M',
                                     'LOCAL',
                                     'LOCAL')

        # Create Replication Task
        replication_options = {
            "NAME": "rep-dataset-prop",
            "TRANSPORT": "transport-local",
            "SOURCE": "tank/source",
            "INCLUDE_PROPERTIES": True,
            "DESTINATION": "tank/destination",
            "READ_ONLY_POLICY": "readonly-ignore",
            "MATCHING_SCHEMA": True,
            "NAMING_SCHEMA": "rep-%Y-%m-%d_%H-%M",
            "RUN_AUTOMATICALLY": False,
            }

        REP.create_advanced_replication_task_local(replication_options)
        REP.click_run_now_replication_task_by_name('rep-dataset-prop')

        # Verify destination dataset values are set
        NAV.navigate_to_datasets()
        DATA.expand_all_datasets()
        DATA.select_dataset('destination')
        DATA.click_edit_dataset_space_button()
        assert COM.get_input_property('refquota', 'value') == '2 GiB'
        assert COM.get_input_property('quota', 'value') == '4 GiB'
        COM.close_right_panel()

    @allure.tag("Create")
    @allure.story("Run Replication Task with Include Dataset Properties disabled")
    def test_run_replicate_task_with_include_dataset_properties_disabled(self) -> None:
        """
        Summary: This test verifies a replicate task does not copy the dataset properties

        Test Steps:
        1. Create Periodic Snapshot
        2. Create Replication Task (Include Dataset Properties = True)
        3. Trigger Replication Task
        4. Verify destination dataset values are not set
        """

        # Create Periodic Snapshot
        NAV.navigate_to_data_protection()
        REP.create_periodic_snapshot('tank/source',
                                     'tank/destination',
                                     'rep-%Y-%m-%d_%H-%M',
                                     'LOCAL',
                                     'LOCAL')

        # Create Replication Task
        replication_options = {
            "NAME": "rep-dataset-prop",
            "TRANSPORT": "transport-local",
            "SOURCE": "tank/source",
            "INCLUDE_PROPERTIES": False,
            "DESTINATION": "tank/destination",
            "READ_ONLY_POLICY": "readonly-ignore",
            "MATCHING_SCHEMA": True,
            "NAMING_SCHEMA": "rep-%Y-%m-%d_%H-%M",
            "RUN_AUTOMATICALLY": False,
            }

        REP.create_advanced_replication_task_local(replication_options)
        REP.click_run_now_replication_task_by_name('rep-dataset-prop')

        # Verify destination dataset values are set
        NAV.navigate_to_datasets()
        DATA.expand_all_datasets()
        DATA.select_dataset('destination')
        DATA.click_edit_dataset_space_button()
        assert COM.get_input_property('refquota', 'value') != '2 GiB'
        assert COM.get_input_property('quota', 'value') != '4 GiB'
        COM.close_right_panel()
