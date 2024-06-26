from helper.api import GET, DELETE, PUT, Response
from helper.global_config import shared_config
from helper.global_config import private_config
from keywords.api.common import API_Common as API


class API_DELETE:

    @classmethod
    def delete_all_periodic_snapshots_tasks(cls) -> dict:
        """
        This method delete all periodic snapshot tasks.

        :return: The dictionary response from the job.

        Example:
            - API_POST.delete_all_periodic_snapshots_tasks()
        """
        response = GET('/pool/snapshottask').json()
        while response:
            task_id = response[0]['id']
            response = DELETE(f'/pool/snapshottask/id/{task_id}', {})
            assert response.status_code == 200, response.text
            response = GET('/pool/snapshottask').json()
        return response

    @classmethod
    def delete_certificate(cls, cert_name: str) -> dict:
        """
        This method deletes the given certificate.

        :param cert_name: is name of the certificate.
        :return: the API request response.
        """
        response = GET(f'/certificate?name={cert_name}').json()
        if response:
            cert_id = response[0]['id']
            response = DELETE(f'/certificate/id/{cert_id}')
            assert response.status_code == 200, response.text
            job_status = API.wait_on_job(response.json(), shared_config['LONG_WAIT'])
            return job_status
        return response

    @classmethod
    def delete_certificate_authority(cls, ca_name: str) -> Response:
        """
        This method deletes the given certificate authority.

        :param ca_name: is name of the certificate authority.
        :return: the API request response.
        """
        response = GET(f'/certificateauthority?name={ca_name}').json()
        if response:
            ca_id = response[0]['id']
            response = DELETE(f'/certificateauthority/id/{ca_id}')
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_cloud_sync_credential(cls, name: str) -> Response:
        """
        This method deletes the Cloud Sync credential by the given name.

        :param name: is name of the cloud sync credential.
        :return: the API request response.

        Example:
            - API_DELETE.delete_cloud_sync_credential('name')
        """
        response = GET(f'/cloudsync/credentials?name={name}').json()
        if response:
            cred_id = response[0]['id']
            response = DELETE(f'/cloudsync/credentials/id/{cred_id}')
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_cloud_sync_task(cls, description: str) -> Response:
        """
        This method deletes the Cloud Sync task by the given task description.

        :param description: is description of the cloud sync task.
        :return: the API request response.

        Example:
            - API_DELETE.delete_cloud_sync_task('description')
        """
        response = GET(f'/cloudsync?description={description}').json()
        if response:
            task_id = response[0]['id']
            response = DELETE(f'/cloudsync/id/{task_id}')
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
    def delete_replication_task(cls, name: str) -> Response:
        """
        This method deletes replication task by the given name.

        :param name: is the replication name.
        :return: the API request response.

        Example:
            - API_DELETE.delete_replication_task('name')
        """
        response = GET(f'/replication?name={name}').json()
        if response:
            rep_id = response[0]['id']
            response = DELETE(f'/replication/id/{rep_id}')
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_scrub_task(cls, pool_name: str) -> Response:
        """
        This method deletes scrub task by the given pool_name.

        :param pool_name: is the pool name.
        :return: the API request response.

        Example:
            - API_DELETE.delete_scrub_task('pool_name')
        """
        response = GET(f'/pool/scrub?pool_name={pool_name}').json()
        if response:
            pool_id = response[0]['id']
            response = DELETE(f'/pool/scrub/id/{pool_id}')
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_share(cls, sharetype: str, name: str) -> Response:
        """
        This method deletes the given share by given share type.

        :param sharetype: is the type of the given share.
        :param name: is the share name.
        :return: the API request response.
        """
        search = 'name='
        if sharetype == 'nfs':
            search = 'path=/mnt/'
        response = GET(f'/sharing/{sharetype}?{search}{name}').json()
        if response:
            share_id = str(API.get_id_by_type(f'/sharing/{sharetype}?', name))
            response = DELETE(f'/sharing/{sharetype}/id/' + share_id)
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_smart_test(cls, description: str) -> Response:
        """
        This method deletes the smart test.

        :param description: is description of the smart test.
        :return: the API request response.

        Example:
            - API_DELETE.delete_smart_test('smart desc')
        """
        response = GET(f'/smart/test?desc={description}').json()
        if response:
            smart_id = response[0]['id']
            response = DELETE(f'/smart/test/id/{smart_id}')
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_snapshot(cls, snapshot_id: str, defer: bool = False, recursive: bool = False) -> Response:
        """
        This method deletes the given snapshot.

        :param snapshot_id: is id of the snapshot.
        :param defer: is True to defer delete.
        :param recursive: is True to delete recursively.
        :return: the API request response.

        Example:
            - API_DELETE.delete_snapshot('snapshot_id')
            - API_DELETE.delete_snapshot('snapshot_id', defer=True)
            - API_DELETE.delete_snapshot('snapshot_id', recursive=True)
        """
        payload = {'defer': defer, 'recursive': recursive}
        response = DELETE(f'/zfs/snapshot/id/{snapshot_id.replace("/", "%2F")}', payload)
        assert response.status_code == 200, response.text
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
