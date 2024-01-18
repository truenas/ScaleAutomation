from helper.api import GET, Response


class API_GET:
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
        pool_id = GET(f'/pool/?name={name}').json()[0]['id']
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
