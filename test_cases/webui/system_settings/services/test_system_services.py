import pytest

import xpaths
from helper.global_config import private_config
from helper.data_config import get_data_list
from keywords.webui.common import Common as COM
from keywords.webui.system_services import System_Services as SERV
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.ftp import FTP
from keywords.webui.iscsi import iSCSI
from keywords.webui.nfs import NFS
from keywords.webui.smart import SMART
from keywords.webui.smb import SMB
from keywords.webui.snmp import SNMP
from keywords.webui.ssh_connection import SSH_Connection as SSH
from keywords.webui.ups import UPS


class Test_System_Services:
    @pytest.fixture(scope='class', autouse=True)
    def setup_class(self) -> None:
        """
        This method navigates to the System Settings Services page.
        """
        NAV.navigate_to_system_settings_services()
        assert COM.assert_page_header("Services") is True

    @pytest.fixture(scope='class', autouse=True)
    def teardown_class(self):
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
        SERV.click_edit_button_by_servicename('FTP')
        assert COM.assert_right_panel_header('FTP') is True
        FTP.verify_ftp_service_basic_edit_ui()
        COM.click_advanced_options_button()
        FTP.verify_ftp_service_advanced_edit_ui()
        COM.close_right_panel()
        assert COM.assert_page_header("Services") is True

    def test_verify_iscsi_service_edit_ui(self):
        """
        This test verifies the edit UI for the iSCSI service.
        """
        SERV.click_edit_button_by_servicename('iSCSI')
        iSCSI.verify_iscsi_sharing_configuration_page_opens()
        iSCSI.verify_iscsi_global_configuration_ui()
        iSCSI.verify_iscsi_configuration_tabs()
        COM.click_button('wizard')
        assert COM.assert_right_panel_header('iSCSI Wizard') is True
        iSCSI.verify_iscsi_configuration_wizard_create_choose_block_device_ui()
        COM.close_right_panel()
        assert COM.assert_page_header("iSCSI") is True
        NAV.navigate_to_system_settings_services()
        assert COM.assert_page_header("Services") is True

    def test_verify_nfs_service_edit_ui(self):
        """
        This test verifies the edit UI for the NFS service.
        """
        NFS.verify_nfs_sessions_page_opens()
        NAV.navigate_to_system_settings_services()
        assert COM.assert_page_header("Services") is True
        SERV.click_edit_button_by_servicename('NFS')
        assert COM.assert_right_panel_header('NFS') is True
        NFS.verify_nfs_service_edit_ui()
        COM.close_right_panel()
        assert COM.assert_page_header("Services") is True

    def test_verify_smart_service_edit_ui(self):
        """
        This test verifies the edit UI for the S.M.A.R.T. service.
        """
        SERV.click_edit_button_by_servicename('S.M.A.R.T.')
        assert COM.assert_right_panel_header('S.M.A.R.T.') is True
        SMART.verify_smart_service_edit_ui()
        COM.close_right_panel()
        assert COM.assert_page_header("Services") is True

    def test_verify_smb_service_edit_ui(self):
        """
        This test verifies the edit UI for the SMB service.
        """
        SMB.verify_smb_audit_page_opens()
        NAV.navigate_to_system_settings_services()
        assert COM.assert_page_header("Services") is True
        SMB.verify_smb_sessions_page_opens()
        NAV.navigate_to_system_settings_services()
        assert COM.assert_page_header("Services") is True
        SERV.click_edit_button_by_servicename('SMB')
        assert COM.assert_right_panel_header('SMB') is True
        SMB.verify_smb_service_basic_edit_ui()
        SERV.click_advanced_settings_button()
        SMB.verify_smb_service_advanced_edit_ui()
        COM.close_right_panel()
        assert COM.assert_page_header("Services") is True

    def test_verify_snmp_service_edit_ui(self):
        """
        This test verifies the edit UI for the SNMP service.
        """
        SERV.click_edit_button_by_servicename('SNMP')
        assert COM.assert_right_panel_header('SNMP') is True
        SNMP.verify_snmp_service_edit_ui()
        COM.close_right_panel()
        assert COM.assert_page_header("Services") is True

    def test_verify_ssh_service_edit_ui(self):
        """
        This test verifies the edit UI for the SSH service.
        """
        SERV.click_edit_button_by_servicename('SSH')
        assert COM.assert_right_panel_header('SSH') is True
        SSH.verify_ssh_service_basic_edit_ui()
        SERV.click_advanced_settings_button('SSH')
        SSH.verify_ssh_service_advanced_edit_ui()
        COM.close_right_panel()
        assert COM.assert_page_header("Services") is True

    def test_verify_ups_service_edit_ui(self):
        """
        This test verifies the edit UI for the UPS service.
        """
        SERV.click_edit_button_by_servicename('UPS')
        assert COM.assert_right_panel_header('UPS') is True
        UPS.verify_ups_service_edit_ui()
        COM.close_right_panel()
        assert COM.assert_page_header("Services") is True
