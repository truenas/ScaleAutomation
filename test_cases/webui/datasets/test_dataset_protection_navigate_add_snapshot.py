import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation

@pytest.mark.random_order(disabled=True)
@pytest.mark.parametrize('data', get_data_list('datasets')[5:6], scope='class')
class Test_Dataset_Protection_Navigate_Add_Snapshot:
    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def create_dataset(data):
        """
        This fixture creates a dataset for the test cass.
        """
        assert API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200

    @staticmethod
    def on_the_datasets_page_verify_the_snapshot_opens(data):
        """
        This test verify verity the snapshot opens on the datasets page.
        """
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()
        Datasets.select_dataset(data["dataset"])
        Datasets.click_create_snapshot_button()
        assert Datasets.is_add_snapshot_right_panel_visible() is True
        Common.close_right_panel()

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def delete_dataset(data):
        """
        This fixture deletes the dataset created for the test cass.
        """
        yield
        assert API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200
