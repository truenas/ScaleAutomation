import allure
import pytest

from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM


@allure.tag("Apps", "WG Easy")
@allure.epic("Apps")
@allure.feature("Apps-Edit")
class Test_Edit_Webdav:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self):
        """
        This method sets up WG Easy app for test
        """
        assert Apps.verify_app_installed('WG Easy') is True

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        """
        This method clears any Apps and Datasets after test is run for a clean environment
        """
        yield
        # Clean up environment.
        Apps.delete_app('WG Easy')
        assert Apps.is_app_installed('WG Easy') is False

    @allure.tag("Update")
    @allure.story("Edit App WG Easy values-Configuration")
    def test_edit_webdav_app_configuration(self):
        """
        This method verifies the WG Easy app configuration values can be edited
        """
        # edit app initial values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('WG-Easy Configuration')
        COM.set_input_field('host', '10.234.27.201')
        COM.set_input_field('password', 'test1234')
        COM.set_input_field('keep-alive', '50')
        COM.set_input_field('client-mtu', '2840')
        COM.set_input_field('client-address-range', '10.16.0.x')
        COM.set_input_field('client-dns-server', '2.2.2.2')
        COM.click_save_button_and_wait_for_progress_bar()
        assert COM.assert_page_header('Installed') is True
        assert Apps.is_app_running('WG Easy') is True

        # verify edited app values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('WG-Easy Configuration')
        assert COM.get_input_property('host') == '10.234.27.201'
        assert COM.get_input_property('password') == 'test1234'
        assert COM.get_input_property('keep-alive') == '50'
        assert COM.get_input_property('client-mtu') == '2840'
        assert COM.get_input_property('client-address-range') == '10.16.0.x'
        assert COM.get_input_property('client-dns-server') == '2.2.2.2'
        COM.click_link('breadcrumb-applications')

    @allure.tag("Update")
    @allure.story("Edit App WG Easy values-Advanced Pod")
    def test_edit_webdav_app_advanced_pod(self):
        """
        This method verifies the WG Easy app advanced pod values can be edited
        """
        # edit app initial values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Advanced Pod Configuration')
        COM.click_button('add-item-dns-options')
        COM.set_input_field('name', 'Option Name')
        COM.set_input_field('value', 'Option Value')
        COM.click_save_button_and_wait_for_progress_bar()
        assert COM.assert_page_header('Installed') is True
        assert Apps.is_app_running('WG Easy') is True

        # verify edited app values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Advanced Pod Configuration')
        assert COM.get_input_property('name') == 'Option Name'
        assert COM.get_input_property('value') == 'Option Value'
        COM.click_link('breadcrumb-applications')

    @allure.tag("Update")
    @allure.story("Edit App WG Easy values-Network")
    def test_edit_webdav_app_network(self):
        """
        This method verifies the WG Easy app network values can be edited
        """
        # edit app initial values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Network Configuration')
        COM.set_input_field('udp-port', '30000')
        COM.set_input_field('web-port', '30001')
        COM.unset_checkbox('host-network')
        COM.click_save_button_and_wait_for_progress_bar()
        assert COM.assert_page_header('Installed') is True
        assert Apps.is_app_running('WG Easy') is True

        # verify edited app values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Network Configuration')
        assert COM.get_input_property('udp-port') == '30000'
        assert COM.get_input_property('web-port') == '30001'
        assert COM.is_checked('host-network') is False
        COM.click_link('breadcrumb-applications')

    @allure.tag("Update")
    @allure.story("Edit App WG Easy values-Storage")
    def test_edit_webdav_app_storage(self):
        """
        This method verifies the WG Easy app storage values can be edited
        """
        # edit app initial values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Storage Configuration')
        COM.click_button('add-item-additional-storage')
        COM.set_input_field('mount-path', '/mnt/anywhere', True)
        COM.set_input_field('dataset-name', 'storage')
        COM.click_save_button_and_wait_for_progress_bar()
        assert COM.assert_page_header('Installed') is True
        assert Apps.is_app_running('WG Easy') is True

        # verify edited app values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Storage Configuration')
        assert COM.get_input_property('mount-path') == '/mnt/anywhere'
        assert COM.get_input_property('dataset-name') == 'storage'
        COM.click_link('breadcrumb-applications')

    @allure.tag("Update")
    @allure.story("Edit App WG Easy values-Resources")
    def test_edit_webdav_app_resources(self):
        """
        This method verifies the WG Easy app resources values can be edited
        """
        # edit app initial values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Resources Configuration')
        COM.set_input_field('cpu', '8000m')
        COM.set_input_field('memory', '16Gi')
        COM.click_save_button_and_wait_for_progress_bar()
        assert COM.assert_page_header('Installed') is True
        assert Apps.is_app_running('WG Easy') is True

        # verify edited app values
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Resources Configuration')
        assert COM.get_input_property('cpu') == '8000m'
        assert COM.get_input_property('memory') == '16Gi'
        COM.click_link('breadcrumb-applications')
