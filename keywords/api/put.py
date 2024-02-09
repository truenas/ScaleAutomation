from helper.api import PUT, Response
from helper.global_config import private_config
from keywords.api.common import API_Common


class API_PUT:
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
    def set_app_pool(cls, pool: str) -> Response:
        return PUT('/kubernetes/', {'pool': pool, 'servicelb': True})

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
