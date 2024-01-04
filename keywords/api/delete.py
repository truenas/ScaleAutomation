from helper.api import DELETE, Response
from helper.global_config import private_config
from keywords.api.common import API_Common as API
from helper.api import GET


class API_DELETE:
    @classmethod
    def delete_share(cls, sharetype: str, name: str) -> Response:
        """
        This method deletes the given share by given share type.

        :param sharetype: is the type of the given share.
        :param name: is the share nome.
        :return: the API request response.
        """
        response = GET(f'/sharing/{sharetype}?name={name}').json()
        if response:
            smb_id = str(API.get_id_by_type(f'/sharing/{sharetype}?', name))
            response = DELETE(f'/sharing/{sharetype}/id/' + smb_id)
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_dataset(cls, name: str) -> Response:
        """
        This method deletes the given dataset.

        :param name: is the share nome.
        :return: the API request response.
        """
        name = name.replace('/', '%2F')
        response = GET(f'/pool/dataset?name={name}').json()
        if response:
            response = DELETE(f'/pool/dataset/id/' + name)
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_user(cls, name: str) -> Response:
        """
        This method deletes the user.

        :param name: is nane of the user.
        :return: the API request response.
        """
        response = GET(f'/user?username={name}').json()
        if response:
            user_id = str(API.get_user_id(name))
            response = DELETE(f'/user/id/{user_id}')
            assert response.status_code == 200, response.text
        return response

