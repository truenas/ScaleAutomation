import allure
import pytest
from helper.global_config import shared_config
from keywords.api.rsynctask import API_Rsync_Task
from keywords.webui.common import Common
from keywords.webui.data_protection import Data_Protection
from keywords.webui.navigation import Navigation
from keywords.webui.rsync_task import Rsync_Task


@allure.tag('Read Only Admin', 'Rsync Tasks', 'Data Protection', 'Users', 'Permissions')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Read_Only_Admin_Data_Protection_Rsync_Tasks:

    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self):
        shared_config['TASK_ID'] = API_Rsync_Task.create_rsync_task('roa rsync task').json()['id']

    @pytest.fixture(autouse=True, scope='class')
    def tear_down_test(self):
        yield
        API_Rsync_Task.delete_rsync_task(task_id=shared_config['TASK_ID'])

    @pytest.fixture(autouse=True, scope='function')
    def navigate_to_data_protection(self):
        Navigation.navigate_to_data_protection()
        assert Data_Protection.assert_rsync_task_card_header_is_visible() is True

    @pytest.fixture(scope='function')
    def navigate_to_rsync_tasks(self):
        Data_Protection.click_the_rsync_task_header_link()
        assert Common.assert_page_header('Rsync Task') is True

    @allure.tag("Read")
    @allure.story('Verify That The Read-Only Admin Can View Configured Rsync Task')
    def test_read_only_admin_can_view_the_configured_rsync_task(self):
        """
        This test verifies that the read-only admin can view rsync task.
        1. Navigate to the data protection page.
        2. Verify that the rsync task is visible on the Rsync Task card as a read-only admin.
        """
        assert Data_Protection.assert_rsync_task_is_visible_on_card('/mnt/tank') is True

    @allure.tag("Read")
    @allure.story('Verify That The Read-Only Admin Can Access The Rsync Task List View From The Data Protection Page')
    def test_read_only_admin_can_access_rsync_task_list_view_from_the_data_protection_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the read-only admin can access the rsync task list view from the data protection page.
        1. Navigate to the data protection page.
        2. Click on the Rsync Task header link.
        3. Verify that the rsync task listed and visible on the page as a read-only admin.
        """
        assert Rsync_Task.assert_rsync_task_is_visible_on_page('/mnt/tank') is True

    @allure.tag("Create")
    @allure.story('Verify That The Read-Only Admin Cannot Add A Rsync Task From The Card')
    def test_read_only_admin_cannot_add_a_rsync_task_from_the_card(self):
        """
        This test verifies that the read-only admin cannot add a rsync task from the card.
        1. Navigate to the data protection page.
        2. Verify the add button on Rsync Task card is locked and not clickable as a read-only admin.
        """
        assert Data_Protection.assert_add_rsync_task_button_is_restricted() is True

    @allure.tag("Create")
    @allure.story('Verify That The Read-Only Admin Cannot Add A Rsync Task From The Page')
    def test_read_only_admin_cannot_add_a_rsync_task_from_the_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the read-only admin cannot add a rsync task from the page.
        1. Navigate to the data protection page.
        2. Click on the Rsync Task header link.
        3. Verify the Add button on the Rsync Task page is locked and not clickable as a read-only admin.
        """
        assert Rsync_Task.assert_add_rsync_task_button_is_restricted() is True

    @allure.tag("Update")
    @allure.story('Verify That The Read-Only Admin Cannot Modify A Rsync Task From The Card')
    def test_read_only_admin_cannot_modify_a_rsync_task_from_the_card(self):
        """
        This test verifies that the read-only admin cannot modify a rsync task from the card.
        1. Navigate to the data protection page.
        2. On the Rsync Task card, click on the edit button on the Rsync Task.
        3. verify the edit panel header is visible and the header is read-only as a read-only admin.
        4. verify the save button is locked and not clickable as a read-only admin.
        """
        Data_Protection.click_edit_rsync_task_by_path('/mnt/tank')
        assert Rsync_Task.assert_edit_rsync_task_panel_header_is_visible() is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()

    @allure.tag("Update")
    @allure.story('Verify That The Read-Only Admin Cannot Modify A Rsync Task From The Page')
    def test_read_only_admin_cannot_modify_a_rsync_task_from_the_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the read-only admin cannot modify a rsync task from the page.
        1. Navigate to the data protection page.
        2. Click on the Rsync Task header link.
        3. On the Rsync Task page, click on the edit button on the Rsync Task.
        4. verify the edit panel header is visible and the header is read-only as a read-only admin.
        5. verify the save button is locked and not clickable as a read-only admin.
        """
        Rsync_Task.click_edit_rsync_task_by_path('/mnt/tank')
        assert Rsync_Task.assert_edit_rsync_task_panel_header_is_visible() is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()

    @allure.tag("Delete")
    @allure.story('Verify That The Read-Only Admin Cannot Delete A Rsync Task From The Card')
    def test_read_only_admin_cannot_delete_a_rsync_task_from_the_card(self):
        """
        This test verifies that the read-only admin cannot delete a rsync task from the card.
        1. Navigate to the data protection page.
        2. Verify the delete button of a Rsync Task on Rsync Task card is locked and not clickable as a read-only admin.
        """
        assert Data_Protection.assert_delete_rsync_task_button_is_restricted('/mnt/tank') is True

    @allure.tag("Delete")
    @allure.story('Verify That The Read-Only Admin Cannot Delete A Rsync Task From The Page')
    def test_read_only_admin_cannot_delete_a_rsync_task_from_the_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the read-only admin cannot delete a rsync task from the page.
        1. Navigate to the data protection page.
        2. Click on the Rsync Task header link.
        3. Verify the Delete button of a Rsync Task on the Rsync Task page is locked and not clickable as a read-only admin.
        """
        assert Rsync_Task.assert_delete_rsync_task_button_is_restricted('/mnt/tank') is True

    @allure.tag("Update")
    @allure.story('Verify That The Read-Only Admin Cannot Enable And Disable Rsync Tasks')
    def test_read_only_admin_cannot_enable_and_disable_rsync_tasks(self):
        """
        This test verifies that the read-only admin cannot enable and disable rsync tasks.
        1. Navigate to the data protection page.
        2. Verify the Rsync Task Enabled toggle is locked and not clickable as a read-only admin.
        3. Disable the rsync task.
        4. Verify the Rsync Task Enabled toggle is locked and not clickable as a read-only admin.
        """
        assert Data_Protection.assert_enable_rsync_task_toggle_is_restricted('/mnt/tank') is True
        API_Rsync_Task.disable_rsync_task(shared_config['TASK_ID'])
        Navigation.navigate_to_data_protection()
        assert Data_Protection.assert_rsync_task_card_header_is_visible() is True
        assert Data_Protection.assert_enable_rsync_task_toggle_is_restricted('/mnt/tank') is True

    @allure.tag("Update")
    @allure.story('Verify That The Read-Only Admin Cannot Run A Rsync Task From The Card')
    def test_read_only_admin_cannot_run_a_rsync_task_from_the_card(self):
        """
        This test verifies that the read-only admin cannot run a rsync task from the card.
        1. Navigate to the data protection page.
        2. Verify the Run button on the Rsync Task card is locked and not clickable as a read-only admin.
        """
        assert Data_Protection.assert_run_rsync_task_button_is_restricted('/mnt/tank') is True

    @allure.tag("Update")
    @allure.story('Verify That The Read-Only Admin Cannot Run A Rsync Task From The Page')
    def test_read_only_admin_cannot_run_a_rsync_task_from_the_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the read-only admin cannot run a rsync task from the page.
        1. Navigate to the data protection page.
        2. Click on the Rsync Task header link.
        3. Verify the Run button on the Rsync Task page is locked and not clickable as a read-only admin.
        """
        assert Rsync_Task.assert_run_rsync_task_button_is_restricted('/mnt/tank') is True
