import pytest

from helper.data_config import get_data_list
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.system_services import System_Services as SERV


@pytest.mark.parametrize('services', get_data_list('system_services'), scope='class')
class Test_System_Services:

    @pytest.fixture(scope='function', autouse=True)
    def setup_test(self) -> None:
        """
        This method navigates to the System Settings Services page.
        """
        NAV.navigate_to_system_settings_services()

    @pytest.fixture(scope='function', autouse=True)
    def teardown_test(self):
        """
        This method navigates to the Dashboard at the end of the test.
        """
        yield
        NAV.navigate_to_dashboard()

    @classmethod
    def test_verify_system_services_start(cls, services) -> None:
        """
        This test verifies the that the system services can be started via the WebUI
        """
        runnable_bool = eval(services['runnable'])
        error_dialog_bool = eval(services['error_dialog'])
        SERV.stop_service_by_api(services['service_name'])
        assert not SERV.is_service_status_running_by_name(services['service_name'])
        SERV.start_service_by_name(services['service_name'], error_dialog_bool, runnable_bool)
        assert SERV.is_service_status_running_by_name(services['service_name']) is runnable_bool
        SERV.stop_service_by_api(services['service_name'])

    @classmethod
    def test_verify_system_services_stop(cls, services) -> None:
        """
        This test verifies the that the system services can be stopped via the WebUI
        """
        runnable_bool = eval(services['runnable'])
        if runnable_bool:
            SERV.start_service_by_api(services['service_name'])
            SERV.is_service_status_running_by_name(services['service_name'])
            SERV.stop_service_by_name(services['service_name'])
            assert not SERV.is_service_status_running_by_name(services['service_name'])
            SERV.stop_service_by_api(services['service_name'])
