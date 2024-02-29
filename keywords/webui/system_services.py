import xpaths
from helper.webui import WebUI
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM


services_list = ['ftp', 'iscsi', 'nfs', 'smart', 'smb', 'snmp', 'ssh', 'ups']


class System_Services:
    @classmethod
    def assert_all_services_autostart_off(cls):
        for items in services_list:
            assert not cls.is_service_autostart_set_by_name(items)

    @classmethod
    def assert_all_services_autostart_on(cls):
        for items in services_list:
            assert cls.is_service_autostart_set_by_name(items)

    @classmethod
    def assert_all_services_running(cls):
        for items in services_list:
            if items == 'ups':
                assert not cls.is_service_status_running_by_name(items)
            else:
                assert cls.is_service_status_running_by_name(items)

    @classmethod
    def assert_all_services_not_running(cls):
        for items in services_list:
            assert not cls.is_service_status_running_by_name(items)

    @classmethod
    def click_advanced_settings_button(cls, service: str = None) -> None:
        """
        This method clicks the Advanced Settings button.

        Example:
            - Common.click_advanced_settings_button()
        """
        if service.lower() == "ssh":
            COM.click_advanced_options_button()
        else:
            COM.click_button('toggle-advanced-settings')

    @classmethod
    def click_edit_button_by_servicename(cls, servicename: str) -> None:
        """
        This method clicks the edit button for the given service.

        :param servicename: the name of the service.
        """
        name = cls.return_backend_service_name(servicename, False)
        COM.click_button(f'{name}-edit')

    @classmethod
    def is_service_autostart_set_by_name(cls, service: str) -> bool:
        """
        This method returns the state of the auto start checkbox of the given service.

        :param service: The system name of the service
        :return: returns the state of the auto start checkbox of the given service.
        """
        service_backend = cls.return_backend_service_name(service)
        assert (COM.is_visible(xpaths.common_xpaths.checkbox_field(f'{service_backend}')))
        return COM.is_checked(f'{service_backend}')

    @classmethod
    def is_service_status_running_by_name(cls, service: str) -> bool:
        """
        This method returns the running status of the given service.

        :param service: The system name of the service
        :return: returns the running status of the given service.
        """
        service_backend = cls.return_backend_service_name(service)
        return COM.is_toggle_enabled(service_backend)

    @classmethod
    def restart_service_by_api(cls, service: str) -> None:
        """
        This method starts the given service

        :param service: is the name of the service to start
        """
        assert API_POST.start_service(service).status_code == 200

    @classmethod
    def return_backend_service_name(cls, service: str, append: bool = True) -> str:
        """
        This method returns the backend name of the given service.

        :param append: Whether to append "-service" to the end of the converted name. Default value, True.
        :param service: The name of the service.
        :return: returns the state of the backend name of the given service.
        """
        returned_name = service.lower()
        match service.lower():
            case 'iscsi':
                returned_name = 'iscsitarget'
            case 'smart' | 's.m.a.r.t.':
                returned_name = 'smartd'
            case 'smb':
                returned_name = 'cifs'
            case _:
                pass
        if append:
            returned_name = returned_name+'-service'
        return returned_name

    @classmethod
    def set_all_services_autostart_off(cls):
        """
        This method sets the auto start checkbox of all services to off.
        """
        for items in services_list:
            cls.toggle_service_autostart(items, False)

    @classmethod
    def set_all_services_autostart_on(cls):
        """
        This method sets the auto start checkbox of all services to on.
        """
        for items in services_list:
            cls.toggle_service_autostart(items, True)

    @classmethod
    def set_all_services_autostart_off_by_api(cls):
        """
        This method sets the auto start status of all services to off via api call.
        """
        for items in services_list:
            cls.set_service_autostart_off_by_api(items)

    @classmethod
    def set_all_services_running_status_by_state(cls, state: bool):
        """
        This method returns toggles on the auto start checkbox of all services.

        :param state: The state to toggle the service running status to.
        """
        for items in services_list:
            if state:
                if items == "ups":
                    cls.start_service_by_name(items, True, False)
                else:
                    cls.start_service_by_name(items)
            else:
                cls.stop_service_by_name(items)

    @classmethod
    def set_service_autostart_off(cls, service: str):
        """
        This method returns toggles off the auto start checkbox of the given service.

        :param service: The name of the service.
        """
        cls.toggle_service_autostart(service, False)

    @classmethod
    def set_service_autostart_on(cls, service: str):
        """
        This method returns toggles on the auto start checkbox of the given service.

        :param service: The name of the service.
        """
        cls.toggle_service_autostart(service, True)

    @classmethod
    def set_service_autostart_off_by_api(cls, service: str):
        """
        This method sets the auto start status of the given service to off via api call..

        :param service: The name of the service.
        """
        assert API_PUT.set_service_autostart(service, False).status_code == 200

    @classmethod
    def set_service_autostart_on_by_api(cls, service: str):
        """
        This method sets the auto start status of the given service to on via api call.

        :param service: The name of the service.
        """
        assert API_PUT.set_service_autostart(service, True).status_code == 200

    @classmethod
    def start_all_services(cls):
        """
        This method starts all services.
        """
        cls.set_all_services_running_status_by_state(True)

    @classmethod
    def start_service_by_api(cls, service: str) -> None:
        """
        This method starts the given service via API call.

        :param service: is the name of the service to start
        """
        service_backend = cls.return_backend_service_name(service, False)
        assert API_POST.start_service(service_backend).status_code == 200

    @classmethod
    def start_service_by_name(cls, service: str, error_dialog: bool = False, runnable: bool = True):
        """
        This method starts the given service via WebUI.

        :param service: The name of the service.
        :param error_dialog: If the service displays an error dialog upon starting.
        :param runnable: If the service is able to start without error by default.
        """
        if runnable:
            cls.toggle_service_running_status_by_name(service, True, error_dialog)

    @classmethod
    def stop_all_services(cls):
        """
        This method stops all services.
        """
        cls.set_all_services_running_status_by_state(False)

    @classmethod
    def stop_all_services_by_api(cls):
        """
        This method stops all services by api call.
        """
        for items in services_list:
            cls.stop_service_by_api(items)

    @classmethod
    def stop_service_by_api(cls, service: str) -> None:
        """
        This method stops the given service via API call.

        :param service: The name of the service to stop
        """
        service_backend = cls.return_backend_service_name(service, False)
        assert API_POST.stop_service(service_backend).status_code == 200

    @classmethod
    def stop_service_by_name(cls, service: str):
        """
        This method stops the given service via WebUI.
        """
        cls.toggle_service_running_status_by_name(service, False)

    @classmethod
    def toggle_service_autostart(cls, service: str, state: bool):
        """
        This method returns toggles the auto start checkbox of the given service to the given state.

        :param service: The name of the service.
        :param state: The state to toggle the service auto start status to.
        """
        service_backend = cls.return_backend_service_name(service)
        COM.set_checkbox_by_state(f'{service_backend}', state)
        assert (COM.is_checked(f'{service_backend}') is state)

    @classmethod
    def toggle_service_running_status_by_name(cls, service: str, state: bool, error_dialog: bool = False):
        """
        This toggles the running status of the given service.

        :param service: The name of the service.
        :param state: The state to toggle the given service to.
        :param error_dialog: If the service displays an error dialog upon starting.
        """
        service_backend = cls.return_backend_service_name(service)
        if COM.is_toggle_enabled(service_backend) is not state:
            COM.set_toggle_by_state(service_backend, state)
            if error_dialog | state is False:
                COM.assert_confirm_dialog()
            i = 0
            WebUI.wait_until_visible(xpaths.common_xpaths.toggle_field(service_backend))
            while COM.is_toggle_enabled(service_backend) is not state:
                WebUI.delay(2)
                i += 1
                if i >= 10:
                    print(f'Total wait: 20 seconds. Toggle still did not equal {state}')
                    break
        assert (COM.is_toggle_enabled(service_backend) is state)

    @classmethod
    def verify_edit_button_visible_by_servicename(cls, servicename: str) -> None:
        name = cls.return_backend_service_name(servicename)
        assert COM.is_visible(xpaths.common_xpaths.button_field(f'{name}-edit'))

    @classmethod
    def verify_ftp_service_basic_edit_ui(cls) -> None:
        """
        This method verifies the basic edit UI of the FTP service.
        """
        assert COM.is_visible(xpaths.common_xpaths.input_field('port')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('clients')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('ipconnections')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('loginattempt')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('timeout-notransfer')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('timeout')) is True

    @classmethod
    def verify_ftp_service_advanced_edit_ui(cls) -> None:
        """
        This method verifies the advanced edit UI of the FTP service.
        """
        cls.verify_ftp_service_basic_edit_ui()
        assert COM.is_visible(xpaths.common_xpaths.input_field('port')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('defaultroot')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('rootlogin')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('onlyanonymous')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('onlylocal')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('ident')) is True
        cls.verify_ftp_service_permission_tables_ui()
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('tls')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('passiveportsmin')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('passiveportsmax')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('fxp')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('resume')) is True
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field('reversedns')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('masqaddress')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('banner')) is True
        assert COM.is_visible(xpaths.common_xpaths.textarea_field('options')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('localuserbw')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('localuserdlbw')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('anonuserbw')) is True
        assert COM.is_visible(xpaths.common_xpaths.input_field('anonuserdlbw')) is True

    @classmethod
    def verify_ftp_service_permission_tables_ui(cls) -> None:
        """
        This method verifies the file and directory permissions tables on the advanced FTP Edit UI.
        """
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('user', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('user', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('user', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('group', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('group', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('group', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('other', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('other', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_file_permissions_table_checkbox('other', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('user', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('user', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('user', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('group', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('group', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('group', 'execute')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('other', 'read')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('other', 'write')) is True
        assert COM.is_visible(xpaths.services.ftp_directory_permissions_table_checkbox('other', 'execute')) is True
