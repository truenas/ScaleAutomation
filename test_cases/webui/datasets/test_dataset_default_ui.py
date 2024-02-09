import pytest
from helper.global_config import shared_config
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.random_order(disabled=True)
class Test_Dataset_Default_UI:
    @staticmethod
    def navigate_to_datasets():
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()
        Datasets.click_dataset_location('tank')

    @staticmethod
    def verify_dataset_search_and_tree():
        assert Datasets.assert_search_field() is True
        assert Datasets.assert_dataset_tree() is True

    @staticmethod
    @pytest.mark.parametrize("card", shared_config['DATASET_CARDS'])
    def verify_card_visible_(card):
        assert Common.is_card_visible(card) is True

    @staticmethod
    def verify_dataset_default_buttons():
        assert Datasets.assert_add_zvol_button() is True
        assert Datasets.assert_add_dataset_button() is True
