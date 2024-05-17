import allure
import pytest
from helper.global_config import shared_config
from keywords.api.rsynctask import API_Rsync_Task
from keywords.webui.common import Common
from keywords.webui.data_protection import Data_Protection
from keywords.webui.navigation import Navigation
from keywords.webui.rsync_task import Rsync_Task


@allure.tag('Share Admin', 'Rsync Tasks', 'Data Protection', 'Users', 'Permissions')
@allure.epic('Permissions')
@allure.feature('Read Only Admin')
class Test_Share_Admin_Data_Protection_Rsync_Tasks:

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
        assert Rsync_Task.assert_rsync_task_page_header() is True

    @allure.tag("Read")
    @allure.story('Verify That The Share Admin Can View Configured Rsync Task')
    def test_share_admin_can_view_the_configured_rsync_task(self):
        """
        This test verifies that the share admin can view rsync task.
        - Navigate to the data protection page.
        - Verify that the rsync task is visible on the Rsync Task card as a share admin.
        """
        assert Data_Protection.assert_rsync_task_is_visible_on_card('/mnt/tank') is True

    @allure.tag("Read")
    @allure.story('Verify That The Share Admin Can Access The Rsync Task List View From The Data Protection Page')
    def test_share_admin_can_access_rsync_task_list_view_from_the_data_protection_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the share admin can access the rsync task list view from the data protection page.
        - Navigate to the data protection page.
        - Click on the Rsync Task header link.
        - Verify that the rsync task listed and visible on the page as a share admin.
        """
        assert Rsync_Task.assert_rsync_task_is_visible_on_page('/mnt/tank') is True

    @allure.tag("Create")
    @allure.story('Verify That The Share Admin Cannot Add A Rsync Task From The Card')
    def test_share_admin_cannot_add_a_rsync_task_from_the_card(self):
        """
        This test verifies that the share admin cannot add a rsync task from the card.
        - Navigate to the data protection page.
        - Verify the add button on Rsync Task card is locked and not clickable as a share admin.
        """
        assert Data_Protection.assert_add_rsync_task_button_is_restricted() is True

    @allure.tag("Create")
    @allure.story('Verify That The Share Admin Cannot Add A Rsync Task From The Page')
    def test_share_admin_cannot_add_a_rsync_task_from_the_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the share admin cannot add a rsync task from the page.
        - Navigate to the data protection page.
        - Click on the Rsync Task header link.
        - Verify the Add button on the Rsync Task page is locked and not clickable as a share admin.
        """
        assert Rsync_Task.assert_add_rsync_task_button_is_restricted() is True

    @allure.tag("Update")
    @allure.story('Verify That The Share Admin Cannot Modify A Rsync Task From The Card')
    def test_share_admin_cannot_modify_a_rsync_task_from_the_card(self):
        """
        This test verifies that the share admin cannot modify a rsync task from the card.
        - Navigate to the data protection page.
        - click on the edit button on the Rsync Task.
        - verify the edit panel header is visible and the header is read-only as a share admin.
        - verify the save button is locked and not clickable as a share admin.
        """
        Data_Protection.click_edit_rsync_task_by_path('/mnt/tank')
        assert Rsync_Task.assert_edit_rsync_task_panel_header_is_visible() is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()

    @allure.tag("Update")
    @allure.story('Verify That The Share Admin Cannot Modify A Rsync Task From The Page')
    def test_share_admin_cannot_modify_a_rsync_task_from_the_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the share admin cannot modify a rsync task from the page.
        - Navigate to the data protection page.
        - Click on the Rsync Task header link.
        - On the Rsync Task page, click on the edit button on the Rsync Task.
        - verify the edit panel header is visible and the header is read-only as a share admin.
        - verify the save button is locked and not clickable as a share admin.
        """
        Rsync_Task.click_edit_rsync_task_by_path('/mnt/tank')
        assert Rsync_Task.assert_edit_rsync_task_panel_header_is_visible() is True
        assert Common.assert_header_readonly_badge() is True
        assert Common.assert_save_button_is_restricted() is True
        Common.close_right_panel()

    @allure.tag("Delete")
    @allure.story('Verify That The Share Admin Cannot Delete A Rsync Task From The Card')
    def test_share_admin_cannot_delete_a_rsync_task_from_the_card(self):
        """
        This test verifies that the share admin cannot delete a rsync task from the card.
        - Navigate to the data protection page.
        - Verify the delete button of a Rsync Task on Rsync Task card is locked and not clickable as a share admin.
        """
        assert Data_Protection.assert_delete_rsync_task_button_is_restricted('/mnt/tank') is True

    @allure.tag("Delete")
    @allure.story('Verify That The Share Admin Cannot Delete A Rsync Task From The Page')
    def test_share_admin_cannot_delete_a_rsync_task_from_the_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the share admin cannot delete a rsync task from the page.
        - Navigate to the data protection page.
        - Click on the Rsync Task header link.
        - Verify the Delete button of a Rsync Task on the Rsync Task page is locked and not clickable as a share admin.
        """
        assert Rsync_Task.assert_delete_rsync_task_button_is_restricted('/mnt/tank') is True

    @allure.tag("Update")
    @allure.story('Verify That The Share Admin Cannot Enable And Disable Rsync Tasks')
    def test_share_admin_cannot_enable_and_disable_rsync_tasks(self):
        """
        This test verifies that the share admin cannot enable and disable rsync tasks.
        - Navigate to the data protection page.
        - Verify the Enable and Disable button on the Rsync Task card is locked and not clickable as a share admin.
        """
        assert Data_Protection.assert_enable_rsync_task_toggle_is_restricted('/mnt/tank') is True

    @allure.tag("Update")
    @allure.story('Verify That The Share Admin Cannot Run A Rsync Task From The Card')
    def test_share_admin_cannot_run_a_rsync_task_from_the_card(self):
        """
        This test verifies that the share admin cannot run a rsync task from the card.
        - Navigate to the data protection page.
        - Verify the Run button on the Rsync Task card is locked and not clickable as a share admin.
        """
        assert Data_Protection.assert_run_rsync_task_button_is_restricted('/mnt/tank') is True

    @allure.tag("Update")
    @allure.story('Verify That The Share Admin Cannot Run A Rsync Task From The Page')
    def test_share_admin_cannot_run_a_rsync_task_from_the_page(self, navigate_to_rsync_tasks):
        """
        This test verifies that the share admin cannot run a rsync task from the page.
        - Navigate to the data protection page.
        - Click on the Rsync Task header link.
        - Verify the Run button on the Rsync Task page is locked and not clickable as a share admin.
        """
        assert Rsync_Task.assert_run_rsync_task_button_is_restricted('/mnt/tank') is True
