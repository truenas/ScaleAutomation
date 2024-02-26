import pytest
from helper.data_config import get_data_list
from keywords.api.post import API_POST
from keywords.api.delete import API_DELETE
from keywords.webui.common import Common
from keywords.webui.datasets import Datasets
from keywords.webui.navigation import Navigation


@pytest.mark.parametrize('data', get_data_list('datasets')[6:], scope='class')
class Test_Dataset_Access_Editing_Capacity_Setting:
    """
    This test class verifies user quotas can be access and edited.
    """

    @pytest.fixture(scope='class', autouse=True)
    def setup_test_class(self, data):
        """
        This setup fixture create the dataset for the test class.
        """
        API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}')

    def test_dataset_access_editing_capacity_setting(self, data):
        """
        This test navigates to datasets page.
        """
        # Navigate to Datasets page
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

        # Selects the pool and click edit dataset space button on the space management card.
        Datasets.select_dataset(data["pool"])
        assert Datasets.is_space_management_card_visible() is True
        Datasets.click_edit_dataset_space_button()

        # On the capacity settings panel set quota for dataset and all children to 8 GiB.
        assert Datasets.is_capacity_settings_right_panel_visible()
        Datasets.set_quota_for_this_dataset('8 GiB')
        Datasets.set_quota_for_this_dataset_and_all_children('8 GiB')
        assert Common.click_save_button_and_wait_for_progress_bar() is True

        # Verify the system quota for dataset and all children is 8 GiB.
        assert Datasets.assert_space_available_to_dataset_size('8 GiB')
        assert Datasets.assert_applied_dataset_quota_size('8 GiB')

        # Select the dataset and verify the space available and applied inherited quotas size are 8 GiB.
        Datasets.select_dataset(data["dataset"])
        assert Datasets.assert_space_available_to_dataset_size('8 GiB') is True
        assert Datasets.assert_applied_inherited_quotas_size(f'8 GiB from {data["pool"]}') is True

        # Click on the dataset space management edit button and set reserved space for
        # dataset and children to 2 GiB.
        Datasets.click_edit_dataset_space_button()
        assert Datasets.is_capacity_settings_right_panel_visible()
        Datasets.set_reserved_space_for_this_dataset('2 GiB')
        Datasets.set_reserved_space_for_this_dataset_and_all_children('2 GiB')
        assert Common.click_save_button_and_wait_for_progress_bar() is True

        # Verify the system reserved space for dataset and all children is 2 GiB.
        assert Datasets.assert_reserved_for_dataset_size('2 GiB') is True
        assert Datasets.assert_reserved_for_dataset_and_children_size('2 GiB') is True

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_test_class(self, data):
        """
        This tear down fixture removes the quotas for on the pool dataset and remove the dataset
        for the test class.
        """
        yield
        Datasets.select_dataset(data["pool"])
        assert Datasets.is_space_management_card_visible() is True
        Datasets.click_edit_dataset_space_button()
        assert Datasets.is_capacity_settings_right_panel_visible() is True
        Datasets.unset_quota_for_this_dataset()
        Datasets.unset_quota_for_this_dataset_and_all_children()
        assert Common.click_save_button_and_wait_for_progress_bar() is True
        API_DELETE.delete_dataset(f'{data["pool"]}/{data["dataset"]}')
