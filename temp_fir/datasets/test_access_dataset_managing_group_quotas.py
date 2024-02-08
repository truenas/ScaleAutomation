import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list('datasets')[6:], scope='class')
class Test_Access_Dataset_Managing_Group_Quotas:
    """
    This test cases verifies the access to dataset managing user quotas.
    """

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def create_dataset(data):
        """
        This method creates a dataset for the test case.
        """
        API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}')

    @staticmethod
    def navigate_to_datasets(data):
        """
        This method navigates to datasets page.
        """
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

    @staticmethod
    def select_the_pool_then_the_dataset(data):
        Datasets.select_dataset(data["pool"])
        Datasets.select_dataset(data["dataset"])

    @staticmethod
    def on_the_space_management_card_click_on_the_group_quotas_and_verify_the_page_open(data):
        """
        This test verifies the group quotas page for the given dataset opens.
        """
        assert Datasets.is_space_management_card_visible()
        Datasets.click_manage_group_quotas_link()
        assert Datasets.is_group_quotas_page_visible()

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def delete_dataset(data):
        """
        This method deletes the created dataset.
        """
        yield
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}')
