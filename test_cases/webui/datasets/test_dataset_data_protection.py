import pytest
from helper.global_config import shared_config
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list('datasets')[5:6], scope='class')
class Test_Dataset_Data_Protection:
    """
    Test class for dataset data protection card links.
    """
    @pytest.fixture(scope='class', autouse=True)
    def setup_test_class(self, data):
        """
        This test creates a dataset for the test case.
        """
        assert API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200

    @pytest.mark.parametrize('link', shared_config['DATA_PROTECTION_LINKS'])
    def test_dataset_data_protection_card_links(self, data, link):
        """
        This test navigates to datasets page and on the dataset click data protection link.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()
        Datasets.select_dataset(data["dataset"])

        # Click on data protection link and verify that the page of the link opens.
        assert Datasets.assert_click_protection_manage_link_works(link) is True

    def test_dataset_data_protection_navigate_add_snapshot(self, data):
        """
        This test verify verity the snapshot opens on the datasets page.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()
        Datasets.select_dataset(data["dataset"])

        # Click on add snapshot button and verify that the add snapshot right panel is visible.
        Datasets.click_create_snapshot_button()
        assert Datasets.is_add_snapshot_right_panel_visible() is True
        Common.close_right_panel()

    @pytest.mark.parametrize('task', shared_config['DATASET_PROTECTION_TASKS'])
    def test_dataset_protection_tasks_values_is_visible(self, data, task):
        """
        This test verifies the dataset protection tasks is visible and its value exists.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()
        Datasets.select_dataset(data["dataset"])

        # Verify that the dataset value exists in the data protection card.
        assert Datasets.is_protection_task_visible(task) is True
        # With a new dataset the value is 0.
        assert Datasets.get_protection_task_value(task) == '0'

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_class(self, data):
        """
        This test deletes the dataset created for the test class.
        """
        yield
        assert API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200
