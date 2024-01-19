import pytest
from helper.data_config import get_data_and_name_list
from keywords.api.get import API_GET
from keywords.api.post import API_POST
from keywords.ssh.zpool import Zpool_SSH
from keywords.webui.navigation import Navigation
from keywords.webui.pool_creation_wizard import Pool_Creation_Wizard as PCW
from keywords.webui.storage import Storage


@pytest.mark.parametrize('layout,data', get_data_and_name_list('create-data-pool', 'pool-layout'), scope='class')
class Test_Create_Data_Pool:

    @staticmethod
    def navigate_to_storage_dashboard_page(layout, data):
        """
        This test navigates to storage dashboard page
        """
        Navigation.navigate_to_storage()
        assert Storage.assert_storage_dashboard_page() is True

    @staticmethod
    def click_create_data_pool(layout, data):
        """
        This test clicks on create data pool button
        """
        Storage.click_create_pool_button()
        assert PCW.assert_pool_creation_wizard_page() is True

    @staticmethod
    def on_the_general_info_step_set_the_name_of_the_pool_and_click_next(layout, data):
        """
        This test sets the name of the pool
        """
        assert PCW.assert_step_header_is_open('General Info')
        PCW.set_name_entry(data['pool-name'])
        PCW.click_next_button('general')

    @staticmethod
    def on_the_data_step_set_the_pool_layout_disk_size_width_and_vdevs_and_click_next(layout, data):
        """
        This test sets the pool layout, disk size, width and vdevs
        """
        assert PCW.assert_step_header_is_open('Data')
        PCW.select_layout_option('data', data['pool-layout'])
        PCW.select_disk_size_option('data', '20 GiB (HDD)')  # 20 GiB (HDD)()
        PCW.select_width_option('data', int(data['disk-width']))
        PCW.select_number_of_vdevs_option('data', 1)
        PCW.click_save_and_go_to_review_button('data')

    @staticmethod
    def on_the_review_step_verify_the_data_and_click_create_and_confirm(layout, data):
        """
        This test verifies the review step UI data and click on create button to creates the pool.
        """
        assert PCW.assert_step_header_is_open('Review') is True
        assert PCW.assert_pool_name_value(data['pool-name']) is True
        assert PCW.assert_data_value(data['pool-data']) is True
        assert PCW.assert_est_usable_raw_capacity(data['raw-capacity']) is True
        PCW.click_create_pool_button()
        PCW.click_confirm_waring_dialog()
        assert PCW.assert_create_pool_dialog_not_visible() is True

    @staticmethod
    def on_the_storage_dashboard_page_verify_the_pool_and_the_vdevs_exist_in_ui(layout, data):
        """
        This test verifies the pool and the vdevs exist in the storage dashboard page
        """
        assert Storage.assert_storage_dashboard_page() is True
        assert Storage.is_pool_name_header_visible(data['pool-name']) is True
        assert Storage.assert_pool_data_vdevs_value(data['pool-name'], data['data-vdefs']) is True

    @staticmethod
    def then_verify_the_pool_and_the_type_with_the_api_and_the_zpool_command(layout, data):
        """
        This test verifies the pool and the type with the API and the zpool command
        """
        assert API_GET.get_pool(data['pool-name'])
        assert API_GET.get_pool_type(data['pool-name'])
        assert Zpool_SSH.verify_pool_status_exist(data['pool-name'])
        # The next step is not applicable for Stripe pool.
        if data['cmd-pool-type'] != 'NA':
            assert Zpool_SSH.verify_pool_status_contain_text(data['pool-name'], data['cmd-pool-type'])

    @staticmethod
    def clean_up(layout, data):
        """
        This step remove the pool
        """
        assert API_POST.export_pool(data['pool-name'], True)['state'] == 'SUCCESS'
