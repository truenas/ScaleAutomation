import allure
import pytest

import xpaths
from keywords.webui.common import Common as COM
from keywords.webui.navigation import Navigation as NAV
from keywords.webui.system_services import System_Services as SERV


@allure.tag('Share Admin', 'System Settings', 'Services Page', "Users", 'Permissions')
@allure.epic('Permissions')
@allure.feature('Share Admin')
class Test_Share_Admin_System_Settings_Advanced:

    @pytest.fixture(autouse=True, scope='class')
    def setup_system_settings_advanced(self):
        """
        Summary: This setup fixture System Settings Services page for all test cases.
        """
        NAV.navigate_to_system_settings_services()

    @allure.tag("Read")
    @allure.story("Share Admin Can See the System Settings Services Page")
    def test_share_admin_can_see_the_system_settings_services_page(self):
        """
        Summary: This test verifies the share admin is able to access and see all details in the System Settings > Services view.

        Test Steps:
        1. Verify the share admin is able to see for each service Services view page (Name, Running, Automatic, Edit)
        """
        assert COM.assert_page_header('Services')

        # FTP Service
        assert COM.is_table_row_visible('service-ftp') is True
        assert COM.is_text_visible('FTP') is True
        assert COM.is_toggle_visible('running-service-ftp-row-toggle') is True
        assert COM.is_toggle_visible('start-automatically-service-ftp-row-toggle') is True
        assert COM.is_button_visible('service-ftp-edit-row-action') is True

        # iSCSI Service
        assert COM.is_table_row_visible('service-iscsi') is True
        assert COM.is_text_visible('iSCSI') is True
        assert COM.is_toggle_visible('running-service-iscsi-row-toggle') is True
        assert COM.is_toggle_visible('start-automatically-service-iscsi-row-toggle') is True
        assert COM.is_button_visible('service-iscsi-edit-row-action') is True

        # NFS Service
        assert COM.is_table_row_visible('service-nfs') is True
        assert COM.is_text_visible('NFS') is True
        assert COM.is_toggle_visible('running-service-nfs-row-toggle') is True
        assert COM.is_toggle_visible('start-automatically-service-nfs-row-toggle') is True
        assert COM.is_button_visible('service-nfs-list-row-action') is True
        assert COM.is_button_visible('service-nfs-edit-row-action') is True

        # SMART Service
        assert COM.is_table_row_visible('service-smart') is True
        assert COM.is_text_visible('S.M.A.R.T.') is True
        assert COM.is_toggle_visible('running-service-smart-row-toggle') is True
        assert COM.is_toggle_visible('start-automatically-service-smart-row-toggle') is True
        assert COM.is_button_visible('service-smart-edit-row-action') is True

        # SMB Service
        assert COM.is_table_row_visible('service-smb') is True
        assert COM.is_text_visible('SMB') is True
        assert COM.is_toggle_visible('running-service-smb-row-toggle') is True
        assert COM.is_toggle_visible('start-automatically-service-smb-row-toggle') is True
        assert COM.is_button_visible('service-smb-receipt-long-row-action') is True
        assert COM.is_button_visible('service-smb-list-row-action') is True
        assert COM.is_button_visible('service-smb-edit-row-action') is True

        # SNMP Service
        assert COM.is_table_row_visible('service-snmp') is True
        assert COM.is_text_visible('SNMP') is True
        assert COM.is_toggle_visible('running-service-snmp-row-toggle') is True
        assert COM.is_toggle_visible('start-automatically-service-snmp-row-toggle') is True
        assert COM.is_button_visible('service-snmp-edit-row-action') is True

        # SSH Service
        assert COM.is_table_row_visible('service-ssh') is True
        assert COM.is_text_visible('SSH') is True
        assert COM.is_toggle_visible('running-service-ssh-row-toggle') is True
        assert COM.is_toggle_visible('start-automatically-service-ssh-row-toggle') is True
        assert COM.is_button_visible('service-ssh-edit-row-action') is True

        # UPS Service
        assert COM.is_table_row_visible('service-ups') is True
        assert COM.is_text_visible('UPS') is True
        assert COM.is_toggle_visible('running-service-ups-row-toggle') is True
        assert COM.is_toggle_visible('start-automatically-service-ups-row-toggle') is True
        assert COM.is_button_visible('service-ups-edit-row-action') is True

    @allure.tag("Update")
    @allure.story("Share Admin Is Able to Modify iSCSI, NFS, SMB Services")
    def test_share_admin_able_to_modify_specific_services(self):
        """
        Summary: This test verifies the share admin is able to modify iSCSI, NFS, SMB Services.

        Test Steps:
        1. Verify modify iSCSI Services (edit, change values, save)
        2. Verify modify NFS Services (edit, change values, save)
        3. Verify modify SMB Services (edit, change values, save)
        """

        # iSCSI Service
        COM.unset_toggle('running-service-iscsi-row-toggle')
        COM.click_button('service-iscsi-edit-row-action')
        assert COM.assert_page_header('iSCSI') is True
        COM.set_input_field('pool-avail-threshold', '80')
        COM.click_save_button_and_wait_for_progress_bar()
        assert COM.assert_page_header('Start iSCSI Service') is True
        COM.click_button('do-not-start')
        NAV.navigate_to_system_settings_services()
        COM.click_button('service-iscsi-edit-row-action')
        assert COM.get_element_property(xpaths.common_xpaths.input_field('pool-avail-threshold'), 'value') == '80'
        NAV.navigate_to_system_settings_services()

        # NFS Service
        COM.click_button('service-nfs-edit-row-action')
        assert COM.assert_right_panel_header('NFS') is True
        COM.set_checkbox('allow-nonroot')
        COM.click_save_button_and_wait_for_progress_bar()
        COM.click_button('service-nfs-edit-row-action')
        assert COM.is_checked('allow-nonroot') is True
        COM.close_right_panel()

        # SMB Service
        COM.click_button('service-smb-edit-row-action')
        assert COM.assert_right_panel_header('SMB') is True
        COM.set_input_field('netbiosname', 'edited')
        COM.click_save_button_and_wait_for_progress_bar()
        COM.click_button('service-smb-edit-row-action')
        assert COM.get_element_property(xpaths.common_xpaths.input_field('netbiosname'), 'value') == 'EDITED'
        COM.close_right_panel()

    @allure.tag("Update")
    @allure.story("Share Admin Is Not Able to Modify FTP, SMART, SNMP, SSH, UPS Services")
    def test_share_admin_not_able_to_modify_specific_services(self):
        """
        Summary: This test verifies the share admin is not able to modify FTP, SMART, SNMP, SSH, UPS Services.

        Test Steps:
        1. Verify not able to modify FTP Services (running, automatic, edit)
        2. Verify not able to modify SMART Services (running, automatic, edit)
        3. Verify not able to modify SNMP Services (running, automatic, edit)
        4. Verify not able to modify SSH Services (running, automatic, edit)
        5. Verify not able to modify UPS Services (running, automatic, edit)
        """
        # FTP Service
        assert COM.assert_toggle_is_restricted('running-service-ftp-row-toggle') is True
        assert COM.assert_toggle_is_restricted('start-automatically-service-ftp-row-toggle') is True
        assert COM.assert_button_is_restricted('service-ftp-edit-row-action') is True

        # SMART Service
        assert COM.assert_toggle_is_restricted('running-service-smart-row-toggle') is True
        assert COM.assert_toggle_is_restricted('start-automatically-service-smart-row-toggle') is True
        assert COM.assert_button_is_restricted('service-smart-edit-row-action') is True

        # SNMP Service
        assert COM.assert_toggle_is_restricted('running-service-snmp-row-toggle') is True
        assert COM.assert_toggle_is_restricted('start-automatically-service-snmp-row-toggle') is True
        assert COM.assert_button_is_restricted('service-snmp-edit-row-action') is True

        # SSH Service
        assert COM.assert_toggle_is_restricted('running-service-ssh-row-toggle') is True
        assert COM.assert_toggle_is_restricted('start-automatically-service-ssh-row-toggle') is True
        assert COM.assert_button_is_restricted('service-ssh-edit-row-action') is True

        # UPS Service
        assert COM.assert_toggle_is_restricted('running-service-ups-row-toggle') is True
        assert COM.assert_toggle_is_restricted('start-automatically-service-ups-row-toggle') is True
        assert COM.assert_button_is_restricted('service-ups-edit-row-action') is True

    @allure.tag("Update")
    @allure.story("Share Admin Is Able to Start iSCSI, NFS, SMB Services")
    def test_share_admin_able_to_start_specific_services(self):
        """
        Summary: This test verifies the share admin is able to start iSCSI, NFS, SMB Services.

        Test Steps:
        1. Verify start iSCSI Services (running, automatic)
        2. Verify start NFS Services (running, automatic)
        3. Verify start SMB Services (running, automatic)
        """

        # iSCSI Service
        SERV.stop_service_by_name('iscsi')
        SERV.start_service_by_name('iscsi', True)
        SERV.set_service_autostart_off('iscsi')
        SERV.set_service_autostart_on('iscsi')

        # NFS Service
        SERV.stop_service_by_name('nfs')
        SERV.start_service_by_name('nfs', True)
        SERV.set_service_autostart_off('nfs')
        SERV.set_service_autostart_on('nfs')

        # SMB Service
        SERV.stop_service_by_name('smb')
        SERV.start_service_by_name('smb', True)
        SERV.set_service_autostart_off('smb')
        SERV.set_service_autostart_on('smb')

    @allure.tag("Update")
    @allure.story("Share Admin Is Able to Stop iSCSI, NFS, SMB Services")
    def test_share_admin_able_to_stop_specific_services(self):
        """
        Summary: This test verifies the share admin is able to stop iSCSI, NFS, SMB Services.

        Test Steps:
        1. Verify stop iSCSI Services (running)
        2. Verify stop NFS Services (running)
        3. Verify stop SMB Services (running)
        """

        # iSCSI Service
        SERV.start_service_by_name('iscsi', True)
        SERV.stop_service_by_name('iscsi')
        SERV.set_service_autostart_on('iscsi')
        SERV.set_service_autostart_off('iscsi')

        # NFS Service
        SERV.start_service_by_name('nfs', True)
        SERV.stop_service_by_name('nfs')
        SERV.set_service_autostart_on('nfs')
        SERV.set_service_autostart_off('nfs')

        # SMB Service
        SERV.start_service_by_name('smb', True)
        SERV.stop_service_by_name('smb')
        SERV.set_service_autostart_on('smb')
        SERV.set_service_autostart_off('smb')
