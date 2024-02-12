import xpaths
from keywords.webui.common import Common as COM


services_list = ['ftp', 'iscsi', 'nfs', 'smart', 'smb', 'snmp', 'ssh', 'ups']


class System_Services:
    @classmethod
    def is_service_autostart_set_by_name(cls, service: str) -> bool:
        """
        This method returns the state of the auto start checkbox of the given service.

        :param service: The system name of the service
        :return: returns the state of the auto start checkbox of the given service.
        """
        service_backend = cls.return_backend_service_name(service)
        assert (COM.is_visible(xpaths.common_xpaths.checkbox_field(f'{service_backend}-service')))
        return COM.is_checked(f'{service_backend}-service')

    @classmethod
    def return_backend_service_name(cls, service: str) -> str:
        """
        This method returns the backend name of the given service.

        :param service: The name of the service.
        :return: returns the state of the backend name of the given service.
        """
        returned_name = service
        match service.lower():
            case 'iscsi':
                returned_name = 'iscsitarget'
            case 'smart' | 's.m.a.r.t.':
                returned_name = 'smartd'
            case 'smb':
                returned_name = 'cifs'
            case _:
                pass
        return returned_name

    @classmethod
    def set_all_services_auto_start(cls, state: bool):
        """
        This method returns the state of the auto start checkbox of the given service.

        :param state: The state to toggle the services to.
        :return: returns the state of the auto start checkbox of the given service.
        """
        for items in services_list:
            cls.toggle_service_auto_start(items, state)

    @classmethod
    def set_all_services_auto_start_off(cls):
        """
        This method returns toggles off the auto start checkbox of all services.
        """
        cls.set_all_services_auto_start(False)

    @classmethod
    def set_all_services_auto_start_on(cls):
        """
        This method returns toggles on the auto start checkbox of all services.
        """
        cls.set_all_services_auto_start(True)

    @classmethod
    def set_service_auto_start_off(cls, service: str):
        """
        This method returns toggles off the auto start checkbox of the given service.

        :param service: The name of the service.
        """
        cls.toggle_service_auto_start(service, False)

    @classmethod
    def set_service_auto_start_on(cls, service: str):
        """
        This method returns toggles on the auto start checkbox of the given service.

        :param service: The name of the service.
        """
        cls.toggle_service_auto_start(service, True)

    @classmethod
    def toggle_service_auto_start(cls, service: str, state: bool):
        """
        This method returns toggles the auto start checkbox of the given service to the given state.

        :param service: The name of the service.
        :param state: The state to toggle the services to.
        """
        service_backend = cls.return_backend_service_name(service)
        print(f'Service: {service}')
        autostart = COM.is_checked(f'{service_backend}-service')
        print(f'Set Service: {service} Auto Start to: {state} current status is: {autostart}')
        if autostart is not state:
            COM.set_checkbox(xpaths.common_xpaths.checkbox_field(f'{service_backend}-service'))
        autostart = COM.is_checked(f'{service_backend}-service')
        assert (autostart is state)
        print(f'Service Name: {service} exists and running status is: {autostart}')
