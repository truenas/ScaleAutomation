from keywords.api.post import API_POST


class Services:
    @classmethod
    def restart_service_by_api(cls, service: str) -> None:
        """
        This method starts the given service

        :param service: is the name of the service to start
        """
        assert API_POST.start_service(service).status_code == 200

    @classmethod
    def start_service_by_api(cls, service: str) -> None:
        """
        This method starts the given service

        :param service: is the name of the service to start
        """
        assert API_POST.start_service(service).status_code == 200

    @classmethod
    def stop_service_by_api(cls, service: str) -> None:
        """
        This method stops the given service

        :param service: is the name of the service to stop
        """
        assert API_POST.stop_service(service).status_code == 200
