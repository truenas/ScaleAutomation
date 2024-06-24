import time
from helper.api import GET, Response


class API_Common:
    @classmethod
    def get_id_by_type(cls, path: str, name: str) -> int:
        """
        This method search name of specified path and return the ID.

        :param path: is the path to search the name to get the ID.
        :param name: is the name of the to get the ID from.
        :return: the ID of name of specified path.

        Example:
            - API_Common.get_id_by_type('user?', 'username')
        """
        search = 'path=/mnt/' if 'nfs' in path else 'name='
        user_results = GET(f"/{path}{search}{name}")
        assert user_results.status_code == 200, user_results.text
        return user_results.json()[0]['id']

    @classmethod
    def get_group_id(cls, group: str) -> int:
        """
        This method return the ID of the specified group.

        :param group: is the name of the group to get the ID from.
        :return: the ID of the specified group.

        Example:
            - API_Common.get_group_id('group1')
        """
        return cls.get_id_by_type("group?", group)

    @classmethod
    def get_jobs(cls, value: str, attribute) -> Response:
        """
        This method gets all the jobs related to the value of the attribute.

        :param value: is the value to search with.
        :param attribute: is the attribute to search options: [id, method, state]
        :return: the API request response.

        Example:
            - API_Common.get_jobs('system.debug', 'state')
        """
        response = GET(f'/core/get_jobs/?{attribute}={value}')
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def get_a_job_id(cls, value: str, attribute) -> int:
        """
        This method return the ID of the specified job.

        :param value: is the value of the job to get the ID from.
        :param attribute: is the attribute of the job to get the ID from.
            options: [method, state]
        :return: the ID of the specified job.

        Example:
            - API_Common.get_a_job_id('system.debug', 'state')
        """
        return cls.get_jobs(value, attribute).json()[-1]['id']

    @classmethod
    def get_pool_id(cls, name: str) -> int:
        """
        This method return the ID of the specified group.

        :param name: is the name of the pool to get the ID from.
        :return: the ID of the specified pool.

        Example:
            - API_Common.get_pool_id('tank')
        """
        return cls.get_id_by_type("pool?", name)

    @classmethod
    def get_privilege_id(cls, privilege: str) -> int:
        """
        This method return the ID of the specified privilege.

        :param privilege: is the name of the privilege to get the ID from.
        :return: the ID of the specified privilege.

        Example:
            - API_Common.get_privilege_id('privilege1')
        """
        return cls.get_id_by_type("privilege?", privilege)

    @classmethod
    def get_privilege_gid(cls, privilege: str) -> int:
        """
        This method return the GID of the specified privilege.

        :param privilege: is the name of the privilege to get the GID from.
        :return: the GID of the specified privilege.

        Example:
            - API_Common.get_privilege_gid('privilege1')
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

        Example:
            - API_Common.get_ssh_id('ssh1')
        """
        return cls.get_id_by_type("keychaincredential?", ssh)

    @classmethod
    def get_user_id(cls, username: str) -> int:
        """
        This method return the ID of the specified username.

        :param username: is the username of the user to get the ID from.
        :return: the ID of the specified username.

        Example:
            - API_Common.get_user_id('username')
        """
        return cls.get_id_by_type("user?user", username)

    @classmethod
    def get_user_uid(cls, username: str) -> int:
        """
        This method return the ID of the specified username.

        :param username: is the username of the user to get the ID from.
        :return: the ID of the specified username.

        Example:
            - API_Common.get_user_uid('username')
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
        print(f"@@@ SYSTEM IS: {state.text}")
        return state.text.__contains__("READY")

    @classmethod
    def wait_on_job(cls, job_id: int, max_timeout: int) -> dict:
        """
        This method wait for API ID to return SUCCESS or FAILED and TIMEOUT.

        :param job_id: is the id number of the job.
        :param max_timeout: is the time in second to time out the wait for SUCCESS or FAILED.
        :return: a dictionary with the state and the json results as a dictionary.

        Example:
            - API_Common.wait_on_job(1234, 60)
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
