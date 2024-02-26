import pytest
from helper.global_config import shared_config
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


class Test_Dataset_Default_UI:
    """
    Test cases for dataset default UI.
    """
    @pytest.fixture(autouse=True, scope='class')
    def setup_test_class(self):
        """
        This setup fixture navigates to the datasets page and selects the dataset for each test method.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()
        Datasets.click_dataset_location('tank')

    def verify_dataset_search_and_tree(self):
        """
        Verify that the search field and the dataset tree are visible.
        """
        assert Datasets.assert_search_field() is True
        assert Datasets.assert_dataset_tree() is True

    @pytest.mark.parametrize("card", shared_config['DATASET_CARDS'])
    def verify_card_visible_(self, card):
        """
        Verify that the given card is visible.
        """
        assert Common.is_card_visible(card) is True

    def verify_dataset_default_buttons(self):
        """
        Verify that the dataset default buttons are visible.
        """
        assert Datasets.assert_add_zvol_button() is True
        assert Datasets.assert_add_dataset_button() is True
