from keywords.webui.apps import Apps
from keywords.webui.common import Common as COM


class Test_Edit_WG_Easy_Network:

    @staticmethod
    def test_edit_app() -> None:
        """
        This test verifies the app can be edited
        """
        assert Apps.verify_app_installed('WG Easy')
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Network Configuration')
        COM.set_input_field('udp-port', '30000')
        COM.set_input_field('web-port', '30001')
        COM.unset_checkbox('host-network')
        COM.click_save_button_and_wait_for_progress_bar()
        assert COM.assert_page_header('Installed')
        assert Apps.is_app_running('WG Easy')

    @staticmethod
    def verify_edit_values() -> None:
        """
        This test verifies the edited values of the app
        """
        Apps.edit_app('WG Easy')
        Apps.navigate_to_app_section('Network Configuration')
        assert COM.get_input_property('udp-port') == '30000'
        assert COM.get_input_property('web-port') == '30001'
        assert COM.is_checked('host-network') is False
        COM.click_link('breadcrumb-applications')

    @staticmethod
    def verify_teardown() -> None:
        """
        This test removes the given app
        """
        # reset the change
        Apps.delete_app('WG Easy')
        assert Apps.is_app_installed('WG Easy') is False
