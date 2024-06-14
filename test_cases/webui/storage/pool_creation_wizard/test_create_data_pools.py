import allure
import pytest
from helper.data_config import get_data_and_name_list
from keywords.api.get import API_GET
from keywords.api.post import API_POST
from keywords.ssh.zpool import Zpool_SSH
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation
from keywords.webui.pool_creation_wizard import Pool_Creation_Wizard as PCW
from keywords.webui.storage import Storage


@pytest.mark.parametrize('layout,data', get_data_and_name_list('create-data-pool', 'pool-layout'), scope='class')
@allure.tag("Pool Creation Wizard")
@allure.epic("Storage")
@allure.feature("Pool Creation Wizard")
class Test_Create_Data_Pool:
    """
    Test cases for creating data pools with the Pool Creation Wizard.
    """

    @allure.tag("Create")
    @allure.story("Create Pool With Data Disks Only")
    def test_create_a_pool_with_data_disk_only(self, layout, data):
        """
        This method test create data disks pools with the given data from the Pool Creation Wizard UI.
        """
        # Navigate to storage dashboard page
        Navigation.navigate_to_storage()
        assert Storage.assert_storage_dashboard_page() is True

        # Click on create data pool button
        Storage.click_create_pool_button()
        assert PCW.assert_pool_creation_wizard_page() is True

        # On the general info step set the name of the pool
        assert Common.assert_step_header_is_open('General Info')
        assert Common.assert_progress_bar_not_visible() is True
        PCW.set_name_entry(data['pool-name'])
        PCW.click_next_button('general')

        # On the data step set the pool layout, disk size, width and vdevs
        assert Common.assert_step_header_is_open('Data')
        assert Common.assert_progress_bar_not_visible() is True
        PCW.select_layout_option('data', data['pool-layout'])
        PCW.select_disk_size_option('data', '1.82 GiB (HDD)')
        PCW.select_width_option('data', int(data['disk-width']))
        PCW.select_number_of_vdevs_option('data', 1)
        PCW.click_save_and_go_to_review_button('data')

        # On the review step UI verify the data, then click on create button to creates the pool
        assert Common.assert_step_header_is_open('Review') is True
        assert Common.assert_progress_bar_not_visible() is True
        assert PCW.assert_pool_name_value(data['pool-name']) is True
        assert PCW.assert_data_value(data['pool-data']) is True
        assert PCW.assert_est_usable_raw_capacity(data['raw-capacity']) is True
        PCW.click_create_pool_button()
        PCW.click_confirm_waring_dialog()
        assert PCW.assert_create_pool_dialog_not_visible() is True

        # Verify the pool and the vdevs exist in the storage dashboard page
        assert Storage.assert_storage_dashboard_page() is True
        assert Storage.is_pool_name_header_visible(data['pool-name']) is True
        assert Storage.assert_pool_data_vdevs_value(data['pool-name'], data['data-vdefs']) is True

        # Verify the pool and the type with the API and the zpool command
        assert API_GET.get_pool(data['pool-name'])
        assert API_GET.get_pool_type(data['pool-name'])
        assert Zpool_SSH.verify_pool_status_exist(data['pool-name'])
        # The next step is not applicable for a Stripe pool.
        if data['cmd-pool-type'] != 'NA':
            assert Zpool_SSH.verify_pool_status_contain_text(data['pool-name'], data['cmd-pool-type'])

    @pytest.fixture(scope='class', autouse=True)
    def tear_down_test(self, layout, data):
        """
        This step remove the pool with the API call.
        """
        yield
        assert API_POST.export_pool(data['pool-name'], True)['state'] == 'SUCCESS'
