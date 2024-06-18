from helper.api import GET, Response


class API_System:
    @classmethod
    def get_system_debug(cls) -> Response:
        """
        This method gets the system debug.

        :return: The API request response.

        Example:
            - API_System.get_system_debug()
        """
        response = GET('/system/debug')
        assert response.status_code == 200, response.text
        return response
