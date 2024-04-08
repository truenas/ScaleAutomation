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
    def create_certificate(cls, data: dict, ca_id: int) -> dict:
        payload = {
            'name': data['name'],
            'create_type': 'CERTIFICATE_CREATE_INTERNAL',
            'signedby': ca_id,
            'key_type': data['key_type'].upper(),
            'digest_algorithm': data['confirm_digest_algorithm'],
            'lifetime': data['lifetime'],
            'country': data['api_country'],
            'state': data['state'],
            'city': data['city'],
            'organization': data['organization'],
            'organizational_unit': data['organizational_unit'],
            'email': data['email'],
            'common': data['common_name'],
            'san': [data['san']],
        }
        response = POST('/certificate/', payload)
        assert response.status_code == 200, response.text
        job_status = API_Common.wait_on_job(response.json(), shared_config['LONG_WAIT'])
        assert job_status['state'] == 'SUCCESS', job_status['results']
        return job_status

    @classmethod
    def create_certificate_authority(cls, data: dict) -> Response:
        """
        This method creates a certificate authority with the given data.

        :param data: A dictionary of the data to create the certificate authority.
        :return: The API request response.
        """
        payload = {
            'name': data['name'],
            'create_type': 'CA_CREATE_INTERNAL',
            'key_type': data['key_type'].upper(),
            'digest_algorithm': data['confirm_digest_algorithm'],
            'lifetime': data['lifetime'],
            'country': data['api_country'],
            'state': data['state'],
            'city': data['city'],
            'organization': data['organization'],
            'organizational_unit': data['organizational_unit'],
            'email': data['email'],
            'common': data['common_name'],
            'san': [data['san']],
            'cert_extensions': {
                'BasicConstraints': {
                    'ca': True,
                    'path_length': 0,
                    'extension_critical': False
                },
                'KeyUsage': {
                    'enabled': True,
                    'key_cert_sign': True,
                    'crl_sign': True,
                    'extension_critical': True
                }
            }
        }
        response = POST('/certificateauthority/', payload)
        return response

    @classmethod
    def create_certificate_signing_requests(cls, data: dict) -> dict:
        """
        This method creates a certificate signing request with the given data.

        :param data: A dictionary of the data to create the certificate signing request.
        :return: The API request response.
        """
        payload = {
            'name': data['name'],
            'create_type': 'CERTIFICATE_CREATE_CSR',
            'key_type': data['key_type'].upper(),
            'key_length': int(data['key_length']),
            'digest_algorithm': data['confirm_digest_algorithm'],
            'country': data['api_country'],
            'state': data['state'],
            'city': data['city'],
            'organization': data['organization'],
            'organizational_unit': data['organizational_unit'],
            'email': data['email'],
            'common': data['common_name'],
            'san': [data['san']],
        }
        response = POST('/certificate/', payload)
        job_status = API_Common.wait_on_job(response.json(), shared_config['LONG_WAIT'])
        assert job_status['state'] == 'SUCCESS', job_status['results']
        return job_status

    @classmethod
    def create_dataset(cls, name: str, sharetype: str = 'GENERIC') -> Response:
        """
        This method creates the given dataset.

        :param name: is the name of the dataset.
        :param sharetype: is the sharetype of the dataset.
        :return: the API request response.

        Example:
            - API_POST.create_dataset('tank/test-dataset', 'GENERIC')
        """
        response = GET(f'/pool/dataset?name={name}').json()
        if not response:
            response = POST('/pool/dataset', {"name": name, "share_type": sharetype})
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def create_encrypted_dataset(cls, dataset: str) -> Response:
        """
        This method creates an encrypted dataset.

        :param dataset: The dataset pool and name.
        :return: The API response.

        Example:
            - API_POST.create_encrypted_dataset('tank/test-dataset')
        """
        payload = {
            "name": dataset,
            "encryption_options": {
                "generate_key": False,
                "pbkdf2iters": 555000,
                "algorithm": "AES-256-GCM",
                "passphrase": "encryption"
            },
            "inherit_encryption": False,
            "encryption": True
        }
        return POST('/pool/dataset/', payload)

    @classmethod
    def create_group(cls, group_name: str, smb_access: bool = False) -> Response:
        """
        This method creates the given group by API call

        :param group_name: is the name of the group to delete
        :param smb_access: allow smb access for the group.
        :return: returns the new group id
        """
        response = GET(f'/group?name={group_name}').json()
        if not response:
            payload = {
                "name": group_name,
                "smb": smb_access
            }
            response = POST('/group', payload)
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def create_inherit_encrypted_dataset(cls, dataset: str) -> Response:
        """
        This method creates a dataset that inherit encrypted for the parent dataset.
        :param dataset: The dataset pool and name.
        :return: The API response.

        Example:
            - API_POST.create_inherit_encrypted_dataset('tank/parent-dataset/child-dataset')
        """
        payload = {
            "name": dataset,
            "encryption_options": {
                "generate_key": False,
                "pbkdf2iters": 555000,
                "algorithm": "AES-256-GCM",
                "passphrase": "encryption"
            },
            "inherit_encryption": True,
            "encryption": False
        }
        return POST('/pool/dataset/', payload)

    @classmethod
    def create_non_admin_user(cls, name: str, fullname: str, password: str, smb_auth: str = 'False') -> Response:
        """
        This method creates a new non-admin user.

        :param name: is the name of the user.
        :param fullname: is the fullname of the user.
        :param password: is the password of the user.
        :param smb_auth: does user require SMB Authentication ['True'/'False'].
        :return: the API request response.
        """
        response = GET(f'/user?username={name}').json()
        if not response:
            payload = {
                "username": name,
                "group_create": True,
                "home": "/mnt/tank",
                "home_create": True,
                "full_name": fullname,
                "email": f"{name}@nowhere.com",
                "password": password,
                "shell": "/usr/bin/bash",
                "ssh_password_enabled": True,
                "smb": eval(smb_auth.lower().capitalize())
            }
            response = POST(f'/user', payload)
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def create_non_admin_user_existing_group(cls, name: str, fullname: str, password: str, group: str, smb_auth: str = 'False') -> Response:
        """
        This method creates a new non-admin user that is a member of the given group.

        :param name: is the name of the user.
        :param fullname: is the fullname of the user.
        :param password: is the password of the user.
        :param group: is the group name to add the new user to.
        :param smb_auth: does user require SMB Authentication ['True'/'False'].
        :return: the API request response.
        """
        group_id = API_Common.get_group_id(group)
        response = GET(f'/user?username={name}').json()
        if not response:
            payload = {
                "username": name,
                "group_create": False,
                "group": group_id,
                "home": "/mnt/tank",
                "home_create": True,
                "full_name": fullname,
                "email": f"{name}@nowhere.com",
                "password": password,
                "shell": "/usr/bin/bash",
                "ssh_password_enabled": True,
                "smb": eval(smb_auth.lower().capitalize())
            }
            response = POST(f'/user', payload)
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def create_read_only_admin(cls, username: str, fullname: str, password: str, smb_auth: str = 'True') -> Response:
        readonly_administrators = API_GET.get_group_id('truenas_readonly_administrators')
        payload = {
            "username": username,
            "group_create": True,
            "groups": [readonly_administrators],
            "home": "/mnt/tank",
            "home_create": True,
            "full_name": fullname,
            "email": f"{username}@nowhere.com",
            "password": password,
            "shell": "/usr/bin/bash",
            "ssh_password_enabled": True,
            "smb": eval(smb_auth.lower().capitalize())
        }
        return POST('/user', payload)

    @classmethod
    def create_remote_dataset(cls, name: str, sharetype: str = 'GENERIC') -> Response:
        """
        This method creates the given remote dataset.

        :param name: is the name of the remote dataset.
        :param sharetype: is the sharetype of the dataset.
        :return: the API request response.

        Example:
            - API_POST.create_remote_dataset('tank/test-dataset', 'GENERIC')
        """
        private_config['API_IP'] = private_config['REP_DEST_IP']
        response = GET(f'/pool/dataset?name={name}').json()
        private_config['API_IP'] = private_config['IP']
        if not response:
            private_config['API_IP'] = private_config['REP_DEST_IP']
            response = cls.create_dataset(name, sharetype)
            private_config['API_IP'] = private_config['IP']
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def create_remote_encrypted_dataset(cls, dataset: str) -> Response:
        """
        This method creates an encrypted remote dataset.

        :param dataset: The remote dataset pool and name.
        :return: The API response.

        Example:
            - API_POST.create_remote_encrypted_dataset('tank/test-dataset')
        """
        private_config['API_IP'] = private_config['REP_DEST_IP']
        response = cls.create_encrypted_dataset(dataset)
        private_config['API_IP'] = private_config['IP']
        return response

    @classmethod
    def create_remote_non_admin_user(cls, name: str, fullname: str, password: str, smb_auth: str = 'False') -> Response:
        """
        This method creates a new non-admin user.

        :param name: is the name of the user.
        :param fullname: is the fullname of the user.
        :param password: is the password of the user.
        :param smb_auth: does user require SMB Authentication ['True'/'False'].
        :return: the API request response.

        Example:
            - API_POST.create_remote_non_admin_user('tank/test-dataset')
        """
        private_config['API_IP'] = private_config['REP_DEST_IP']
        response = cls.create_non_admin_user(name, fullname, password, smb_auth)
        private_config['API_IP'] = private_config['IP']
        return response

    @classmethod
    def create_remote_snapshot(cls, dataset: str, name: str, recursive: bool = False, suspend_vms: bool = False,
                               vmware_sync: bool = False) -> Response:
        """
        This method creates the given snapshot on remote system.

        :param dataset: is the name of the dataset.
        :param name: is the name of the snapshot.
        :param recursive: Optional - True if should the snapshot be recursive else False.
        :param suspend_vms: Optional - True if should the snapshot suspend vms else False.
        :param vmware_sync: Optional - True if should the snapshot sync vmware else False.

        :return: the API request response.

        Example:
            - API_POST.create_remote_snapshot('tank/test-dataset', 'test-snapshot')
        """
        private_config['API_IP'] = private_config['REP_DEST_IP']
        response = cls.create_snapshot(dataset, name, recursive, suspend_vms, vmware_sync)
        private_config['API_IP'] = private_config['IP']
        return response

    @classmethod
    def create_share(cls, sharetype: str, name: str, path: str, guest: bool = False, comment: str = '') -> Response:
        """
        This method creates the given share.

        :param sharetype: is the sharetype of the share.
        :param name: is the name of the share.
        :param path: is the path of the share.
        :param guest: optional - whether to allow guests to access the share.
        :param comment: optional - the comment/description of the share.
        :return: the API request response.

        Example:
            - API_POST.create_share('smb', 'tank', '/mnt/tank/test-dataset', guest=True)
            - API_POST.create_share('smb', 'tank', '/mnt/tank/test-dataset')
            - API_POST.create_share('nfs', 'tank', '/mnt/tank/test-dataset')
        """
        response = GET(f'/sharing/{sharetype}?name={name}').json()
        if not response:
            if sharetype == 'smb':
                payload = {
                    "name": name,
                    "path": path,
                    "guestok": guest,
                    "comment": comment
                }
                response = POST(f'/sharing/{sharetype}', payload)
            if sharetype == 'nfs':
                response = POST(f'/sharing/{sharetype}/', {"path": path, "comment": comment})
            assert response.status_code == 200, response.text
        return response

    @classmethod
    def create_snapshot(cls, dataset: str, name: str, recursive: bool = False, suspend_vms: bool = False,
                        vmware_sync: bool = False) -> Response:
        """
        This method creates the given snapshot.

        :param dataset: is the name of the dataset.
        :param name: is the name of the snapshot.
        :param recursive: Optional - True if should the snapshot be recursive else False.
        :param suspend_vms: Optional - True if should the snapshot suspend vms else False.
        :param vmware_sync: Optional - True if should the snapshot sync vmware else False.

        :return: the API request response.

        Example:
            - API_POST.create_snapshot('tank/test-dataset', 'test-snapshot')
        """
        payload = {
            "dataset": dataset,
            "name": name,
            "recursive": recursive,
            "suspend_vms": suspend_vms,
            "vmware_sync": vmware_sync
        }
        response = POST('/zfs/snapshot/', payload)
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_all_dataset_snapshots(cls, dataset: str) -> dict:
        """
        This method delete all snapshots from given dataset.

        :param dataset: The dataset snapshots ar to be deleted from.
        :return: The dictionary response from the job.

        Example:
            - API_POST.delete_all_dataset_snapshots('tank/test-dataset')
        """
        payload = {"name": dataset}
        response = POST('/pool/dataset/destroy_snapshots', payload)
        assert response.status_code == 200, response.text
        job_status = API_Common.wait_on_job(response.json(), shared_config['LONG_WAIT'])
        assert job_status['state'] == 'SUCCESS', job_status['results']
        return job_status

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
        assert job_status['state'] == 'SUCCESS', job_status['results']
        return job_status

    @classmethod
    def is_service_running(cls, service: str) -> bool:
        """
        This method returns True if the service is running. otherwise False.

        :param service: is the service nome.
        :return: True if the service is running, otherwise False.
        """
        return POST('/service/started/', service).json()

    @classmethod
    def leave_active_directory(cls, username: str, password: str) -> dict:
        """
        This method leave the active directory.
        :param username: The username of the active directory user.
        :param password: the password of the active directory user.
        :return: the API request response dictionary.

        Example:
            - API_POST.leave_active_directory('admin', 'password')
        """
        result = POST('/activedirectory/leave', {'username': username, 'password': password})
        assert result.status_code == 200, result.text
        job_status = API_Common.wait_on_job(result.json(), shared_config['LONG_WAIT'])
        assert job_status['state'] == 'SUCCESS', job_status['results']
        return job_status['results']

    @classmethod
    def lock_dataset(cls, dataset: str) -> Response:
        """
        This method locks the given dataset.

        :param dataset: the dataset to lock.
        :return: the API request response dictionary.

        Example:
            - API_POST.lock_dataset('tank/my_dataset')
        """

        payload = {'id': dataset}
        return cls.toggle_dataset_lock_by_state(payload, 'lock', 'local')

    @classmethod
    def lock_remote_dataset(cls, dataset: str) -> Response:
        """
        This method locks the given remote dataset.

        :param dataset: the remote dataset to lock.
        :return: the API request response dictionary.

        Example:
            - API_POST.lock_remote_dataset('tank/my_dataset')
        """

        payload = {'id': dataset}
        return cls.toggle_dataset_lock_by_state(payload, 'lock', 'remote')

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
    def set_filesystem_acl(cls, payload: dict) -> Response:
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
        shared_config['SMB_ACL_ENTRY'] = {"ae_who_sid": "S-1-1-0", "ae_type": "ALLOWED", "ae_perm": "FULL"}

    @classmethod
    def start_remote_service(cls, service: str) -> Response:
        """
        This method starts the specified remote service of the default NAS.

        :param service: is the remote service name.
        :return: the API request response.
        """
        private_config['API_IP'] = private_config['REP_DEST_IP']
        response = cls.start_service(service)
        private_config['API_IP'] = private_config['IP']
        return response

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

    @classmethod
    def toggle_dataset_lock_by_state(cls, payload: dict, state: str, system: str = 'local') -> Response:
        """
        This method toggles the lock of the given dataset to the given lock state.

        :param payload: the payload to set the state of the dataset.
        :param system: the system of the dataset is located on. ['local'/'remote']
        :param state: the state to lock. ['lock'/'unlock']
        :return: the API request response dictionary.

        Example:
            - API_POST.toggle_dataset_lock_by_state(payload, 'lock', 'local')
            - API_POST.toggle_dataset_lock_by_state(payload, 'unlock', 'remote')
        """

        if system == 'remote':
            private_config['API_IP'] = private_config['REP_DEST_IP']

        response = POST(f'/pool/dataset/{state}', payload)
        job_status = API_Common.wait_on_job(response.json(), shared_config['WAIT'])
        assert job_status['state'] == 'SUCCESS', job_status['results']
        if system == 'remote':
            private_config['API_IP'] = private_config['IP']
        return response

    @classmethod
    def unlock_dataset(cls, dataset: str) -> Response:
        """
        This method unlocks the given dataset.

        :param dataset: the dataset to lock.
        :return: the API request response dictionary.

        Example:
            - API_POST.unlock_dataset('tank/my_dataset')
        """

        unlock_options = {"datasets": [{"name": dataset, "passphrase": "encryption"}]}
        payload = {"id": dataset, "unlock_options": unlock_options}
        return cls.toggle_dataset_lock_by_state(payload, 'unlock', 'local')

    @classmethod
    def unlock_remote_dataset(cls, dataset: str) -> Response:
        """
        This method unlocks the given remote dataset.

        :param dataset: the remote dataset to lock.
        :return: the API request response dictionary.

        Example:
            - API_POST.unlock_remote_dataset('tank/my_dataset')
        """

        unlock_options = {"datasets": [{"name": dataset, "passphrase": "encryption"}]}
        payload = {"id": dataset, "unlock_options": unlock_options}
        return cls.toggle_dataset_lock_by_state(payload, 'unlock', 'remote')
