import pytest

import xpaths
from helper.global_config import private_config
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.system_services import System_Services as SERV


class Test_System_Services:
    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method navigates to the System Settings Services page.
        """
        NAV.navigate_to_system_settings_services()
        assert COM.assert_page_header("Services") is True

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        """
        This method navigates to the Dashboard at the end of the test.
        """
        yield
        SERV.stop_all_services_by_api()
        SERV.set_all_services_autostart_off_by_api()
        SERV.set_service_autostart_on_by_api('SMART')
        SERV.start_service_by_api('SMART')
        if COM.is_visible(xpaths.common_xpaths.close_right_panel()):
            COM.close_right_panel()
        NAV.navigate_to_dashboard()

    @pytest.mark.parametrize('services', get_data_list('system_services'), scope='function')
    def test_verify_system_services_start(self, services):
        """
        This test verifies the that the system services can be started via the WebUI
        """
        runnable_bool = eval(services['runnable'])
        error_dialog_bool = eval(services['error_dialog'])
        SERV.stop_service_by_api(services['service_name'])
        assert SERV.is_service_status_running_by_name(services['service_name']) is False
        SERV.start_service_by_name(services['service_name'], error_dialog_bool, runnable_bool)
        assert SERV.is_service_status_running_by_name(services['service_name']) is runnable_bool
        SERV.stop_service_by_api(services['service_name'])

    @pytest.mark.parametrize('services', get_data_list('system_services'), scope='function')
    def test_verify_system_services_stop(self, services):
        """
        This test verifies the that the system services can be stopped via the WebUI
        """
        runnable_bool = eval(services['runnable'])
        if runnable_bool:
            SERV.start_service_by_api(services['service_name'])
            assert SERV.is_service_status_running_by_name(services['service_name']) is True
            SERV.stop_service_by_name(services['service_name'])
            assert SERV.is_service_status_running_by_name(services['service_name']) is False
            SERV.stop_service_by_api(services['service_name'])

    def test_verify_system_services_do_autostart_on_reboot(self):
        """
        This test verifies the that the system services will auto start when set to via WebUI.
        """
        SERV.stop_all_services_by_api()
        SERV.set_all_services_autostart_on()
        SERV.assert_all_services_autostart_on()
        SERV.assert_all_services_not_running()
        COM.reboot_system()
        COM.set_login_form(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_system_settings_services()
        SERV.assert_all_services_autostart_on()
        SERV.assert_all_services_running()

    def test_verify_system_services_do_not_autostart_on_reboot(self):
        """
        This test verifies the that the system services will not auto start when not set via WebUI.
        """
        SERV.stop_all_services_by_api()
        SERV.set_all_services_autostart_off()
        SERV.assert_all_services_autostart_off()
        SERV.assert_all_services_not_running()
        COM.reboot_system()
        COM.set_login_form(private_config['USERNAME'], private_config['PASSWORD'])
        NAV.navigate_to_system_settings_services()
        SERV.assert_all_services_autostart_off()
        SERV.assert_all_services_not_running()

    def test_verify_ftp_service_edit_ui(self):
        """
        This test verifies the edit UI for the FTP service.
        """
        SERV.click_service_edit_button('FTP')
        assert COM.assert_right_panel_header('FTP') is True
        assert SERV.verify_ftp_service_edit_ui() is True
        COM.close_right_panel()
        assert COM.assert_page_header("Services") is True

