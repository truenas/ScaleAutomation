import pytest
from helper.data_config import get_data_list
from helper.global_config import shared_config
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list('datasets')[5:6], scope='class')
class Test_Verify_Dataset_Protection_Tasks_Values:
    """
    The test class for verifying the dataset protection tasks values.
    """
    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def create_dataset_and_navigate_to_datasets_page(data):
        """
        This fixture creates a dataset for the test cass.
        """
        assert API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

    @staticmethod
    @pytest.mark.parametrize('task', shared_config['DATASET_PROTECTION_TASKS'])
    def verify_dataset_protection_tasks_and_value(data, task):
        """
        This test verifies the dataset protection tasks is visible and its value is not empty.
        """
        Datasets.select_dataset(data["dataset"])
        assert Datasets.is_protection_task_visible(task) is True
        # With a new dataset the value is 0.
        assert Datasets.get_protection_task_value(task) == '0'

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def delete_dataset(data):
        """
        This fixture deletes the dataset created for the test cass.
        """
        yield
        assert API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200
