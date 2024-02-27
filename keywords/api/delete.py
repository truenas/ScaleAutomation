from helper.api import GET, DELETE, PUT, Response
from helper.global_config import private_config
from keywords.api.common import API_Common as API


class API_DELETE:
    @classmethod
    def delete_share(cls, sharetype: str, name: str) -> Response:
        """
        This method deletes the given share by given share type.

        :param sharetype: is the type of the given share.
        :param name: is the share nome.
        :return: the API request response.
        """
        search = 'name='
        if sharetype == 'nfs':
            search = 'path=/mnt/'
        response = GET(f'/sharing/{sharetype}?{search}{name}').json()
        if response:
            smb_id = str(API.get_id_by_type(f'/sharing/{sharetype}?', name))
            response = DELETE(f'/sharing/{sharetype}/id/' + smb_id)
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_dataset(cls, name: str, recursive: bool = False, force: bool = False) -> Response:
        """
        This method deletes the given dataset.

        :param name: is the dataset name.
        :param recursive: is True to delete recursively.
        :param force: is True to force delete.
        :return: the API request response.
        """
        name = name.replace('/', '%2F')
        response = GET(f'/pool/dataset?name={name}').json()
        if response:
            response = DELETE(f'/pool/dataset/id/{name}', {'recursive': recursive, 'force': force})
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_group(cls, name: str, privilege: str = None) -> Response:
        """
        This method deletes the group.

        :param name: is nane of the group.
        :param privilege: is privilege of the group.
        :return: the API request response.
        """
        if privilege:
            # get privilege id
            privilege_id = API.get_privilege_id(privilege)
            # remove privilege from group
            if privilege_id:
                privilege_gid = API.get_privilege_gid(privilege)
                payload = {"local_groups": [privilege_gid]}
                response = PUT(f'/privilege/id/{privilege_id}', payload)
                assert response.status_code == 200, response.text
        # remove group
        response = GET(f'/group?name={name}').json()
        if response:
            group_id = str(API.get_group_id(name))
            response = DELETE(f'/group/id/{group_id}')
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_remote_dataset(cls, name: str, recursive: bool = False, force: bool = False) -> Response:
        """
        This method deletes the given remote dataset.

        :param name: is the remote dataset name.
        :param recursive: is True to delete recursively.
        :param force: is True to force delete.
        :return: the API request response.
        """
        name = name.replace('/', '%2F')
        private_config['API_IP'] = private_config['REP_DEST_IP']
        response = GET(f'/pool/dataset?name={name}').json()
        private_config['API_IP'] = private_config['IP']
        if response:
            private_config['API_IP'] = private_config['REP_DEST_IP']
            # response = DELETE(f'/pool/dataset/id/{name}', {'recursive': recursive, 'force': force})
            response = cls.delete_dataset(name, recursive, force)
            private_config['API_IP'] = private_config['IP']
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_remote_user(cls, name: str) -> Response:
        """
        This method deletes the user.

        :param name: is name of the user.
        :return: the API request response.

        Example:
            - API_DELETE.delete_remote_user('myUser')
        """
        private_config['API_IP'] = private_config['REP_DEST_IP']
        response = cls.delete_user(name)
        private_config['API_IP'] = private_config['IP']
        return response

    @classmethod
    def delete_ssh_keypairs(cls, name: str) -> Response:
        """
        This method deletes the given ssh keypairs.

        :param name: is name of the ssh keypairs.
        :return: the API request response.
        """
        name = name + " Key"
        response = GET(f'/keychaincredential?name={name}').json()
        if response:
            ssh_id = API.get_ssh_id(name)
            response = DELETE(f'/keychaincredential/id/{ssh_id}')
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_ssh_connection(cls, name: str) -> Response:
        """
        This method deletes the given ssh connection.

        :param name: is name of the ssh connection.
        :return: the API request response.
        """
        response = GET(f'/keychaincredential?name={name}').json()
        if response:
            ssh_id = API.get_ssh_id(name)
            response = DELETE(f'/keychaincredential/id/{ssh_id}')
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_user(cls, name: str) -> Response:
        """
        This method deletes the user.

        :param name: is name of the user.
        :return: the API request response.

        Example:
            - API_DELETE.delete_user('myUser')
        """
        response = GET(f'/user?username={name}').json()
        if response:
            user_id = str(API.get_user_id(name))
            response = DELETE(f'/user/id/{user_id}')
            assert response.status_code == 200, response.text
        return response
