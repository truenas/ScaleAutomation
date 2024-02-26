from keywords.webui.common import Common
from keywords.webui.navigation import Navigation
from keywords.webui.datasets import Datasets


class Test_Navigate_Datasets:

    def test_navigate_datasets_to_add_dataset(self):
        """
        This test navigates to the datasets page and add a dataset.
        """
        # Navigate to Datasets page.
        Navigation.navigate_to_datasets()

        # Click on add dataset.
        Datasets.click_add_dataset_button()
        Common.assert_right_panel_header('Add Dataset')
        Common.close_right_panel()

    def test_navigate_datasets_to_add_zvol(self):
        """
        This test navigates to the datasets page and add a zpool.
        """
        # Navigate to Datasets page.
        Navigation.navigate_to_datasets()

        # Click on add zvol.
        Datasets.click_add_zvol_button()
        Common.assert_right_panel_header('Add Zvol')
        Common.close_right_panel()
