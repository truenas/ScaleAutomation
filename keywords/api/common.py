import time
from helper.api import GET


class API_Common:
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
    def get_id_by_type(cls, path: str, name: str) -> int:
        """
        This method search name of specified path and return the ID.

        :param path: is the path to search the name to get the ID.
        :param name: is the name of the to get the ID from.
        :return: the ID of name of specified path.
        """
        user_results = GET(f"/{path}name={name}")
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
            if job_state in ('RUNNING', 'WAITING'):
                time.sleep(5)
            elif job_state in ('SUCCESS', 'FAILED'):
                return {'state': job_state, 'results': job_results.json()[0]}
            if timeout >= max_timeout:
                return {'state': 'TIMEOUT', 'results': job_results.json()[0]}
            timeout += 5
