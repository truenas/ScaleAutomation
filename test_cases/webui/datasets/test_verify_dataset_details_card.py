import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list("datasets")[2:3], scope="class")
class Test_Verify_Dataset_Details_Card:
    """
    Test class for verifying dataset details Card.
    """

    @pytest.fixture(scope='class', autouse=True)
    def setup_test_class(self, data):
        """
        This setup fixture creates a dataset for the test class.
        """
        assert API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200

    def test_verify_dataset_ui_details(self, data):
        """
        This test verifies some of the dataset UI details.
        """
        # Navigate to Datasets page.
        Navigation.navigate_to_datasets()

        Datasets.click_dataset_location(data['dataset'])
        assert Common.is_card_visible('Dataset Details') is True
        assert Datasets.assert_details_type('FILESYSTEM') is True
        assert Datasets.assert_details_sync('STANDARD') is True
        assert Datasets.assert_details_compression_level('Inherit (LZ4)') is True
        assert Datasets.assert_details_enable_atime('OFF') is True
        assert Datasets.assert_details_zfs_deduplication('OFF') is True
        assert Datasets.assert_details_case_sensitivity('ON') is True
        assert Datasets.assert_details_path(f'{data["pool"]}/{data["dataset"]}') is True

        assert Datasets.assert_edit_dataset_button() is True
        assert Datasets.assert_delete_dataset_button() is True

    def test_verify_dataset_edit_button(self, data):
        """
        This test verifies the edit dataset button.
        """
        Navigation.navigate_to_datasets()
        Datasets.click_dataset_location(data['dataset'])
        assert Common.is_card_visible('Dataset Details') is True
        assert Datasets.assert_edit_dataset_button() is True
        Datasets.click_edit_dataset_button()
        assert Common.assert_right_panel_header('Edit Dataset') is True
        Common.close_right_panel()


    @pytest.fixture(scope='class', autouse=True)
    def tear_down_class(self, data):
        """
        This fixture deletes the dataset created for the test class.
        """
        yield
        assert API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}').status_code == 200