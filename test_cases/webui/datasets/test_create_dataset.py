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

    @pytest.fixture(scope='function', autouse=True)
    def setup_class(self, data):
        """
        This fixture deletes the created dataset for the class.
        """
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}')

    @pytest.fixture(scope='function', autouse=True)
    def teardown_class(self, data):
        """
        This fixture deletes the created dataset for the class.
        """
        yield
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}')

    def test_create_dataset(seff, data):
        """
        This test navigates to datasets page.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

        # Select the pool and click on add dataset.
        Datasets.select_dataset(data["pool"])
        Datasets.click_add_dataset_button()

        # Create a dataset and save it.
        Common.assert_right_panel_header('Add Dataset')
        Datasets.set_dataset_name(data["dataset"])
        Common.click_save_button_and_wait_for_progress_bar()

        # Verify that the created dataset exists in the datasets page.
        Datasets.is_dataset_visible(data["pool"], data["dataset"])
