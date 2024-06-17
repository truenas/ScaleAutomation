import time
from helper.api import GET


class API_Common:
    @classmethod
    def get_id_by_type(cls, path: str, name: str) -> int:
        """
        This method search name of specified path and return the ID.

        :param path: is the path to search the name to get the ID.
        :param name: is the name of the to get the ID from.
        :return: the ID of name of specified path.
        """
        search = 'name='
        if path.__contains__('nfs'):
            search = 'path=/mnt/'
        user_results = GET(f"/{path}{search}{name}")
        assert user_results.status_code == 200, user_results.text
        return user_results.json()[0]['id']

    @classmethod
    def get_group_id(cls, group: str) -> int:
        """
        This method return the ID of the specified group.

        :param group: is the name of the group to get the ID from.
        :return: the ID of the specified group.
        """
        return cls.get_id_by_type("group?", group)

    @classmethod
    def get_pool_id(cls, name: str) -> int:
        """
        This method return the ID of the specified group.

        :param name: is the name of the pool to get the ID from.
        :return: the ID of the specified pool.
        """
        return cls.get_id_by_type("pool?", name)

    @classmethod
    def get_privilege_id(cls, privilege: str) -> int:
        """
        This method return the ID of the specified privilege.

        :param privilege: is the name of the privilege to get the ID from.
        :return: the ID of the specified privilege.
        """
        return cls.get_id_by_type("privilege?", privilege)

    @classmethod
    def get_privilege_gid(cls, privilege: str) -> int:
        """
        This method return the GID of the specified privilege.

        :param privilege: is the name of the privilege to get the GID from.
        :return: the GID of the specified privilege.
        """
        user_results = GET(f"/privilege?name={privilege}")
        assert user_results.status_code == 200, user_results.text
        return user_results.json()[0]['local_groups'][0]['gid']

    @classmethod
    def get_ssh_id(cls, ssh: str) -> int:
        """
        This method return the ID of the specified ssh connection.

        :param ssh: is the name of the ssh connection to get the ID from.
        :return: the ID of the specified ssh connection.
        """
        return cls.get_id_by_type("keychaincredential?", ssh)

    @classmethod
    def get_user_id(cls, username: str) -> int:
        """
        This method return the ID of the specified username.

        :param username: is the username of the user to get the ID from.
        :return: the ID of the specified username.
        """
        return cls.get_id_by_type("user?user", username)

    @classmethod
    def get_user_uid(cls, username: str) -> int:
        """
        This method return the ID of the specified username.

        :param username: is the username of the user to get the ID from.
        :return: the ID of the specified username.
        """
        user_results = GET(f"/user?username={username}")
        assert user_results.status_code == 200, user_results.text
        return user_results.json()[0]['uid']

    @classmethod
    def is_system_ready(cls) -> bool:
        """
        This method returns True if the system is READY, otherwise False. [ SHUTTING_DOWN, READY, BOOTING ]

        :return: returns True if the system is READY, otherwise False.

        Example:
        - API_Common.is_system_ready()
        """
        state = GET("/system/state")
        print("@@@ SYSTEM IS: "+state.text)
        return state.text.__contains__("READY")

    @classmethod
    def wait_on_job(cls, job_id: int, max_timeout: int) -> dict:
        """
        This method wait for API ID to return SUCCESS or FAILED and TIMEOUT.

        :param job_id: is the id number of the job.
        :param max_timeout: is the time in second to time out the wait for SUCCESS or FAILED.
        :return: a dictionary with the state and the json results as a dictionary.
        """
        timeout = 0
        while True:
            job_results = GET(f'/core/get_jobs/?id={job_id}')
            job_state = job_results.json()[0]['state']
            match job_state:
                case 'RUNNING' | 'WAITING':
                    time.sleep(5)
                case 'SUCCESS' | 'FAILED' | 'ABORTED':
                    return {'state': job_state, 'results': job_results.json()[0]}
            if timeout >= max_timeout:
                print(f'JOB {job_id} TIMEOUT EXCEEDED. JOB STATE: {job_state}')
                return {'state': 'TIMEOUT', 'results': job_results.json()[0]}
            timeout += 5
