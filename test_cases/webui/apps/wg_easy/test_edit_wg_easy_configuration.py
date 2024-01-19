import pytest

from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM


class Test_Edit_WG_Easy_Configuration:

    @staticmethod
    def test_edit_app() -> None:
        """
        This test verifies the app can be edited
        """
        assert Apps.verify_app_installed('WG Easy')
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Network Configuration')
        COM.set_input_field('host', '10.234.27.201')
        COM.set_input_field('password', 'test1234')
        COM.set_input_field('keep-alive', '50')
        COM.set_input_field('client-mtu', '2840')
        COM.set_input_field('client-address-range', '10.16.0.x')
        COM.set_input_field('client-dns-server', '2.2.2.2')
        COM.click_save_button()
        assert COM.assert_page_header('Installed')
        assert Apps.is_app_running('WG Easy')

    @staticmethod
    def verify_edit_values() -> None:
        """
        This test verifies the edited values of the app
        """
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Network Configuration')
        assert COM.get_element_property('host') == '10.234.27.201'
        assert COM.get_element_property('password') == 'test1234'
        assert COM.get_element_property('keep-alive') == '50'
        assert COM.get_element_property('client-mtu') == '2840'
        assert COM.get_element_property('client-address-range') == '10.16.0.x'
        assert COM.get_element_property('client-dns-server') == '2.2.2.2'
        COM.click_link('breadcrumb-applications')

    @staticmethod
    def verify_teardown() -> None:
        """
        This test removes the given app
        """
        # reset the change
        Apps.delete_app('WG Easy')
        assert Apps.is_app_installed('WG Easy') is False
