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

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def create_dataset(data):
        """
        This test adds the dataset for the test case.
        """
        API_POST.create_dataset(f'{data["pool"]}/{data["dataset"]}')

    @staticmethod
    def navigate_to_datasets(data):
        """
        This test navigates to datasets page.
        """
        Navigation.navigate_to_datasets()
        Datasets.assert_datasets_page_header()

    @staticmethod
    def select_the_pool_then_click_edit_dataset_space_button_on_the_space_management_card(data):
        """
        This test selects the pool and click edit dataset space button on the space management card.
        """
        Datasets.select_dataset(data["pool"])
        assert Datasets.is_space_management_card_visible() is True
        Datasets.click_edit_dataset_space_button()

    @staticmethod
    def on_the_capacity_settings_panel_set_quota_for_dataset_and_all_children_to_8_gib_and_save(data):
        """
        This test on the capacity settings panel set quota for dataset and all children to 8 GiB.
        """
        assert Datasets.is_capacity_settings_right_panel_visible()
        Datasets.set_quota_for_this_dataset('8 GiB')
        Datasets.set_quota_for_this_dataset_and_all_children('8 GiB')
        assert Common.click_save_button_and_wait_for_progress_bar() is True

    @staticmethod
    def verify_the_pool_quota_for_dataset_and_all_children_is_8_gib(data):
        """
        This test verifies the system quota for dataset and all children is 8 GiB.
        """
        assert Datasets.assert_space_available_to_dataset_size('8 GiB')
        assert Datasets.assert_applied_dataset_quota_size('8 GiB')

    @staticmethod
    def select_the_dataset_and_verify_the_space_available_and_applied_inherited_quotas_size_are_8_gib(data):
        """
        This test selects the dataset and verify the space available and applied inherited quotas size are 8 GiB.
        """
        Datasets.select_dataset(data["dataset"])
        assert Datasets.assert_space_available_to_dataset_size('8 GiB') is True
        assert Datasets.assert_applied_inherited_quotas_size(f'8 GiB from {data["pool"]}') is True

    @staticmethod
    def click_on_the_dataset_space_management_edit_button_and_set_reserved_space_for_dataset_and_children_to_2_gib(data):
        """
        This test click on the dataset space management edit button and set reserved space for dataset and children to 2 GiB.
        """
        Datasets.click_edit_dataset_space_button()
        assert Datasets.is_capacity_settings_right_panel_visible()
        Datasets.set_reserved_space_for_this_dataset('2 GiB')
        Datasets.set_reserved_space_for_this_dataset_and_all_children('2 GiB')
        assert Common.click_save_button_and_wait_for_progress_bar() is True

    @staticmethod
    def verify_the_system_reserved_space_for_dataset_and_all_children_is_2_gib(data):
        """
        This test verifies the system reserved space for dataset and all children is 2 GiB.
        """
        assert Datasets.assert_reserved_for_dataset_size('2 GiB') is True
        assert Datasets.assert_reserved_for_dataset_and_children_size('2 GiB') is True

    @staticmethod
    @pytest.fixture(scope='class', autouse=True)
    def remove_pool_and_delete_dataset(data):
        """
        This test removes the quotas for on the pool dataset and remove the dataset.
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
