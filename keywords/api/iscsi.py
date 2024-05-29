from helper.api import DELETE, GET, POST, Response
from keywords.api.dataset import API_DATASET
from keywords.api.delete import API_DELETE


class API_ISCSI:
    @classmethod
    def create_iscsi_extent_disk(cls, name: str, zvol: str) -> Response:
        """
        This method creates the given iscsi extent.

        :param name: The name of the iscsi extent.
        :param zvol: The zvol of the iscsi extent.
        :return: the API request response.

        Example:
            - API_ISCSI.create_iscsi_extent_disk('my-extent', 'tank/test-zvol')
        """
        payload = {
            'type': 'DISK',
            'disk': f'zvol/{zvol}',
            'name': name
        }
        return POST('/iscsi/extent/', payload)

    @classmethod
    def create_iscsi_portal(cls, comment: str) -> Response:
        """
        This method creates the given iscsi portal.

        :param comment: The comment of the iscsi portal.
        :return: the API request response.

        Example:
            - API_ISCSI.create_iscsi_portal('my-portal')
        """
        payload = {
            'comment': comment,
            'listen': [
                {
                    'ip': '0.0.0.0',
                }
            ]
        }
        return POST('/iscsi/portal/', payload)

    @classmethod
    def create_iscsi_share(cls, share_name: str, pool_name: str, lunid: int) -> None:
        """
        This method creates the given iscsi share.

        :param share_name: The name of the iscsi share.
        :param pool_name: The name of the pool.
        :param lunid: The lunid of the iscsi share.

        Example:
            - API_ISCSI.create_iscsi_share('my-share', 'myPool')
        """
        zvol_response = API_DATASET.create_zvol(f'{pool_name}/{share_name}', 1024000, '4K')
        assert zvol_response.status_code == 200, zvol_response.text

        portal_response = cls.create_iscsi_portal(share_name)
        assert portal_response.status_code == 200, portal_response.text

        target_response = cls.create_iscsi_target(share_name, portal_response.json()['id'])
        assert target_response.status_code == 200, target_response.text

        extent_response = cls.create_iscsi_extent_disk(share_name, f'{pool_name}/{share_name}')
        assert extent_response.status_code == 200, extent_response.text

        targetextent_response = cls.create_iscsi_targetextent(lunid, target_response.json()['id'], extent_response.json()['id'])
        assert targetextent_response.status_code == 200, targetextent_response.text

    @classmethod
    def create_iscsi_target(cls, target_name: str, portal_id: int) -> Response:
        """
        This method creates the given iscsi target.

        :param target_name: The name of the iscsi target.
        :param portal_id: The id of the portal.
        :return: the API request response.

        Example:
            - API_ISCSI.create_iscsi_target('my-target', 1)
        """
        payload = {
            'name': target_name,
            'groups': [
                {'portal': portal_id}
            ]
        }
        return POST('/iscsi/target/', payload)

    @classmethod
    def create_iscsi_targetextent(cls, lunid: int, target_id: int, extent_id: int) -> Response:
        """
        This method creates the given iscsi target extent.

        :param lunid: The lunid of the iscsi target extent.
        :param target_id: The id of the target.
        :param extent_id: The id of the extent.
        :return: the API request response.

        Example:
            - API_ISCSI.create_iscsi_targetextent(1, 1, 1)
        """
        payload = {
            'target': target_id,
            'lunid': lunid,
            'extent': extent_id
        }
        return POST('/iscsi/targetextent/', payload)

    @classmethod
    def delete_iscsi_extent(cls, extent_name: str) -> Response:
        """
        This method deletes the given iscsi extent.

        :param extent_name: The name of the iscsi extent.

        Example:
            - API_ISCSI.delete_iscsi_extent('my-extent')
        """
        extent_id = GET(f"/iscsi/extent?name={extent_name}").json()[0]['id']
        return DELETE(f'/iscsi/extent/id/{extent_id}/')

    @classmethod
    def delete_iscsi_portal(cls, comment: str) -> Response:
        """
        This method deletes the given iscsi portal.

        :param comment: The comment of the iscsi portal.

        Example:
            - API_ISCSI.delete_iscsi_portal('my-portal')
        """
        portal_id = GET(f"/iscsi/portal?comment={comment}").json()[0]['id']
        return DELETE(f'/iscsi/portal/id/{portal_id}/')

    @classmethod
    def delete_iscsi_share(cls, share_name: str, pool_name: str, lunid: int) -> None:
        """
        This method deletes the given iscsi share.

        :param share_name: The name of the iscsi share.
        :param pool_name: The name of the pool.
        :param lunid: The lunid of the iscsi share.

        Example:
            - API_ISCSI.delete_iscsi_share('my-share', 'myPool')
        """
        targetextent_response = cls.delete_iscsi_targetextent(lunid)
        assert targetextent_response.status_code == 200, targetextent_response.text

        extent_response = cls.delete_iscsi_extent(share_name)
        assert extent_response.status_code == 200, extent_response.text

        target_response = cls.delete_iscsi_target(share_name)
        assert target_response.status_code == 200, target_response.text

        portal_response = cls.delete_iscsi_portal(share_name)
        assert portal_response.status_code == 200, portal_response.text

        zvol_response = API_DELETE.delete_dataset(f'{pool_name}/{share_name}', force=True)
        assert zvol_response.status_code == 200, zvol_response.text

    @classmethod
    def delete_iscsi_target(cls, target_name: str) -> Response:
        """
        This method deletes the given iscsi target.

        :param target_name: The name of the iscsi target.

        Example:
            - API_ISCSI.delete_iscsi_target('my-target')
        """
        target_id = GET(f"/iscsi/target?name={target_name}").json()[0]['id']
        return DELETE(f'/iscsi/target/id/{target_id}/')

    @classmethod
    def delete_iscsi_targetextent(cls, lunid: int) -> Response:
        """
        This method deletes the given iscsi target extent.

        :param lunid: The lunid of the iscsi target extent.

        Example:
            - API_ISCSI.delete_iscsi_targetextent('my-extent')
        """
        targetextent_id = GET(f"/iscsi/targetextent?lunid={lunid}").json()[0]['id']
        return DELETE(f'/iscsi/targetextent/id/{targetextent_id}/')
