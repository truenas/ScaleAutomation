import allure
import pytest

import xpaths.common_xpaths
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.data_protection import Data_Protection as DP
from keywords.webui.navigation import Navigation as NAV


@allure.tag('Read Only Admin', 'Periodic Snapshot Tasks', "Users", 'Permissions', 'Data Protection')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_Periodic_Snapshot_Tasks:
    """
    This test class tests read-only admin Periodic Snapshot Tasks
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_class(self):
        """
        This setup fixture create the dataset and read-only admin for all test cases.
        """
        API_POST.create_dataset('tank/persnap_ro')
        API_POST.delete_all_dataset_snapshots('tank/persnap_ro')
        API_POST.create_snapshot('tank/persnap_ro', 'persnap_ro')
        API_POST.create_snapshot_task('tank/persnap_ro')
        NAV.navigate_to_data_protection()

    @pytest.fixture(autouse=True, scope='class')
    def teardown_class(self):
        """
        This teardown fixture delete the Periodic Snapshot Tasks and read-only admin for all test cases.
        """
        yield
        API_POST.delete_all_dataset_snapshots('tank/persnap_ro')
        API_DELETE.delete_all_periodic_snapshots_tasks()
        API_DELETE.delete_dataset('tank/persnap_ro')

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See The Periodic Snapshot Tasks")
    def test_read_only_admin_can_see_the_periodic_snapshot_tasks(self):
        """
        This test verifies the read-only admin is able to see Periodic Snapshot tasks.
        """
        assert DP.assert_periodic_snapshot_task_dataset('tank/persnap_ro') is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Can View the Configured Periodic Snapshot Task")
    def test_read_only_admin_can_view_the_configured_periodic_snapshot_task(self):
        """
        This test verifies the read-only admin is able to view the configured Periodic Snapshot task.
        """
        DP.click_edit_periodic_snapshot_task('tank/persnap_ro')
        assert COM.is_visible(xpaths.common_xpaths.select_field("dataset")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("exclude")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("recursive")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("lifetime-value")) is True
        assert COM.is_visible(xpaths.common_xpaths.select_field("lifetime-unit")) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field("naming-schema")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("allow-empty")) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field("enabled")) is True
        assert COM.is_visible(xpaths.common_xpaths.button_field("save")) is True

        # Verify Sub-sections
        assert COM.is_visible(xpaths.common_xpaths.any_text("Dataset")) is True
        assert COM.is_visible(xpaths.common_xpaths.any_text("Schedule")) is True

        # Verify can view Custom Schedule Dialog
        COM.select_option('schedule-presets', 'schedule-presets-00')
        assert DP.assert_preset_dialog_visible() is True
        COM.click_button("done")
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to add a Periodic Snapshot task")
    def test_read_only_admin_can_not_add_periodic_snapshot_task(self):
        """
        This test verifies the read-only admin is not able to add a Periodic Snapshot task.
        """
        assert DP.assert_add_periodic_snapshot_task_button_is_locked_and_not_clickable() is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to delete a Periodic Snapshot task")
    def test_read_only_admin_can_not_delete_periodic_snapshot_task(self):
        """
        This test verifies the read-only admin is not able to delete a Periodic Snapshot task.
        """
        assert DP.assert_delete_periodic_snapshot_task_button_is_locked_and_not_clickable('tank/persnap_ro') is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to modify a Periodic Snapshot task")
    def test_read_only_admin_can_not_modify_periodic_snapshot_task(self):
        """
        This test verifies the read-only admin is not able to modify a Periodic Snapshot task.
        """
        DP.click_edit_periodic_snapshot_task('tank/persnap_ro')
        assert COM.assert_button_is_locked_and_not_clickable('save') is True
        COM.close_right_panel()

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to enable and disable Periodic Snapshot tasks")
    def test_read_only_admin_can_not_enable_and_disable_periodic_snapshot_task(self):
        """
        This test verifies the read-only admin is not able to enable and disable Periodic Snapshot tasks.
        """
        assert DP.assert_enable_periodic_snapshot_task_toggle_is_locked_and_not_clickable('tank/persnap_ro') is True
        API_PUT.set_periodic_snapshot_task_enabled('tank/persnap_ro', False)
        NAV.navigate_to_data_protection()
        assert DP.assert_enable_periodic_snapshot_task_toggle_is_locked_and_not_clickable('tank/persnap_ro') is True

    @allure.tag("Read")
    @allure.story("Read Only Admin Can See The VM Periodic Snapshot Tasks")
    def test_read_only_admin_can_see_the_vm_periodic_snapshot_tasks(self):
        """
        This test verifies the read-only admin is not able to run the Periodic Snapshot task.
        """
        COM.click_link('snapshot-task-vmware-snapshots')
        assert COM.assert_page_header('VMware Snapshots') is True
        NAV.navigate_to_data_protection()

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to add a VM Periodic Snapshot")
    def test_read_only_admin_can_not_add_vm_periodic_snapshot(self):
        """
        This test verifies the read-only admin is not able to add a VM Periodic Snapshot.
        """
        COM.click_link('snapshot-task-vmware-snapshots')
        assert DP.assert_add_vm_periodic_snapshot_button_is_locked_and_not_clickable() is True
        NAV.navigate_to_data_protection()

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to delete a Periodic Snapshot task")
    @pytest.mark.skip(reason="@@@ test_read_only_admin_can_not_delete_vm_periodic_snapshot: Currently ONLY available on a VMware box.")
    def test_read_only_admin_can_not_delete_vm_periodic_snapshot(self):
        """
        This test verifies the read-only admin is not able to delete a Periodic Snapshot task.
        """
        COM.click_link('snapshot-task-vmware-snapshots')
        assert DP.assert_delete_vm_periodic_snapshot_task_button_is_locked_and_not_clickable('tank/persnap_ro') is True
        NAV.navigate_to_data_protection()

    @allure.tag("Read")
    @allure.story("Read Only Admin Is Not Able to modify a Periodic Snapshot task")
    @pytest.mark.skip(reason="@@@ test_read_only_admin_can_not_modify_vm_periodic_snapshot: Currently ONLY available on a VMware box.")
    def test_read_only_admin_can_not_modify_vm_periodic_snapshot(self):
        """
        This test verifies the read-only admin is not able to modify a Periodic Snapshot task.
        """
        COM.click_link('snapshot-task-vmware-snapshots')
        DP.click_edit_vm_periodic_snapshot_task('tank/persnap_ro')
        assert COM.assert_button_is_locked_and_not_clickable('save') is True
        NAV.navigate_to_data_protection()
