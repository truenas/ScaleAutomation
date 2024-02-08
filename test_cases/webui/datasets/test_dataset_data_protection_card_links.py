import pytest
from helper.global_config import shared_config
from helper.data_config import get_data_list
from keywords.api.delete import API_DELETE
from keywords.api.post import API_POST
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.random_order(disabled=True)
@pytest.mark.parametrize('data', get_data_list('datasets')[5:6], scope='class')
class Test_Dataset_Data_Protection_Card_Links:
    """
    Test class for dataset data protection card links.
    """
    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def create_dataset(data):
        """
        This test creates a dataset for the test case.
        """
        assert API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200

    @staticmethod
    @pytest.mark.parametrize('link', shared_config['DATA_PROTECTION_LINKS'])
    def navigate_to_datasets_page_and_on_the_dataset_click_data_protection_link(data, link):
        """
        This test navigates to datasets page and on the dataset click data protection link.
        """
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()
        Datasets.select_dataset(data["dataset"])
        assert Datasets.click_protection_manage_link(link) is True

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def delete_dataset(data):
        """
        This test deletes the dataset created for the test case.
        """
        yield
        assert API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200
