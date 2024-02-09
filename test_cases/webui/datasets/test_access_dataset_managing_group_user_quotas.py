import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list('datasets')[6:], scope='class')
class Test_Access_Dataset_Managing_Group_And_User_Quotas:
    """
    This test class verifies the group quotas and user quotas pages.
    """

    @pytest.fixture(scope='class', autouse=True)
    def setup_test_class(self, data):
        """
        This setup fixture creates a dataset for the test class.
        """
        API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}')

    @pytest.fixture(scope='function', autouse=True)
    def setup_test_method(self, data):
        """
        This setup fixture navigates to the datasets page and selects the dataset for each test method.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

        # Select the pool and the dataset
        Datasets.select_dataset(data["pool"])
        Datasets.select_dataset(data["dataset"])

    def test_access_dataset_managing_group_quotas(self, data):
        """
        This test verifies the group quotas page open.
        """
        # Verify the group quotas page for the given dataset opens.
        assert Datasets.is_space_management_card_visible()
        Datasets.click_manage_group_quotas_link()
        assert Datasets.is_group_quotas_page_visible()

    def test_access_dataset_managing_user_quotas(self, data):
        """
        This test verifies the user quotas page open.
        """
        # Verify the user quotas page for the given dataset opens.
        assert Datasets.is_space_management_card_visible()
        Datasets.click_manage_user_quotas_link()
        assert Datasets.is_user_quotas_page_visible()

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_class(self, data):
        """
        This tear down fixture deletes the created dataset.
        """
        yield
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}')
