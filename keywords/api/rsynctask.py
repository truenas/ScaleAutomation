from helper.api import POST, Response, DELETE, PUT
from helper.global_config import private_config


class API_Rsync_Task:
    @classmethod
    def create_rsync_task(cls, description: str) -> Response:
        """
        This method creates the given rsync task.

        :param description: is the description of the rsync task.
        :return: the API request response.

        Example:
            - API_POST.create_rsync_task('description')
        """
        payload = {
            'delete': False,
            'desc': description,
            'direction': 'PUSH',
            'enabled': True,
            'mode': 'MODULE',
            'path': '/mnt/tank',
            'recursive': True,
            'remotehost': private_config['REP_DEST_IP'],
            'remotemodule': 'tank',
            'user': 'admin',
        }
        response = POST('/rsynctask', payload)
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def delete_rsync_task(cls, task_id: int = None) -> Response:
        """
        This method deletes the given rsync task.

        :param task_id: optional param that is the id of the rsync task.
        :return: the API request response.

        Example:
            - API_POST.delete_rsync_task('description')
        """
        response = DELETE(f'/rsynctask/id/{task_id}')
        assert response.status_code == 200, response.text
        return response

    @classmethod
    def disable_rsync_task(cls, task_id: int = None) -> Response:
        """
        This method dissables the given rsync task.

        :param task_id: optional param that is the id of the rsync task.
        :return: the API request response.

        Example:
            - API_POST.dissable_rsync_task('description')
        """
        payload = {'enabled': False}
        response = PUT(f'/rsynctask/id/{task_id}', payload)
        assert response.status_code == 200, response.text
        return response
