from helper.api import PUT, Response, GET
from helper.global_config import private_config, shared_config
from keywords.api.common import API_Common


class API_PUT:
    @classmethod
    def disable_active_directory(cls) -> dict:
        """
        This method disable active directory.

        :return: the API request response json as dictionary.
        """
        return cls.update_active_directory({"enable": False})

    @classmethod
    def disable_service_at_boot(cls, service: str) -> Response:
        """
        This method disable starting the specified service at boot.

        :param service: is the service nome.
        :return: the API request response.
        """
        return cls.update_service_at_boot(service, False)

    @classmethod
    def disable_user_all_sudo_commands(cls, username: str) -> Response:
        """
        This method disable user sudo commands.

        :param username: the username of the user.
        :return: the API request response.
        """
        private_config['SSH_USERNAME'] = username
        return cls.update_user(username, {"sudo_commands": []})

    @classmethod
    def disable_user_all_sudo_commands_no_password(cls, username: str) -> Response:
        """
        This method disable user sudo commands no password.

        :param username: the username of the user.
        :return: the API request response.
        """
        private_config['SSH_USERNAME'] = username
        return cls.update_user(username, {"sudo_commands_nopasswd": []})

    @classmethod
    def disable_user_ssh_password(cls, username: str) -> Response:
        """
        This method disable ssh password login.

        :param username: the username of the user.
        :return: the API request response.
        """
        return cls.update_user(username, {"ssh_password_enabled": False})

    @classmethod
    def enable_active_directory(cls) -> dict:
        """
        This method enable active directory.

        :return: the API request response json as dictionary.
        """
        return cls.update_active_directory({"enable": True})

    @classmethod
    def enable_service_at_boot(cls, service: str) -> Response:
        """
        This method enable starting the specified service at boot.

        :param service: is the service name.
        :return: the API request response.
        """
        return cls.update_service_at_boot(service, True)

    @classmethod
    def enable_user_all_sudo_commands(cls, username: str) -> Response:
        """
        This method enable user sudo commands.

        :param username: the username of the user.
        :return: the API request response.
        """
        private_config['SSH_USERNAME'] = username
        return cls.update_user(username, {"sudo_commands": ["ALL"]})

    @classmethod
    def enable_user_all_sudo_commands_no_password(cls, username: str) -> Response:
        """
        This method enable user sudo commands no password.

        :param username: the username of the user.
        :return: the API request response.
        """
        private_config['SSH_USERNAME'] = username
        return cls.update_user(username, {"sudo_commands_nopasswd": ["ALL"]})

    @classmethod
    def enable_user_ssh_password(cls, username: str) -> Response:
        """
        This method enable ssh password login.

        :param username: the username of the user.
        :return: the API request response.
        """
        private_config['SSH_USERNAME'] = username
        return cls.update_user(username, {"ssh_password_enabled": True})

    @classmethod
    def join_active_directory(cls, username: str, password: str, domain: str) -> dict:
        """
        This method join the active directory.
        :param username: The username of the active directory user.
        :param password: The password of the active directory user.
        :param domain: The name of the domain of the active directory.
        :return: the API request response json as dictionary.
        """
        payload = {
            'bindpw': password,
            'bindname': username,
            'domainname': domain,
            'netbiosname': shared_config['HOSTNAME'],
            'dns_timeout': 15,
            'verbose_logging': True,
            'enable': True
        }
        return cls.update_active_directory(payload)

    @classmethod
    def set_app_pool(cls, pool: str) -> dict:
        """
        This method set the app pool with the kubernetes API call.
        :param pool: The name of the pool.
        :return: The API request response.

        Example:
            - API_PUT.set_app_pool('tank')
        """
        response = PUT('/kubernetes/', {'pool': pool, 'servicelb': True})
        assert response.status_code == 200, response.text
        job_result = API_Common.wait_on_job(response.json(), shared_config['LONG_WAIT'])
        assert job_result['state'] == 'SUCCESS', str(job_result)
        return job_result

    @classmethod
    def set_dataset_quota(cls, dataset_name: str, quota: int) -> Response:
        """
        This method set the quota for the specified dataset.
        :param dataset_name: The name of the dataset.
        :param quota: The quota value.
        :return: The API request response.

        Example:
            - API_PUT.set_dataset_refquota('test-dataset', 0)
        """
        response = PUT(f'/pool/dataset/id/{dataset_name.replace("/", "%2F")}', {'quota': quota})
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def set_dataset_refquota(cls, dataset_name: str, refquota: int) -> Response:
        """
        This method set the refquota for the specified dataset.
        :param dataset_name: The name of the dataset.
        :param refquota: The refquota value.
        :return: The API request response.

        Example:
            - API_PUT.set_dataset_refquota('test-dataset', 0)
        """
        response = PUT(f'/pool/dataset/id/{dataset_name.replace("/", "%2F")}', {'refquota': refquota})
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def set_dataset_refreservation(cls, dataset_name: str, refreservation: int) -> Response:
        """
        This method set the refreservation for the specified dataset.
        :param dataset_name: The name of the dataset.
        :param refreservation: The refreservation value.
        :return: The API request response.

        Example:
            - API_PUT.set_dataset_refreservation('test-dataset', 0)
        """
        response = PUT(f'/pool/dataset/id/{dataset_name.replace("/", "%2F")}', {'refreservation': refreservation})
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def set_dataset_reservation(cls, dataset_name: str, reservation: int) -> Response:
        """
        This method set the reservation for the specified dataset.
        :param dataset_name: The name of the dataset.
        :param reservation: The reservation value.
        :return: The API request response.

        Example:
            - API_PUT.set_dataset_reservation('test-dataset', 0)
        """
        response = PUT(f'/pool/dataset/id/{dataset_name.replace("/", "%2F")}', {'reservation': reservation})
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def set_hostname(cls) -> Response:
        """
        This method set the hostname for the specified pool.
        :return: The API request response.

        Example:
            - API_PUT.set_hostname()
        """
        return cls.update_network_configuration({'hostname': shared_config['HOSTNAME']})

    @classmethod
    def set_nameservers(cls, nameserver1: str, nameserver2: str = '', nameserver3: str = '') -> Response:
        """
        This method set the nameservers for the specified pool.
        :param nameserver1: The first nameserver IP.
        :param nameserver2: The second nameserver IP.
        :param nameserver3: The third nameserver IP.
        :return: The API request response.

        Example:
            - API_PUT.set_nameservers('1.1.1.1', '2.2.2.2', '3.3.3.3')
            - API_PUT.set_nameservers('1.1.1.1')
            - API_PUT.set_nameservers('1.1.1.1', '2.2.2.2')
            - API_PUT.set_nameservers("1.1.1.1", "", "")
        """
        payload = {
            'nameserver1': f'{nameserver1}',
            'nameserver2': f'{nameserver2}',
            'nameserver3': f'{nameserver3}'
        }
        return cls.update_network_configuration(payload)

    @classmethod
    def set_service_autostart(cls, service: str, state: bool):
        """
        This method sets the autostart status of the given service to the given state.

        :param service: the name of the service.
        :param state: the state to set the service to.
        :return: The API request response.
        """
        serviceid = ''
        match service.lower():
            case 'smb':
                serviceid = '4'
            case 'ftp':
                serviceid = '6'
            case 'iscsi':
                serviceid = '7'
            case 'nfs':
                serviceid = '9'
            case 'snmp':
                serviceid = '10'
            case 'ssh':
                serviceid = '11'
            case 'ups':
                serviceid = '14'
            case 'smart' | 's.m.a.r.t.':
                serviceid = '18'
            case _:
                pass
        return PUT(f'/service/id/{serviceid}', {"enable": state})

    @classmethod
    def set_user_groups(cls, username: str, groups: list) -> Response:
        """
        This method set the groups for the specified user.

        :param username: the username of the user.
        :param groups: List of groups name.
        :return: The API request response.
        """
        private_config['SSH_USERNAME'] = username
        groups_id = [API_Common.get_group_id(group) for group in groups]
        return cls.update_user(username, {'groups': groups_id})

    @classmethod
    def set_user_ssh_public_key(cls, username: str, pubkey: str) -> Response:
        """
        This method set the ssh public key for the specified user.

        :param username: the username of the user.
        :param pubkey: the public key to be set
        :return: the API request response.
        """
        private_config['SSH_USERNAME'] = username
        return cls.update_user(username, {"sshpubkey": pubkey})

    @classmethod
    def unset_user_ssh_public_key(cls, username: str) -> Response:
        """
        This method unset the ssh public key for the specified user.

        :param username: the username of the user.
        :return: the API request response.
        """
        return cls.update_user(username, {"sshpubkey": ""})

    @classmethod
    def update_active_directory(cls, payload: dict) -> dict:
        """
        This method update the active directory configuration.

        :param payload: is the dictionary of parameter to update.
        :return: the API request response json as dictionary.
        """
        result = PUT('/activedirectory/', payload)
        assert result.status_code == 200, result.text
        job_result = API_Common.wait_on_job(result.json()['job_id'], shared_config['EXTRA_LONG_WAIT'])
        assert job_result['state'] == 'SUCCESS', job_result['results']
        return job_result['results']

    @classmethod
    def update_network_configuration(cls, payload: dict) -> Response:
        """
        This method update the network configuration.

        :param payload: is the dictionary of parameter to update.
        :return: the API request response.
        """
        return PUT('/network/configuration/', payload)

    @classmethod
    def update_service_at_boot(cls, service: str, enable: bool) -> Response:
        """
        This method disable or enable the specified service.

        :param service: is the service name.
        :param enable: is True to enable false to enable
        :return: the API request response.
        """
        return PUT(f'/service/id/{service}', {"enable": enable})

    @classmethod
    def update_user(cls, username: str, payload: dict) -> Response:
        """
        This method update the parameter of the user specified.

        :param username: the username of the user.
        :param payload: is the dictionary of parameter to update.
        :return: the API request response.
        """
        userid = API_Common.get_user_id(username)
        return PUT(f'/user/id/{userid}', payload)

    @classmethod
    def set_cloud_sync_task_enabled(cls, name: str, state: bool = True) -> Response:
        """
        This method sets the given cloud sync task to the given enabled state.

        :param name: is name of the cloud sync credential.
        :param state: is the state to set the cloud sync task. Default is True
        :return: the API request response.

        Example:
            - API_POST.set_cloud_sync_task_enabled('name')
            - API_POST.set_cloud_sync_task_enabled('name', False)
        """
        cred_id = 0
        response = GET(f'/cloudsync/credentials?name={name}').json()
        if response:
            cred_id = response[0]['id']
        payload = {
          "enabled": state
        }
        response = PUT(f'/cloudsync/id/{cred_id}', payload)
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def set_periodic_snapshot_task_enabled(cls, path: str, state: bool = True) -> Response:
        """
        This method sets the given periodic snapshot task to the given enabled state.

        :param path: is name of the periodic snapshot credential.
        :param state: is the state to set the periodic snapshot task. Default is True
        :return: the API request response.

        Example:
            - API_POST.set_periodic_snapshot_task_enabled('name')
            - API_POST.set_periodic_snapshot_task_enabled('name', False)
        """
        cred_id = 0
        response = GET(f'/pool/snapshottask?dataset={path}').json()
        if response:
            cred_id = response[0]['id']
        payload = {
          "enabled": state
        }
        response = PUT(f'/pool/snapshottask/id/{cred_id}', payload)
        assert response.status_code == 200, response.text
        return response

