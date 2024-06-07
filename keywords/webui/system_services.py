import xpaths
from helper.webui import WebUI
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM


services_list = ['ftp', 'iscsi', 'nfs', 'smart', 'smb', 'snmp', 'ssh', 'ups']


class System_Services:
    @classmethod
    def assert_all_services_autostart_off(cls) -> None:
        for items in services_list:
            assert not cls.is_service_autostart_set_by_name(items)
            assert API_POST.is_service_autostart_enabled(cls.return_backend_service_name(items, False)) is False

    @classmethod
    def assert_all_services_autostart_on(cls) -> None:
        for items in services_list:
            assert cls.is_service_autostart_set_by_name(items)
            assert API_POST.is_service_autostart_enabled(cls.return_backend_service_name(items, False)) is True

    @classmethod
    def assert_all_services_running(cls) -> None:
        for items in services_list:
            if items == 'ups':
                assert cls.is_service_running_toggle_enabled(items) is False
                assert API_POST.is_service_running(cls.return_backend_service_name(items, False)) is False
            else:
                assert cls.is_service_running_toggle_enabled(items)
                assert API_POST.is_service_running(cls.return_backend_service_name(items, False)) is True

    @classmethod
    def assert_all_services_not_running(cls) -> None:
        for items in services_list:
            assert not cls.is_service_running_toggle_enabled(items)
            assert API_POST.is_service_running(cls.return_backend_service_name(items, False)) is False

    @classmethod
    def click_advanced_settings_button(cls, service: str = '') -> None:
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
        service_backend = cls.return_backend_service_name(service, True)
        assert COM.is_visible(xpaths.common_xpaths.checkbox_field(service_backend)) is True
        return COM.is_checked(service_backend)

    @classmethod
    def is_service_running_toggle_enabled(cls, service: str) -> bool:
        """
        This method returns true if the given service running toggle is enabled, otherwise returns false.

        :param service: The system name of the service
        :return: true if the given service running toggle is enabled
        """
        service_backend = cls.return_backend_service_name(service, True)
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
            returned_name += '-service'
        return returned_name

    @classmethod
    def set_all_services_autostart_off(cls) -> None:
        """
        This method sets the auto start checkbox of all services to off.
        """
        for items in services_list:
            cls.toggle_service_autostart(items, False)

    @classmethod
    def set_all_services_autostart_on(cls) -> None:
        """
        This method sets the auto start checkbox of all services to on.
        """
        for items in services_list:
            cls.toggle_service_autostart(items, True)

    @classmethod
    def set_all_services_autostart_off_by_api(cls) -> None:
        """
        This method sets the auto start status of all services to off via api call.
        """
        for items in services_list:
            cls.set_service_autostart_off_by_api(items)

    @classmethod
    def set_all_services_running_status_by_state(cls, state: bool) -> None:
        """
        This method returns toggles on the auto start checkbox of all services.

        :param state: The state to toggle the service running status to.
        """
        for items in services_list:
            if state:
                if items == "ups":
                    cls.start_service_by_name(items, False)
                else:
                    cls.start_service_by_name(items, state)
            else:
                cls.stop_service_by_name(items)

    @classmethod
    def set_service_autostart_off(cls, service: str) -> None:
        """
        This method returns toggles off the auto start checkbox of the given service.

        :param service: The name of the service.
        """
        cls.toggle_service_autostart(service, False)

    @classmethod
    def set_service_autostart_on(cls, service: str) -> None:
        """
        This method returns toggles on the auto start checkbox of the given service.

        :param service: The name of the service.
        """
        cls.toggle_service_autostart(service, True)

    @classmethod
    def set_service_autostart_off_by_api(cls, service: str) -> None:
        """
        This method sets the auto start status of the given service to off via api call.

        :param service: The name of the service.
        """
        assert API_PUT.set_service_autostart(service, False).status_code == 200

    @classmethod
    def set_service_autostart_on_by_api(cls, service: str) -> None:
        """
        This method sets the auto start status of the given service to on via api call.

        :param service: The name of the service.
        """
        assert API_PUT.set_service_autostart(service, True).status_code == 200

    @classmethod
    def start_all_services(cls) -> None:
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
        if service_backend == "ups":
            assert API_POST.start_service(service_backend).json() is False
        else:
            assert API_POST.start_service(service_backend).json() is True

    @classmethod
    def start_service_by_name(cls, service: str, runnable: bool) -> None:
        """
        This method starts the given service via WebUI.
        :param service: The name of the service.
        :param runnable: If the service is runnable without error by default.
        """
        cls.toggle_service_running_status_by_name(service, runnable)

    @classmethod
    def stop_all_services(cls) -> None:
        """
        This method stops all services.
        """
        cls.set_all_services_running_status_by_state(False)

    @classmethod
    def stop_all_services_by_api(cls) -> None:
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
    def stop_service_by_name(cls, service: str) -> None:
        """
        This method stops the given service via WebUI.
        """
        cls.toggle_service_running_status_by_name(service, False)

    @classmethod
    def toggle_service_autostart(cls, service: str, state: bool) -> None:
        """
        This method returns toggles the auto start checkbox of the given service to the given state.

        :param service: The name of the service.
        :param state: The state to toggle the service auto start status to.
        """
        service_backend = cls.return_backend_service_name(service, True)
        COM.set_checkbox_by_state(service_backend, state)
        assert (COM.is_checked(service_backend) is state)
        assert API_POST.is_service_autostart_enabled(cls.return_backend_service_name(service, False)) is state

    @classmethod
    def toggle_service_running_status_by_name(cls, service: str, state: bool) -> None:
        """
        This toggles the running status of the given service.
        :param service: The name of the service.
        :param state: The state to toggle the given service to.
        """
        service_backend = cls.return_backend_service_name(service, True)
        if service == 'UPS':
            toggle = WebUI.xpath(xpaths.common_xpaths.toggle_field(service_backend))
            toggle.click()
            assert COM.assert_progress_spinner_not_visible() is True
            COM.assert_dialog_visible('Error starting service UPS.')
            COM.click_error_dialog_close_button()
        if COM.is_toggle_enabled(service_backend) is not state:
            COM.set_toggle_by_state(service_backend, state)
            assert COM.assert_progress_spinner_not_visible() is True
            if not state:
                COM.assert_confirm_dialog()
            i = 0
            assert WebUI.wait_until_visible(xpaths.common_xpaths.toggle_field(service_backend)) is True
            while COM.is_toggle_enabled(service_backend) is not state:
                WebUI.delay(2)
                i += 1
                if i >= 10:
                    print(f'Total wait: 20 seconds. Toggle still did not equal {state}')
                    break
        assert (COM.is_toggle_enabled(service_backend) is state)
        assert API_POST.is_service_running(cls.return_backend_service_name(service, False)) is state

    @classmethod
    def verify_edit_button_visible_by_servicename(cls, servicename: str) -> None:
        name = cls.return_backend_service_name(servicename, True)
        assert COM.is_visible(xpaths.common_xpaths.button_field(f'{name}-edit'))

    @classmethod
    def set_nfs_service_protocols(cls, options: str) -> None:
        """
        This method sets the NFS service Enabled Protocols.

        :param options: The protocols to set. NFSv3 and/or NFSv4
        """
        if COM.is_visible('//*[@data-test="select-protocols"]//*[contains(text(), "NFSv3")]') is False & options.__contains__('NFSv3'):
            COM.select_option('protocols', 'protocols-nf-sv-3')
        if COM.is_visible('//*[@data-test="select-protocols"]//*[contains(text(), "NFSv4")]') is False & options.__contains__('NFSv4'):
            COM.select_option('protocols', 'protocols-nf-sv-4')
        WebUI.delay(0.5)
        