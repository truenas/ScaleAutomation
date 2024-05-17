from helper.api import POST, Response, GET, DELETE
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
    def delete_rsync_task(cls, description: str = None, task_id: int = None) -> Response:
        """
        This method deletes the given rsync task.

        :param description: optional param that is name of the rsync credential.
        :param task_id: optional param that is the id of the rsync task.
        :return: the API request response.

        Example:
            - API_POST.delete_rsync_task('description')
        """
        if not task_id and description:
            task_id = GET(f'/rsynctask?description={description}').json()[0]['id']
        response = DELETE(f'/rsynctask/id/{task_id}')
        assert response.status_code == 200, response.text
        return response
