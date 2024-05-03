import allure
import pytest

import xpaths.common_xpaths
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Share Admin', 'Cloud Sync Tasks', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Share Admin')
@pytest.mark.parametrize('cloud_sync', get_data_list('backup_credentials'), scope='class')
class Test_Share_Admin_Cloud_Sync_Tasks:
    """
    This test class tests share admin Cloud Sync Tasks
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self, cloud_sync):
        """
        This setup fixture create the dataset and share admin for all test cases.
        """
        API_DELETE.delete_cloud_sync_task(cloud_sync['description'])
        API_DELETE.delete_cloud_sync_credential(cloud_sync['name'])
        API_POST.create_cloud_sync_credential(cloud_sync['name'], cloud_sync['provider'], cloud_sync['access_key'], cloud_sync['secret_key'])
        API_POST.create_cloud_sync_task(cloud_sync['name'], cloud_sync['description'])
        NAV.navigate_to_data_protection()

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_test(self, cloud_sync):
        """
        This teardown fixture delete the Scrub Tasks and share admin for all test cases.
        """
        yield
        API_DELETE.delete_cloud_sync_task(cloud_sync['description'])
        API_DELETE.delete_cloud_sync_credential(cloud_sync['name'])

    @allure.tag("Read")
    @allure.story("Share Admin Can See The Cloud Sync Tasks")
    def test_share_admin_can_see_the_cloud_sync_tasks(self, cloud_sync):
        """
        This test verifies the share admin is able to see Cloud Sync tasks.
        """
        assert DP.assert_cloud_sync_task_description(cloud_sync['description']) is True

    @allure.tag("Read")
    @allure.issue("NAS-128725", "NAS-128725")
    @allure.story("Share Admin Can View the Configured Cloud Sync Task")
    def test_share_admin_can_view_the_configured_cloud_sync_task(self, cloud_sync):
        """
        This test verifies the share admin is able to view the configured Cloud Sync task.
        """
        DP.click_edit_cloud_sync_task(cloud_sync['description'])
        assert COM.is_visible(xpaths.common_xpaths.input_field("description")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("direction")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("bucket-input")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("path-destination")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("enabled")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("dry-run")) is True

        # Verify Sub-sections
        assert COM.is_visible(xpaths.common_xpaths.any_text("Transfer")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Remote")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Control")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Advanced Options")) is True

        # Verify can view Custom Schedule Dialog
        COM.select_option('cloudsync-picker-presets', 'cloudsync-picker-presets-00')
        assert DP.assert_preset_dialog_visible() is True
        COM.click_button("done")
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to add a Cloud Sync task")
    def test_share_admin_can_not_add_cloud_sync_task(self):
        """
        This test verifies the share admin is not able to add a Cloud Sync task.
        """
        assert DP.assert_add_cloud_sync_task_button_is_locked_and_not_clickable() is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to delete a Cloud Sync task")
    def test_share_admin_can_not_delete_cloud_sync_task(self, cloud_sync):
        """
        This test verifies the share admin is not able to delete a Cloud Sync task.
        """
        assert DP.assert_delete_cloud_sync_task_button_is_locked_and_not_clickable(cloud_sync['description']) is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to modify a Cloud Sync task")
    def test_share_admin_can_not_modify_cloud_sync_task(self, cloud_sync):
        """
        This test verifies the share admin is not able to modify a Cloud Sync task.
        """
        DP.click_edit_cloud_sync_task(cloud_sync['description'])
        assert COM.assert_button_is_locked_and_not_clickable('save') is True
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able to enable and disable Cloud Sync tasks")
    def test_share_admin_can_not_enable_and_disable_cloud_sync_task(self, cloud_sync):
        """
        This test verifies the share admin is not able to enable and disable Cloud Sync tasks.
        """
        assert DP.assert_enable_cloud_sync_task_toggle_is_locked_and_not_clickable(cloud_sync['description']) is True
        API_PUT.set_cloud_sync_task_enabled(cloud_sync['name'], False)
        NAV.navigate_to_data_protection()
        assert DP.assert_enable_cloud_sync_task_toggle_is_locked_and_not_clickable(cloud_sync['description']) is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able To Run the Cloud Sync task")
    def test_share_admin_can_not_run_cloud_sync_task(self, cloud_sync):
        """
        This test verifies the share admin is not able to run the Cloud Sync task.
        """
        assert DP.assert_run_cloud_sync_task_button_is_locked_and_not_clickable(cloud_sync['description']) is True

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able To Dry Run the Cloud Sync task")
    def test_share_admin_can_not_dry_run_cloud_sync_task(self, cloud_sync):
        """
        This test verifies the share admin is not able to dry run the Cloud Sync task.
        """
        assert DP.assert_dry_run_cloud_sync_task_button_is_locked_and_not_clickable(cloud_sync['description']) is True
        DP.click_edit_cloud_sync_task(cloud_sync['description'])
        assert COM.assert_button_is_locked_and_not_clickable('dry-run') is True
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Share Admin Is Not Able To Restore the Cloud Sync task")
    def test_share_admin_can_not_restore_cloud_sync_task(self, cloud_sync):
        """
        This test verifies the share admin is not able to restore the Cloud Sync task.
        """
        assert DP.assert_restore_cloud_sync_task_button_is_locked_and_not_clickable(cloud_sync['description']) is True
