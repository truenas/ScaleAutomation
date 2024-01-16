import pytest
from helper.data_config import get_data_list
from keywords.webui.apps import Apps
from keywords.webui.datasets import Datasets as DATASET


@pytest.mark.parametrize('app_data', get_data_list('apps'), scope='class')
class Test_Start_App:

    @staticmethod
    def verify_start_app(app_data) -> None:
        """
        This test verifies the given app is started

        :param app_data: test data listing different apps to iterate through
        """
        Apps.verify_app_installed(app_data['app-name'])
        assert Apps.assert_stop_app(app_data['app-name'])
        assert Apps.assert_start_app(app_data['app-name'])

    @staticmethod
    def verify_teardown(app_data) -> None:
        """
        This test removes the given app

        :param app_data: test data listing different apps to iterate through
        """
        # reset the change
        Apps.delete_app(app_data['app-name'])
        assert Apps.is_app_installed(app_data['app-name']) is False
        if app_data['setup-name'] == 'webdav':
            DATASET.delete_dataset_by_api(f'{app_data['pool']}/{app_data['setup-name']}')

