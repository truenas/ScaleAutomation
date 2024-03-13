import allure
import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@allure.tag("Datasets", "Dataset Space Management")
@allure.epic("Datasets")
@allure.feature("Dataset Space Management")
@pytest.mark.parametrize('data', get_data_list('datasets')[6:], scope='class')
class Test_Access_Dataset_Space_Management:
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
    def navigate_to_dataset(self, data):
        """
        This setup fixture navigates to the datasets page for each test method.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

    @allure.tag("Read")
    @allure.story("Dataset Space Management Details")
    def test_pool_dataset_space_management_details(self, data):
        """
        This test verifies the space management card details.
        """
        Datasets.select_dataset(data["pool"])
        assert Datasets.is_space_management_card_visible()

        assert Datasets.assert_total_allocation_size('GiB') is True
        assert Datasets.assert_data_written_size('KiB') is True
        assert Datasets.assert_children_size('GiB') is True

        assert Datasets.assert_space_available_to_dataset_size('GiB') is True
        assert Datasets.assert_user_quotas('Quotas set for ') is True
        assert Datasets.assert_user_quotas(' user') is True
        assert Datasets.assert_user_quotas(' user') is True

        assert Datasets.assert_group_quotas('Quotas set for ') is True
        assert Datasets.assert_group_quotas(' group') is True

    @allure.tag("Read")
    @allure.story("Dataset Space Management Details")
    def test_dataset_space_management_details(self, data):
        # Select the pool and the dataset
        Datasets.select_dataset(data["pool"])
        Datasets.select_dataset(data["dataset"])
        assert Datasets.is_space_management_card_visible() is True

        assert Datasets.assert_total_allocation_size('KiB') is True
        assert Datasets.assert_data_written_size('KiB') is True
        assert Datasets.assert_space_available_to_dataset_size('GiB') is True

        assert Datasets.assert_user_quotas('Quotas set for ') is True
        assert Datasets.assert_user_quotas(' user') is True

        assert Datasets.assert_group_quotas('Quotas set for ') is True
        assert Datasets.assert_group_quotas(' group') is True

    @allure.tag("Read")
    @allure.story("Access Dataset Managing Group Quotas")
    def test_access_dataset_managing_group_quotas(self, data):
        """
        This test verifies the group quotas page open.
        """
        # Select the pool and the dataset
        Datasets.select_dataset(data["pool"])
        Datasets.select_dataset(data["dataset"])
        # Verify the group quotas page for the given dataset opens.
        assert Datasets.is_space_management_card_visible() is True
        Datasets.click_manage_group_quotas_link(data['pool'], data['dataset'])
        assert Datasets.is_group_quotas_page_visible() is True

    @allure.tag("Read")
    @allure.story("Access Dataset Managing User Quotas")
    def test_access_dataset_managing_user_quotas(self, data):
        """
        This test verifies the user quotas page open.
        """
        # Select the pool and the dataset
        Datasets.select_dataset(data["pool"])
        Datasets.select_dataset(data["dataset"])

        # Verify the user quotas page for the given dataset opens.
        assert Datasets.is_space_management_card_visible() is True
        Datasets.click_manage_user_quotas_link(data['pool'], data['dataset'])
        assert Datasets.is_user_quotas_page_visible() is True

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_class(self, data):
        """
        This tear down fixture deletes the created dataset.
        """
        yield
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}')
