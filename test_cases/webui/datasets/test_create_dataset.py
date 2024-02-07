import pytest
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list('datasets')[2:4], scope='class')
class Test_Create_Dataset:
    """
    This test cass creates a dataset and verifies it is in the datasets page.
    """
    @staticmethod
    def navigate_to_datasets(data):
        """
        This test navigates to datasets page.
        """
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

    @staticmethod
    def select_the_pool_dataset_and_click_on_add_dataset(data):
        """
        This test selects the pool and click on add dataset.
        """
        Datasets.select_dataset(data["pool"])
        Datasets.click_add_dataset_button()

    @staticmethod
    def on_add_dataset_right_panel_create_a_dataset_and_save_it(data):
        """
        This test creates a dataset and save it.
        """
        Common.assert_right_panel_header('Add Dataset')
        Datasets.set_dataset_name(data["dataset"])
        Common.click_save_button()
        Common.assert_progress_bar_not_visible()

    @staticmethod
    def verify_the_created_dataset_exists_in_the_datasets_page(data):
        """
        This test verifies the created dataset exists in the datasets page.
        """
        Datasets.is_dataset_visible(data["pool"], data["dataset"])

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def delete_dataset(data):
        """
        This test removes the created dataset.
        """
        yield
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}')