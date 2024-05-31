"""
This module contains keywords for boot and bootenv api
"""
from helper.api import DELETE, GET, POST, Response
from keywords.api.get import API_GET


class API_Boot:
    """
    This class contains boot and bootenv api keywords
    """

    @classmethod
    def create_bootenv(cls, name: str, source: str = None) -> Response:
        """
        This method creates bootenv with the given data.
        :param name: is the name of the bootenv,
        :param source: is the be id/name of to create the bootenv from,
        :return: the API request response,

        Example:
            - API_BootEnv.create_bootenv('name', 'source')
        """
        payload = {"name": name}
        if source:
            payload["source"] = source
        response = POST('/bootenv', payload)
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_bootenv(cls, name: str) -> Response:
        """
        This method deletes the bootenv.
        :param name: is the name of the bootenv.
        :return: the API request response.
        """
        response = DELETE(f'/bootenv/id/{name}')
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def get_boot_device(cls) -> str:
        """
        This method gets the boot device.
        :return: the boot device.
        """
        return cls.get_boot_state().json()['topology']['data'][0]['device']

    @classmethod
    def get_boot_disks(cls) -> list:
        """
        This method gets the boot disks list.
        :return: the list of boot disks.
        """
        response = GET('/boot/get_disks')
        assert response.status_code == 200, response.text
        return response.json()

    @classmethod
    def get_boot_state(cls) -> Response:
        """
        This method gets the bootenvs list.
        :return: the list of bootenvs.
        """
        response = GET('/boot/get_state')
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def get_bootenv(cls) -> Response:
        """
        This method gets the bootenv.
        :return: the API request response.
        """
        response = GET('/bootenv')
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def get_default_bootenv_id(cls) -> str:
        """
        This method gets the default id/name of the bootenv.
        :return: the default id/name of the bootenv.
        """
        # The default bootenv id is the same ad the system short version
        return API_GET.get_system_version_short().json()
