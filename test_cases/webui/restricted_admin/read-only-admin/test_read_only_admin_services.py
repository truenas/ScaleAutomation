import pytest
from helper.global_config import shared_config
from keywords.webui.common import Common
from keywords.webui.navigation import Navigation
from keywords.webui.system_services import System_Services


@pytest.mark.parametrize('service_name', shared_config['SERVICE_NAMES'])
class Test_Read_Only_Admin_Services:

    @pytest.fixture(autouse=True, scope='class')
    def setup_class(self):
        """
        This method navigates to the System Settings Services page.
        """
        Navigation.navigate_to_system_settings_services()

    # Read-only admins shall be able to view the services and their states
    def test_read_only_admin_can_see_the_system_services_and_there_states(self, service_name):
        """
        This test verifies the read-only admin can see the services and their states.
        1. Verify the service for and name is visible
        2. Verify the service running toggle is state is visible.
        3. Verify the service autostart checkbox is state is visible.
        """
        assert System_Services.is_service_row_visible(service_name) is True
        assert Common.is_text_visible(service_name) is True
        # Only verify the status is visible true or false does not matter.
        assert System_Services.is_service_running_toggle_enabled(service_name) in [True, False]
        assert System_Services.is_service_autostart_set_by_name(service_name) in [True, False]

    def test_read_only_admin_cannot_modify_system_services(self, service_name):
        """
        This test verifies the read-only admin cannot modify system services, states and whether they are
        started automatically.
        1. Verify the service running toggle is restricted
        2. Verify the service autostart checkbox is restricted
        3. Verify the service edit button is restricted
        """
        System_Services.is_service_running_toggle_restricted(service_name)
        System_Services.is_service_autostart_checkbox_restricted(service_name)
        System_Services.is_service_edit_button_restricted(service_name)
