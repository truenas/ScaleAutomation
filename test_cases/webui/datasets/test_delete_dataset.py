import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list('datasets')[2:4], scope='class')
class Test_Delete_Dataset:

    @pytest.fixture(scope='class', autouse=True)
    def setup_test_class(self, data):
        """
        This setup fixture the dataset for the test class.
        """
        assert API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200

    def test_delete_dataset(self, data):
        """
        This test deletes the dataset.
        """
        Navigation.navigate_to_datasets()
        Datasets.delete_dataset(data['pool'], data['dataset'])
        assert Datasets.is_dataset_not_visible(data['dataset'])
