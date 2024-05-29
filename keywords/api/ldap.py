import time

from helper.api import GET, PUT, Response
from helper.global_config import shared_config
from keywords.api.common import API_Common


class API_LDAP:

    @classmethod
    def get_ldap_config(cls) -> Response:
        """
        This method gets LDAP configuration.

        :return: The API request response.

        Example:
            - API_Ldap.get_ldap_config()
        """
        return GET('/ldap')

    @classmethod
    def get_ldap_state(cls) -> Response:
        """
        This method gets LDAP state.

        :return: The API request response.

        Example:
            - API_Ldap.get_ldap_state()
        """
        return GET('/ldap/get_state')

    @classmethod
    def get_ldap_schema_choices(cls) -> Response:
        """
        This method gets LDAP schema choices.

        :return: The API request response.

        Example:
            - API_Ldap.get_ldap_schema_choices()
        """
        return GET('/ldap/schema_choices')

    @classmethod
    def get_ldap_ssl_choices(cls) -> Response:
        """
        This method gets LDAP ssl choices.

        :return: The API request response.

        Example:
            - API_Ldap.get_ldap_ssl_choices()
        """
        return GET('/ldap/ssl_choices')

    @classmethod
    def configure_ldap(cls, basedn: str, binddn: str, bindpw: str, hostname: str, ssl: str = 'ON') -> dict:
        """
        This method configures LDAP.

        :param basedn: the base dn
        :param binddn: the bind dn
        :param bindpw: the bind password
        :param hostname: the hostname
        :param ssl: the ssl ON or OFF
        :return: the API request response.

        Example:
            - API_Ldap.configure_ldap('basedn', 'binddn', 'bindpw', 'hostname', 'OFF')
        """
        payload = {
            "basedn": basedn,
            "binddn": binddn,
            "bindpw": bindpw,
            "hostname": [hostname],
            "ssl": ssl,
            "enable": True
        }
        return cls.update_ldap(payload)

    @classmethod
    def disable_ldap(cls) -> dict:
        """
        This method disables LDAP.

        :return: The API request response.

        Example:
            - API_Ldap.disable_ldap()
        """
        return cls.update_ldap({'enable': False})

    @classmethod
    def enable_ldap(cls) -> dict:
        """
        This method enables LDAP.

        :return: The API request response.

        Example:
            - API_Ldap.enable_ldap()
        """
        return cls.update_ldap({'enable': True})

    @classmethod
    def update_ldap(cls, payload: dict) -> dict:
        """
        This method updates the LDAP configuration.

        :param payload: is the payload for the api call.
        :return: the API request response.

        Example:
            - API_Ldap.update_ldap(payload)
        """
        response = PUT('/ldap', payload)
        assert response.status_code == 200, response.text
        # This is to avoid a race condition seen with ldap update.
        time.sleep(1)
        job_result = API_Common.wait_on_job(response.json(), shared_config['EXTRA_LONG_WAIT'])
        assert job_result['state'] == 'SUCCESS', job_result['results']
        return job_result['results']
