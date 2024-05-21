import allure
import pytest

import xpaths.common_xpaths
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Share Admin', 'Scrub Tasks', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Share Admin')
class Test_Share_Admin_Scrub_Tasks:
    """
    This test class tests share admin Scrub Tasks
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self):
        """
        This setup fixture create the dataset and share admin for all test cases.
        """
        API_DELETE.delete_scrub_task("tank")
        API_POST.create_scrub_task()
        NAV.navigate_to_data_protection()

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_test(self):
        """
        This teardown fixture delete the Scrub Tasks and share admin for all test cases.
        """
        yield
        API_DELETE.delete_scrub_task("tank")

    @allure.tag("Read")
    @allure.story("Share Admin Can See The Scrub Tasks")
    def test_share_admin_can_see_the_scrub_tasks(self):
        """
        Summary: This test verifies the share admin is able to see scrub tasks.

        Test Steps:
        1. Verify the share admin is able to see scrub tasks
       """
        assert DP.assert_scrub_task_description("Scrub Task For Pool") is True

    @allure.tag("Read")
    @allure.issue("NAS-128701", "NAS-128701")
    @allure.story("Share Admin Can View the Configured Scrub Task")
    def test_share_admin_can_view_the_configured_scrub_task(self):
        """
        Summary: This test verifies the share admin is able to view the configured scrub task.

        Test Steps:
        1. Click Edit scrub task
        2. Verify scrub Task fields (pool, threshold, description, etc)
        3. Verify can view Custom Schedule dialog
        4. Close right panel
        """
        DP.click_edit_scrub_task("Scrub Task For Pool")
        assert COM.is_visible(xpaths.common_xpaths.select_field("pool")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("threshold")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("description")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("schedule-presets")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("enabled")) is True

        # Verify can view Custom Schedule Dialog
        # TODO: Fix this when issue is resolved
        # DP.set_schedule("custom")
        DP.set_schedule("00-00-7")
        assert DP.assert_preset_dialog_visible() is True
        COM.click_button("done")
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to add a scrub task")
    def test_share_admin_can_not_add_scrub_task(self):
        """
        Summary: This test verifies the share admin is not able to add a scrub task.

        Test Steps:
        1. Verify the add scrub task button is locked and not clickable
        """
        assert DP.assert_add_scrub_task_button_is_restricted() is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to delete a scrub task")
    def test_share_admin_can_not_delete_scrub_task(self):
        """
        Summary: This test verifies the share admin is not able to delete a scrub task.

        Test Steps:
        1. Verify the delete scrub task button is locked and not clickable
        """
        assert DP.assert_delete_scrub_task_button_is_restricted("Scrub Task For Pool") is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to modify a scrub task")
    def test_share_admin_can_not_modify_scrub_task(self):
        """
        Summary: This test verifies the share admin is not able to modify a scrub task.

        Test Steps:
        1. Click Edit scrub task
        2. Verify the save scrub task button is locked and not clickable
        3. Close right panel
        """
        DP.click_edit_scrub_task("Scrub Task For Pool")
        assert COM.assert_button_is_restricted('save') is True
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to enable and disable scrub tasks")
    def test_share_admin_can_not_enable_and_disable_scrub_task(self):
        """
        Summary: This test verifies the share admin is not able to enable and disable scrub tasks.

        Test Steps:
        1. Verify the enabled scrub task toggle is locked and not clickable
        2. Set scrub task to disabled through API
        3. Refresh page (re-navigate to Data Protection page)
        4. Verify the disabled Cloud Sync task toggle is locked and not clickable
        """
        assert DP.assert_enable_scrub_task_toggle_is_restricted("Scrub Task For Pool") is True
        # Create disabled Scrub Task
        API_DELETE.delete_scrub_task("tank")
        API_POST.create_scrub_task(enable=False)
        NAV.navigate_to_data_protection()
        assert DP.assert_enable_scrub_task_toggle_is_restricted("Scrub Task For Pool") is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able To modify the Resilver Priority")
    def test_share_admin_can_not_modify_resilver_priority(self):
        """
        Summary: This test verifies the share admin is not able to modify the Resilver Priority.

        Test Steps:
        1. Verify the adjust scrub task button is locked and not clickable
        """
        assert COM.assert_button_is_restricted('scrub-task-adjust-scrub') is True
