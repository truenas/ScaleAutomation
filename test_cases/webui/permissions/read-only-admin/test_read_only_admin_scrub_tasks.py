import allure
import pytest

import xpaths.common_xpaths
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Read Only Admin', 'Scrub Tasks', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_Scrub_Tasks:
    """
    This test class tests read-only admin Scrub Tasks
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self):
        """
        This setup fixture create the dataset and read-only admin for all test cases.
        """
        API_POST.create_scrub_task()
        NAV.navigate_to_data_protection()

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_test(self):
        """
        This teardown fixture delete the Scrub Tasks and read-only admin for all test cases.
        """
        yield
        API_DELETE.delete_scrub_task("tank")

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See The Scrub Tasks")
    def test_read_only_admin_can_see_the_scrub_tasks(self):
        """
        This test verifies the read-only admin is able to see scrub tasks.
        """
        assert DP.assert_scrub_task_description("Scrub Task For Pool") is True

    @allure.tag("Read")
    @allure.issue("NAS-128701", "NAS-128701")
    @allure.story("Read Only Admin Can View the Configured Scrub Task")
    def test_read_only_admin_can_view_the_configured_scrub_task(self):
        """
        This test verifies the read-only admin is able to view the configured scrub task.
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
    @allure.story("Read Only Admin Is Not Able to add a scrub task")
    def test_read_only_admin_can_not_add_scrub_task(self):
        """
        This test verifies the read-only admin is not able to add a scrub task.
        """
        assert DP.assert_add_scrub_task_button_is_locked_and_not_clickable() is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to delete a scrub task")
    def test_read_only_admin_can_not_delete_scrub_task(self):
        """
        This test verifies the read-only admin is not able to delete a scrub task.
        """
        assert DP.assert_delete_scrub_task_button_is_locked_and_not_clickable("Scrub Task For Pool") is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to modify a scrub task")
    def test_read_only_admin_can_not_modify_scrub_task(self):
        """
        This test verifies the read-only admin is not able to modify a scrub task.
        """
        DP.click_edit_scrub_task("Scrub Task For Pool")
        assert COM.assert_button_is_locked_and_not_clickable('save') is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to enable and disable scrub tasks")
    def test_read_only_admin_can_not_enable_and_disable_scrub_task(self):
        """
        This test verifies the read-only admin is not able to enable and disable scrub tasks.
        """
        assert DP.assert_enable_scrub_task_toggle_is_locked_and_not_clickable("Scrub Task For Pool") is True
        # Create disabled Scrub Task
        API_DELETE.delete_scrub_task("tank")
        API_POST.create_scrub_task(enable=False)
        NAV.navigate_to_data_protection()
        assert DP.assert_enable_scrub_task_toggle_is_locked_and_not_clickable("Scrub Task For Pool") is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able To modify the Resilver Priority")
    def test_read_only_admin_can_not_modify_resilver_priority(self):
        """
        This test verifies the read-only admin is not able to modify the Resilver Priority.
        """
        assert COM.assert_button_is_locked_and_not_clickable('scrub-task-adjust-scrub') is True
