from helper.api import POST, Response, GET
from helper.global_config import shared_config, private_config
from keywords.api.common import API_Common
from keywords.api.get import API_GET


class API_POST:
    @classmethod
    def add_smb_acl_entry(cls, who: str, userid: int, permission: str, perm_type: str):
        """
        This method sets the values for an SMB_ACL_ENTRY

        :param who: is the type of user to have acl permissions: [USER/GROUP/BOTH]
        :param userid: is the id of the user/group used in the 'who' parameter as an integer
        :param permission: is the permission to be assigned: [FULL/CHANGE/READ]
        :param perm_type: is the permission type to be assigned: [ALLOWED/DENIED]
        """
        entry = {"ae_who_id": {"id_type": who, "id": userid}, "ae_perm": permission, "ae_type": perm_type}
        if who == 'everyone@':
            entry = {"ae_who_sid": "S-1-1-0", "ae_perm": permission, "ae_type": perm_type}
        shared_config['SMB_ACL_ENTRY'].append(entry)

    @classmethod
    def clear_smb_acl_entry(cls):
        """
        This method clears the SMB_ACL_ENTRY field
        """
        shared_config['SMB_ACL_ENTRY'] = []

    @classmethod
    def create_dataset(cls, name: str, sharetype: str = 'GENERIC') -> Response:
        """
        This method deletes the given dataset.

        :param name: is the name of the dataset.
        :param sharetype: is the sharetype of the dataset.
        :return: the API request response.
        """
        response = GET(f'/pool/dataset?name={name}').json()
        if not response:
            response = POST('/pool/dataset', {"name": name, "share_type": sharetype})
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def create_non_admin_user(cls, name: str, fullname: str, password: str, smb_auth: str = 'false') -> Response:
        """
        This method creates a new non-admin user.

        :param name: is the name of the user.
        :param fullname: is the fullname of the user.
        :param password: is the password of the user.
        :param smb_auth: does user require SMB Authentication ['true'/'false'].
        :return: the API request response.
        """
        response = GET(f'/user?username={name}').json()
        if not response:
            response = POST(f'/user', {"username": name, "group_create": True, "home": "/mnt/tank", "home_create": True, "full_name": fullname, "email": name + "@nowhere.com", "password": password, "shell": "/usr/bin/bash", "ssh_password_enabled": True, "smb": bool(smb_auth)})
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def create_share(cls, sharetype: str, name: str, path: str) -> Response:
        """
        This method deletes the given dataset.

        :param sharetype: is the sharetype of the share.
        :param name: is the name of the share.
        :param path: is the path of the share.
        :return: the API request response.
        """
        response = GET(f'/sharing/{sharetype}?name={name}').json()
        if not response:
            response = POST(f'/sharing/{sharetype}/', {"name": name, "path": path})
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def export_pool(cls, name: str, destroy: bool = False) -> dict:
        """
        This method exports the given pool.

        :param name: is the name of the pool.
        :param destroy: True if should the pool be destroyed else False.
        :return: The dictionary response from the job.

        Example:
           - API_POST.export_pool('test-pool', True)
           - API_POST.export_pool('test-pool')
        """
        payload = {
            "cascade": True,
            "restart_services": True,
            "destroy": destroy
        }
        pool_id = API_GET.get_pool_id(name)
        response = POST(f'/pool/id/{pool_id}/export/', payload)
        assert response.status_code == 200, response.text
        job_status = API_Common.wait_on_job(response.json(), shared_config['EXTRA_LONG_WAIT'])
        return job_status

    @classmethod
    def is_service_running(cls, service: str) -> bool:
        """
        This method returns True if the service is running. otherwise False.

        :param service: is the service nome.
        :return: True if the service is running, otherwise False.
        """
        print(POST('service/started/', service))
        return bool(POST('service/started/', service).text)

    @classmethod
    def restart_replication_service(cls, service: str) -> Response:
        """
        This method restart the specified service of the replication NAS.

        :param service: is the service name.
        :return: the API request response.
        """
        return cls.set_service_by_system_and_state(service, 'restart', 'replication')

    @classmethod
    def restart_service(cls, service: str) -> Response:
        """
        This method restart the specified service of the NAS.

        :param service: is the service name.
        :return: the API request response.
        """
        return cls.set_service_by_system_and_state(service, 'restart', 'default')

    @classmethod
    def set_dataset_permissions_user_and_group(cls, dataset: str, user: str, group: str) -> Response:
        """
        This method deletes the given dataset.

        :param dataset: is the dataset name.
        :param user: is the user to set permissions.
        :param group: is the group to set permissions.
        :return: the API request response.
        """
        dataset = dataset.replace('/', '%2F')
        response = GET(f'/pool/dataset/id/{dataset}').json()
        if response:
            response = POST(f'/pool/dataset/id/{dataset}/permission', {"user": user, "group": group})
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def set_filesystem_acl(cls, payload: str) -> Response:
        """
        This method deletes the given dataset.

        :param payload: is the payload for the api call.
        :return: the API request response.
        """
        response = POST(f'/filesystem/setacl', payload)
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def set_service_by_system_and_state(cls, service: str, state: str, system: str = 'default') -> Response:
        """
        This method can start stop and restart the service for the default or replication NAS.

        :param service: is the service name.
        :param state: is the start, stop, or restart.
        :param system: uses default or replication for the replication NAS.
        :return: the API request response.
        """
        if system == 'replication':
            private_config['API_IP'] = private_config['REP_DEST_IP']
        results = POST(f'/service/{state}', {"service": service})
        if system == 'replication':
            private_config['API_IP'] = private_config['IP']
        assert cls.is_service_running(service) is results.json()
        return results

    @classmethod
    def set_smb_acl(cls, name: str) -> Response:
        """
        This method sets the SMB_ACL_ENTRY to default value

        :param name: is the name of the smb share
        :return: the API request response.
        """
        response = POST('/sharing/smb/setacl', {"share_name": name, "share_acl": shared_config['SMB_ACL_ENTRY']})
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def set_smb_acl_entry_to_default(cls):
        """
        This method sets the SMB_ACL_ENTRY to default value
        """
        shared_config['SMB_ACL_ENTRY'] = '{"ae_who_sid": "S-1-1-0", "ae_type": "ALLOWED","ae_perm": "FULL"}'

    @classmethod
    def start_replication_service(cls, service: str) -> Response:
        """
        This method start the specified service of the replication NAS.

        :param service: is the service name.
        :return: the API request response.
        """
        return cls.set_service_by_system_and_state(service, 'start', 'replication')

    @classmethod
    def start_service(cls, service: str) -> Response:
        """
        This method start the specified service of the default NAS.

        :param service: is the service name.
        :return: the API request response.
        """
        return cls.set_service_by_system_and_state(service, 'start', 'default')

    @classmethod
    def stop_replication_service(cls, service: str) -> Response:
        """
        This method stop the specified service of the replication NAS.

        :param service: is the service name.
        :return: the API request response.
        """
        return cls.set_service_by_system_and_state(service, 'stop', 'replication')

    @classmethod
    def stop_service(cls, service: str) -> Response:
        """
        This method stop the specified service of the default NAS.

        :param service: is the service name.
        :return: the API request response.
        """
        return cls.set_service_by_system_and_state(service, 'stop', 'default')
