import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list('datasets')[6:], scope='class')
class Test_Access_Dataset_Managing_User_Quotas:
    """
    This test verifies the access to dataset managing user quotas
    """

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def create_dataset(data):
        """
        This test adds the dataset for the test.
        """
        API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}')

    @staticmethod
    def navigate_to_datasets(data):
        """
        This test navigates to datasets page
        """
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

    @staticmethod
    def select_the_pool_then_the_dataset(data):
        """
        This test selects the pool and dataset
        """
        Datasets.select_dataset(data["pool"])
        Datasets.select_dataset(data["dataset"])

    @staticmethod
    def on_the_space_management_card_click_on_the_user_quotas_and_verify_the_page_open(data):
        """
        This test verifies the user quotas page
        """
        assert Datasets.is_space_management_card_visible()
        Datasets.click_manage_user_quotas_link()
        assert Datasets.is_user_quotas_page_visible()

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def delete_dataset(data):
        """
        This test removes the dataset
        """
        yield
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}')
