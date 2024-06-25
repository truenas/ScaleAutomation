import allure
import pytest

import xpaths.common_xpaths
from helper.data_config import get_data_list
from helper.global_config import private_config, shared_config
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.ssh_connection import SSH_Connection as SSHCON


@allure.tag('Read Only Admin', 'Replication Tasks', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
@pytest.mark.parametrize('rep', get_data_list('replication')[:1], scope='class')
class Test_Read_Only_Admin_Replication_Tasks:
    """
    This test class tests read-only admin Replication Tasks
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self, rep):
        """
        Summary: This setup fixture create the dataset and read-only admin for all test cases.
        """
        # Setup SSH connections.
        COM.logoff_truenas()
        COM.login_to_truenas(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_backup_credentials()
        SSHCON.assert_ssh_connection_exists(rep['connection-name'])
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        API_POST.start_service('ssh')
        private_config['API_IP'] = private_config['REP_DEST_IP']
        API_PUT.enable_user_all_sudo_commands_no_password(private_config['USERNAME'])
        API_PUT.enable_user_ssh_password(private_config['USERNAME'])
        API_POST.start_service('ssh')
        private_config['API_IP'] = private_config['IP']

        # Remove Snapshots if exists
        NAV.navigate_to_data_protection()
        DP.delete_all_replication_tasks()
        DP.delete_all_periodic_snapshot_tasks()

        API_POST.create_dataset(rep['source'])
        API_POST.create_dataset(rep['destination'])
        API_POST.delete_all_dataset_snapshots(rep['source'])
        API_POST.delete_all_dataset_snapshots(rep['destination'])
        API_POST.create_replication_task(rep['task-name'], rep['source'], rep['destination'])
        COM.logoff_truenas()
        COM.login_to_truenas(shared_config['ROA_USER'], shared_config['ROA_PASSWORD'])
        NAV.navigate_to_data_protection()

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_test(self, rep):
        """
        Summary: This teardown fixture delete the Replication Tasks and read-only admin for all test cases.
        """
        yield
        NAV.navigate_to_data_protection()
        DP.delete_all_periodic_snapshot_tasks()
        API_DELETE.delete_replication_task(rep['task-name'])
        API_POST.delete_all_dataset_snapshots(rep['source'])
        API_POST.delete_all_dataset_snapshots(rep['destination'])
        API_DELETE.delete_dataset(rep['source'])
        API_DELETE.delete_dataset(rep['destination'])

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See The Replication Tasks")
    def test_read_only_admin_can_see_the_replication_tasks(self, rep):
        """
        Summary: This test verifies the read-only admin is able to see Replication tasks.

        Test Steps:
        1. Verify the read-only admin is able to see Replication tasks
        2. Navigate to Replication tasks page
        3. Verify the read-only admin is able to see Replication tasks
        """
        assert DP.assert_replication_task_name(rep['task-name']) is True
        DP.click_card_page_link('Replication Tasks')
        assert DP.assert_replication_page_replication_task_name(rep['task-name']) is True
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Can View the Configured Replication Task")
    def test_read_only_admin_can_view_the_configured_replication_task(self, rep):
        """
        Summary: This test verifies the read-only admin is able to view the configured Replication task.

        Test Steps:
        1. Click Edit Replication task
        2. Verify Replication Task fields (description, direction, bucket-input, etc.)
        3. Verify subsections (Transfer, Remote, Control, Advanced Options)
        4. Verify can view Custom Schedule dialog
        5. Close right panel
        6. Navigate to Replication tasks page
        7. Verify the Replication tasks page test fields (name, transport, logging-level, etc.)
        """
        DP.click_edit_replication_task_by_name(rep['task-name'])
        assert COM.is_visible(xpaths.common_xpaths.input_field("name")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("transport")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("logging-level")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("enabled")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("compressed")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True

        # Verify Sub-sections
        assert COM.is_visible(xpaths.common_xpaths.any_text("General")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Transport Options")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Source")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Destination")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Replication Schedule")) is True

        # Verify can view Custom Schedule Dialog
        COM.select_option('schedule-picker-presets', 'schedule-picker-presets-00')
        assert DP.assert_preset_dialog_visible() is True
        COM.click_button("done")
        COM.close_right_panel()

        # Navigate to Replication tasks page
        DP.click_card_page_link('Replication Tasks')
        DP.expand_replication_task_by_name(rep['task-name'])
        DP.click_replication_page_edit_replication_task_button()

        # Verify Replication tasks page fields
        assert COM.is_visible(xpaths.common_xpaths.input_field("name")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("transport")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("logging-level")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("enabled")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("compressed")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True
        COM.close_right_panel()
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to add a Replication task")
    def test_read_only_admin_can_not_add_replication_task(self):
        """
        Summary: This test verifies the read-only admin is not able to add a Replication task.

        Test Steps:
        1. Verify the add Replication task button is locked and not clickable
        2. Navigate to Replication tasks page
        3. Verify the Replication tasks page add SMART test button is locked and not clickable
        """
        assert DP.assert_add_replication_task_button_is_restricted() is True
        DP.click_card_page_link('Replication Tasks')
        assert DP.assert_add_replication_task_button_is_restricted() is True
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to delete a Replication task")
    def test_read_only_admin_can_not_delete_replication_task(self, rep):
        """
        Summary: This test verifies the read-only admin is not able to delete a Replication task.

        Test Steps:
        1. Verify the delete Replication task button is locked and not clickable
        2. Navigate to Replication tasks page
        3. Verify the Replication tasks page delete Replication task button is locked and not clickable
        """
        assert DP.assert_delete_replication_task_button_is_restricted(rep['task-name']) is True
        DP.click_card_page_link('Replication Tasks')
        DP.expand_replication_task_by_name(rep['task-name'])
        assert DP.assert_replication_page_delete_replication_task_button_is_restricted(rep['task-name']) is True
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to modify a Replication task")
    def test_read_only_admin_can_not_modify_replication_task(self, rep):
        """
        Summary: This test verifies the read-only admin is not able to modify a Replication task.

        Test Steps:
        1. Click Edit Replication task
        2. Verify the save Replication task button is locked and not clickable
        3. Close right panel
        4. Navigate to Replication tasks page
        5. Verify the Replication tasks page save Replication task button is locked and not clickable
        """
        DP.click_edit_replication_task_by_name(rep['task-name'])
        assert COM.assert_button_is_restricted('save') is True
        COM.close_right_panel()
        DP.click_card_page_link('Replication Tasks')
        DP.expand_replication_task_by_name(rep['task-name'])
        DP.click_replication_page_edit_replication_task_button()
        assert COM.assert_button_is_restricted('save') is True
        COM.close_right_panel()
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.issue("NAS-129103", "NAS-129103")
    @allure.story("Read Only Admin Is Not Able to enable and disable Replication tasks")
    def test_read_only_admin_can_not_enable_and_disable_replication_task(self, rep):
        """
        Summary: This test verifies the read-only admin is not able to enable and disable Replication tasks.

        Test Steps:
        1. Verify the enabled Replication task toggle is locked and not clickable
        2. Set Replication to disabled through API
        3. Refresh page (re-navigate to Data Protection page)
        4. Verify the disabled Replication task toggle is locked and not clickable
        5. Navigate to Replication tasks page
        6. Verify the Replication tasks page enabled Replication task toggle is locked and not clickable
        """
        assert COM.assert_toggle_is_restricted(f'enabled-replication-task-{rep["task-name"]}-row-toggle') is True
        DP.click_card_page_link('Replication Tasks')
        assert COM.assert_toggle_is_restricted(f'enabled-replication-task-{rep["task-name"]}-row-toggle') is True
        COM.click_link('breadcrumb-data-protection')
        API_PUT.set_replication_task_enabled(rep['task-name'], False)
        NAV.navigate_to_data_protection()
        assert COM.assert_toggle_is_restricted(f'enabled-replication-task-{rep["task-name"]}-row-toggle') is True
        DP.click_card_page_link('Replication Tasks')
        assert COM.assert_toggle_is_restricted(f'enabled-replication-task-{rep["task-name"]}-row-toggle') is True
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able To Run the Replication task")
    def test_read_only_admin_can_not_run_replication_task(self, rep):
        """
        Summary: This test verifies the read-only admin is not able to run the Replication task.

        Test Steps:
        1. Verify the run Replication task button is locked and not clickable
        2. Navigate to Replication tasks page
        3. Verify the Replication tasks page run Replication task button is locked and not clickable
        """
        assert DP.assert_run_replication_task_button_is_restricted(rep['task-name']) is True
        DP.click_card_page_link('Replication Tasks')
        DP.expand_replication_task_by_name(rep['task-name'])
        assert DP.assert_replication_page_run_replication_task_button_is_restricted(rep['task-name']) is True
        COM.click_link('breadcrumb-data-protection')

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able To Restore the Replication task")
    def test_read_only_admin_can_not_restore_replication_task(self, rep):
        """
        Summary: This test verifies the read-only admin is not able to restore the Replication task.

        Test Steps:
        1. Verify the restore Replication task button is locked and not clickable
        5. Navigate to Replication tasks page
        6. Verify the Replication tasks page restore Replication task button is locked and not clickable
        """
        assert DP.assert_restore_replication_task_button_is_restricted(rep['task-name']) is True
        DP.click_card_page_link('Replication Tasks')
        DP.expand_replication_task_by_name(rep['task-name'])
        assert DP.assert_replication_page_restore_replication_task_button_is_restricted(rep['task-name']) is True
        COM.click_link('breadcrumb-data-protection')
