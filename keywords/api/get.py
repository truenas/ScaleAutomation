from helper.api import GET, Response


class API_GET:
    @classmethod
    def get_group(cls, name: str) -> Response:
        """
        This method gets the group by given name.

        :param name: Is the name of the group.
        :return: The API request response.

        Example:
            - API_GET.get_group('group1')
        """
        response = GET(f'/group/?group={name}')
        return response

    @classmethod
    def get_group_id(cls, name: str) -> int:
        """
        This method gets the group id by given name.

        :param name: Is the name of the group.
        :return: The group id.

        Example:
            - API_GET.get_group_id('group1')
        """
        return cls.get_group(name).json()[0]['id']

    @classmethod
    def get_pool(cls, name: str) -> Response:
        """
        This method gets the pool by given name.

        :param name: Is the name of the pool.
        :return: The API request response.

        Example:
            - API_GET.get_pool('pool1')
        """
        pool_id = cls.get_pool_id(name)
        response = GET(f'/pool/id/{pool_id}/')
        return response

    @classmethod
    def get_pool_id(cls, name: str) -> int:
        """
        This method gets the pool id by given name.

        :param name: Is the name of the pool.
        :return: The pool id.

        Example:
            - API_GET.get_pool_id('pool1')
        """
        pool_id = None
        response = GET(f'/pool/?name={name}')
        if response.json():
            pool_id = response.json()[0]['id']
        return pool_id

    @classmethod
    def get_pool_type(cls, name: str) -> str:
        """
        This method gets the pool type by given name.

        :param name: Is the name of the pool.
        :return: The pool type.

        Example:
            - API_GET.get_pool_type('pool1')
        """
        return cls.get_pool(name).json()['topology']['data'][0]['type']

    @classmethod
    def get_system_product_name(cls) -> Response:
        """
        This method gets the system product name.

        :return: The API request response.

        Example:
            - API_GET.get_system_product_name()
        """
        response = GET('/system/product_name/')
        return response

    @classmethod
    def get_system_product_type(cls) -> Response:
        """
        This method gets the system product type.

        :return: The API request response.

        Example:
            - API_GET.get_system_product_type()
        """
        response = GET('/system/product_type/')
        return response

    @classmethod
    def get_system_state(cls) -> str:
        """
        This method gets the system state.

        :return: The API request response. [ SHUTTING_DOWN, READY, BOOTING ]

        Example:
            - API_GET.get_system_state()
        """
        response = GET('/system/state/')
        return response.text

    @classmethod
    def get_system_version(cls) -> Response:
        """
        This method gets the system version.

        :return: The API request response.

        Example:
            - API_GET.get_system_version()
        """
        response = GET('/system/version/')
        return response

    @classmethod
    def get_system_version_short(cls) -> Response:
        """
        This method gets the system version short.

        :return: The API request response.

        Example:
            - API_GET.get_system_version_short()
        """
        response = GET('/system/version_short/')
        return response
