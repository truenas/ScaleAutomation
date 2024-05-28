from helper.api import POST, Response


class API_DATASET:
    @classmethod
    def create_zvol(cls, name: str, volsize: int, volblocksize: str) -> Response:
        """
        This method creates the given zvol.

        :param name: is the name of the zvol.
        :param volsize: is the size of the zvol.
        :param volblocksize: is the blocksize of the zvol:
            - 512, 512B, 1K, 2K, 4K, 8K, 16K, 32K, 64K, 128K
        :return: the API request response.

        Example:
            - API_DATASET.create_zvol('tank/test-dataset', 1024000, '4k')
        """
        payload = {
            'name': name,
            'type': 'VOLUME',
            'volsize': volsize,
            'volblocksize': volblocksize
        }
        return POST("/pool/dataset/", payload)
