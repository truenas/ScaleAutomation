import allure
import pytest
from helper.global_config import shared_config
from keywords.api.common import API_Common
from keywords.webui.advanced import Advanced
from keywords.webui.common import Common as COM


@allure.tag('Share Admin', 'Jobs', 'Tasks', 'Permissions')
@allure.epic('permissions')
@allure.feature('Share Admin')
class Test_Share_Admin_Jobs_Task:

    @pytest.fixture(autouse=True, scope='class')
    def setup_test(self):
        """
        This fixture gets a debug to create a job that will be used in the test.
        """
        Advanced.get_debug_files()
        # get a job ID that will be used in the test
        shared_config['JOB_ID'] = API_Common.get_a_job_id('system.debug', 'method')

    @allure.story('Share Admin Can View the List of Jobs and Tasks that They Have Triggered')
    def test_share_admin_can_view_the_list_of_jobs_and_tasks_that_they_have_triggered(self):
        """
        This test verifies the share admin is able to view the list of jobs and tasks that they have triggered.
        1. Click on Jobs Manager button
        2. Click on History button
        3. Verify is able to view the list of jobs and tasks that they have triggered.
        """
        COM.click_button('jobs-manager')
        assert COM.assert_right_panel_header('Jobs') is True
        COM.click_button('history')
        assert COM.assert_page_header('Jobs')
        assert COM.is_row_visible(f'job-{shared_config["JOB_ID"]}') is True
        assert COM.assert_text_is_visible('system.debug') is True
        assert COM.assert_text_is_visible('SUCCESS') is True
